# CropDeal Platform - Background Daemon Master Launcher
$ErrorActionPreference = "Continue"

Write-Host "========================================================" -ForegroundColor Green
Write-Host "       CROPDEAL PLATFORM - BACKEND CLUSTER DAEMON       " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green

Set-Location -Path "D:\cropdealnaresh"

$javaArgs = "-Xms32m -Xmx130m -XX:+TieredCompilation -XX:TieredStopAtLevel=1"
$procs = @()

# 1. Eureka Server & Config Server
Write-Host "`n[1/3] Launching Eureka Server [8761] and Config Server [8888]..." -ForegroundColor Cyan
$pEureka = Start-Process -FilePath "java" `
    -ArgumentList "$javaArgs -jar target\eureka-server-1.0.0.jar" `
    -WorkingDirectory "D:\cropdealnaresh\eureka-server" `
    -PassThru
$procs += $pEureka

$pConfig = Start-Process -FilePath "java" `
    -ArgumentList "$javaArgs -jar target\config-server-1.0.0.jar" `
    -WorkingDirectory "D:\cropdealnaresh\config-server" `
    -PassThru
$procs += $pConfig

Write-Host "Waiting 18 seconds for Eureka and Config Server to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 18

# 2. Business Microservices
Write-Host "`n[2/3] Launching 15 Business Microservices..." -ForegroundColor Cyan
$services = @(
    @{ Name="auth-service"; Dir="D:\cropdealnaresh\auth-service"; Jar="target\auth-service-1.0.0.jar"; Port=8081 },
    @{ Name="user-service"; Dir="D:\cropdealnaresh\user-sevice"; Jar="target\user-service-1.0.0.jar"; Port=8082 },
    @{ Name="crop-service"; Dir="D:\cropdealnaresh\crop-service"; Jar="target\crop-service-1.0.0.jar"; Port=8083 },
    @{ Name="price-service"; Dir="D:\cropdealnaresh\price-service"; Jar="target\price-service-1.0.0.jar"; Port=8084 },
    @{ Name="negotiation-service"; Dir="D:\cropdealnaresh\negotiation-service"; Jar="target\negotiation-service-1.0.0.jar"; Port=8085 },
    @{ Name="bidding-service"; Dir="D:\cropdealnaresh\bidding-service"; Jar="target\bidding-service-1.0.0.jar"; Port=8086 },
    @{ Name="wallet-service"; Dir="D:\cropdealnaresh\wallet-service"; Jar="target\wallet-service-1.0.0.jar"; Port=8087 },
    @{ Name="order-service"; Dir="D:\cropdealnaresh\order-service"; Jar="target\order-service-1.0.0.jar"; Port=8088 },
    @{ Name="payment-service"; Dir="D:\cropdealnaresh\payment-service"; Jar="target\payment-service-1.0.0.jar"; Port=8089 },
    @{ Name="invoice-service"; Dir="D:\cropdealnaresh\invoice-service"; Jar="target\invoice-service-1.0.0.jar"; Port=8090 },
    @{ Name="delivery-service"; Dir="D:\cropdealnaresh\deliveryservice"; Jar="target\delivery-service-1.0.0.jar"; Port=8091 },
    @{ Name="notification-service"; Dir="D:\cropdealnaresh\notification-service"; Jar="target\notification-service-1.0.0.jar"; Port=8092 },
    @{ Name="price-alert-service"; Dir="D:\cropdealnaresh\price-alert-service"; Jar="target\price-alert-service-1.0.0.jar"; Port=8094 },
    @{ Name="report-service"; Dir="D:\cropdealnaresh\report-service"; Jar="target\report-service-1.0.0.jar"; Port=8095 },
    @{ Name="chatbot-service"; Dir="D:\cropdealnaresh\chatbot-service"; Jar="target\chatbot-service-1.0.0.jar"; Port=8096 }
)

foreach ($svc in $services) {
    Write-Host "  -> Launching $($svc.Name) on port $($svc.Port)..." -ForegroundColor Gray
    $p = Start-Process -FilePath "java" `
        -ArgumentList "$javaArgs -jar $($svc.Jar)" `
        -WorkingDirectory $svc.Dir `
        -PassThru
    $procs += $p
    Start-Sleep -Milliseconds 600
}

Write-Host "`nWaiting 12 seconds for microservices to register with Eureka..." -ForegroundColor Yellow
Start-Sleep -Seconds 12

# 3. API Gateway
Write-Host "`n[3/3] Launching API Gateway [8080]..." -ForegroundColor Cyan
$pGateway = Start-Process -FilePath "java" `
    -ArgumentList "$javaArgs -jar target\api-gateway-1.0.0.jar" `
    -WorkingDirectory "D:\cropdealnaresh\api-gateway" `
    -PassThru
$procs += $pGateway

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "All 18 Backend Microservices are actively running! ($($procs.Count) processes)" -ForegroundColor Green
Write-Host "  - Eureka Server:    http://localhost:8761" -ForegroundColor Yellow
Write-Host "  - API Gateway:      http://localhost:8080" -ForegroundColor Yellow
Write-Host "  - Swagger UI:       http://localhost:8080/swagger-ui.html" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Green

# Daemon keepalive loop
while ($true) {
    Start-Sleep -Seconds 30
}
