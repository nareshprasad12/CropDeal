package com.example.notification.service;

import com.example.notification.dto.NotificationRequest;
import com.example.notification.dto.NotificationResponse;
import com.example.notification.entity.Notification;
import com.example.notification.exception.NotificationException;
import com.example.notification.repository.NotificationRepository;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import com.example.notification.config.RabbitMQConfig;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class NotificationServiceImpl
        implements NotificationService {

    private final NotificationRepository notificationRepository;
    private final TemplateService templateService;
    private final EmailService emailService;
    private final RabbitTemplate rabbitTemplate;

    public NotificationServiceImpl(
            NotificationRepository notificationRepository,
            TemplateService templateService,
            EmailService emailService,
            RabbitTemplate rabbitTemplate) {

        this.notificationRepository = notificationRepository;
        this.templateService = templateService;
        this.emailService = emailService;
        this.rabbitTemplate = rabbitTemplate;
    }

    @Override
    public NotificationResponse sendNotification(
            NotificationRequest request) {

        try {
            // Asynchronously publish to RabbitMQ exchange with dynamic routing key based on notification type
            if (rabbitTemplate != null) {
                String type = request.getType() != null ? request.getType().toUpperCase() : "SYSTEM";
                String exchange = RabbitMQConfig.EXCHANGE;
                String routingKey;

                switch (type) {
                    case "ORDER":
                        routingKey = "cropdeal.order.notification";
                        exchange = RabbitMQConfig.ORDER_EXCHANGE;
                        break;
                    case "PRICE_ALERT":
                        routingKey = "price.alert";
                        com.example.notification.dto.PriceAlertTriggeredEvent alertEvent = new com.example.notification.dto.PriceAlertTriggeredEvent();
                        String digits = request.getRecipient() != null ? request.getRecipient().replaceAll("\\D+", "") : "1";
                        try {
                            alertEvent.setUserId(Long.parseLong(digits.isEmpty() ? "1" : digits));
                        } catch (Exception e) {
                            alertEvent.setUserId(1L);
                        }
                        alertEvent.setMessage(request.getMessage());
                        alertEvent.setTitle(request.getMessage());
                        alertEvent.setCropName("APMC Commodity");
                        alertEvent.setUserRole("USER");
                        alertEvent.setTimestamp(LocalDateTime.now());
                        rabbitTemplate.convertAndSend(exchange, routingKey, alertEvent);
                        break;
                    case "BID":
                        routingKey = "bid.placed";
                        break;
                    case "NEGOTIATION":
                        routingKey = "negotiation.offer";
                        break;
                    case "DELIVERY":
                        routingKey = "delivery.status";
                        break;
                    case "CROP":
                    case "CROP_PUBLISHED":
                        routingKey = "crop.published";
                        break;
                    default:
                        routingKey = "notification.general";
                        break;
                }

                if (!"PRICE_ALERT".equals(type)) {
                    Map<String, Object> payload = new java.util.HashMap<>();
                    payload.put("recipient", request.getRecipient());
                    payload.put("type", request.getType());
                    payload.put("message", request.getMessage());
                    payload.put("orderId", request.getOrderId());
                    payload.put("timestamp", System.currentTimeMillis());
                    rabbitTemplate.convertAndSend(exchange, routingKey, payload);
                }
            }

            NotificationResponse response = new NotificationResponse();
            response.setRecipient(request.getRecipient());
            response.setType(request.getType() != null ? request.getType() : "SYSTEM");
            response.setMessage(request.getMessage());
            response.setOrderId(request.getOrderId());
            response.setStatus("QUEUED");
            response.setCreatedAt(LocalDateTime.now());

            return response;

        } catch (Exception e) {
            throw new NotificationException(
                    "Failed to send notification: " + e.getMessage()
            );
        }
    }

    @Override
    public NotificationResponse sendOtp(
            String phoneNumber,
            String otp) {

        String message =
                templateService.generateOtpMessage(otp);

        System.out.println(
                "SMS TO " + phoneNumber + ": " + message
        );

        Notification notification =
                new Notification();

        notification.setRecipient(phoneNumber);
        notification.setType("DELIVERY_OTP");
        notification.setMessage(message);
        notification.setStatus("SENT");

        Notification saved =
                notificationRepository.save(notification);

        return mapToResponse(saved);
    }

    @Override
    public NotificationResponse
    sendDeliveryCompletedNotification(
            String phoneNumber,
            Long orderId) {

        String message =
                templateService
                        .generateDeliveryCompletedMessage(
                                orderId
                        );

        System.out.println(
                "SMS TO " + phoneNumber + ": " + message
        );

        Notification notification =
                new Notification();

        notification.setRecipient(phoneNumber);
        notification.setType("DELIVERY_COMPLETED");
        notification.setMessage(message);
        notification.setOrderId(orderId);
        notification.setStatus("SENT");

        Notification saved =
                notificationRepository.save(notification);

        return mapToResponse(saved);
    }

    @Override
    public NotificationResponse getNotification(
            Long notificationId) {

        Notification notification =
                notificationRepository.findById(notificationId)
                        .orElseThrow(
                                () -> new NotificationException(
                                        "Notification not found"
                                )
                        );

        return mapToResponse(notification);
    }

    @Override
    public List<NotificationResponse>
    getNotificationsByRecipient(
            String recipient) {

        return notificationRepository
                .findByRecipientOrderByCreatedAtDesc(
                        recipient
                )
                .stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Override
    public List<NotificationResponse>
    getNotificationsByOrder(Long orderId) {

        return notificationRepository
                .findByOrderId(orderId)
                .stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Override
    public List<NotificationResponse> getNotificationsByUser(String userId) {
        if (userId == null || userId.trim().isEmpty()) {
            return List.of();
        }

        String u = userId.trim();
        List<String> recipients = new ArrayList<>();
        recipients.add(u);
        recipients.add("USER_" + u);
        recipients.add("ALL");
        recipients.add(u.toLowerCase());

        String digits = u.replaceAll("\\D+", "");
        if (!digits.isEmpty()) {
            recipients.add(digits);
            recipients.add("USER_" + digits);
            recipients.add("dealer-" + digits);
            recipients.add("farmer-" + digits);
            recipients.add("delivery-" + digits);
            recipients.add("delivery_partner-" + digits);
            if (digits.equals("1")) recipients.add("farmer");
            if (digits.equals("2")) recipients.add("dealer");
            if (digits.equals("3")) recipients.add("delivery");
            if (digits.equals("4")) recipients.add("admin");
        }

        if (u.toLowerCase().contains("farmer")) recipients.add("1");
        if (u.toLowerCase().contains("dealer")) recipients.add("2");
        if (u.toLowerCase().contains("delivery")) recipients.add("3");
        if (u.toLowerCase().contains("admin")) recipients.add("4");

        return notificationRepository
                .findByRecipientInOrderByCreatedAtDesc(recipients)
                .stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Override
    public void markAsRead(Long notificationId) {
        notificationRepository.findById(notificationId).ifPresent(n -> {
            n.setStatus("READ");
            notificationRepository.save(n);
        });
    }

    @Override
    public void markAllAsRead(String userId) {
        List<NotificationResponse> list = getNotificationsByUser(userId);
        list.forEach(r -> {
            notificationRepository.findById(r.getId()).ifPresent(n -> {
                n.setStatus("READ");
                notificationRepository.save(n);
            });
        });
    }

    @Override
    public void clearAllForUser(String userId) {
        List<NotificationResponse> list = getNotificationsByUser(userId);
        list.forEach(r -> {
            try {
                notificationRepository.deleteById(r.getId());
            } catch (Exception ignored) {}
        });
    }

    @Override
    public void deleteNotification(Long notificationId) {
        try {
            notificationRepository.deleteById(notificationId);
        } catch (Exception ignored) {}
    }

    private NotificationResponse mapToResponse(
            Notification notification) {

        NotificationResponse response =
                new NotificationResponse();

        response.setId(
                notification.getId()
        );

        response.setRecipient(
                notification.getRecipient()
        );

        response.setType(
                notification.getType()
        );

        response.setMessage(
                notification.getMessage()
        );

        response.setStatus(
                notification.getStatus()
        );

        response.setOrderId(
                notification.getOrderId()
        );

        response.setCreatedAt(
                notification.getCreatedAt()
        );

        response.setRead(
                "READ".equalsIgnoreCase(notification.getStatus())
        );

        return response;
    }
}
