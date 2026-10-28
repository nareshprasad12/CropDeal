package com.example.notification.service;

import com.example.notification.config.RabbitMQConfig;
import com.example.notification.dto.PriceAlertTriggeredEvent;
import com.example.notification.entity.Notification;
import com.example.notification.repository.NotificationRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class PriceAlertConsumer {

    private static final Logger log = LoggerFactory.getLogger(PriceAlertConsumer.class);

    private final NotificationRepository notificationRepository;

    public PriceAlertConsumer(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    /**
     * 1. Price Alert Queue Consumer (cropdeal.price-alert.queue)
     */
    @RabbitListener(queues = RabbitMQConfig.PRICE_ALERT_QUEUE)
    public void consumePriceAlert(PriceAlertTriggeredEvent event) {
        if (event == null) {
            log.warn("Received null PriceAlertTriggeredEvent");
            return;
        }

        log.info("Processing PriceAlertTriggeredEvent from cropdeal.price-alert.queue: subId={}, userId={}, role={}, crop={}, matchedPrice={}",
                event.getSubscriptionId(), event.getUserId(), event.getUserRole(), event.getCropName(), event.getMatchedPrice());

        try {
            Notification notification = new Notification();
            String rec = event.getUserId() != null ? String.valueOf(event.getUserId()) : "1";
            notification.setRecipient(rec);
            notification.setType("PRICE_ALERT");
            String msg = event.getMessage() != null ? event.getMessage() : (event.getTitle() != null ? event.getTitle() : "Government APMC Market Price Alert Triggered");
            notification.setMessage(msg);
            notification.setStatus("SENT");

            Notification saved = notificationRepository.save(notification);
            log.info("Persisted price alert notification #{} for user {}", saved.getId(), saved.getRecipient());
        } catch (Exception ex) {
            log.error("Failed to save price alert notification for user {}: {}", event.getUserId(), ex.getMessage(), ex);
        }
    }

    /**
     * 2. General Notification Queue Consumer (cropdeal.notification.queue)
     * Handles all notifications across the application:
     * - Order events (ORDER_PLACED, ORDER_COMPLETED, ORDER_COMPENSATED)
     * - Crop published & crop updates
     * - Negotiations & offers
     * - Deliveries & status tracking
     * - Biddings
     * - Wallet & system alerts
     */
    @RabbitListener(queues = RabbitMQConfig.QUEUE)
    public void consumeNotificationQueue(Map<String, Object> event) {
        if (event == null || event.isEmpty()) {
            log.warn("Received empty event from cropdeal.notification.queue");
            return;
        }

        log.info("Processing notification event from cropdeal.notification.queue: {}", event);

        try {
            // 1. Order Service Event with eventType (e.g. ORDER_PLACED, ORDER_COMPLETED, ORDER_COMPENSATED)
            if (event.containsKey("eventType")) {
                String eventType = String.valueOf(event.get("eventType"));
                Object orderIdObj = event.get("orderId");
                Long orderId = orderIdObj != null ? Long.valueOf(String.valueOf(orderIdObj)) : null;
                String cropName = String.valueOf(event.getOrDefault("cropName", "Crop"));
                String totalAmount = String.valueOf(event.getOrDefault("totalAmount", "0"));
                Object farmerIdObj = event.get("farmerId");
                Object dealerIdObj = event.get("dealerId");

                if ("ORDER_PLACED".equalsIgnoreCase(eventType)) {
                    // 1. Notify Farmer
                    if (farmerIdObj != null) {
                        saveDirectNotification(
                                String.valueOf(farmerIdObj),
                                "ORDER",
                                String.format("🎉 Crop Purchased: Dealer purchased \"%s\" (Order #%s). Total earned: ₹%s. Wallet credited!",
                                        cropName, orderId != null ? orderId : "N/A", totalAmount),
                                orderId
                        );
                    }

                    // 2. Notify Dealer
                    if (dealerIdObj != null) {
                        saveDirectNotification(
                                String.valueOf(dealerIdObj),
                                "ORDER",
                                String.format("✅ Order Confirmed: Order #%s for \"%s\" placed successfully. Total paid: ₹%s.",
                                        orderId != null ? orderId : "N/A", cropName, totalAmount),
                                orderId
                        );
                    }
                    return;
                } else if ("ORDER_COMPLETED".equalsIgnoreCase(eventType)) {
                    if (dealerIdObj != null) {
                        saveDirectNotification(
                                String.valueOf(dealerIdObj),
                                "ORDER",
                                String.format("🚚 Order #%s Delivered Successfully! Thank you for trading on CropDeal.",
                                        orderId != null ? orderId : "N/A"),
                                orderId
                        );
                    }
                    return;
                } else if ("ORDER_COMPENSATED".equalsIgnoreCase(eventType)) {
                    String reason = String.valueOf(event.getOrDefault("reason", "Payment issue"));
                    if (dealerIdObj != null) {
                        saveDirectNotification(
                                String.valueOf(dealerIdObj),
                                "ORDER",
                                String.format("⚠️ Order #%s Cancelled: %s. Compensating refund processed.",
                                        orderId != null ? orderId : "N/A", reason),
                                orderId
                        );
                    }
                    return;
                }
            }

            // 2. Direct Notification Request (ORDER, CROP_PUBLISHED, NEGOTIATION, DELIVERY, BID, WALLET, SYSTEM)
            saveMapNotification(event, "SYSTEM");

        } catch (Exception ex) {
            log.error("Failed to process event from cropdeal.notification.queue: {}", ex.getMessage(), ex);
        }
    }

    private void saveMapNotification(Map<String, Object> event, String defaultType) {
        try {
            Object recipientObj = event.get("recipient");
            if (recipientObj == null) recipientObj = event.get("userId");
            String recipient = recipientObj != null ? String.valueOf(recipientObj) : "1";

            Object typeObj = event.get("type");
            String type = typeObj != null ? String.valueOf(typeObj) : defaultType;

            Object msgObj = event.get("message");
            if (msgObj == null) msgObj = event.get("title");
            if (msgObj == null) msgObj = "New " + defaultType + " update";
            String message = String.valueOf(msgObj);

            Long orderId = null;
            Object orderIdObj = event.get("orderId");
            if (orderIdObj != null) {
                try {
                    orderId = Long.valueOf(String.valueOf(orderIdObj));
                } catch (Exception ignored) {}
            }

            saveDirectNotification(recipient, type, message, orderId);
        } catch (Exception ex) {
            log.error("Failed to save {} notification from cropdeal.notification.queue: {}", defaultType, ex.getMessage(), ex);
        }
    }

    private void saveDirectNotification(String recipient, String type, String message, Long orderId) {
        Notification notification = new Notification();
        String rec = recipient != null ? recipient.trim() : "1";
        String digits = rec.replaceAll("\\D+", "");
        if (!digits.isEmpty() && (rec.toLowerCase().startsWith("dealer") || rec.toLowerCase().startsWith("farmer") || rec.toLowerCase().startsWith("delivery") || rec.toUpperCase().startsWith("USER_"))) {
            rec = digits;
        }
        notification.setRecipient(rec);
        notification.setType(type != null ? type : "SYSTEM");
        notification.setMessage(message != null ? message : "New notification");
        notification.setOrderId(orderId);
        notification.setStatus("SENT");
        Notification saved = notificationRepository.save(notification);
        log.info("Persisted {} notification #{} for user {}", saved.getType(), saved.getId(), saved.getRecipient());
    }
}
