package com.cropdeal.priceservice.controller;

import com.cropdeal.priceservice.dto.CropPriceResponse;
import com.cropdeal.priceservice.dto.PriceRecommendationResponse;
import com.cropdeal.priceservice.dto.PriceSearchRequest;
import com.cropdeal.priceservice.dto.SyncResponse;
import com.cropdeal.priceservice.dto.SyncStatusResponse;
import com.cropdeal.priceservice.entity.MarketPrice;
import com.cropdeal.priceservice.service.PriceService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import java.time.LocalDate;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping({"/api/prices", "/api/v1/prices"})
@Tag(name = "Market & Government Pricing", description = "Endpoints for market prices, commodity lookup, and government data")
public class PriceController {

    private final PriceService priceService;

    public PriceController(PriceService priceService) {
        this.priceService = priceService;
    }

    /**
     * Server-side paginated retrieval of government & APMC mandi prices.
     * Example: GET /api/prices?page=0&size=25&sortBy=arrivalDate&direction=desc
     */
    @GetMapping
    @Operation(summary = "Get paginated mandi prices", description = "Server-side pagination and filtering across all stored government mandi records")
    public ResponseEntity<Page<MarketPrice>> getPrices(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "25") int size,
            @RequestParam(defaultValue = "arrivalDate") String sortBy,
            @RequestParam(defaultValue = "desc") String direction,
            @RequestParam(required = false) String commodity,
            @RequestParam(required = false) String state,
            @RequestParam(required = false) String district,
            @RequestParam(required = false) String market,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate arrivalDate) {

        Sort.Direction dir = "asc".equalsIgnoreCase(direction) ? Sort.Direction.ASC : Sort.Direction.DESC;
        String safeSort = switch (sortBy) {
            case "commodity" -> "commodity";
            case "state" -> "state";
            case "district" -> "district";
            case "market" -> "market";
            case "modalPrice", "modalPricePerKg" -> "modalPrice";
            case "minPrice", "minPricePerKg" -> "minPrice";
            case "maxPrice", "maxPricePerKg" -> "maxPrice";
            default -> "arrivalDate";
        };

        Pageable pageable = PageRequest.of(Math.max(0, page), Math.max(1, Math.min(size, 200)), Sort.by(dir, safeSort));
        Page<MarketPrice> result = priceService.getPaginatedPrices(commodity, state, district, market, arrivalDate, pageable);
        return ResponseEntity.ok(result);
    }

    /**
     * Store and display the last successful update time and sync metadata.
     */
    @GetMapping("/sync-status")
    @Operation(summary = "Get government data sync status", description = "Returns metadata for the most recent government data synchronization")
    public ResponseEntity<SyncStatusResponse> getSyncStatus() {
        return ResponseEntity.ok(priceService.getSyncStatus());
    }

    /**
     * Location-based Mandi price recommendation for farmer produce posting (crops/add).
     */
    @GetMapping("/recommendation")
    @Operation(summary = "Get location-based mandi price recommendation", description = "Recommends benchmark prices by District, State, or National APMC rates")
    public ResponseEntity<PriceRecommendationResponse> getPriceRecommendation(
            @RequestParam String commodity,
            @RequestParam(required = false) String location,
            @RequestParam(required = false) String state,
            @RequestParam(required = false) String district) {
        return ResponseEntity.ok(priceService.getPriceRecommendation(commodity, location, state, district));
    }

    /**
     * Distinct available states from database.
     */
    @GetMapping("/states")
    @Operation(summary = "Get distinct states", description = "Returns all unique states present in the mandi database")
    public ResponseEntity<List<String>> getStates() {
        return ResponseEntity.ok(priceService.getDistinctStates());
    }

    /**
     * Distinct available commodities from database.
     */
    @GetMapping("/commodities")
    @Operation(summary = "Get distinct commodities", description = "Returns all unique commodities present in the mandi database")
    public ResponseEntity<List<String>> getCommodities() {
        return ResponseEntity.ok(priceService.getDistinctCommodities());
    }

    /**
     * Searches district first, then state, while keeping the requested grade
     * isolated. Only the latest available arrival date is used.
     */
    @PostMapping("/lookup")
    @Operation(summary = "Lookup market crop price from database", description = "Queries database for latest arrival date price by commodity, state, district, grade")
    public CropPriceResponse lookupPrice(@Valid @RequestBody PriceSearchRequest request) {
        return priceService.getCropPrice(request);
    }

    /** Lookup latest database benchmark price directly by commodity name */
    @GetMapping("/commodity/{commodity}")
    @Operation(summary = "Lookup latest price by commodity name from database", description = "Finds latest stored database price for the given commodity")
    public ResponseEntity<CropPriceResponse> getPriceByCommodity(@PathVariable String commodity) {
        return priceService.getLatestPriceByCommodity(commodity)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    /** Validate crop price against database benchmark (used by chatbot and services) */
    @GetMapping("/validate")
    @Operation(summary = "Validate crop price against database benchmark")
    public ResponseEntity<CropPriceResponse> validateCropPrice(
            @RequestParam(required = false) String cropName,
            @RequestParam(required = false) String commodity) {
        String query = cropName != null ? cropName : commodity;
        return priceService.getLatestPriceByCommodity(query)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    /** Returns latest-day aggregated prices for all crops available in the database. */
    @GetMapping("/all")
    @Operation(summary = "Get all latest crop prices from database", description = "Returns stored government and market prices for all crops in our database")
    public List<CropPriceResponse> getAllLatestPrices() {
        return priceService.getAllLatestCropPrices();
    }

    /** Manual trigger to sync government prices on-demand */
    @PostMapping("/sync")
    @Operation(summary = "Manually synchronize government prices", description = "On-demand synchronization from data.gov.in. Disabled on startup to prevent repeated external calls.")
    public ResponseEntity<SyncResponse> syncGovernmentPrices() {
        return ResponseEntity.ok(priceService.syncLatestGovernmentPrices());
    }
}
