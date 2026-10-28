package com.cropdeal.pricealert.service;

import com.cropdeal.pricealert.client.PriceServiceClient;
import com.cropdeal.pricealert.dto.CreateSubscriptionRequest;
import com.cropdeal.pricealert.dto.DatabasePriceDto;
import com.cropdeal.pricealert.dto.PriceAlertTriggeredEvent;
import com.cropdeal.pricealert.dto.SubscriptionResponse;
import com.cropdeal.pricealert.entity.PriceAlertNotification;
import com.cropdeal.pricealert.entity.PriceAlertSubscription;
import com.cropdeal.pricealert.enums.AlertSourceType;
import com.cropdeal.pricealert.repository.PriceAlertNotificationRepository;
import com.cropdeal.pricealert.repository.PriceAlertSubscriptionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.List;
import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
@Slf4j
public class PriceSubscriptionService {

    private final PriceAlertSubscriptionRepository subscriptionRepository;
    private final PriceAlertNotificationRepository notificationRepository;
    private final PriceServiceClient priceServiceClient;
    private final PriceAlertPublisher alertPublisher;
    private final PriceAlertMatchingEngine matchingEngine;

    @Transactional
    public SubscriptionResponse createSubscription(CreateSubscriptionRequest request) {
        log.info("Creating price subscription for userId={}, role={}, crop={}, targetPrice={}",
                request.getUserId(), request.getUserRole(), request.getCropName(), request.getTargetPrice());

        PriceAlertSubscription subscription = PriceAlertSubscription.builder()
                .userId(request.getUserId())
                .userRole(request.getUserRole())
                .cropName(request.getCropName().trim().toLowerCase())
                .targetPrice(request.getTargetPrice())
                .priceCondition(request.getPriceCondition())
                .district(request.getDistrict() != null ? request.getDistrict().trim() : null)
                .state(request.getState() != null ? request.getState().trim() : null)
                .unit(request.getUnit() != null ? request.getUnit().trim() : "kg")
                .active(true)
                .build();

        PriceAlertSubscription saved = subscriptionRepository.save(subscription);

        // Immediate check against stored database market prices to trigger alert synchronously if condition is satisfied
        try {
            if (priceServiceClient != null && alertPublisher != null && matchingEngine != null) {
                List<DatabasePriceDto> dbPrices = priceServiceClient.getLatestStoredPricesFromDb();
                if (dbPrices != null && !dbPrices.isEmpty()) {
                    String subCrop = saved.getCropName().trim().toLowerCase();
                    for (DatabasePriceDto priceDto : dbPrices) {
                        if (priceDto.getCommodity() == null) continue;
                        String com = priceDto.getCommodity().trim().toLowerCase();
                        if (com.contains(subCrop) || subCrop.contains(com)) {
                            Double pVal = priceDto.getModalPricePerKg();
                            if (pVal == null || pVal <= 0) pVal = priceDto.getMinPricePerKg();
                            if (pVal == null || pVal <= 0) pVal = priceDto.getMaxPricePerKg();
                            if (pVal != null && pVal > 0) {
                                BigDecimal effectivePrice = BigDecimal.valueOf(pVal).setScale(2, RoundingMode.HALF_UP);
                                boolean conditionMet = matchingEngine.evaluatePriceCondition(saved.getPriceCondition(), saved.getTargetPrice(), effectivePrice);
                                if (conditionMet) {
                                    String cropDisplay = priceDto.getCommodity().substring(0, 1).toUpperCase() + priceDto.getCommodity().substring(1).toLowerCase();
                                    String title = String.format("🔔 Price Alert Triggered: %s at ₹%.2f/kg", cropDisplay, effectivePrice);
                                    String message = String.format("Government APMC market price for %s has reached ₹%.2f/kg, satisfying your %s alert threshold (₹%.2f/kg).",
                                            cropDisplay, effectivePrice, saved.getPriceCondition(), saved.getTargetPrice());

                                    PriceAlertNotification notif = PriceAlertNotification.builder()
                                            .subscriptionId(saved.getId())
                                            .userId(saved.getUserId())
                                            .sourceType(AlertSourceType.MARKET_PRICE)
                                            .sourceId(System.currentTimeMillis())
                                            .cropName(cropDisplay)
                                            .targetPrice(saved.getTargetPrice())
                                            .matchedPrice(effectivePrice)
                                            .message(message)
                                            .notificationSent(true)
                                            .triggeredAt(LocalDateTime.now())
                                            .build();
                                    notificationRepository.save(notif);

                                    PriceAlertTriggeredEvent event = PriceAlertTriggeredEvent.builder()
                                            .subscriptionId(saved.getId())
                                            .userId(saved.getUserId())
                                            .userRole(saved.getUserRole())
                                            .cropName(cropDisplay)
                                            .targetPrice(saved.getTargetPrice())
                                            .matchedPrice(effectivePrice)
                                            .priceCondition(saved.getPriceCondition())
                                            .sourceType(AlertSourceType.MARKET_PRICE)
                                            .sourceId(notif.getSourceId())
                                            .district(priceDto.getDistrict())
                                            .state(priceDto.getState())
                                            .unit("kg")
                                            .title(title)
                                            .message(message)
                                            .timestamp(LocalDateTime.now())
                                            .build();

                                    alertPublisher.publishAlert(event);
                                    saved.setLastNotifiedAt(LocalDateTime.now());
                                    subscriptionRepository.save(saved);
                                    log.info("Triggered price alert immediately for user {} on subscription #{}: matched ₹{}",
                                            saved.getUserId(), saved.getId(), effectivePrice);
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        } catch (Exception ex) {
            log.warn("Immediate price alert check for subscription #{} encountered error: {}", saved.getId(), ex.getMessage());
        }

        return SubscriptionResponse.fromEntity(saved);
    }

    @Transactional(readOnly = true)
    public List<SubscriptionResponse> getSubscriptionsByUser(Long userId) {
        return subscriptionRepository.findByUserId(userId).stream()
                .map(SubscriptionResponse::fromEntity)
                .toList();
    }

    @Transactional(readOnly = true)
    public SubscriptionResponse getSubscriptionById(Long id) {
        return subscriptionRepository.findById(id)
                .map(SubscriptionResponse::fromEntity)
                .orElseThrow(() -> new NoSuchElementException("Price alert subscription not found with id: " + id));
    }

    @Transactional
    public SubscriptionResponse toggleSubscriptionStatus(Long id, boolean active) {
        PriceAlertSubscription subscription = subscriptionRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Price alert subscription not found with id: " + id));
        subscription.setActive(active);
        PriceAlertSubscription saved = subscriptionRepository.save(subscription);
        return SubscriptionResponse.fromEntity(saved);
    }

    @Transactional
    public void deleteSubscription(Long id) {
        if (!subscriptionRepository.existsById(id)) {
            throw new NoSuchElementException("Price alert subscription not found with id: " + id);
        }
        subscriptionRepository.deleteById(id);
    }

    @Transactional(readOnly = true)
    public List<PriceAlertNotification> getAlertHistoryForUser(Long userId) {
        return notificationRepository.findByUserIdOrderByTriggeredAtDesc(userId);
    }

    @Transactional(readOnly = true)
    public List<PriceAlertNotification> getAlertHistoryForSubscription(Long subscriptionId) {
        return notificationRepository.findBySubscriptionIdOrderByTriggeredAtDesc(subscriptionId);
    }
}
