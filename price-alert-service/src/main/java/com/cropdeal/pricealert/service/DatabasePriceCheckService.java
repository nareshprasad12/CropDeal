package com.cropdeal.pricealert.service;

import com.cropdeal.pricealert.client.PriceServiceClient;
import com.cropdeal.pricealert.dto.DatabasePriceDto;
import com.cropdeal.pricealert.dto.MatchMarketPriceRequest;
import com.cropdeal.pricealert.dto.MatchResultResponse;
import com.cropdeal.pricealert.entity.PriceAlertSubscription;
import com.cropdeal.pricealert.repository.PriceAlertSubscriptionRepository;
import com.cropdeal.pricealert.repository.PriceAlertNotificationRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class DatabasePriceCheckService {

    private final PriceServiceClient priceServiceClient;
    private final PriceAlertMatchingEngine matchingEngine;
    private final PriceAlertSubscriptionRepository subscriptionRepository;
    private final PriceAlertNotificationRepository notificationRepository;

    /**
     * Checks all active subscriptions against the government/market prices stored in our local DB.
     * This avoids continuously fetching from external government APIs.
     */
    public MatchResultResponse checkActiveSubscriptionsAgainstDatabasePrices() {
        log.info("Starting evaluation of active price subscriptions against prices stored in our database...");

        List<DatabasePriceDto> dbPrices = priceServiceClient.getLatestStoredPricesFromDb();
        if (dbPrices.isEmpty()) {
            log.info("No stored crop prices available in database at this moment.");
            return MatchResultResponse.builder()
                    .matchedCount(0)
                    .notificationsTriggered(0)
                    .message("No prices currently stored in database to evaluate.")
                    .build();
        }

        int totalEvaluated = 0;
        int totalTriggered = 0;
        long syntheticId = 1000L;

        for (DatabasePriceDto priceDto : dbPrices) {
            if (priceDto.getCommodity() == null || priceDto.getCommodity().isBlank()) {
                continue;
            }

            Double priceVal = priceDto.getModalPricePerKg();
            if (priceVal == null || priceVal <= 0) {
                if (priceDto.getMinPricePerKg() != null && priceDto.getMinPricePerKg() > 0) {
                    priceVal = priceDto.getMinPricePerKg();
                } else if (priceDto.getMaxPricePerKg() != null && priceDto.getMaxPricePerKg() > 0) {
                    priceVal = priceDto.getMaxPricePerKg();
                } else {
                    continue;
                }
            }

            BigDecimal effectivePrice = BigDecimal.valueOf(priceVal).setScale(2, RoundingMode.HALF_UP);
            syntheticId++;

            MatchMarketPriceRequest matchRequest = MatchMarketPriceRequest.builder()
                    .priceId(syntheticId)
                    .cropName(priceDto.getCommodity())
                    .marketPrice(effectivePrice)
                    .marketName(priceDto.getState() != null ? priceDto.getState() + " Mandi" : "Government Mandi")
                    .district(priceDto.getDistrict())
                    .state(priceDto.getState())
                    .unit("kg")
                    .build();

            int matched = matchingEngine.matchMarketPrice(matchRequest);
            totalEvaluated++;
            totalTriggered += matched;
        }

        String msg = String.format("Evaluated %d database crop prices against active subscriptions. Alerts triggered: %d",
                totalEvaluated, totalTriggered);
        log.info(msg);

        return MatchResultResponse.builder()
                .matchedCount(totalEvaluated)
                .notificationsTriggered(totalTriggered)
                .message(msg)
                .build();
    }

    /**
     * Checks crop price subscriptions against our database prices ONLY upon user login.
     * No background continuous polling is performed.
     */
    public MatchResultResponse checkUserSubscriptionsOnLogin(Long userId) {
        if (userId == null) {
            return MatchResultResponse.builder()
                    .matchedCount(0)
                    .notificationsTriggered(0)
                    .message("User ID is required for login price check.")
                    .build();
        }

        List<PriceAlertSubscription> userSubs = subscriptionRepository.findByUserIdAndActiveTrue(userId);
        if (userSubs == null || userSubs.isEmpty()) {
            return MatchResultResponse.builder()
                    .matchedCount(0)
                    .notificationsTriggered(0)
                    .message("No active price subscriptions found for user " + userId)
                    .build();
        }

        Set<String> subscribedCrops = userSubs.stream()
                .filter(s -> s.getCropName() != null && !s.getCropName().isBlank())
                .map(s -> s.getCropName().trim().toLowerCase())
                .collect(Collectors.toSet());

        log.info("Checking crop alerts from local database for userId {} on login (subscribed to: {})...", userId, subscribedCrops);

        List<DatabasePriceDto> dbPrices = priceServiceClient.getLatestStoredPricesFromDb();
        if (dbPrices == null || dbPrices.isEmpty()) {
            log.info("No stored crop prices available in database at this moment for user {}.", userId);
            return MatchResultResponse.builder()
                    .matchedCount(0)
                    .notificationsTriggered(0)
                    .message("No prices currently stored in database.")
                    .build();
        }

        int totalEvaluated = 0;
        int totalTriggered = 0;
        long syntheticId = 1000L;

        java.util.Set<Long> notifiedSubs = new java.util.HashSet<>();
        for (DatabasePriceDto priceDto : dbPrices) {
            if (priceDto.getCommodity() == null || priceDto.getCommodity().isBlank()) {
                continue;
            }

            // High performance filter: evaluate only prices matching the user's subscribed crops
            if (!subscribedCrops.contains(priceDto.getCommodity().trim().toLowerCase())) {
                continue;
            }

            List<PriceAlertSubscription> pendingSubs = userSubs.stream()
                    .filter(s -> !notifiedSubs.contains(s.getId()) && s.getLastNotifiedAt() == null && !notificationRepository.existsBySubscriptionId(s.getId()))
                    .filter(s -> s.getCropName() != null && s.getCropName().trim().equalsIgnoreCase(priceDto.getCommodity().trim()))
                    .toList();

            if (pendingSubs.isEmpty()) {
                continue;
            }

            Double priceVal = priceDto.getModalPricePerKg();
            if (priceVal == null || priceVal <= 0) {
                if (priceDto.getMinPricePerKg() != null && priceDto.getMinPricePerKg() > 0) {
                    priceVal = priceDto.getMinPricePerKg();
                } else if (priceDto.getMaxPricePerKg() != null && priceDto.getMaxPricePerKg() > 0) {
                    priceVal = priceDto.getMaxPricePerKg();
                } else {
                    continue;
                }
            }

            BigDecimal effectivePrice = BigDecimal.valueOf(priceVal).setScale(2, RoundingMode.HALF_UP);
            syntheticId++;

            MatchMarketPriceRequest matchRequest = MatchMarketPriceRequest.builder()
                    .priceId(syntheticId)
                    .cropName(priceDto.getCommodity())
                    .marketPrice(effectivePrice)
                    .marketName(priceDto.getState() != null ? priceDto.getState() + " Mandi" : "Government Mandi")
                    .district(priceDto.getDistrict())
                    .state(priceDto.getState())
                    .unit("kg")
                    .build();

            int matched = matchingEngine.matchUserSubscriptionsAgainstMarketPrice(userId, matchRequest, pendingSubs);
            if (matched > 0) {
                pendingSubs.forEach(s -> notifiedSubs.add(s.getId()));
            }
            totalEvaluated++;
            totalTriggered += matched;
        }

        String msg = String.format("Evaluated %d matching database crop prices for user %d on login. New alerts triggered: %d",
                totalEvaluated, userId, totalTriggered);
        log.info(msg);

        return MatchResultResponse.builder()
                .matchedCount(totalEvaluated)
                .notificationsTriggered(totalTriggered)
                .message(msg)
                .build();
    }
}
