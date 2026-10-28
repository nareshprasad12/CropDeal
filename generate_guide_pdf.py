# -*- coding: utf-8 -*-
"""
CropDeal Microservices Master Study Guide & Interview Handbook
Generates a comprehensive, publication-quality HTML document and converts it to PDF
using Microsoft Edge headless engine.
Covers: Auth Service, User Service, and Review Service in CropDeal.
"""

import os
import subprocess
import sys

OUTPUT_HTML = r"D:\cropdealnaresh\CropDeal_Study_Guide.html"
OUTPUT_PDF = r"D:\cropdealnaresh\CropDeal_User_Auth_Review_Services_Interview_Guide.pdf"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CropDeal - Auth Service, User Service & Review Service: Complete Code Walkthrough & Spring Boot Interview Guide</title>
<style>
  @page {
    size: A4;
    margin: 15mm 12mm 15mm 12mm;
    @bottom-right {
      content: counter(page);
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.6;
    font-size: 13.5px;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  .cover-page {
    text-align: center;
    padding: 50px 20px 40px;
    border-bottom: 3px solid #10b981;
    margin-bottom: 30px;
    background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
    border-radius: 12px;
  }

  .cover-title {
    font-size: 28px;
    font-weight: 800;
    color: #065f46;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
  }

  .cover-subtitle {
    font-size: 17px;
    font-weight: 600;
    color: #0284c7;
    margin-bottom: 16px;
  }

  .cover-meta {
    font-size: 13px;
    color: #64748b;
    margin-top: 15px;
  }

  .badge {
    display: inline-block;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 2px 4px;
  }
  .badge-emerald { background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
  .badge-sky { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
  .badge-amber { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }

  h1 {
    font-size: 22px;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 36px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  h2 {
    font-size: 17px;
    color: #1e3a8a;
    margin-top: 24px;
    margin-bottom: 10px;
    border-left: 4px solid #3b82f6;
    padding-left: 8px;
  }

  h3 {
    font-size: 14.5px;
    color: #334155;
    margin-top: 18px;
    margin-bottom: 8px;
    font-weight: 700;
  }

  p {
    margin-top: 0;
    margin-bottom: 10px;
    text-align: justify;
  }

  ul, ol {
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 22px;
  }

  li {
    margin-bottom: 4px;
  }

  code {
    font-family: "Cascadia Code", Consolas, Monaco, "Courier New", monospace;
    font-size: 12px;
    background-color: #f1f5f9;
    color: #b91c1c;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }

  pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 14px 16px;
    border-radius: 8px;
    font-family: "Cascadia Code", Consolas, Monaco, monospace;
    font-size: 11.5px;
    line-height: 1.45;
    overflow-x: auto;
    margin-top: 8px;
    margin-bottom: 14px;
    border: 1px solid #334155;
    white-space: pre-wrap;
    word-break: break-word;
  }

  pre .kw { color: #f472b6; font-weight: bold; } /* keyword */
  pre .ann { color: #fbbf24; font-weight: bold; } /* annotation */
  pre .str { color: #34d399; } /* string */
  pre .typ { color: #60a5fa; } /* type/class */
  pre .com { color: #94a3b8; font-style: italic; } /* comment */
  pre .fn  { color: #a78bfa; } /* function */

  .callout {
    padding: 12px 16px;
    border-radius: 8px;
    margin: 14px 0;
    font-size: 13px;
  }
  .callout-interview {
    background-color: #eff6ff;
    border-left: 5px solid #2563eb;
    color: #1e3a8a;
  }
  .callout-architecture {
    background-color: #f0fdf4;
    border-left: 5px solid #10b981;
    color: #065f46;
  }
  .callout-warning {
    background-color: #fffbeb;
    border-left: 5px solid #f59e0b;
    color: #92400e;
  }
  .callout-title {
    font-weight: 700;
    font-size: 13.5px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 12.5px;
  }
  th, td {
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }
  th {
    background-color: #f8fafc;
    color: #0f172a;
    font-weight: 700;
  }
  tr:nth-child(even) {
    background-color: #f8fafc;
  }

  .qa-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #6366f1;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 16px;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .qa-question {
    font-weight: 700;
    color: #1e1b4b;
    font-size: 14px;
    margin-bottom: 8px;
  }
  .qa-answer {
    color: #334155;
    font-size: 13px;
  }

  .diagram-box {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px;
    margin: 14px 0;
    font-family: monospace;
    font-size: 11px;
    line-height: 1.35;
    color: #0f172a;
    overflow-x: auto;
    page-break-inside: avoid;
  }

  .page-break {
    page-break-before: always;
  }

  .toc-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px dotted #cbd5e1;
    font-size: 13px;
  }
  .toc-item a {
    text-decoration: none;
    color: #1e3a8a;
    font-weight: 600;
  }
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-title">CropDeal Microservices Master Study Guide</div>
  <div class="cover-subtitle">Auth Service, User Service & Review Service — Line-by-Line Code Breakdown & Spring Boot Interview Preparation</div>
  <div>
    <span class="badge badge-emerald">Spring Boot 3.x</span>
    <span class="badge badge-sky">Spring Security 6</span>
    <span class="badge badge-amber">Stateless JWT</span>
    <span class="badge badge-purple">OpenFeign RPC</span>
    <span class="badge badge-emerald">JPA & Hibernate</span>
    <span class="badge badge-sky">Distributed Saga</span>
  </div>
  <div class="cover-meta">
    <strong>Author:</strong> CropDeal Backend Engineering Team &bull; 
    <strong>Target Role:</strong> Java / Spring Boot Microservices Developer &bull; 
    <strong>Repository:</strong> CropDeal Architecture
  </div>
</div>

<!-- TABLE OF CONTENTS -->
<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; margin-bottom: 30px;">
  <h2 style="margin-top: 0; border-left: none; padding-left: 0; color: #0f172a;">Table of Contents</h2>
  <div class="toc-item"><a href="#section-1">1. Architectural Blueprint & Inter-Service Topology</a><span>Section 1</span></div>
  <div class="toc-item"><a href="#section-2">2. Auth Service: Deep Dive, Line-by-Line Breakdown & Security</a><span>Section 2</span></div>
  <div class="toc-item"><a href="#section-3">3. User Service: Architecture, Profiles, Admin Governance & RBAC</a><span>Section 3</span></div>
  <div class="toc-item"><a href="#section-4">4. Review Service / Farmer Reviews: Workflow, Math & Decoupling</a><span>Section 4</span></div>
  <div class="toc-item"><a href="#section-5">5. Distributed Flows: Registration Saga & Stateless JWT Validation</a><span>Section 5</span></div>
  <div class="toc-item"><a href="#section-6">6. 30+ High-Yield Spring Boot Interview Questions & Answers</a><span>Section 6</span></div>
  <div class="toc-item"><a href="#section-7">7. Quick-Reference Spring Boot Annotations Dictionary</a><span>Section 7</span></div>
</div>

<!-- SECTION 1 -->
<div id="section-1">
  <h1>1. Architectural Blueprint & Inter-Service Topology</h1>
  <p>
    CropDeal is architected as an enterprise-grade agricultural e-commerce microservices platform.
    In microservice design, two foundational principles dictate how user authentication, domain profiles, and customer feedback are structured:
  </p>
  <ul>
    <li><strong>Separation of Concerns (Identity vs. Profile):</strong> Authentication concerns (credentials, password hashing, token generation, OAuth2 handshakes, password resets) are isolated in <code>auth-service</code>, while domain profile records (farm sizes, bank accounts, dealer businesses, addresses, ratings) reside in <code>user-service</code>.</li>
    <li><strong>Database per Service:</strong> <code>auth-service</code> communicates strictly with <code>cropdeal_auth_db</code>, and <code>user-service</code> communicates strictly with <code>cropdeal_user_db</code>. No cross-database joins or shared database connections are permitted.</li>
    <li><strong>Stateless Authentication Chain:</strong> All downstream services (including <code>user-service</code>, <code>bidding-service</code>, etc.) authenticate incoming requests locally by validating the cryptographic HMAC-SHA256 signature of the JWT token without making synchronous blocking HTTP calls back to <code>auth-service</code>.</li>
  </ul>

  <div class="diagram-box">
+---------------------------------------------------------------------------------------------------+
|                                  API GATEWAY (Port 8080)                                         |
|  - Routes /api/auth/**                 -> auth-service:8081                                       |
|  - Routes /api/users/**, /api/farmers/**, /api/dealers/**, /api/reviews/** -> user-service:8082   |
+---------------------------------------------------------------------------------------------------+
                                         |                                  |
               [HTTP /api/auth/**]       |        [HTTP /api/reviews/**]     |
                                         v                                  v
+--------------------------------------------------+     +------------------------------------------+
|                  AUTH-SERVICE                    |     |               USER-SERVICE               |
|  Port: 8081                                      |     |  Port: 8082                              |
|  Database: cropdeal_auth_db                      |     |  Database: cropdeal_user_db              |
|  - User Entity (Credentials, Role, Status)       |     |  - Farmer Entity (Profile, Farm, Rating) |
|  - BCryptPasswordEncoder                         |     |  - Dealer Entity (Business, Phone)       |
|  - JwtService (Token Minting, Verification)      |     |  - DeliveryPartner Entity (Vehicles)     |
|  - SecurityFilterChain (Stateless, Public Auth)  |     |  - FarmerReview Entity (1-5 Star Ratings)|
|  - Feign Client: UserServiceClient ------------->|---->|  - Feign Client: AuthServiceClient        |
|  - Facebook OAuth2 & JavaMailSender OTP          |     |  - Stateless JwtAuthenticationFilter     |
+--------------------------------------------------+     +------------------------------------------+
  </div>

  <div class="callout callout-architecture">
    <div class="callout-title">&#127963; Architecture Note: Why Review Service is in User Service</div>
    In the current working deployment, the Review module (<code>FarmerReview</code>, <code>FarmerReviewController</code>, <code>FarmerReviewService</code>, <code>FarmerReviewRepository</code>) is hosted as a dedicated domain package inside <code>user-service</code>. The API Gateway explicitly routes all <code>/api/reviews/**</code> requests to port 8082. Furthermore, in <code>config-server</code>, a standalone <code>review-service.properties</code> configuration is pre-configured on port 8094. This illustrates a textbook <em>Strangler Fig / Modular Monolith</em> microservice pattern: building domain cohesion first, with clean interfaces ready for extraction into an independent microservice!
  </div>
</div>

<!-- SECTION 2 -->
<div id="section-2" class="page-break">
  <h1>2. Auth Service: Deep Dive, Line-by-Line Breakdown & Security</h1>
  <p>
    <code>auth-service</code> handles identity management, user onboarding, credential encryption, JWT token issuance, password recovery, and Facebook OAuth2 authentication.
  </p>

  <h2>2.1 The Domain Model: User.java</h2>
  <p>Located at: <code>com.cropdeal.auth.entity.User</code></p>
  <pre>
<span class="ann">@Entity</span>
<span class="ann">@Table</span>(name = <span class="str">"users"</span>, uniqueConstraints = {
    <span class="ann">@UniqueConstraint</span>(name = <span class="str">"uk_user_email"</span>, columnNames = <span class="str">"email"</span>)
})
<span class="kw">public class</span> <span class="typ">User</span> {
    <span class="ann">@Id</span>
    <span class="ann">@GeneratedValue</span>(strategy = <span class="typ">GenerationType</span>.IDENTITY)
    <span class="kw">private</span> <span class="typ">Long</span> id;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>, unique = <span class="kw">true</span>, length = 150)
    <span class="kw">private</span> <span class="typ">String</span> email;

    <span class="ann">@Column</span>(unique = <span class="kw">true</span>, length = 100)
    <span class="kw">private</span> <span class="typ">String</span> username;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>)
    <span class="kw">private</span> <span class="typ">String</span> password;

    <span class="ann">@Enumerated</span>(<span class="typ">EnumType</span>.STRING)
    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>, length = 30)
    <span class="kw">private</span> <span class="typ">Role</span> role; <span class="com">// FARMER, DEALER, DELIVERY_PARTNER, ADMIN</span>

    <span class="ann">@Enumerated</span>(<span class="typ">EnumType</span>.STRING)
    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>, length = 20)
    <span class="kw">private</span> <span class="typ">UserStatus</span> status; <span class="com">// ACTIVE, SUSPENDED, DELETED</span>

    <span class="ann">@Enumerated</span>(<span class="typ">EnumType</span>.STRING)
    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>, length = 20)
    <span class="kw">private</span> <span class="typ">AuthProvider</span> authProvider = <span class="typ">AuthProvider</span>.LOCAL; <span class="com">// LOCAL, FACEBOOK</span>

    <span class="ann">@Column</span>(length = 100)
    <span class="kw">private</span> <span class="typ">String</span> providerId;

    <span class="ann">@Column</span>(length = 255)
    <span class="kw">private</span> <span class="typ">String</span> resetToken;
    <span class="kw">private</span> <span class="typ">LocalDateTime</span> resetTokenExpiry;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>, updatable = <span class="kw">false</span>)
    <span class="kw">private</span> <span class="typ">LocalDateTime</span> createdAt;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>)
    <span class="kw">private</span> <span class="typ">LocalDateTime</span> updatedAt;

    <span class="ann">@PrePersist</span>
    <span class="kw">protected void</span> <span class="fn">onCreate</span>() {
        <span class="typ">LocalDateTime</span> now = <span class="typ">LocalDateTime</span>.now();
        createdAt = now;
        updatedAt = now;
        <span class="kw">if</span> (status == <span class="kw">null</span>) status = <span class="typ">UserStatus</span>.ACTIVE;
        <span class="kw">if</span> (authProvider == <span class="kw">null</span>) authProvider = <span class="typ">AuthProvider</span>.LOCAL;
    }

    <span class="ann">@PreUpdate</span>
    <span class="kw">protected void</span> <span class="fn">onUpdate</span>() {
        updatedAt = <span class="typ">LocalDateTime</span>.now();
    }
}
  </pre>

  <h3>Key Concepts & Line-by-Line Explanation:</h3>
  <ul>
    <li><code>@Entity</code> & <code>@Table</code>: Maps the Java class to the MySQL relational table <code>users</code>. The <code>@UniqueConstraint</code> explicitly adds a database-level unique index on the email column.</li>
    <li><code>GenerationType.IDENTITY</code>: Relies on MySQL's native <code>AUTO_INCREMENT</code> primary key generation.</li>
    <li><code>@Enumerated(EnumType.STRING)</code>: <strong>Critical interview point!</strong> Always use <code>EnumType.STRING</code> rather than <code>EnumType.ORDINAL</code>. Ordinal saves numbers (0, 1, 2) which breaks data integrity if someone reorders enum constants or inserts a new role in the future!</li>
    <li><code>@PrePersist</code> and <code>@PreUpdate</code>: JPA Entity Lifecycle callback annotations. <code>@PrePersist</code> triggers right before Hibernate issues the SQL <code>INSERT</code> statement, setting audit timestamps and default statuses automatically without polluting service layer logic. <code>@PreUpdate</code> triggers right before SQL <code>UPDATE</code>.</li>
  </ul>

  <h2>2.2 Security Architecture: SecurityConfig.java</h2>
  <p>Located at: <code>com.cropdeal.auth.security.SecurityConfig</code></p>
  <pre>
<span class="ann">@Configuration</span>
<span class="ann">@EnableMethodSecurity</span>
<span class="kw">public class</span> <span class="typ">SecurityConfig</span> {
    <span class="kw">private final</span> <span class="typ">JwtAuthenticationFilter</span> jwtAuthenticationFilter;
    <span class="kw">private final</span> <span class="typ">OAuth2AuthenticationSuccessHandler</span> oauth2AuthenticationSuccessHandler;

    <span class="ann">@Bean</span>
    <span class="kw">public</span> <span class="typ">PasswordEncoder</span> <span class="fn">passwordEncoder</span>() {
        <span class="kw">return new</span> <span class="typ">BCryptPasswordEncoder</span>();
    }

    <span class="ann">@Bean</span>
    <span class="kw">public</span> <span class="typ">AuthenticationManager</span> <span class="fn">authenticationManager</span>(<span class="typ">AuthenticationConfiguration</span> config) <span class="kw">throws</span> <span class="typ">Exception</span> {
        <span class="kw">return</span> config.getAuthenticationManager();
    }

    <span class="ann">@Bean</span>
    <span class="kw">public</span> <span class="typ">SecurityFilterChain</span> <span class="fn">securityFilterChain</span>(<span class="typ">HttpSecurity</span> http) <span class="kw">throws</span> <span class="typ">Exception</span> {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session.sessionCreationPolicy(<span class="typ">SessionCreationPolicy</span>.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(
                    <span class="str">"/api/auth/register"</span>, <span class="str">"/api/auth/login"</span>, <span class="str">"/api/auth/facebook"</span>,
                    <span class="str">"/api/auth/forgot-password"</span>, <span class="str">"/api/auth/reset-password"</span>,
                    <span class="str">"/api/auth/verify-otp"</span>, <span class="str">"/api/auth/change-password"</span>,
                    <span class="str">"/oauth2/**"</span>, <span class="str">"/login/oauth2/**"</span>,
                    <span class="str">"/swagger-ui/**"</span>, <span class="str">"/v3/api-docs/**"</span>, <span class="str">"/actuator/**"</span>
                ).permitAll()
                .requestMatchers(<span class="str">"/api/auth/users/**"</span>).hasRole(<span class="str">"ADMIN"</span>)
                .anyRequest().authenticated()
            )
            .oauth2Login(oauth2 -> oauth2.successHandler(oauth2AuthenticationSuccessHandler))
            .addFilterBefore(jwtAuthenticationFilter, <span class="typ">UsernamePasswordAuthenticationFilter</span>.class);

        <span class="kw">return</span> http.build();
    }
}
  </pre>

  <div class="callout callout-interview">
    <div class="callout-title">&#128161; Interview Gold: Spring Security 6 & Spring Boot 3 Changes</div>
    <ul>
      <li>In Spring Boot 3 (Spring Security 6), <code>WebSecurityConfigurerAdapter</code> is completely removed! You declare a <code>@Bean SecurityFilterChain</code> using the lambda DSL: <code>http.csrf(csrf -> csrf.disable())</code>.</li>
      <li><code>SessionCreationPolicy.STATELESS</code> tells Spring Security never to create or store an <code>HttpSession</code>. The server remains stateless, which is essential for horizontal scalability across Docker containers.</li>
      <li><code>csrf.disable()</code> is safe and standard for REST APIs using Bearer JWT tokens because browsers do not automatically send JWT headers on cross-site requests, making CSRF attacks impossible.</li>
      <li><code>.addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class)</code> ensures our custom filter intercepts and validates the Bearer token before Spring Security attempts username/password form authentication.</li>
    </ul>
  </div>

  <h2>2.3 Token Engine: JwtService.java</h2>
  <p>Located at: <code>com.cropdeal.auth.security.JwtService</code></p>
  <pre>
<span class="ann">@Service</span>
<span class="kw">public class</span> <span class="typ">JwtService</span> {
    <span class="ann">@Value</span>(<span class="str">"${jwt.secret}"</span>)
    <span class="kw">private</span> <span class="typ">String</span> secret;

    <span class="ann">@Value</span>(<span class="str">"${jwt.expiration}"</span>) <span class="com">// 86400000 ms = 24 hours</span>
    <span class="kw">private long</span> expiration;

    <span class="kw">private</span> <span class="typ">SecretKey</span> <span class="fn">getSigningKey</span>() {
        <span class="kw">return</span> <span class="typ">Keys</span>.hmacShaKeyFor(secret.getBytes(<span class="typ">StandardCharsets</span>.UTF_8));
    }

    <span class="kw">public</span> <span class="typ">String</span> <span class="fn">generateToken</span>(<span class="typ">User</span> user) {
        <span class="kw">return</span> <span class="typ">Jwts</span>.builder()
                .subject(user.getEmail())
                .claim(<span class="str">"userId"</span>, user.getId())
                .claim(<span class="str">"role"</span>, <span class="str">"ROLE_"</span> + user.getRole().name())
                .issuedAt(<span class="kw">new</span> <span class="typ">Date</span>())
                .expiration(<span class="kw">new</span> <span class="typ">Date</span>(<span class="typ">System</span>.currentTimeMillis() + expiration))
                .signWith(getSigningKey())
                .compact();
    }

    <span class="kw">public boolean</span> <span class="fn">isTokenValid</span>(<span class="typ">String</span> token) {
        <span class="kw">try</span> {
            <span class="typ">Claims</span> claims = extractAllClaims(token);
            <span class="kw">return</span> claims.getExpiration().after(<span class="kw">new</span> <span class="typ">Date</span>());
        } <span class="kw">catch</span> (<span class="typ">Exception</span> e) {
            <span class="kw">return false</span>;
        }
    }

    <span class="kw">private</span> <span class="typ">Claims</span> <span class="fn">extractAllClaims</span>(<span class="typ">String</span> token) {
        <span class="kw">return</span> <span class="typ">Jwts</span>.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }
}
  </pre>

  <h3>JwtService Deep Dive:</h3>
  <ol>
    <li><strong>JJWT 0.12+ Migration:</strong> Modern JJWT uses <code>Jwts.builder().verifyWith(key).build().parseSignedClaims(token).getPayload()</code> instead of the deprecated <code>parser().setSigningKey().parseClaimsJws().getBody()</code>.</li>
    <li><strong>Claims Payload:</strong> Includes <code>sub</code> (subject = email), custom claim <code>userId</code>, and custom claim <code>role</code> (prefixed with <code>ROLE_</code> for Spring Security compatibility).</li>
    <li><strong>Security Signature:</strong> Uses HMAC-SHA256 (<code>Keys.hmacShaKeyFor</code>) requiring a minimum 256-bit (32 byte) secret key.</li>
  </ol>

  <h2>2.4 Core Business Logic: AuthServiceImpl.java</h2>
  <p>Located at: <code>com.cropdeal.auth.service.AuthServiceImpl</code></p>
  
  <h3>Method 1: User Registration with Distributed Profile Creation</h3>
  <pre>
<span class="ann">@Override</span>
<span class="kw">public</span> <span class="typ">MessageResponse</span> <span class="fn">register</span>(<span class="typ">RegisterRequest</span> request) {
    <span class="com">// 1. Prevent public registration as ADMIN</span>
    <span class="kw">if</span> (request.getRole() == <span class="typ">Role</span>.ADMIN) {
        <span class="kw">throw new</span> <span class="typ">IllegalArgumentException</span>(<span class="str">"Admin registration is not allowed"</span>);
    }

    <span class="typ">String</span> email = request.getEmail().trim().toLowerCase();
    <span class="typ">String</span> username = (request.getUsername() != <span class="kw">null</span> && !request.getUsername().trim().isEmpty())
            ? request.getUsername().trim().toLowerCase()
            : email.split(<span class="str">"@"</span>)[0];

    <span class="com">// 2. Check duplicate constraints</span>
    <span class="kw">if</span> (userRepository.existsByEmail(email) || userRepository.existsByUsername(username)) {
        <span class="kw">throw new</span> <span class="typ">UserAlreadyExistsException</span>(<span class="str">"Already registered, please login"</span>);
    }

    <span class="com">// 3. Hash password and persist identity in cropdeal_auth_db</span>
    <span class="typ">User</span> user = <span class="kw">new</span> <span class="typ">User</span>();
    user.setEmail(email);
    user.setUsername(username);
    user.setPassword(passwordEncoder.encode(request.getPassword()));
    user.setRole(request.getRole());
    user.setStatus(<span class="typ">UserStatus</span>.ACTIVE);
    <span class="typ">User</span> savedUser = userRepository.save(user);

    <span class="com">// 4. Inter-service RPC call to User Service via OpenFeign</span>
    <span class="kw">try</span> {
        <span class="typ">String</span> displayName = request.getName() != <span class="kw">null</span> ? request.getName().trim() : username;
        <span class="typ">String</span> phoneNum = request.getPhone() != <span class="kw">null</span> ? request.getPhone().trim() : <span class="str">"9876543210"</span>;

        <span class="typ">CreateProfileRequest</span> profileRequest = <span class="kw">new</span> <span class="typ">CreateProfileRequest</span>(
                savedUser.getId(), displayName, email, phoneNum, request.getRole()
        );
        userServiceClient.createProfile(profileRequest);
    } <span class="kw">catch</span> (<span class="typ">Exception</span> e) {
        <span class="com">// 5. Compensating transaction: roll back local identity if profile creation fails!</span>
        userRepository.delete(savedUser);
        <span class="kw">throw new</span> <span class="typ">RuntimeException</span>(<span class="str">"Unable to create user profile: "</span> + e.getMessage());
    }

    <span class="kw">return new</span> <span class="typ">MessageResponse</span>(<span class="str">"Registration successful"</span>);
}
  </pre>

  <div class="callout callout-interview">
    <div class="callout-title">&#128161; Interview Question: How do you handle distributed transactions during registration?</div>
    <p>
      In a monolithic app, an <code>@Transactional</code> boundary wraps both user and profile table inserts in a single database commit. But in microservices, <code>User</code> is in <code>cropdeal_auth_db</code> and <code>Farmer/Dealer</code> is in <code>cropdeal_user_db</code>! 
      In this code, we implemented a <strong>Compensating Transaction (Saga Pattern)</strong>:
      If the Feign client call to <code>userServiceClient.createProfile(...)</code> throws an exception (e.g. network timeout or database error in user-service), the catch block immediately executes <code>userRepository.delete(savedUser)</code> to compensate and prevent orphaned identity records.
    </p>
  </div>

  <h3>Method 2: Multi-Identifier Login</h3>
  <pre>
<span class="ann">@Override</span>
<span class="kw">public</span> <span class="typ">LoginResponse</span> <span class="fn">login</span>(<span class="typ">LoginRequest</span> request) {
    <span class="typ">String</span> identifier = request.getEmail() != <span class="kw">null</span> ? request.getEmail().trim().toLowerCase() : request.getUsername().trim().toLowerCase();

    <span class="com">// Looks up by email OR by username in single query pipeline</span>
    <span class="typ">User</span> user = userRepository.findByEmail(identifier)
            .or(() -> userRepository.findByUsername(identifier))
            .orElseThrow(() -> <span class="kw">new</span> <span class="typ">InvalidCredentialsException</span>(<span class="str">"Invalid email or password"</span>));

    <span class="com">// Verify raw password against BCrypt hash</span>
    <span class="kw">if</span> (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
        <span class="kw">throw new</span> <span class="typ">InvalidCredentialsException</span>(<span class="str">"Invalid email or password"</span>);
    }

    <span class="com">// Verify account status (Admin block support)</span>
    <span class="kw">if</span> (user.getStatus() != <span class="typ">UserStatus</span>.ACTIVE) {
        <span class="kw">throw new</span> <span class="typ">InvalidCredentialsException</span>(<span class="str">"User account is blocked by administrator"</span>);
    }

    <span class="com">// Generate JWT and trigger async price alerts</span>
    <span class="typ">String</span> token = jwtService.generateToken(user);
    triggerLoginCropAlerts(user.getId());

    <span class="kw">return new</span> <span class="typ">LoginResponse</span>(user.getId(), user.getEmail(), user.getUsername(), <span class="str">"ROLE_"</span> + user.getRole().name(), token);
}
  </pre>

  <h3>Method 3: Password Reset via 6-Digit OTP</h3>
  <pre>
<span class="com">// 1. Generate 6-digit random code and set 15-minute expiration</span>
<span class="typ">String</span> resetToken = <span class="typ">String</span>.format(<span class="str">"%06d"</span>, <span class="kw">new</span> <span class="typ">Random</span>().nextInt(900000) + 100000);
user.setResetToken(resetToken);
user.setResetTokenExpiry(<span class="typ">LocalDateTime</span>.now().plusMinutes(15));
userRepository.save(user);

<span class="com">// 2. Send email via JavaMailSender (Gmail SMTP with STARTTLS)</span>
<span class="typ">SimpleMailMessage</span> mailMessage = <span class="kw">new</span> <span class="typ">SimpleMailMessage</span>();
mailMessage.setTo(user.getEmail());
mailMessage.setSubject(<span class="str">"CropDeal - Password Reset OTP"</span>);
mailMessage.setText(<span class="str">"Your One-Time Password (OTP) is: "</span> + resetToken);
mailSender.send(mailMessage);
  </pre>
</div>

<!-- SECTION 3 -->
<div id="section-3" class="page-break">
  <h1>3. User Service: Architecture, Profiles, Admin Governance & RBAC</h1>
  <p>
    <code>user-service</code> (port 8082) manages rich business profiles for Farmers, Dealers, and Delivery Partners, provides admin oversight dashboards, and houses the farmer review rating subsystem.
  </p>

  <h2>3.1 Stateless JWT Authentication Filter in Downstream Services</h2>
  <p>Located at: <code>com.cropdeal.user.security.JwtAuthenticationFilter</code></p>
  <pre>
<span class="ann">@Component</span>
<span class="kw">public class</span> <span class="typ">JwtAuthenticationFilter</span> <span class="kw">extends</span> <span class="typ">OncePerRequestFilter</span> {
    <span class="kw">private final</span> <span class="typ">JwtService</span> jwtService;

    <span class="ann">@Override</span>
    <span class="kw">protected void</span> <span class="fn">doFilterInternal</span>(
            <span class="typ">HttpServletRequest</span> request, <span class="typ">HttpServletResponse</span> response, <span class="typ">FilterChain</span> filterChain)
            <span class="kw">throws</span> <span class="typ">ServletException</span>, <span class="typ">IOException</span> {

        <span class="typ">String</span> authHeader = request.getHeader(<span class="str">"Authorization"</span>);
        <span class="kw">if</span> (!<span class="typ">StringUtils</span>.hasText(authHeader) || !authHeader.startsWith(<span class="str">"Bearer "</span>)) {
            filterChain.doFilter(request, response);
            <span class="kw">return</span>;
        }

        <span class="typ">String</span> token = authHeader.substring(7);
        <span class="kw">try</span> {
            <span class="kw">if</span> (jwtService.isTokenValid(token)) {
                <span class="typ">String</span> email = jwtService.extractEmail(token);
                <span class="typ">Long</span> userId = jwtService.extractUserId(token);
                <span class="typ">String</span> role = jwtService.extractRole(token);

                <span class="kw">if</span> (email != <span class="kw">null</span> && <span class="typ">SecurityContextHolder</span>.getContext().getAuthentication() == <span class="kw">null</span>) {
                    <span class="typ">UserPrincipal</span> principal = <span class="kw">new</span> <span class="typ">UserPrincipal</span>(userId, email, role);
                    <span class="typ">UsernamePasswordAuthenticationToken</span> authentication =
                            <span class="kw">new</span> <span class="typ">UsernamePasswordAuthenticationToken</span>(principal, <span class="kw">null</span>, principal.getAuthorities());
                    authentication.setDetails(<span class="kw">new</span> <span class="typ">WebAuthenticationDetailsSource</span>().buildDetails(request));
                    <span class="typ">SecurityContextHolder</span>.getContext().setAuthentication(authentication);
                }
            }
        } <span class="kw">catch</span> (<span class="typ">Exception</span> ignored) {}

        filterChain.doFilter(request, response);
    }
}
  </pre>

  <div class="callout callout-interview">
    <div class="callout-title">&#128161; Interview Concept: Stateless SecurityContext Population</div>
    Notice the difference between <code>auth-service</code> and <code>user-service</code>:
    <ul>
      <li>In <code>auth-service</code>, the filter calls <code>userDetailsService.loadUserByUsername(email)</code> which queries the MySQL database to verify credentials.</li>
      <li>In <code>user-service</code>, the filter <strong>does not hit the database at all!</strong> It verifies the cryptographic HMAC signature using the shared secret key, extracts <code>userId</code>, <code>email</code>, and <code>role</code> directly from the JWT claims, and populates <code>UserPrincipal</code> directly into <code>SecurityContextHolder</code>.</li>
      <li>This achieves true zero-latency, stateless authentication in every downstream microservice!</li>
    </ul>
  </div>

  <h2>3.2 Domain Entities: Farmer, Dealer & DeliveryPartner</h2>
  <table>
    <thead>
      <tr>
        <th>Entity</th>
        <th>Key Columns</th>
        <th>Unique Constraints</th>
        <th>Special Attributes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Farmer</strong></td>
        <td><code>id, userId, name, phone, address, farmLocation, bankDetails</code></td>
        <td><code>uk_farmer_user_id (user_id)</code></td>
        <td><code>averageRating (Double)</code>, <code>totalReviews (Integer)</code>, <code>isBlocked (Boolean)</code></td>
      </tr>
      <tr>
        <td><strong>Dealer</strong></td>
        <td><code>id, userId, name, phone, businessName, address, bankDetails</code></td>
        <td><code>uk_dealer_user_id (user_id)</code></td>
        <td><code>businessName</code> for commercial trading</td>
      </tr>
      <tr>
        <td><strong>DeliveryPartner</strong></td>
        <td><code>id, userId, name, phone, address, vehicleType, vehicleNumber</code></td>
        <td><code>uk_delivery_partner_user_id (user_id)</code></td>
        <td><code>availabilityStatus (AVAILABLE, BUSY, OFFLINE)</code></td>
      </tr>
    </tbody>
  </table>

  <h2>3.3 Controller Layer & Method-Level Security: FarmerController.java</h2>
  <pre>
<span class="ann">@RestController</span>
<span class="ann">@RequestMapping</span>(<span class="str">"/api/farmers"</span>)
<span class="kw">public class</span> <span class="typ">FarmerController</span> {
    <span class="kw">private final</span> <span class="typ">FarmerService</span> farmerService;

    <span class="ann">@GetMapping</span>(<span class="str">"/me"</span>)
    <span class="ann">@PreAuthorize</span>(<span class="str">"hasRole('FARMER')"</span>)
    <span class="kw">public</span> <span class="typ">ResponseEntity</span>&lt;<span class="typ">FarmerResponse</span>&gt; <span class="fn">getMyProfile</span>(
            <span class="ann">@AuthenticationPrincipal</span> <span class="typ">UserPrincipal</span> principal) {
        <span class="kw">return</span> <span class="typ">ResponseEntity</span>.ok(farmerService.getFarmerByUserId(principal.getUserId()));
    }

    <span class="ann">@PutMapping</span>(<span class="str">"/me"</span>)
    <span class="ann">@PreAuthorize</span>(<span class="str">"hasRole('FARMER')"</span>)
    <span class="kw">public</span> <span class="typ">ResponseEntity</span>&lt;<span class="typ">FarmerResponse</span>&gt; <span class="fn">updateMyProfile</span>(
            <span class="ann">@AuthenticationPrincipal</span> <span class="typ">UserPrincipal</span> principal,
            <span class="ann">@Valid</span> <span class="ann">@RequestBody</span> <span class="typ">FarmerUpdateRequest</span> request) {
        <span class="kw">return</span> <span class="typ">ResponseEntity</span>.ok(farmerService.updateFarmerByUserId(principal.getUserId(), request));
    }

    <span class="ann">@GetMapping</span>(<span class="str">"/{id}"</span>)
    <span class="ann">@PreAuthorize</span>(<span class="str">"hasAnyRole('FARMER', 'DEALER', 'ADMIN')"</span>)
    <span class="kw">public</span> <span class="typ">ResponseEntity</span>&lt;<span class="typ">FarmerResponse</span>&gt; <span class="fn">getFarmerById</span>(<span class="ann">@PathVariable</span> <span class="typ">Long</span> id) {
        <span class="kw">return</span> <span class="typ">ResponseEntity</span>.ok(farmerService.getFarmerById(id));
    }
}
  </pre>

  <h3>Key Annotations Explained:</h3>
  <ul>
    <li><code>@PreAuthorize("hasRole('FARMER')")</code>: Spring Security Expression (SpEL) evaluated before invoking the method. It checks if the current <code>Authentication</code> in <code>SecurityContext</code> has authority <code>ROLE_FARMER</code>.</li>
    <li><code>@AuthenticationPrincipal UserPrincipal principal</code>: Binds the custom <code>UserPrincipal</code> object stored in the <code>SecurityContext</code> directly into the controller method parameter, eliminating manual casting.</li>
  </ul>

  <h2>3.4 Inter-Service Governance: AdminUserController & Feign Client</h2>
  <p>Located at: <code>com.cropdeal.user.controller.AdminUserController</code></p>
  <pre>
<span class="ann">@PostMapping</span>(<span class="str">"/users/{userId}/block"</span>)
<span class="kw">public</span> <span class="typ">ResponseEntity</span>&lt;<span class="typ">Map</span>&lt;<span class="typ">String</span>, <span class="typ">Object</span>&gt;&gt; <span class="fn">blockUser</span>(
        <span class="ann">@PathVariable</span> <span class="typ">Long</span> userId,
        <span class="ann">@RequestParam</span>(defaultValue = <span class="str">"Blocked by Administrator"</span>) <span class="typ">String</span> reason,
        <span class="typ">HttpServletRequest</span> httpRequest) {

    <span class="com">// Protect root admin account</span>
    <span class="kw">if</span> (userId != <span class="kw">null</span> && userId == 4L) {
        <span class="kw">return</span> <span class="typ">ResponseEntity</span>.badRequest().body(<span class="typ">Map</span>.of(<span class="str">"error"</span>, <span class="str">"Bad Request"</span>, <span class="str">"message"</span>, <span class="str">"Administrator account cannot be blocked"</span>));
    }

    <span class="com">// 1. Mark blocked in User Service domain</span>
    farmerRepository.findByUserId(userId).ifPresent(f -> {
        f.setIsBlocked(<span class="kw">true</span>);
        farmerRepository.save(f);
    });

    <span class="com">// 2. Propagate status update to Auth Service via OpenFeign client</span>
    <span class="typ">String</span> authHeader = httpRequest.getHeader(<span class="str">"Authorization"</span>);
    <span class="kw">try</span> {
        authServiceClient.updateUserStatus(userId, <span class="kw">new</span> <span class="typ">UserStatusUpdateRequest</span>(<span class="str">"SUSPENDED"</span>), authHeader);
    } <span class="kw">catch</span> (<span class="typ">Exception</span> e) {
        log.warn(<span class="str">"Could not sync SUSPENDED status to auth-service: {}"</span>, e.getMessage());
    }

    <span class="kw">return</span> <span class="typ">ResponseEntity</span>.ok(<span class="typ">Map</span>.of(<span class="str">"message"</span>, <span class="str">"User blocked successfully"</span>, <span class="str">"userId"</span>, userId, <span class="str">"status"</span>, <span class="str">"BLOCKED"</span>));
}
  </pre>
</div>

<!-- SECTION 4 -->
<div id="section-4" class="page-break">
  <h1>4. Review Service / Farmer Reviews: Workflow, Math & Decoupling</h1>
  <p>
    Customer reviews build trust in agricultural trading. When a dealer completes a purchase order from a farmer, they can rate the farmer from 1 to 5 stars and leave written feedback.
  </p>

  <h2>4.1 The Review Entity: FarmerReview.java</h2>
  <pre>
<span class="ann">@Entity</span>
<span class="ann">@Table</span>(name = <span class="str">"farmer_reviews"</span>, indexes = {
    <span class="ann">@Index</span>(name = <span class="str">"idx_review_farmer"</span>, columnList = <span class="str">"farmerId"</span>),
    <span class="ann">@Index</span>(name = <span class="str">"idx_review_order"</span>, columnList = <span class="str">"orderId"</span>, unique = <span class="kw">true</span>)
})
<span class="kw">public class</span> <span class="typ">FarmerReview</span> {
    <span class="ann">@Id</span>
    <span class="ann">@GeneratedValue</span>(strategy = <span class="typ">GenerationType</span>.IDENTITY)
    <span class="kw">private</span> <span class="typ">Long</span> id;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>)
    <span class="kw">private</span> <span class="typ">Long</span> farmerId;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>)
    <span class="kw">private</span> <span class="typ">Long</span> dealerId;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>, unique = <span class="kw">true</span>)
    <span class="kw">private</span> <span class="typ">Long</span> orderId;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>)
    <span class="kw">private</span> <span class="typ">Integer</span> rating; <span class="com">// 1 to 5</span>

    <span class="ann">@Column</span>(length = 1000)
    <span class="kw">private</span> <span class="typ">String</span> comment;

    <span class="ann">@Column</span>(nullable = <span class="kw">false</span>, updatable = <span class="kw">false</span>)
    <span class="kw">private</span> <span class="typ">LocalDateTime</span> createdAt;

    <span class="ann">@PrePersist</span>
    <span class="kw">void</span> <span class="fn">prePersist</span>() { createdAt = <span class="typ">LocalDateTime</span>.now(); }
}
  </pre>

  <h3>Database Design Highlights:</h3>
  <ul>
    <li><code>@Index(name = "idx_review_order", columnList = "orderId", unique = true)</code>: <strong>Guarantees Idempotency!</strong> Each completed order can only ever be reviewed once. Any accidental double submission is rejected at both the database level (SQL 1062 Duplicate entry) and the service validation level.</li>
    <li><code>@Index(name = "idx_review_farmer", columnList = "farmerId")</code>: Creates a B-Tree index on <code>farmerId</code> for instantaneous retrieval of a farmer's review history.</li>
  </ul>

  <h2>4.2 Immutable DTOs via Java Records</h2>
  <pre>
<span class="kw">public record</span> <span class="typ">CreateReviewRequest</span>(
    <span class="ann">@NotNull</span> <span class="typ">Long</span> farmerId,
    <span class="ann">@NotNull</span> <span class="typ">Long</span> dealerId,
    <span class="ann">@NotNull</span> <span class="typ">Long</span> orderId,
    <span class="ann">@NotNull</span> <span class="ann">@Min</span>(1) <span class="ann">@Max</span>(5) <span class="typ">Integer</span> rating,
    <span class="ann">@Size</span>(max = 1000) <span class="typ">String</span> comment
) {}

<span class="kw">public record</span> <span class="typ">FarmerReviewResponse</span>(
    <span class="typ">Long</span> id,
    <span class="typ">Long</span> farmerId,
    <span class="typ">Long</span> dealerId,
    <span class="typ">Long</span> orderId,
    <span class="typ">Integer</span> rating,
    <span class="typ">String</span> comment,
    <span class="typ">LocalDateTime</span> createdAt
) {}
  </pre>

  <div class="callout callout-interview">
    <div class="callout-title">&#128161; Interview Tip: Why Java Records for DTOs in Spring Boot 3?</div>
    Java 14+ Records are immutable data carriers. The compiler automatically generates <code>private final</code> fields, a canonical constructor, getters (e.g. <code>request.rating()</code>), <code>equals()</code>, <code>hashCode()</code>, and <code>toString()</code>. They eliminate boilerplate Lombok annotations (<code>@Getter, @AllArgsConstructor</code>) and guarantee thread-safety.
  </div>

  <h2>4.3 The Review Engine & Real-Time Rating Math: FarmerReviewServiceImpl.java</h2>
  <pre>
<span class="ann">@Service</span>
<span class="ann">@Transactional</span>
<span class="kw">public class</span> <span class="typ">FarmerReviewServiceImpl</span> <span class="kw">implements</span> <span class="typ">FarmerReviewService</span> {
    <span class="kw">private final</span> <span class="typ">FarmerReviewRepository</span> reviewRepository;
    <span class="kw">private final</span> <span class="typ">FarmerRepository</span> farmerRepository;

    <span class="ann">@Override</span>
    <span class="kw">public</span> <span class="typ">FarmerReviewResponse</span> <span class="fn">submitReview</span>(<span class="typ">CreateReviewRequest</span> request) {
        <span class="com">// 1. Validate Order uniqueness</span>
        <span class="kw">if</span> (reviewRepository.existsByOrderId(request.orderId())) {
            <span class="kw">throw new</span> <span class="typ">IllegalArgumentException</span>(<span class="str">"Order "</span> + request.orderId() + <span class="str">" has already been reviewed."</span>);
        }

        <span class="com">// 2. Verify Farmer exists</span>
        <span class="typ">Farmer</span> farmer = farmerRepository.findById(request.farmerId())
                .orElseThrow(() -> <span class="kw">new</span> <span class="typ">FarmerNotFoundException</span>(request.farmerId()));

        <span class="com">// 3. Save new review record</span>
        <span class="typ">FarmerReview</span> review = <span class="kw">new</span> <span class="typ">FarmerReview</span>();
        review.setFarmerId(request.farmerId());
        review.setDealerId(request.dealerId());
        review.setOrderId(request.orderId());
        review.setRating(request.rating());
        review.setComment(request.comment());
        <span class="typ">FarmerReview</span> savedReview = reviewRepository.save(review);

        <span class="com">// 4. Recalculate Average Rating across all reviews for this farmer</span>
        <span class="typ">List</span>&lt;<span class="typ">FarmerReview</span>&gt; allReviews = reviewRepository.findByFarmerIdOrderByCreatedAtDesc(farmer.getId());
        <span class="kw">double</span> avg = allReviews.stream()
                               .mapToInt(<span class="typ">FarmerReview</span>::getRating)
                               .average()
                               .orElse(0.0);

        <span class="com">// 5. Round to 1 decimal place and update farmer record</span>
        farmer.setAverageRating(<span class="typ">Math</span>.round(avg * 10.0) / 10.0);
        farmer.setTotalReviews(allReviews.size());
        farmerRepository.save(farmer);

        <span class="kw">return</span> toResponse(savedReview);
    }
}
  </pre>

  <h3>Rating Calculation Walkthrough & Stream API:</h3>
  <ol>
    <li><code>allReviews.stream().mapToInt(FarmerReview::getRating)</code>: Converts the review object stream to a primitive <code>IntStream</code>, eliminating autoboxing overhead.</li>
    <li><code>.average()</code>: Computes the arithmetic mean, returning an <code>OptionalDouble</code>.</li>
    <li><code>.orElse(0.0)</code>: Handles the edge case where no reviews exist, defaulting to 0.0 without throwing <code>NoSuchElementException</code>.</li>
    <li><code>Math.round(avg * 10.0) / 10.0</code>: Multiplies by 10, rounds to the nearest integer, and divides by 10.0 to format cleanly to one decimal place (e.g. <code>4.66666...</code> &rarr; <code>4.7</code>).</li>
  </ol>
</div>

<!-- SECTION 5 -->
<div id="section-5" class="page-break">
  <h1>5. Distributed Flows: Registration Saga & Stateless JWT Validation</h1>

  <h2>5.1 End-to-End Registration Saga Sequence</h2>
  <div class="diagram-box">
Client                     API Gateway                Auth Service             User Service            cropdeal_auth_db      cropdeal_user_db
  |                             |                          |                         |                        |                     |
  |--- POST /api/auth/register->|                          |                         |                        |                     |
  |    (email, pass, role)      |--- Forward Request ----->|                         |                        |                     |
  |                             |                          |-- Check Exists -------->|                        |                     |
  |                             |                          |-- BCrypt Encode --------|                        |                     |
  |                             |                          |-- INSERT User ---------------------------------->| (Commit User)       |
  |                             |                          |                         |                        |                     |
  |                             |                          |-- Feign: createProfile->|                        |                     |
  |                             |                          |   (userId, name, phone) |-- INSERT Farmer/Dealer---------------------->| (Commit Profile)
  |                             |                          |                         |-- 201 Created -------->|                     |
  |                             |                          |                         |                        |                     |
  |                             |                          |-- If Feign Fails:       |                        |                     |
  |                             |                          |   DELETE User ---------------------------------->| (Compensate/Delete) |
  |                             |                          |                                                  |                     |
  |                             |<-- 201 MessageResponse --|                                                  |                     |
  |<-- HTTP 201 Created --------|                          |                                                  |                     |
  </div>

  <h2>5.2 End-to-End Login & Authenticated Request Flow</h2>
  <div class="diagram-box">
1. LOGIN PHASE:
Dealer                       API Gateway               Auth Service                MySQL (cropdeal_auth_db)
  |                               |                         |                                  |
  |--- POST /api/auth/login ----->|                         |                                  |
  |    {email, password}          |--- Forward Request ---->|                                  |
  |                               |                         |--- SELECT * FROM users --------->|
  |                               |                         |<-- User Record ------------------|
  |                               |                         |--- BCrypt.matches()              |
  |                               |                         |--- Jwts.builder().signWith()     |
  |                               |<-- LoginResponse(token)-|                                  |
  |<-- Token + User Info ---------|                         |                                  |

2. AUTHENTICATED API REQUEST PHASE (Zero DB calls to Auth Service):
Dealer                       API Gateway               User Service (JwtFilter)     MySQL (cropdeal_user_db)
  |                               |                         |                                  |
  |--- GET /api/farmers/me ------>|                         |                                  |
  |    Authorization: Bearer xyz  |--- Forward Request ---->|                                  |
  |                               |                         |--- Validate HMAC Signature       |
  |                               |                         |--- Extract userId, role          |
  |                               |                         |--- SecurityContext = Principal   |
  |                               |                         |--- SELECT * FROM farmers ------->|
  |                               |                         |<-- Farmer Profile ---------------|
  |                               |<-- 200 FarmerResponse --|                                  |
  |<-- Farmer JSON ---------------|                         |                                  |
  </div>
</div>

<!-- SECTION 6 -->
<div id="section-6" class="page-break">
  <h1>6. 30+ High-Yield Spring Boot Interview Questions & Answers</h1>

  <div class="qa-card">
    <div class="qa-question">Q1: How does authentication and authorization work in your CropDeal microservices architecture?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> Authentication is handled centrally by <code>auth-service</code>. When a user submits credentials, <code>auth-service</code> verifies them using <code>BCryptPasswordEncoder</code>, checks that the user status is <code>ACTIVE</code>, and signs a stateless JWT containing the subject (email), <code>userId</code>, and granted authorities (<code>ROLE_FARMER</code>, <code>ROLE_DEALER</code>, etc.) using HMAC-SHA256.<br>
      For authorization across all downstream services (such as <code>user-service</code>), each service contains a <code>JwtAuthenticationFilter</code>. It parses the incoming <code>Authorization: Bearer &lt;token&gt;</code> header, validates the signature using the shared secret key, and populates Spring's <code>SecurityContextHolder</code> with an authenticated <code>UserPrincipal</code>. Endpoints are then guarded at the method level using <code>@PreAuthorize("hasRole('FARMER')")</code>.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q2: Why did you separate Auth Service and User Service into two distinct databases?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> This adheres to the <em>Single Responsibility Principle</em> and the microservice <em>Database-per-Service</em> pattern. 
      <code>auth-service</code> is an identity provider responsible for credentials, password recovery OTPs, and OAuth2 tokens. 
      <code>user-service</code> is a business domain service responsible for agricultural profiles, land locations, bank details, and dealer ratings. 
      Separating them enables independent scaling (auth receives high traffic during logins, user-service during browsing), isolated security boundaries (credential database is shielded from general domain queries), and technology independence.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q3: How do you handle distributed transactions between Auth Service and User Service during registration?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> We implemented the <strong>Saga Pattern with Compensating Transactions</strong>. When <code>authService.register()</code> runs, it first saves the credentials to <code>cropdeal_auth_db</code>. It then invokes <code>userServiceClient.createProfile(...)</code> via OpenFeign to provision the profile in <code>cropdeal_user_db</code>. 
      If the Feign RPC call fails or throws an exception, the catch block executes <code>userRepository.delete(savedUser)</code>, rolling back the newly created user in <code>auth-service</code> so no orphaned credentials remain in the system.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q4: What is the role of OncePerRequestFilter and why is it preferred for JWT authentication?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> Standard servlet filters can sometimes be invoked more than once per HTTP request (for example, during internal request dispatches, error forwards, or asynchronous requests). <code>OncePerRequestFilter</code> is an abstract Spring Web filter that guarantees execution exactly once per request thread. This prevents redundant cryptographic JWT parsing and eliminates duplicate SecurityContext population.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q5: How does your Review system prevent duplicate reviews for the same order?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> We enforce idempotency at two independent layers:
      <ol>
        <li><strong>Database Constraint:</strong> In <code>FarmerReview.java</code>, the column <code>orderId</code> is declared <code>@Column(nullable = false, unique = true)</code> and backed by a database unique index <code>@Index(name = "idx_review_order", columnList = "orderId", unique = true)</code>.</li>
        <li><strong>Service-Level Pre-Check:</strong> In <code>FarmerReviewServiceImpl</code>, before persisting, we check <code>if (reviewRepository.existsByOrderId(request.orderId()))</code> and throw an <code>IllegalArgumentException</code> if already present.</li>
      </ol>
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q6: What is the difference between @Transactional and @Transactional(readOnly = true)?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> <code>@Transactional</code> opens a read-write transaction with Hibernate. Hibernate maintains entity dirty-checking snapshots in memory and automatically flushes changes to the database at commit time.<br>
      When <code>readOnly = true</code> is specified on query methods (e.g., <code>getFarmerById()</code>), Hibernate optimizes memory by turning off dirty-checking snapshot creation. Additionally, underlying database drivers can optimize locks and route read queries to read-replicas in clustered databases.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q7: How does Spring Data JPA execute repository methods like findByFarmerIdOrderByCreatedAtDesc without SQL?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> Spring Data JPA uses <strong>Method Name Query Derivation</strong>. At application startup, Spring's <code>RepositoryFactorySupport</code> parses the method name using keywords (<code>findBy</code>, <code>OrderBy</code>, <code>Desc</code>) against the entity's property names (<code>farmerId</code>, <code>createdAt</code>). It builds an Abstract Syntax Tree (AST) and generates a JPA Criteria query / JPQL statement dynamically. Under the hood, Spring creates a dynamic JDK proxy that implements the interface and executes the generated query via the <code>EntityManager</code>.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q8: Why did you use BCryptPasswordEncoder and how does BCrypt protect against brute-force attacks?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> BCrypt is a slow, adaptive one-way cryptographic hashing algorithm based on the Blowfish cipher. It incorporates a salt automatically into the generated 60-character string (preventing rainbow table lookups) and utilizes a configurable <em>work factor</em> (logarithmic rounds, default 10). Because it is deliberately computationally intensive, it makes offline GPU/ASIC brute-force dictionary attacks infeasible.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q9: How does @RestControllerAdvice handle exceptions across your microservice?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> <code>@RestControllerAdvice</code> is a specialization of <code>@Component</code> that intercepts exceptions thrown by any <code>@RequestMapping</code> method across all controllers. Using <code>@ExceptionHandler(FarmerNotFoundException.class)</code>, we catch specific domain exceptions and return standardized JSON error bodies containing <code>timestamp</code>, HTTP <code>status</code> code (e.g. 404), <code>error</code> message, and request <code>path</code>. This decouples error handling from business logic.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q10: Why did you use Java Records for DTOs like CreateReviewRequest?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> Java Records (introduced in Java 14, finalized in Java 16) are concise, immutable data-carrier classes. When writing <code>public record CreateReviewRequest(...)</code>, the Java compiler automatically creates final fields, canonical constructor, accessors, <code>equals</code>, <code>hashCode</code>, and <code>toString</code>. They are ideal for DTOs because incoming HTTP request bodies should never be modified once received, guaranteeing thread safety.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q11: What is the purpose of Spring Cloud OpenFeign and how does it work?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> OpenFeign is a declarative HTTP client. Instead of writing boilerplate <code>RestTemplate</code> or <code>WebClient</code> code with manual serialization, URL concatenation, and header parsing, we simply declare an interface with Spring MVC annotations (<code>@FeignClient(name = "user-service")</code>, <code>@PostMapping</code>). At runtime, Spring Cloud creates a dynamic proxy that serializes method arguments into HTTP request bodies, handles URL routing (including Eureka service discovery and client-side load balancing via Spring Cloud LoadBalancer), and deserializes responses.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q12: How does @PreAuthorize enforce role-based access control?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> <code>@PreAuthorize</code> relies on Spring AOP (Aspect-Oriented Programming). When <code>@EnableMethodSecurity</code> is present on a configuration class, Spring creates a proxy around the controller bean. Before the target method executes, the <code>MethodSecurityInterceptor</code> evaluates the Spring Expression Language (SpEL) expression (e.g. <code>hasRole('ADMIN')</code>). It compares the required role against the <code>GrantedAuthority</code> list in <code>SecurityContextHolder.getContext().getAuthentication()</code>. If authorization fails, it aborts execution and throws an <code>AccessDeniedException</code> (HTTP 403 Forbidden).
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q13: How does your review rating recalculation work and how would you optimize it for millions of reviews?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> In our current service, upon saving a new review, we query <code>findByFarmerIdOrderByCreatedAtDesc</code>, use the Java Stream API:
      <code>allReviews.stream().mapToInt(FarmerReview::getRating).average().orElse(0.0)</code>, and persist the rounded average back to the <code>Farmer</code> entity.<br>
      <strong>Scale Optimization:</strong> For high-volume production, calculating average across all historical records in memory becomes inefficient. We would optimize by:
      <ol>
        <li>Using an incremental moving average formula: <code>newAvg = ((oldAvg * oldCount) + newRating) / (oldCount + 1)</code>, which executes in <code>O(1)</code> time without querying previous reviews.</li>
        <li>Offloading calculation asynchronously using an event message broker (e.g. RabbitMQ/Kafka): publishing a <code>ReviewCreatedEvent</code> and letting a background worker update the farmer rating asynchronously.</li>
      </ol>
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q14: How does Spring Cloud Gateway route traffic to Auth and User services?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> Spring Cloud Gateway is built on Spring WebFlux and Project Reactor (non-blocking Netty server). In <code>application.yml</code>, routes are defined with <strong>Predicates</strong> and <strong>Filters</strong>:
      <ul>
        <li>Predicates match incoming HTTP request paths (e.g., <code>Path=/api/auth/**</code> &rarr; <code>http://localhost:8081</code>, <code>Path=/api/users/**, /api/reviews/**</code> &rarr; <code>http://localhost:8082</code>).</li>
        <li>Filters allow mutating request/response headers, stripping path prefixes, or enforcing rate-limiting before forwarding to the target microservice.</li>
      </ul>
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q15: What is the difference between @NotNull, @NotEmpty, and @NotBlank in Bean Validation?</div>
    <div class="qa-answer">
      <strong>Answer:</strong>
      <ul>
        <li><code>@NotNull</code>: Validates that the value is not <code>null</code>. Allows empty strings <code>""</code> or whitespace <code>"   "</code>.</li>
        <li><code>@NotEmpty</code>: Validates that the value is not <code>null</code> and its length/size is greater than 0 (e.g. for Strings, Collections, Maps, Arrays). However, a string with only whitespace <code>"   "</code> passes.</li>
        <li><code>@NotBlank</code>: Validates that the string is not <code>null</code> and the trimmed length is greater than 0. It rejects <code>null</code>, <code>""</code>, and whitespace-only strings <code>"   "</code>. (Used for names, emails, passwords).</li>
      </ul>
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q16: How does the Admin block/unblock synchronization work across User and Auth services?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> When an Admin blocks a user via <code>POST /api/admin/users/{userId}/block</code> in <code>user-service</code>:
      <ol>
        <li>The local <code>Farmer</code> record has <code>isBlocked</code> set to <code>true</code>.</li>
        <li><code>AdminUserController</code> uses the OpenFeign <code>AuthServiceClient</code> to call <code>PUT /api/auth/users/{userId}/status</code> with status <code>SUSPENDED</code>.</li>
        <li><code>auth-service</code> updates the <code>User</code> entity status to <code>SUSPENDED</code>.</li>
        <li>If that user attempts to log in, <code>authService.login()</code> checks <code>user.getStatus() != UserStatus.ACTIVE</code> and immediately throws an <code>InvalidCredentialsException("User account is blocked by administrator")</code>, revoking platform access!</li>
      </ol>
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q17: What are JPA Lifecycle Callbacks and how are @PrePersist and @PreUpdate used here?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> JPA lifecycle callbacks allow developers to execute custom logic at specific stages of an entity's lifecycle. In our <code>User</code> and <code>FarmerReview</code> entities, <code>@PrePersist</code> executes automatically right before the entity is first persisted to the database, setting <code>createdAt</code> and default statuses without manual intervention. <code>@PreUpdate</code> executes before any update statement, keeping <code>updatedAt</code> fresh.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q18: What is the purpose of Spring Boot Actuator in your services?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> Spring Boot Actuator provides production-ready monitoring endpoints. In both services, we expose <code>/actuator/health</code> and <code>/actuator/info</code>. Eureka Server and Docker container orchestrators (like Kubernetes or Docker Compose health checks) ping <code>/actuator/health</code> to verify whether the service and its database connection pool (HikariCP) are operational before routing client traffic.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q19: How do you prevent sensitive database credentials from being committed to source control?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> We leverage Spring Boot's property placeholder resolution with environment variable fallbacks:
      <code>spring.datasource.password=${DB_PASSWORD:defaultPassword}</code>. 
      In production and Docker environments, credentials are injected securely as environment variables or pulled from Spring Cloud Config Server via secret management vaults.
    </div>
  </div>

  <div class="qa-card">
    <div class="qa-question">Q20: How does Eureka Service Discovery work in CropDeal?</div>
    <div class="qa-answer">
      <strong>Answer:</strong> At startup, every microservice (client) with <code>eureka.client.register-with-eureka=true</code> registers its hostname, IP, port, and health status with Eureka Server (port 8761). Clients send periodic heartbeats (every 30 seconds). API Gateway and Feign clients fetch the registry cache (<code>fetch-registry=true</code>) to dynamically discover service locations without hardcoding static IP addresses.
    </div>
  </div>
</div>

<!-- SECTION 7 -->
<div id="section-7" class="page-break">
  <h1>7. Quick-Reference Spring Boot Annotations Dictionary</h1>
  <p>Every annotation used across Auth Service, User Service, and Review Service with interview explanations:</p>
  <table>
    <thead>
      <tr>
        <th>Annotation</th>
        <th>Layer</th>
        <th>Purpose & Interview Explanation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>@RestController</code></td>
        <td>Controller</td>
        <td>Combines <code>@Controller</code> and <code>@ResponseBody</code>. Ensures every handler method serializes return objects directly into JSON/XML HTTP response bodies.</td>
      </tr>
      <tr>
        <td><code>@RequestMapping</code></td>
        <td>Controller</td>
        <td>Maps HTTP request paths and HTTP methods to specific handler classes or controller methods.</td>
      </tr>
      <tr>
        <td><code>@Service</code></td>
        <td>Service</td>
        <td>Specialization of <code>@Component</code>. Indicates that the class contains business logic, calculations, and transactional boundaries.</td>
      </tr>
      <tr>
        <td><code>@Repository</code></td>
        <td>Persistence</td>
        <td>Specialization of <code>@Component</code>. Indicates a Data Access Object (DAO) and enables automatic DataAccessException translation.</td>
      </tr>
      <tr>
        <td><code>@Transactional</code></td>
        <td>Service</td>
        <td>Manages database transaction boundaries via Spring AOP. Automatically commits on success and rolls back on unchecked <code>RuntimeException</code>.</td>
      </tr>
      <tr>
        <td><code>@Entity</code></td>
        <td>Persistence</td>
        <td>Specifies that the Java class is a JPA entity mapped to a relational database table.</td>
      </tr>
      <tr>
        <td><code>@Table</code></td>
        <td>Persistence</td>
        <td>Customizes table name, schema, unique constraints, and database indexes.</td>
      </tr>
      <tr>
        <td><code>@Id</code> & <code>@GeneratedValue</code></td>
        <td>Persistence</td>
        <td>Designates the primary key field and specifies generation strategy (e.g. <code>IDENTITY</code> for auto-increment).</td>
      </tr>
      <tr>
        <td><code>@Enumerated</code></td>
        <td>Persistence</td>
        <td>Specifies how enums are persisted. Always use <code>EnumType.STRING</code> to store readable values rather than volatile ordinal integers.</td>
      </tr>
      <tr>
        <td><code>@PrePersist</code> / <code>@PreUpdate</code></td>
        <td>Persistence</td>
        <td>Lifecycle callbacks executed before database insert and update operations respectively.</td>
      </tr>
      <tr>
        <td><code>@Valid</code></td>
        <td>Controller</td>
        <td>Enforces Jakarta Bean Validation rules declared on the DTO before executing the controller method.</td>
      </tr>
      <tr>
        <td><code>@RequestBody</code></td>
        <td>Controller</td>
        <td>Binds incoming HTTP JSON request payload to a Java DTO via <code>HttpMessageConverter</code> (Jackson).</td>
      </tr>
      <tr>
        <td><code>@PathVariable</code></td>
        <td>Controller</td>
        <td>Extracts dynamic URI template variables (e.g. <code>/api/farmers/{id}</code>) into method arguments.</td>
      </tr>
      <tr>
        <td><code>@RequestParam</code></td>
        <td>Controller</td>
        <td>Extracts query parameters (e.g. <code>?reason=violating</code>) from the URL.</td>
      </tr>
      <tr>
        <td><code>@FeignClient</code></td>
        <td>Integration</td>
        <td>Declares a declarative REST client interface implemented dynamically by Spring Cloud OpenFeign.</td>
      </tr>
      <tr>
        <td><code>@PreAuthorize</code></td>
        <td>Security</td>
        <td>Enforces method-level access control evaluated using Spring Expression Language (SpEL) before method invocation.</td>
      </tr>
      <tr>
        <td><code>@AuthenticationPrincipal</code></td>
        <td>Security</td>
        <td>Resolves the currently authenticated principal directly from <code>SecurityContextHolder</code> into a method parameter.</td>
      </tr>
      <tr>
        <td><code>@RestControllerAdvice</code></td>
        <td>Exception</td>
        <td>Declares global cross-cutting exception handlers returning JSON error responses across all controllers.</td>
      </tr>
      <tr>
        <td><code>@ExceptionHandler</code></td>
        <td>Exception</td>
        <td>Designates a method to handle a specific exception type (e.g. <code>FarmerNotFoundException.class</code>).</td>
      </tr>
    </tbody>
  </table>

  <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 2px solid #e2e8f0; color: #64748b; font-size: 12px;">
    &copy; 2026 CropDeal Engineering Team &bull; Prepared for Senior Spring Boot Microservices Technical Interviews &bull; End of Document
  </div>
</div>

</body>
</html>
"""

def generate_pdf():
    print(f"1. Writing master HTML guide to: {OUTPUT_HTML}")
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"2. Converting HTML to publication-quality PDF via Microsoft Edge headless...")
    args = [
        EDGE_EXE,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUTPUT_PDF}",
        f"file:///{OUTPUT_HTML.replace(os.sep, '/')}"
    ]
    
    result = subprocess.run(args, capture_output=True, text=True)
    if os.path.exists(OUTPUT_PDF):
        size_kb = os.path.getsize(OUTPUT_PDF) / 1024
        print(f"SUCCESS: PDF created at: {OUTPUT_PDF} ({size_kb:.2f} KB)")
        return True
    else:
        print(f"ERROR: PDF was not generated. Return code: {result.returncode}")
        print(f"Stderr: {result.stderr}")
        return False

if __name__ == "__main__":
    success = generate_pdf()
    sys.exit(0 if success else 1)
