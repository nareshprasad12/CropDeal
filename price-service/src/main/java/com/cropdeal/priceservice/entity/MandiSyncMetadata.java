package com.cropdeal.priceservice.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "mandi_sync_metadata")
public class MandiSyncMetadata {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDateTime lastSuccessfulSyncAt;

    @Column(nullable = false, length = 50)
    private String syncStatus; // SUCCESS, FAILED, IN_PROGRESS

    private Integer recordsFetched;

    private Integer recordsInserted;

    private Integer recordsUpdated;

    @Column(length = 2000)
    private String lastError;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public MandiSyncMetadata() {}

    public MandiSyncMetadata(LocalDateTime lastSuccessfulSyncAt, String syncStatus, Integer recordsFetched, Integer recordsInserted, Integer recordsUpdated, String lastError) {
        this.lastSuccessfulSyncAt = lastSuccessfulSyncAt;
        this.syncStatus = syncStatus;
        this.recordsFetched = recordsFetched;
        this.recordsInserted = recordsInserted;
        this.recordsUpdated = recordsUpdated;
        this.lastError = lastError;
    }

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDateTime getLastSuccessfulSyncAt() {
        return lastSuccessfulSyncAt;
    }

    public void setLastSuccessfulSyncAt(LocalDateTime lastSuccessfulSyncAt) {
        this.lastSuccessfulSyncAt = lastSuccessfulSyncAt;
    }

    public String getSyncStatus() {
        return syncStatus;
    }

    public void setSyncStatus(String syncStatus) {
        this.syncStatus = syncStatus;
    }

    public Integer getRecordsFetched() {
        return recordsFetched;
    }

    public void setRecordsFetched(Integer recordsFetched) {
        this.recordsFetched = recordsFetched;
    }

    public Integer getRecordsInserted() {
        return recordsInserted;
    }

    public void setRecordsInserted(Integer recordsInserted) {
        this.recordsInserted = recordsInserted;
    }

    public Integer getRecordsUpdated() {
        return recordsUpdated;
    }

    public void setRecordsUpdated(Integer recordsUpdated) {
        this.recordsUpdated = recordsUpdated;
    }

    public String getLastError() {
        return lastError;
    }

    public void setLastError(String lastError) {
        this.lastError = lastError;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
}
