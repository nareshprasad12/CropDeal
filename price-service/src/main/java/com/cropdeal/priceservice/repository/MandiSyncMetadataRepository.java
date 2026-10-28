package com.cropdeal.priceservice.repository;

import com.cropdeal.priceservice.entity.MandiSyncMetadata;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface MandiSyncMetadataRepository extends JpaRepository<MandiSyncMetadata, Long> {
    Optional<MandiSyncMetadata> findTopByOrderByIdDesc();
    Optional<MandiSyncMetadata> findTopBySyncStatusOrderByIdDesc(String syncStatus);
}
