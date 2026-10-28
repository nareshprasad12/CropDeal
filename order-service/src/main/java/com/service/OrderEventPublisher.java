package com.service;

import com.config.RabbitMQConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.Serializable;
import java.util.Map;

@Component
public class OrderEventPublisher {

    private static final Logger log = LoggerFactory.getLogger(OrderEventPublisher.class);

    @Autowired(required = false)
    private RabbitTemplate rabbitTemplate;

    public void publishOrderPlacedEvent(Long orderId, String cropName, Object totalAmount, Long buyerId, Long farmerId) {
        // Message 1 for Farmer Side (routed to cropdeal.notification.queue)
        Map<String, Object> farmerEvent = new java.util.HashMap<>();
        farmerEvent.put("recipient", String.valueOf(farmerId));
        farmerEvent.put("type", "ORDER");
        farmerEvent.put("message", String.format("🎉 Crop Purchased: Dealer purchased \"%s\" (Order #%s). Total earned: ₹%s. Wallet credited!",
                cropName != null ? cropName : "Harvest", orderId != null ? orderId : "N/A", totalAmount));
        farmerEvent.put("orderId", orderId);
        farmerEvent.put("targetRole", "FARMER");
        farmerEvent.put("farmerId", farmerId);
        farmerEvent.put("dealerId", buyerId);
        farmerEvent.put("cropName", cropName);
        farmerEvent.put("totalAmount", String.valueOf(totalAmount));
        farmerEvent.put("timestamp", System.currentTimeMillis());
        publish("cropdeal.order.placed.farmer", farmerEvent);

        // Message 2 for Dealer Side (routed to cropdeal.notification.queue)
        Map<String, Object> dealerEvent = new java.util.HashMap<>();
        dealerEvent.put("recipient", String.valueOf(buyerId));
        dealerEvent.put("type", "ORDER");
        dealerEvent.put("message", String.format("✅ Order Confirmed: Order #%s for \"%s\" placed successfully. Total paid: ₹%s.",
                orderId != null ? orderId : "N/A", cropName != null ? cropName : "Harvest", totalAmount));
        dealerEvent.put("orderId", orderId);
        dealerEvent.put("targetRole", "DEALER");
        dealerEvent.put("farmerId", farmerId);
        dealerEvent.put("dealerId", buyerId);
        dealerEvent.put("cropName", cropName);
        dealerEvent.put("totalAmount", String.valueOf(totalAmount));
        dealerEvent.put("timestamp", System.currentTimeMillis());
        publish("cropdeal.order.placed.dealer", dealerEvent);
    }

    public void publishOrderCompletedEvent(Long orderId, String status) {
        Map<String, Object> event = Map.of(
                "eventType", "ORDER_COMPLETED",
                "orderId", orderId,
                "status", status,
                "timestamp", System.currentTimeMillis()
        );
        publish("cropdeal.order.completed", event);
    }

    public void publishOrderCompensatedEvent(Long orderId, String reason) {
        Map<String, Object> event = Map.of(
                "eventType", "ORDER_COMPENSATED",
                "orderId", orderId,
                "reason", reason,
                "timestamp", System.currentTimeMillis()
        );
        publish("cropdeal.order.compensated", event);
    }

    private void publish(String routingKey, Map<String, Object> event) {
        if (rabbitTemplate != null) {
            try {
                rabbitTemplate.convertAndSend(RabbitMQConfig.EXCHANGE_NAME, routingKey, event);
                log.info("RabbitMQ published event [{}] successfully: {}", routingKey, event);
            } catch (Exception e) {
                log.warn("RabbitMQ broker unavailable. Continuing without async event: {}", e.getMessage());
            }
        } else {
            log.info("RabbitTemplate not initialized. Mock event published: {}", event);
        }
    }
}
