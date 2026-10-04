@echo off
title CropDeal Platform - Master Startup
color 0A
echo ========================================================
echo         CROPDEAL PLATFORM - FULL SYSTEM LAUNCHER       
echo ========================================================
echo.

cd /d "D:\cropdealnaresh"

echo [1/4] Starting Service Discovery & Central Configuration...
start "Eureka Server [8761]" cmd /k "cd /d D:\cropdealnaresh\eureka-server && ..\mvnw.cmd spring-boot:run"
start "Config Server [8888]" cmd /k "cd /d D:\cropdealnaresh\config-server && ..\mvnw.cmd spring-boot:run"

echo Waiting 15 seconds for Eureka Server and Config Server to initialize...
timeout /t 15 /nobreak >nul

echo [2/4] Starting Business Microservices...
start "Auth Service [8081]" cmd /k "cd /d D:\cropdealnaresh\auth-service && ..\mvnw.cmd spring-boot:run"
start "User Service [8082]" cmd /k "cd /d D:\cropdealnaresh\user-sevice && ..\mvnw.cmd spring-boot:run"
start "Crop Service [8083]" cmd /k "cd /d D:\cropdealnaresh\crop-service && ..\mvnw.cmd spring-boot:run"
start "Price Service [8084]" cmd /k "cd /d D:\cropdealnaresh\price-service && ..\mvnw.cmd spring-boot:run"
start "Negotiation Service [8085]" cmd /k "cd /d D:\cropdealnaresh\negotiation-service && ..\mvnw.cmd spring-boot:run"
start "Bidding Service [8086]" cmd /k "cd /d D:\cropdealnaresh\bidding-service && ..\mvnw.cmd spring-boot:run"
start "Wallet Service [8087]" cmd /k "cd /d D:\cropdealnaresh\wallet-service && ..\mvnw.cmd spring-boot:run"
start "Order Service [8088]" cmd /k "cd /d D:\cropdealnaresh\order-service && ..\mvnw.cmd spring-boot:run"
start "Payment Service [8089]" cmd /k "cd /d D:\cropdealnaresh\payment-service && ..\mvnw.cmd spring-boot:run"
start "Invoice Service [8090]" cmd /k "cd /d D:\cropdealnaresh\invoice-service && ..\mvnw.cmd spring-boot:run"
start "Delivery Service [8091]" cmd /k "cd /d D:\cropdealnaresh\deliveryservice && ..\mvnw.cmd spring-boot:run"
start "Notification Service [8092]" cmd /k "cd /d D:\cropdealnaresh\notification-service && ..\mvnw.cmd spring-boot:run"
start "Price Alert Service [8094]" cmd /k "cd /d D:\cropdealnaresh\price-alert-service && ..\mvnw.cmd spring-boot:run"
start "Report Service [8095]" cmd /k "cd /d D:\cropdealnaresh\report-service && ..\mvnw.cmd spring-boot:run"
start "Chatbot Service [8096]" cmd /k "cd /d D:\cropdealnaresh\chatbot-service && ..\mvnw.cmd spring-boot:run"

echo Waiting 12 seconds for microservices to register with Eureka...
timeout /t 12 /nobreak >nul

echo [3/4] Starting API Gateway [8080]...
start "API Gateway [8080]" cmd /k "cd /d D:\cropdealnaresh\api-gateway && ..\mvnw.cmd spring-boot:run"

echo [4/4] Starting Angular Frontend [4200]...
start "CropDeal Frontend [4200]" cmd /k "cd /d D:\cropdealnaresh\cropdeal-ui && npm start"

echo.
echo ========================================================
echo All CropDeal services have been launched!
echo.
echo Access URLs:
echo   - Frontend UI:         http://localhost:4200
echo   - API Gateway:         http://localhost:8080
echo   - Eureka Dashboard:    http://localhost:8761
echo   - Swagger API Docs:    http://localhost:8080/swagger-ui.html
echo.
echo To STOP all services at any time, run: D:\cropdealnaresh\stop-all.bat
echo ========================================================
pause
