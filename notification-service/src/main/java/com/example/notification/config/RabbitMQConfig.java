package com.example.notification.config;

import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.config.SimpleRabbitListenerContainerFactory;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.support.converter.DefaultJackson2JavaTypeMapper;
import org.springframework.amqp.support.converter.Jackson2JavaTypeMapper;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    public static final String EXCHANGE = "cropdeal.notification.exchange";
    public static final String QUEUE = "cropdeal.notification.queue";
    public static final String ROUTING_KEY = "notification.#";

    public static final String PRICE_ALERT_QUEUE = "cropdeal.price-alert.queue";
    public static final String PRICE_ALERT_ROUTING_KEY = "price.#";

    public static final String ORDER_EXCHANGE = "cropdeal.exchange";

    @Bean
    public TopicExchange notificationExchange() {
        return new TopicExchange(EXCHANGE, true, false);
    }

    @Bean
    public TopicExchange orderExchange() {
        return new TopicExchange(ORDER_EXCHANGE, true, false);
    }

    // 1. Notification Queue (cropdeal.notification.queue) - receives ALL system, order, crop, bid, negotiation, delivery notifications
    @Bean
    public Queue notificationQueue() {
        return new Queue(QUEUE, true);
    }

    @Bean
    public Binding notificationBinding(Queue notificationQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(notificationQueue).to(notificationExchange).with(ROUTING_KEY);
    }

    @Bean
    public Binding notificationExactBinding(Queue notificationQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(notificationQueue).to(notificationExchange).with("notification");
    }

    @Bean
    public Binding notificationOrderBinding(Queue notificationQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(notificationQueue).to(notificationExchange).with("order.#");
    }

    @Bean
    public Binding notificationCropBinding(Queue notificationQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(notificationQueue).to(notificationExchange).with("crop.#");
    }

    @Bean
    public Binding notificationBidBinding(Queue notificationQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(notificationQueue).to(notificationExchange).with("bid.#");
    }

    @Bean
    public Binding notificationNegotiationBinding(Queue notificationQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(notificationQueue).to(notificationExchange).with("negotiation.#");
    }

    @Bean
    public Binding notificationDeliveryBinding(Queue notificationQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(notificationQueue).to(notificationExchange).with("delivery.#");
    }

    @Bean
    public Binding notificationOrderExchangeBinding(Queue notificationQueue, TopicExchange orderExchange) {
        return BindingBuilder.bind(notificationQueue).to(orderExchange).with("cropdeal.order.#");
    }

    // 2. Price Alert Queue (cropdeal.price-alert.queue) - receives ALL price alert notifications
    @Bean
    public Queue priceAlertQueue() {
        return new Queue(PRICE_ALERT_QUEUE, true);
    }

    @Bean
    public Binding priceAlertBinding(Queue priceAlertQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(priceAlertQueue).to(notificationExchange).with(PRICE_ALERT_ROUTING_KEY);
    }

    @Bean
    public Binding priceAlertExactBinding(Queue priceAlertQueue, TopicExchange notificationExchange) {
        return BindingBuilder.bind(priceAlertQueue).to(notificationExchange).with("price.alert");
    }

    @Bean
    public MessageConverter jsonMessageConverter() {
        com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
        mapper.registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule());
        mapper.disable(com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        mapper.configure(com.fasterxml.jackson.databind.DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        Jackson2JsonMessageConverter converter = new Jackson2JsonMessageConverter(mapper);
        DefaultJackson2JavaTypeMapper typeMapper = new DefaultJackson2JavaTypeMapper();
        typeMapper.setTypePrecedence(Jackson2JavaTypeMapper.TypePrecedence.INFERRED);
        converter.setJavaTypeMapper(typeMapper);
        return converter;
    }

    @Bean
    public SimpleRabbitListenerContainerFactory rabbitListenerContainerFactory(
            ConnectionFactory connectionFactory,
            MessageConverter jsonMessageConverter) {
        SimpleRabbitListenerContainerFactory factory = new SimpleRabbitListenerContainerFactory();
        factory.setConnectionFactory(connectionFactory);
        factory.setMessageConverter(jsonMessageConverter);
        return factory;
    }
}
