package com.cropdeal.delivery.client;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import java.util.HashMap;
import java.util.Map;

@Component
public class DeliveryNotificationClient {

    private static final Logger log = LoggerFactory.getLogger(DeliveryNotificationClient.class);
    private final RestClient restClient;
    private final RestClient fallbackRestClient;

    public DeliveryNotificationClient(
            RestClient.Builder builder,
            @Value("${notification.service.url:http://notification-service:8092}") String notificationServiceUrl) {
        this.restClient = builder.baseUrl(notificationServiceUrl).build();
        this.fallbackRestClient = builder.baseUrl("http://localhost:8092").build();
    }

    public void sendDeliveryStatusNotification(Long dealerId, Long orderId, String cropName, String status, String partnerName) {
        if (dealerId == null && orderId == null) {
            return;
        }

        String recipient = dealerId != null ? String.valueOf(dealerId) : "2";
        String title;
        String details;

        switch (status) {
            case "ASSIGNED":
                title = "🚚 Carrier Assigned";
                details = String.format("Logistics carrier %s has accepted pickup for order #%s (%s).",
                        partnerName != null ? partnerName : "Agro Logistics Partner",
                        orderId != null ? orderId : "N/A",
                        cropName != null ? cropName : "Produce");
                break;
            case "PICKED_UP":
                title = "📦 Produce Picked Up from Farm Gate";
                details = String.format("Your order #%s (%s) has been picked up from the farm gate.",
                        orderId != null ? orderId : "N/A",
                        cropName != null ? cropName : "Produce");
                break;
            case "IN_TRANSIT":
                title = "🚚 Shipment In Transit";
                details = String.format("Your order #%s (%s) is on the road heading to the destination warehouse.",
                        orderId != null ? orderId : "N/A",
                        cropName != null ? cropName : "Produce");
                break;
            case "DELIVERED":
                title = "✅ Order Delivered Successfully";
                details = String.format("Your order #%s (%s) has been delivered! Official GST tax invoice receipt is ready.",
                        orderId != null ? orderId : "N/A",
                        cropName != null ? cropName : "Produce");
                break;
            default:
                title = "🚚 Delivery Status Update";
                details = String.format("Order #%s (%s) status changed to %s.",
                        orderId != null ? orderId : "N/A",
                        cropName != null ? cropName : "Produce",
                        status);
                break;
        }

        Map<String, Object> payload = new HashMap<>();
        payload.put("recipient", recipient);
        payload.put("type", "DELIVERY");
        payload.put("message", title + ": " + details);
        payload.put("orderId", orderId != null ? orderId : 0L);

        try {
            restClient.post()
                    .uri("/api/notifications")
                    .body(payload)
                    .retrieve()
                    .toBodilessEntity();
            log.info("Dispatched delivery notification via primary host to dealer {} for order #{}", recipient, orderId);
        } catch (Exception primaryEx) {
            log.debug("Primary notification service call failed ({}), attempting fallback: {}", primaryEx.getMessage(), primaryEx.toString());
            try {
                fallbackRestClient.post()
                        .uri("/api/notifications")
                        .body(payload)
                        .retrieve()
                        .toBodilessEntity();
                log.info("Dispatched delivery notification via fallback localhost to dealer {} for order #{}", recipient, orderId);
            } catch (Exception fallbackEx) {
                log.warn("Failed to dispatch delivery notification to dealer {}: {}", recipient, fallbackEx.getMessage());
            }
        }
    }
}
