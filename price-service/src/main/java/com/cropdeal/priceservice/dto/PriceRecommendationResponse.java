package com.cropdeal.priceservice.dto;

import java.time.LocalDate;

public class PriceRecommendationResponse {

    private String commodity;
    private String state;
    private String district;
    private String market;
    private Double recommendedPricePerKg;
    private Double minPricePerKg;
    private Double maxPricePerKg;
    private Double modalPricePerKg;
    private String matchType; // SAME_DISTRICT, NEAREST_MARKET, REGIONAL_ESTIMATE, NO_DATA
    private String explanation;
    private LocalDate arrivalDate;

    public PriceRecommendationResponse() {}

    public PriceRecommendationResponse(String commodity, String state, String district, String market, Double recommendedPricePerKg, Double minPricePerKg, Double maxPricePerKg, Double modalPricePerKg, String matchType, String explanation, LocalDate arrivalDate) {
        this.commodity = commodity;
        this.state = state;
        this.district = district;
        this.market = market;
        this.recommendedPricePerKg = recommendedPricePerKg;
        this.minPricePerKg = minPricePerKg;
        this.maxPricePerKg = maxPricePerKg;
        this.modalPricePerKg = modalPricePerKg;
        this.matchType = matchType;
        this.explanation = explanation;
        this.arrivalDate = arrivalDate;
    }

    public String getCommodity() {
        return commodity;
    }

    public void setCommodity(String commodity) {
        this.commodity = commodity;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public String getMarket() {
        return market;
    }

    public void setMarket(String market) {
        this.market = market;
    }

    public Double getRecommendedPricePerKg() {
        return recommendedPricePerKg;
    }

    public void setRecommendedPricePerKg(Double recommendedPricePerKg) {
        this.recommendedPricePerKg = recommendedPricePerKg;
    }

    public Double getMinPricePerKg() {
        return minPricePerKg;
    }

    public void setMinPricePerKg(Double minPricePerKg) {
        this.minPricePerKg = minPricePerKg;
    }

    public Double getMaxPricePerKg() {
        return maxPricePerKg;
    }

    public void setMaxPricePerKg(Double maxPricePerKg) {
        this.maxPricePerKg = maxPricePerKg;
    }

    public Double getModalPricePerKg() {
        return modalPricePerKg;
    }

    public void setModalPricePerKg(Double modalPricePerKg) {
        this.modalPricePerKg = modalPricePerKg;
    }

    public String getMatchType() {
        return matchType;
    }

    public void setMatchType(String matchType) {
        this.matchType = matchType;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public LocalDate getArrivalDate() {
        return arrivalDate;
    }

    public void setArrivalDate(LocalDate arrivalDate) {
        this.arrivalDate = arrivalDate;
    }
}
