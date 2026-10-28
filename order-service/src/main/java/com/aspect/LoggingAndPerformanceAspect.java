package com.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

/**
 * Aspect-Oriented Programming (AOP) component for cross-cutting execution logging,
 * latency profiling, and distributed tracing across Order Service business logic.
 */
@Aspect
@Component
public class LoggingAndPerformanceAspect {

    private static final Logger log = LoggerFactory.getLogger(LoggingAndPerformanceAspect.class);

    @Pointcut("within(com.service..*) || within(com.controller..*)")
    public void applicationPackagePointcut() {
    }

    @Around("applicationPackagePointcut()")
    public Object profileMethodExecution(ProceedingJoinPoint joinPoint) throws Throwable {
        String className = joinPoint.getSignature().getDeclaringTypeName();
        String methodName = joinPoint.getSignature().getName();
        long startTime = System.currentTimeMillis();

        log.debug("[AOP Entry] Executing {}.{}()", className, methodName);

        try {
            Object result = joinPoint.proceed();
            long executionTime = System.currentTimeMillis() - startTime;
            log.info("[AOP Audit] Completed {}.{}() in {} ms", className, methodName, executionTime);
            return result;
        } catch (Throwable t) {
            long executionTime = System.currentTimeMillis() - startTime;
            log.error("[AOP Exception] Failed {}.{}() after {} ms with: {}", className, methodName, executionTime, t.getMessage());
            throw t;
        }
    }
}
