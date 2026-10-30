import os
import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, NextPageTemplate, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page

        w, h = self._pagesize

        # Running Header
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawString(30, h - 22, "CROPDEAL MICROSERVICES PLATFORM")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawRightString(w - 30, h - 22, "System Architecture | UML Class Model | Entity-Relationship Schema")
        
        # Header rule
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.6)
        self.line(30, h - 26, w - 30, h - 26)

        # Running Footer
        self.line(30, 26, w - 30, 26)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#94A3B8'))
        self.drawString(30, 16, "Confidential | Agricultural B2B E-Commerce Marketplace | Spring Boot 3.3.13")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(w - 30, 16, page_str)
        self.restoreState()

def create_cropdeal_pdf(output_pdf_path):
    p_w, p_h = letter
    l_w, l_h = landscape(letter)

    doc = BaseDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=32,
        bottomMargin=32
    )

    # Frame dimensions
    cover_frame = Frame(0, 0, p_w, p_h, id='cover_frame', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    portrait_frame = Frame(30, 32, p_w - 60, p_h - 64, id='portrait_frame', leftPadding=0, rightPadding=0, topPadding=4, bottomPadding=4)
    # Landscape: 792 wide, 612 high. Margin 28 left/right -> 736 pt width. Margin 30 top/bottom -> 552 pt height.
    landscape_frame = Frame(28, 30, l_w - 56, l_h - 60, id='landscape_frame', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id='cover', frames=cover_frame, pagesize=letter),
        PageTemplate(id='portrait', frames=portrait_frame, pagesize=letter),
        PageTemplate(id='landscape', frames=landscape_frame, pagesize=landscape(letter))
    ])

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor('#FFFFFF')
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#94A3B8')
    )
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=5
    )
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=7,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.2,
        textColor=colors.HexColor('#1E3A8A')
    )
    table_hdr = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#FFFFFF')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.2,
        textColor=colors.HexColor('#0F172A')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=9.2,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # =============================================================
    # PAGE 1: COVER PAGE
    # =============================================================
    story.append(NextPageTemplate('cover'))
    
    cover_data = [
        [Paragraph("<font size=9 color='#38BDF8'><b>ENTERPRISE SYSTEM ARCHITECTURE & ENGINEERING SPECIFICATIONS</b></font>", subtitle_style)],
        [Spacer(1, 22)],
        [Paragraph("CropDeal Microservices<br/>Architecture & Design", title_style)],
        [Spacer(1, 10)],
        [Paragraph("Comprehensive Technical Reference Manual with Architectural Topology, UML Domain Class Specifications, and Entity-Relationship (ER) Data Models.", subtitle_style)],
        [Spacer(1, 30)],
        [
            Table([
                [
                    Paragraph("<b>System Type:</b>", table_cell_bold),
                    Paragraph("B2B Agricultural Marketplace Platform", table_cell),
                    Paragraph("<b>Build Tool:</b>", table_cell_bold),
                    Paragraph("Apache Maven & Docker Compose", table_cell)
                ],
                [
                    Paragraph("<b>Framework:</b>", table_cell_bold),
                    Paragraph("Spring Boot 3.3.13 | Java 21 LTS", table_cell),
                    Paragraph("<b>Service Discovery:</b>", table_cell_bold),
                    Paragraph("Spring Cloud Netflix Eureka (:8761)", table_cell)
                ],
                [
                    Paragraph("<b>API Gateway:</b>", table_cell_bold),
                    Paragraph("Spring Cloud Gateway (:8080)", table_cell),
                    Paragraph("<b>Configuration:</b>", table_cell_bold),
                    Paragraph("100% Centralized Config Server (:8888)", table_cell)
                ],
                [
                    Paragraph("<b>Message Broker:</b>", table_cell_bold),
                    Paragraph("RabbitMQ 3.x (Direct/Topic AMQP)", table_cell),
                    Paragraph("<b>Relational DB:</b>", table_cell_bold),
                    Paragraph("Distributed MySQL Schemas", table_cell)
                ],
                [
                    Paragraph("<b>Frontend:</b>", table_cell_bold),
                    Paragraph("Angular 17 Responsive Portals", table_cell),
                    Paragraph("<b>Documentation:</b>", table_cell_bold),
                    Paragraph("SpringDoc OpenAPI v3 / Swagger UI", table_cell)
                ]
            ], colWidths=[105, 165, 110, 160], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
                ('TOPPADDING', (0,0), (-1,-1), 6.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6.5),
                ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#FFFFFF'))
            ])
        ],
        [Spacer(1, 50)],
        [
            Table([
                [
                    Paragraph("<b>Direct Trade Engine</b><br/><font size=6.5 color='#94A3B8'>Eliminates middleman exploitation by connecting verified farmers directly to bulk commercial dealers.</font>", subtitle_style),
                    Paragraph("<b>Multi-Model Commerce</b><br/><font size=6.5 color='#94A3B8'>Supports Direct Buy, Real-time Competitive Auctions, and Bilateral Counter-Offer Negotiations.</font>", subtitle_style),
                    Paragraph("<b>Escrow Digital Wallet</b><br/><font size=6.5 color='#94A3B8'>Double-spend protected escrow funds holding until verified OTP delivery confirmation.</font>", subtitle_style)
                ]
            ], colWidths=[180, 180, 180], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
                ('VALIGN', (0,0), (-1,-1), 'TOP')
            ])
        ],
        [Spacer(1, 35)],
        [Paragraph("<font size=7.5 color='#64748B'>CONFIDENTIAL DOCUMENTATION | PREPARED FOR SYSTEM AUDIT, CODE REVIEW, AND PRESENTATIONS | 2026</font>", subtitle_style)]
    ]

    cover_table = Table(cover_data, colWidths=[552])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0B1120')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 32),
        ('RIGHTPADDING', (0,0), (-1,-1), 32)
    ]))
    story.append(cover_table)

    # Next page will be Portrait
    story.append(NextPageTemplate('portrait'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 2: EXECUTIVE SUMMARY & SERVICE DIRECTORY (Portrait)
    # =============================================================
    story.append(Paragraph("1. Executive Summary & Platform Overview", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "<b>CropDeal</b> is an enterprise-grade distributed microservices platform engineered to eliminate exploitative intermediaries in agricultural trade. "
        "Traditional agricultural supply chains leave farmers vulnerable to opaque pricing and delayed payments. CropDeal bridges this divide through a cloud-native "
        "digital marketplace providing transparent pricing, live Mandi market benchmarks (MSP), competitive bidding auctions, and bilateral price negotiations.",
        body_style
    ))

    callout_data = [[
        Paragraph(
            "<b>Architectural Foundation:</b> CropDeal operates across <b>15 independent Spring Boot microservices</b>. "
            "Synchronous HTTP requests enter through a centralized <b>Spring Cloud API Gateway</b> utilizing Eureka client-side load balancing (`lb://`). "
            "Asynchronous workflows (crop alerts, bid updates, negotiations, orders, delivery tracking) are decoupled using a <b>RabbitMQ event bus</b>.",
            callout_style
        )
    ]]
    callout_tbl = Table(callout_data, colWidths=[552])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(callout_tbl)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Platform Microservices Directory & Port Mappings", h2_style))
    
    svc_directory = [
        [Paragraph("Service Name", table_hdr), Paragraph("Port", table_hdr), Paragraph("Primary Domain Responsibility", table_hdr), Paragraph("Database Schema", table_hdr), Paragraph("Messaging Role", table_hdr)],
        [Paragraph("api-gateway", table_cell_bold), Paragraph(":8080", table_cell), Paragraph("Single edge entrypoint, route predicates, JWT auth, CORS, Swagger aggregation", table_cell), Paragraph("Stateless", table_cell), Paragraph("Client Ingress", table_cell)],
        [Paragraph("eureka-server", table_cell_bold), Paragraph(":8761", table_cell), Paragraph("Service registry, heartbeat monitoring, dynamic instance discovery", table_cell), Paragraph("In-Memory", table_cell), Paragraph("Governance", table_cell)],
        [Paragraph("config-server", table_cell_bold), Paragraph(":8888", table_cell), Paragraph("Centralized Git/file properties repository for all 15 services", table_cell), Paragraph("Git / File Repo", table_cell), Paragraph("Central Config", table_cell)],
        [Paragraph("auth-service", table_cell_bold), Paragraph(":8081", table_cell), Paragraph("Authentication, JWT token generation/validation, role-based access control", table_cell), Paragraph("MySQL (auth_db)", table_cell), Paragraph("Auth Events", table_cell)],
        [Paragraph("user-service", table_cell_bold), Paragraph(":8082", table_cell), Paragraph("Farmer, Dealer, and Delivery Partner KYC profiles and reviews", table_cell), Paragraph("MySQL (user_db)", table_cell), Paragraph("Profile Events", table_cell)],
        [Paragraph("crop-service", table_cell_bold), Paragraph(":8083", table_cell), Paragraph("Crop catalog, commodity types, quantity, state/district filters, status", table_cell), Paragraph("MySQL (crop_db)", table_cell), Paragraph("Publish: Crop Posted", table_cell)],
        [Paragraph("price-service", table_cell_bold), Paragraph(":8084", table_cell), Paragraph("National Mandi daily market rates sync, MSP benchmarks, price trends", table_cell), Paragraph("MySQL (price_db)", table_cell), Paragraph("Price Sync", table_cell)],
        [Paragraph("price-alert-service", table_cell_bold), Paragraph(":8094", table_cell), Paragraph("Buyer requests, target threshold subscriptions, automated match triggers", table_cell), Paragraph("MySQL (price_alert_db)", table_cell), Paragraph("Publish: Price Match", table_cell)],
        [Paragraph("negotiation-service", table_cell_bold), Paragraph(":8085", table_cell), Paragraph("Direct bilateral price bargaining, counter-offers, contract lock", table_cell), Paragraph("MySQL (negotiation_db)", table_cell), Paragraph("Publish: Neg Offer", table_cell)],
        [Paragraph("bidding-service", table_cell_bold), Paragraph(":8086", table_cell), Paragraph("Competitive auction listings, real-time bid validation, winner resolution", table_cell), Paragraph("MySQL (bidding_db)", table_cell), Paragraph("Publish: Bid Placed", table_cell)],
        [Paragraph("order-service", table_cell_bold), Paragraph(":8088", table_cell), Paragraph("Central order lifecycle orchestration (Direct, Auction, Negotiation)", table_cell), Paragraph("MySQL (order_db)", table_cell), Paragraph("Publish: Order State", table_cell)],
        [Paragraph("payment-service", table_cell_bold), Paragraph(":8089", table_cell), Paragraph("Transaction settlement, external gateways, automated refunds", table_cell), Paragraph("MySQL (payment_db)", table_cell), Paragraph("Publish: Paid", table_cell)],
        [Paragraph("wallet-service", table_cell_bold), Paragraph(":8087", table_cell), Paragraph("Digital wallet, double-spend prevention, escrow fund reservation & release", table_cell), Paragraph("MySQL (wallet_db)", table_cell), Paragraph("Escrow Events", table_cell)],
        [Paragraph("invoice-service", table_cell_bold), Paragraph(":8090", table_cell), Paragraph("Automated GST/tax calculation, itemized line billing, PDF bill generator", table_cell), Paragraph("MySQL (invoice_db)", table_cell), Paragraph("Consume: Paid", table_cell)],
        [Paragraph("delivery-service", table_cell_bold), Paragraph(":8091", table_cell), Paragraph("Fleet assignment, transit tracking, secure OTP delivery handshake", table_cell), Paragraph("MySQL (delivery_db)", table_cell), Paragraph("Publish: Delivery", table_cell)],
        [Paragraph("notification-service", table_cell_bold), Paragraph(":8092", table_cell), Paragraph("RabbitMQ consumer, omnichannel alerts (in-app, email, push)", table_cell), Paragraph("MySQL (notification_db)", table_cell), Paragraph("Consume: All Queues", table_cell)],
        [Paragraph("chatbot-service", table_cell_bold), Paragraph(":8096", table_cell), Paragraph("Agricultural advisory AI assistant, crop queries, FAQ automated responses", table_cell), Paragraph("In-Memory Knowledge", table_cell), Paragraph("Advisory Chat", table_cell)],
        [Paragraph("report-service", table_cell_bold), Paragraph(":8095", table_cell), Paragraph("Farmer earnings, dealer volume, commodity yield, platform revenue metrics", table_cell), Paragraph("Reporting Views", table_cell), Paragraph("Analytics Sync", table_cell)]
    ]

    svc_tbl = Table(svc_directory, colWidths=[92, 42, 222, 98, 98])
    svc_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')])
    ]))
    story.append(svc_tbl)

    # Next page will be Landscape for Architecture Diagram
    story.append(NextPageTemplate('landscape'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 3: ARCHITECTURAL DIAGRAM (Landscape)
    # =============================================================
    arch_img_path = 'D:\\cropdealnaresh\\doc_gen\\architecture_diagram.png'
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=734, height=520))

    # Next page will be Portrait for Architecture Explanation
    story.append(NextPageTemplate('portrait'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 4: ARCHITECTURAL EXPLANATION (Portrait)
    # =============================================================
    story.append(Paragraph("2. Architectural Breakdown & Deep Dive Explanation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("2.1 Edge Layer: API Gateway & Traffic Ingress", h2_style))
    story.append(Paragraph(
        "The <b>API Gateway (Port 8080)</b> acts as the single reverse proxy and traffic guard for the entire ecosystem. "
        "Rather than exposing internal container ports directly to the outside world, external clients (Angular web application, mobile browsers) "
        "interact exclusively with port 8080. The Gateway provides four critical enterprise capabilities: "
        "<br/>• <b>Dynamic Load-Balanced Routing:</b> Route predicates forward incoming path patterns (e.g. <code>/api/crops/**</code>, <code>/api/orders/**</code>) "
        "to microservices using the logical <code>lb://service-name</code> syntax resolved via Spring Cloud LoadBalancer."
        "<br/>• <b>Centralized JWT Security Filter:</b> Validates cryptographic signatures of Bearer tokens before forwarding requests down to internal services."
        "<br/>• <b>Unified CORS Configuration:</b> Enforces allowed HTTP origins, methods, and headers at the boundary, preventing browser cross-origin blocks."
        "<br/>• <b>OpenAPI Specification Aggregator:</b> Aggregates Swagger documentation from all 15 microservices into a single unified interactive console at <code>/swagger-ui.html</code>.",
        body_style
    ))

    story.append(Paragraph("2.2 Service Governance: Eureka Discovery & Centralized Config", h2_style))
    story.append(Paragraph(
        "CropDeal uses <b>Netflix Eureka (Port 8761)</b> for dynamic service registration. When each microservice boots inside its Docker container, "
        "it registers its container IP and port with Eureka. The Gateway queries Eureka periodically to maintain an up-to-date registry, eliminating static IP hardcoding. "
        "Parallel to Eureka, the <b>Spring Cloud Config Server (Port 8888)</b> provides 100% centralized property management. Individual services do not maintain duplicate local "
        "configuration files; instead, they pull datasource credentials, RabbitMQ bindings, and Eureka URLs dynamically upon startup.",
        body_style
    ))

    story.append(Paragraph("2.3 Asynchronous Event Backbone: RabbitMQ Message Broker", h2_style))
    story.append(Paragraph(
        "To guarantee high throughput and decouple time-sensitive transactions from notification delivery, CropDeal integrates <b>RabbitMQ (Port 5672)</b>. "
        "When business milestones occur, services immediately publish lightweight domain events to <code>cropdeal.exchange</code> without blocking the HTTP thread: "
        "<br/>• <b>Crop Posting Event:</b> Emitted by <code>crop-service</code> &rarr; Consumed by <code>price-alert-service</code> and <code>notification-service</code> to alert subscribed dealers."
        "<br/>• <b>Bidding & Negotiation Events:</b> Emitted on each counter-offer or bid increment &rarr; Instantly dispatches in-app notifications to both parties."
        "<br/>• <b>Order Lifecycle Events:</b> Triggers invoice generation, wallet escrow reservations, and logistics fleet dispatch asynchronously."
        "<br/>• <b>Delivery Status Event:</b> Emitted by delivery partners on transit milestones &rarr; Triggers dealer notifications and releases escrow funds upon final OTP verification.",
        body_style
    ))

    story.append(Paragraph("2.4 Persistence Strategy: Distributed Database Isolation", h2_style))
    story.append(Paragraph(
        "Following microservices architectural best practices, CropDeal avoids a monolithic shared database. Each microservice manages its own logical schema "
        "(e.g., <code>crop_db</code>, <code>order_db</code>, <code>wallet_db</code>). Cross-service relationships are established using immutable soft identifiers "
        "(such as <code>farmer_id</code>, <code>dealer_id</code>, <code>crop_id</code>) rather than direct SQL cross-schema joins. This prevents cascade locks, enables independent horizontal scaling, "
        "and allows individual database schemas to evolve independently.",
        body_style
    ))

    # Next page will be Landscape for Class Diagram
    story.append(NextPageTemplate('landscape'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 5: CLASS DIAGRAM (Landscape)
    # =============================================================
    class_img_path = 'D:\\cropdealnaresh\\doc_gen\\class_diagram.png'
    if os.path.exists(class_img_path):
        story.append(Image(class_img_path, width=734, height=520))

    # Next page will be Portrait for Class Model Explanation
    story.append(NextPageTemplate('portrait'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 6: CLASS MODEL EXPLANATION (Portrait)
    # =============================================================
    story.append(Paragraph("3. Domain Class Model & Collaboration Specifications", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("3.1 4-Tier Software Architecture & Design Patterns", h2_style))
    story.append(Paragraph(
        "Every microservice within CropDeal adheres strictly to an enterprise layered architecture pattern: "
        "<br/>1. <b>REST Controller Layer (<code>@RestController</code>):</b> Defines clean RESTful HTTP endpoints, validates client payloads using Bean Validation (<code>@Valid</code>, <code>@NotNull</code>), "
        "enforces role-based security (<code>@PreAuthorize</code>), and documents schemas for OpenAPI/Swagger."
        "<br/>2. <b>Service Business Logic Layer (<code>@Service</code>):</b> Encapsulates core business transactions, boundary checks, and state transitions. "
        "Methods modifying data state are marked with <code>@Transactional</code> to guarantee ACID atomicity. It acts as the event publisher via <code>RabbitTemplate</code>."
        "<br/>3. <b>Spring Data Repository Layer (<code>@Repository</code>):</b> Extends <code>JpaRepository&lt;Entity, ID&gt;</code>, offering derived query methods and optimized JPQL projections without boilerplate SQL."
        "<br/>4. <b>Domain Entity Layer (<code>@Entity</code>):</b> Represents relational database tables mapped through Hibernate JPA with explicit audit timestamps and validation annotations.",
        body_style
    ))

    story.append(Paragraph("3.2 Key Domain Aggregates & Class Relationships", h2_style))
    
    class_breakdown = [
        [Paragraph("Domain Class", table_hdr), Paragraph("Key Field Members", table_hdr), Paragraph("Core Methods & Operations", table_hdr), Paragraph("Class Relationships & Cardinality", table_hdr)],
        [
            Paragraph("Crop", table_cell_bold),
            Paragraph("farmerId, commodity, state, district, grade, quantity, pricePerUnit, status", table_cell),
            Paragraph("+ isAvailable(): Boolean<br/>+ reserveQuantity()<br/>+ markAsSold()", table_cell),
            Paragraph("Belongs to Farmer (N:1). Associated with BiddingListing (1:1) and Negotiations (1:N).", table_cell)
        ],
        [
            Paragraph("BiddingListing & Bid", table_cell_bold),
            Paragraph("cropId, farmerId, basePrice, currentHighestBid, currentWinnerId, startTime, endTime", table_cell),
            Paragraph("+ placeBid(Bid): Boolean<br/>+ closeAuction(): Long<br/>+ markAsOutbid()", table_cell),
            Paragraph("BiddingListing is aggregate root composing 1..* Bid instances. Associates with winning Dealer.", table_cell)
        ],
        [
            Paragraph("Negotiation & Offer", table_cell_bold),
            Paragraph("cropId, buyerId, sellerId, targetPrice, agreedPrice, status, offers: List&lt;Offer&gt;", table_cell),
            Paragraph("+ addCounterOffer()<br/>+ acceptOffer()<br/>+ rejectNegotiation()", table_cell),
            Paragraph("Negotiation manages a collection of 1..* NegotiationOffer instances representing counter-offers.", table_cell)
        ],
        [
            Paragraph("Order", table_cell_bold),
            Paragraph("farmerId, dealerId, cropId, quantity, unitPrice, totalAmount, status, orderType", table_cell),
            Paragraph("+ calculateTotal()<br/>+ confirmOrder()<br/>+ markDelivered()<br/>+ cancelOrder()", table_cell),
            Paragraph("Central commercial hub. Originates 1:1 Payment, 1:1 Invoice, and 1:1 Delivery.", table_cell)
        ],
        [
            Paragraph("Wallet & Escrow", table_cell_bold),
            Paragraph("userId, userRole, balance, reservedBalance, version (optimistic lock)", table_cell),
            Paragraph("+ creditBalance()<br/>+ debitBalance()<br/>+ reserveEscrow()<br/>+ releaseEscrow()", table_cell),
            Paragraph("Wallet aggregates 1..* WalletTransaction and 1..* WalletReservation records.", table_cell)
        ],
        [
            Paragraph("Delivery & Fleet", table_cell_bold),
            Paragraph("orderId, deliveryAgentId, pickupAddress, deliveryAddress, status, deliveryOtp", table_cell),
            Paragraph("+ assignAgent()<br/>+ updateStatus()<br/>+ verifyOtpAndComplete()", table_cell),
            Paragraph("Delivery aggregates 1..* DeliveryStatusHistory and 1..* DeliveryAssignment.", table_cell)
        ]
    ]

    cls_tbl = Table(class_breakdown, colWidths=[92, 160, 135, 165])
    cls_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')])
    ]))
    story.append(cls_tbl)

    # Next page will be Landscape for Entity Diagram
    story.append(NextPageTemplate('landscape'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 7: ENTITY-RELATIONSHIP (ER) DIAGRAM (Landscape)
    # =============================================================
    er_img_path = 'D:\\cropdealnaresh\\doc_gen\\entity_diagram.png'
    if os.path.exists(er_img_path):
        story.append(Image(er_img_path, width=734, height=520))

    # Next page will be Portrait for ER Explanation
    story.append(NextPageTemplate('portrait'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 8: DATABASE SCHEMA & DATA INTEGRITY EXPLANATION (Portrait)
    # =============================================================
    story.append(Paragraph("4. Database Schema Design & Data Integrity Guidelines", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("4.1 Relational Schema Organization & Key Tables", h2_style))
    story.append(Paragraph(
        "CropDeal's relational architecture balances relational integrity with microservice autonomy. "
        "The schema dictionary is structured across the following primary tables: "
        "<br/>• <b><code>users</code>:</b> Central authentication record storing email, bcrypt hashed password, and role."
        "<br/>• <b><code>farmers</code> & <code>dealers</code>:</b> Extended role-specific profiles linked to <code>users.id</code> via 1:1 foreign key."
        "<br/>• <b><code>crops</code>:</b> Agricultural listings detailing commodity, agricultural grade, quantity in metric units, state, district, and base price."
        "<br/>• <b><code>bidding_listings</code> & <code>bids</code>:</b> Auction listings linked to crops; bids enforce 1:N cardinality with descending order ranking."
        "<br/>• <b><code>negotiations</code> & <code>negotiation_offers</code>:</b> Bilateral chat negotiations tracking agreed price targets."
        "<br/>• <b><code>orders</code>:</b> The central fulfillment record storing quantity, locked unit price, calculated total, and state machine status."
        "<br/>• <b><code>payments</code> & <code>invoices</code>:</b> Financial audit trail, transaction reference hashes, and itemized tax breakdowns."
        "<br/>• <b><code>deliveries</code>:</b> Logistics dispatch tracking pickup/drop coordinates, delivery agent assignment, and OTP verification code."
        "<br/>• <b><code>wallets</code> & <code>wallet_transactions</code>:</b> Digital wallet balances, ledger entries, and escrow hold reservations.",
        body_style
    ))

    story.append(Paragraph("4.2 Enterprise Financial Precision & Concurrency Control", h2_style))
    story.append(Paragraph(
        "To avoid the catastrophic floating-point rounding errors common with standard <code>FLOAT</code> or <code>DOUBLE</code> types in banking applications, "
        "<b>all monetary amounts, unit rates, quantities, and bids are strictly modeled as <code>DECIMAL(12,2)</code> in MySQL and <code>BigDecimal</code> in Java.</b> "
        "<br/><br/>"
        "<b>Optimistic Concurrency Control (<code>@Version</code>):</b> "
        "In high-concurrency environments—such as rapid auction bids or simultaneous order placements—there is a risk of double-spending wallet balances. "
        "CropDeal equips the <code>wallets</code> table with an explicit <code>version BIGINT NOT NULL</code> column. "
        "Hibernate enforces optimistic locking: if two transactions attempt to reserve or debit the same wallet simultaneously, "
        "the second transaction detects a version conflict, rolls back safely, and throws an <code>OptimisticLockException</code>, preventing balance corruption.",
        body_style
    ))

    story.append(Paragraph("4.3 Eventual Consistency & Distributed Transactions (Saga Pattern)", h2_style))
    story.append(Paragraph(
        "Because CropDeal spans multiple independent databases, traditional distributed two-phase commits (2PC) are avoided due to latency and locking bottlenecks. "
        "Instead, the platform implements an <b>Event-Driven Choreographed Saga</b>: "
        "<br/>1. When an order is created (<code>status = CREATED</code>), <code>order-service</code> publishes an <code>OrderCreatedEvent</code>."
        "<br/>2. <code>wallet-service</code> consumes the event and locks funds in escrow (<code>status = ESCROW_RESERVED</code>)."
        "<br/>3. Upon payment confirmation, <code>delivery-service</code> initiates driver dispatch."
        "<br/>4. If any step fails (e.g. insufficient wallet balance or cancelled order), a compensating event is dispatched, releasing the reserved funds and transitioning the order to <code>CANCELLED</code>.",
        body_style
    ))

    # Next page will be Portrait for Cheat Sheet
    story.append(NextPageTemplate('portrait'))
    story.append(PageBreak())

    # =============================================================
    # PAGE 9: BUSINESS WORKFLOWS & PRESENTATION CHEAT SHEET (Portrait)
    # =============================================================
    story.append(Paragraph("5. Business Workflows & Presentation Cheat Sheet", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "Use this structured cheat sheet during technical reviews, professor evaluations, or engineering interviews to clearly explain CropDeal's end-to-end operation.",
        body_style
    ))

    workflows = [
        [Paragraph("Commerce Flow", table_hdr), Paragraph("Step-by-Step Execution Sequence", table_hdr), Paragraph("Involved Services & Protocols", table_hdr)],
        [
            Paragraph("1. Direct Crop Purchase", table_cell_bold),
            Paragraph(
                "1. Farmer posts crop listing with fixed price per unit.<br/>"
                "2. Dealer discovers crop via Gateway search.<br/>"
                "3. Dealer clicks 'Buy Now' &rarr; Order created in CREATED state.<br/>"
                "4. Dealer pays via Escrow Wallet &rarr; Funds reserved.<br/>"
                "5. Delivery partner assigned &rarr; Picks up crop from farm.<br/>"
                "6. Delivery verified with 6-digit OTP &rarr; Funds credited to Farmer.",
                table_cell
            ),
            Paragraph("crop-service (REST)<br/>order-service (REST)<br/>wallet-service (Escrow)<br/>delivery-service (OTP)<br/>notification-service (RabbitMQ)", table_cell)
        ],
        [
            Paragraph("2. Competitive Live Auction", table_cell_bold),
            Paragraph(
                "1. Farmer lists crop for auction with base reserve price and deadline.<br/>"
                "2. Dealers place escalating bids; wallet verifies reserve ability.<br/>"
                "3. Outbid dealers receive instant RabbitMQ notifications.<br/>"
                "4. Countdown timer expires &rarr; Highest valid bid declared winner.<br/>"
                "5. System auto-generates Order with locked winning bid price.",
                table_cell
            ),
            Paragraph("bidding-service (REST)<br/>wallet-service (Hold)<br/>order-service (Auto-Create)<br/>RabbitMQ (bid.events.queue)", table_cell)
        ],
        [
            Paragraph("3. Counter-Offer Price Negotiation", table_cell_bold),
            Paragraph(
                "1. Dealer reviews crop and proposes lower counter-offer rate.<br/>"
                "2. Farmer receives push notification and reviews offer.<br/>"
                "3. Farmer can Accept, Reject, or submit a revised Counter-Offer.<br/>"
                "4. Both parties agree on target price &rarr; Negotiation locked.<br/>"
                "5. Order created automatically with agreed negotiated price.",
                table_cell
            ),
            Paragraph("negotiation-service (REST)<br/>order-service (REST)<br/>RabbitMQ (negotiation.events.queue)", table_cell)
        ],
        [
            Paragraph("4. Smart Mandi Price & Alert Match", table_cell_bold),
            Paragraph(
                "1. Mandi API syncs live wholesale crop prices across districts.<br/>"
                "2. Dealers subscribe to price alert thresholds for specific commodities.<br/>"
                "3. When farmer lists crop matching dealer's target rate, RabbitMQ dispatches instant notification.",
                table_cell
            ),
            Paragraph("price-service (Sync)<br/>price-alert-service (Match)<br/>RabbitMQ (price.alert.queue)", table_cell)
        ]
    ]

    wf_tbl = Table(workflows, colWidths=[112, 295, 145])
    wf_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')])
    ]))
    story.append(wf_tbl)
    story.append(Spacer(1, 12))

    summary_box = [
        [
            Paragraph(
                "<b>Quick Summary for Interview / Presentation:</b><br/>"
                "&bull; <b>Architecture:</b> 15 Spring Boot 3.3.13 microservices running on Java 21, Spring Cloud Gateway (:8080), Netflix Eureka (:8761), and Spring Cloud Config (:8888).<br/>"
                "&bull; <b>Messaging:</b> Event-driven architecture with RabbitMQ decoupled topic exchanges and queues for non-blocking notifications.<br/>"
                "&bull; <b>Security:</b> Centralized JWT authentication filter and role-based access control (Farmer, Dealer, Delivery Partner, Admin).<br/>"
                "&bull; <b>Data Consistency:</b> Distributed database-per-service pattern with optimistic concurrency locking (<code>@Version</code>) and choreographed saga workflows.",
                body_style
            )
        ]
    ]
    sum_tbl = Table(summary_box, colWidths=[552])
    sum_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#86EFAC')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(sum_tbl)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built at: {output_pdf_path}")

if __name__ == '__main__':
    target_path = sys.argv[1] if len(sys.argv) > 1 else 'D:\\cropdealnaresh\\CropDeal_Architecture_Class_Entity_Diagrams.pdf'
    create_cropdeal_pdf(target_path)
