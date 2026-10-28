package com.cropdeal.priceservice.dto;

import java.time.LocalDateTime;

public class SyncStatusResponse {

    private String lastSuccessfulSyncAt;
    private String syncStatus;
    private Integer recordsFetched;
    private Integer recordsInserted;
    private Integer recordsUpdated;
    private String lastError;

    public SyncStatusResponse() {}

    public SyncStatusResponse(String lastSuccessfulSyncAt, String syncStatus, Integer recordsFetched, Integer recordsInserted, Integer recordsUpdated, String lastError) {
        this.lastSuccessfulSyncAt = lastSuccessfulSyncAt;
        this.syncStatus = syncStatus;
        this.recordsFetched = recordsFetched;
        this.recordsInserted = recordsInserted;
        this.recordsUpdated = recordsUpdated;
        this.lastError = lastError;
    }

    public String getLastSuccessfulSyncAt() {
        return lastSuccessfulSyncAt;
    }

    public void setLastSuccessfulSyncAt(String lastSuccessfulSyncAt) {
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
}
