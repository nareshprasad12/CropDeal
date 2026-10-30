import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
import matplotlib.patches as mpatches

def draw_uml_class(ax, x, y, w, h, class_name, stereotype, attributes, methods, border_color='#1E293B', header_bg='#0F172A', text_color='#0F172A'):
    # Outer box
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.008",
                         facecolor='#FFFFFF', edgecolor=border_color, linewidth=1.5, zorder=3)
    ax.add_patch(box)

    # Header Box
    hdr_h = 0.038
    hdr_box = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="round,pad=0,rounding_size=0.008",
                            facecolor=header_bg, edgecolor=border_color, linewidth=1.2, zorder=3.5)
    ax.add_patch(hdr_box)
    rect = Rectangle((x, y + h - hdr_h), w, hdr_h * 0.4, facecolor=header_bg, edgecolor='none', zorder=3.8)
    ax.add_patch(rect)

    # Stereotype & Name
    if stereotype:
        ax.text(x + w * 0.5, y + h - 0.012, f"«{stereotype}»", ha='center', va='center', fontsize=6.2, fontstyle='italic', color='#94A3B8', zorder=4)
        ax.text(x + w * 0.5, y + h - 0.026, class_name, ha='center', va='center', fontsize=7.8, fontweight='bold', color='#FFFFFF', zorder=4)
    else:
        ax.text(x + w * 0.5, y + h - 0.019, class_name, ha='center', va='center', fontsize=8.2, fontweight='bold', color='#FFFFFF', zorder=4)

    # Divider below header
    ax.plot([x, x + w], [y + h - hdr_h, y + h - hdr_h], color=border_color, lw=1, zorder=4)

    # Attributes
    curr_y = y + h - hdr_h - 0.012
    for attr in attributes:
        ax.text(x + 0.008, curr_y, attr, ha='left', va='center', fontsize=6.2, color='#334155', fontfamily='monospace', zorder=4)
        curr_y -= 0.012

    # Divider between attributes and methods
    if methods:
        ax.plot([x, x + w], [curr_y + 0.004, curr_y + 0.004], color='#CBD5E1', lw=0.8, linestyle='-', zorder=4)
        curr_y -= 0.010
        for m in methods:
            ax.text(x + 0.008, curr_y, m, ha='left', va='center', fontsize=6.0, color='#1E293B', fontfamily='monospace', zorder=4)
            curr_y -= 0.012

def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(22, 15), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#F8FAFC')
    outer_border = FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0,rounding_size=0.015",
                                 facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=2, zorder=1)
    ax.add_patch(outer_border)

    # Header Banner
    header = FancyBboxPatch((0.02, 0.925), 0.96, 0.06, boxstyle="round,pad=0,rounding_size=0.008",
                           facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.04, 0.96, "CROPDEAL DOMAIN CLASS MODEL & OBJECT ARCHITECTURE", fontsize=15, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(0.04, 0.938, "UML Class Specifications: Domain Aggregates, Layered Contracts & Microservice Boundary Collaborations", fontsize=9, color='#94A3B8', zorder=3)

    # -------------------------------------------------------------
    # SECTION A: ARCHITECTURAL DESIGN PATTERN (Layered Microservice)
    # -------------------------------------------------------------
    pattern_box = FancyBboxPatch((0.025, 0.79), 0.95, 0.125, boxstyle="round,pad=0,rounding_size=0.008",
                                 facecolor='#F1F5F9', edgecolor='#94A3B8', linewidth=1.2, zorder=2)
    ax.add_patch(pattern_box)
    ax.text(0.035, 0.898, "STANDARD 4-TIER MICROSERVICE DESIGN PATTERN & RESPONSIBILITY SEPARATION", fontsize=9.2, fontweight='bold', color='#1E293B', zorder=3)

    tiers = [
        ("REST Controller", "«Controller»", [
            "+ handleRequest(@Valid DTO): ResponseEntity",
            "+ validateSecurityToken(JWT): Principal",
            "+ publishSwaggerOpenAPI(): OpenAPI"
        ], ["Handles HTTP routing, parameter binding,", "request validation, and security authorization."], '#2563EB'),
        
        ("Service Implementation", "«Service»", [
            "+ executeBusinessRules(Command): Result",
            "+ @Transactional commitStateChange()",
            "+ publishDomainEvent(RabbitTemplate)"
        ], ["Encapsulates core business transactions,", "domain events publishing, and validations."], '#059669'),

        ("Spring Data Repository", "«Repository»", [
            "+ findById(ID): Optional<Entity>",
            "+ save(Entity): Entity",
            "+ findByCustomCriteria(JPQL): List<T>"
        ], ["Data access abstraction providing CRUD and", "optimized derived/native SQL query operations."], '#D97706'),

        ("Domain Entity Model", "«Entity»", [
            "- id: Long {id, generated}",
            "- auditFields: CreatedAt, UpdatedAt",
            "+ getters(), setters(), businessMethods()"
        ], ["Persistent domain entity mapping to relational", "tables with optimistic concurrency control."], '#7C3AED')
    ]

    for idx, (t_name, t_st, t_meth, t_desc, t_col) in enumerate(tiers):
        tx = 0.035 + idx * 0.235
        # Box
        b = FancyBboxPatch((tx, 0.80), 0.225, 0.088, boxstyle="round,pad=0,rounding_size=0.006",
                           facecolor='#FFFFFF', edgecolor=t_col, linewidth=1.5, zorder=3)
        ax.add_patch(b)
        hb = FancyBboxPatch((tx, 0.865), 0.225, 0.023, boxstyle="round,pad=0,rounding_size=0.006",
                            facecolor=t_col, edgecolor=t_col, linewidth=1, zorder=3.5)
        ax.add_patch(hb)
        rect = Rectangle((tx, 0.865), 0.225, 0.01, facecolor=t_col, edgecolor='none', zorder=3.8)
        ax.add_patch(rect)
        ax.text(tx + 0.112, 0.876, f"{t_st} {t_name}", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF', zorder=4)

        for m_idx, m in enumerate(t_meth):
            ax.text(tx + 0.006, 0.852 - m_idx * 0.011, m, fontsize=5.8, fontfamily='monospace', color='#0F172A', zorder=4)
        for d_idx, d in enumerate(t_desc):
            ax.text(tx + 0.006, 0.818 - d_idx * 0.009, d, fontsize=5.6, fontstyle='italic', color='#64748B', zorder=4)

        if idx < 3:
            ax.annotate('', xy=(tx + 0.235, 0.845), xytext=(tx + 0.225, 0.845),
                        arrowprops=dict(arrowstyle="-|>", color='#64748B', lw=1.5, mutation_scale=10), zorder=5)

    # -------------------------------------------------------------
    # SECTION B: CORE DOMAIN CLASS DIAGRAMS (Grouped by Business Domain)
    # -------------------------------------------------------------
    
    # 1. USER & IDENTITY DOMAIN
    draw_uml_class(ax, 0.025, 0.53, 0.17, 0.235, "User", "auth-service",
                   ["- id: Long", "- email: String", "- username: String", "- role: Role", "- status: UserStatus", "- authProvider: AuthProvider", "- providerId: String"],
                   ["+ getRole(): Role", "+ isEnabled(): Boolean", "+ updatePassword()"],
                   border_color='#0284C7', header_bg='#0284C7')

    draw_uml_class(ax, 0.025, 0.27, 0.17, 0.24, "Farmer", "user-service",
                   ["- id: Long", "- userId: Long", "- name: String", "- phone: String", "- address: String", "- farmLocation: String", "- bankDetails: String", "- averageRating: Double"],
                   ["+ getAverageRating()", "+ updateProfile()", "+ addBankDetails()"],
                   border_color='#0284C7', header_bg='#0284C7')

    draw_uml_class(ax, 0.025, 0.025, 0.17, 0.225, "Dealer", "user-service",
                   ["- id: Long", "- userId: Long", "- name: String", "- phone: String", "- businessName: String", "- address: String", "- bankDetails: String"],
                   ["+ getBusinessName()", "+ verifyLicense()", "+ updateBank()"],
                   border_color='#0284C7', header_bg='#0284C7')

    # 2. CATALOG & CROPS DOMAIN
    draw_uml_class(ax, 0.215, 0.53, 0.175, 0.235, "Crop", "crop-service",
                   ["- id: Long", "- farmerId: Long", "- commodity: String", "- state: String", "- district: String", "- grade: String", "- quantity: BigDecimal", "- unit: String", "- pricePerUnit: BigDecimal", "- status: CropStatus"],
                   ["+ isAvailable(): Boolean", "+ reserveQuantity()", "+ markAsSold()"],
                   border_color='#16A34A', header_bg='#16A34A')

    draw_uml_class(ax, 0.215, 0.27, 0.175, 0.24, "CropSubscription", "crop-service",
                   ["- id: Long", "- subscriberId: Long", "- commodity: String", "- state: String", "- district: String", "- grade: String", "- subscribedAt: LocalDateTime"],
                   ["+ matchesCrop(Crop): Boolean", "+ getSubscriberId()"],
                   border_color='#16A34A', header_bg='#16A34A')

    draw_uml_class(ax, 0.215, 0.025, 0.175, 0.225, "MarketPrice", "price-service",
                   ["- id: Long", "- state: String", "- district: String", "- market: String", "- commodity: String", "- variety: String", "- minPrice: BigDecimal", "- maxPrice: BigDecimal", "- modalPrice: BigDecimal", "- arrivalDate: LocalDate"],
                   ["+ getModalPrice()", "+ isWithinMsp()", "+ getTrend()"],
                   border_color='#16A34A', header_bg='#16A34A')

    # 3. AUCTION & NEGOTIATION DOMAIN
    draw_uml_class(ax, 0.41, 0.53, 0.18, 0.235, "BiddingListing", "bidding-service",
                   ["- id: Long", "- cropId: Long", "- farmerId: Long", "- cropName: String", "- quantity: BigDecimal", "- basePrice: BigDecimal", "- currentHighestBid: BigDecimal", "- currentWinnerId: Long", "- startTime: LocalDateTime", "- endTime: LocalDateTime", "- status: ListingStatus"],
                   ["+ placeBid(Bid): Boolean", "+ closeAuction(): Long", "+ getWinner()"],
                   border_color='#EA580C', header_bg='#EA580C')

    draw_uml_class(ax, 0.41, 0.32, 0.18, 0.19, "Bid", "bidding-service",
                   ["- id: Long", "- listingId: Long", "- dealerId: Long", "- bidAmount: BigDecimal", "- status: BidStatus", "- bidTime: LocalDateTime"],
                   ["+ getBidAmount()", "+ markAsOutbid()", "+ markAsWon()"],
                   border_color='#EA580C', header_bg='#EA580C')

    draw_uml_class(ax, 0.41, 0.025, 0.18, 0.275, "Negotiation", "negotiation-service",
                   ["- id: Long", "- cropId: Long", "- buyerId: Long", "- sellerId: Long", "- quantity: BigDecimal", "- targetPrice: BigDecimal", "- agreedPrice: BigDecimal", "- cropName: String", "- status: NegotiationStatus", "- offers: List<Offer>"],
                   ["+ addCounterOffer()", "+ acceptOffer()", "+ rejectNegotiation()"],
                   border_color='#EA580C', header_bg='#EA580C')

    # 4. ORDER & SETTLEMENT DOMAIN
    draw_uml_class(ax, 0.61, 0.48, 0.18, 0.285, "Order", "order-service",
                   ["- id: Long", "- farmerId: Long", "- dealerId: Long", "- cropId: Long", "- cropName: String", "- quantity: Integer", "- unitPrice: BigDecimal", "- totalAmount: BigDecimal", "- status: OrderStatus", "- orderType: OrderType", "- createdAt: LocalDateTime"],
                   ["+ calculateTotal()", "+ confirmOrder()", "+ markAsShipped()", "+ markDelivered()", "+ cancelOrder()"],
                   border_color='#4F46E5', header_bg='#4F46E5')

    draw_uml_class(ax, 0.61, 0.26, 0.18, 0.20, "Payment", "payment-service",
                   ["- id: Long", "- orderId: Long", "- dealerId: Long", "- farmerId: Long", "- amount: BigDecimal", "- paymentMethod: String", "- status: PaymentStatus", "- transactionRef: String"],
                   ["+ processPayment()", "+ verifySuccess()", "+ initiateRefund()"],
                   border_color='#4F46E5', header_bg='#4F46E5')

    draw_uml_class(ax, 0.61, 0.025, 0.18, 0.215, "Invoice", "invoice-service",
                   ["- id: Long", "- invoiceNumber: String", "- orderId: Long", "- paymentId: String", "- farmerId: Long", "- dealerId: Long", "- subtotal: BigDecimal", "- taxAmount: BigDecimal", "- totalAmount: BigDecimal"],
                   ["+ generatePdfBill()", "+ computeGstTax()", "+ getInvoiceItems()"],
                   border_color='#4F46E5', header_bg='#4F46E5')

    # 5. LOGISTICS & ESCROW WALLET DOMAIN
    draw_uml_class(ax, 0.81, 0.53, 0.165, 0.235, "Delivery", "deliveryservice",
                   ["- id: Long", "- orderId: Long", "- deliveryAgentId: Long", "- pickupAddress: String", "- deliveryAddress: String", "- status: DeliveryStatus", "- deliveryOtp: String"],
                   ["+ assignAgent()", "+ updateStatus()", "+ verifyOtpAndComplete()"],
                   border_color='#D97706', header_bg='#D97706')

    draw_uml_class(ax, 0.81, 0.27, 0.165, 0.24, "Wallet", "wallet-service",
                   ["- id: Long", "- userId: Long", "- userRole: String", "- balance: BigDecimal", "- reservedBalance: BigDecimal", "- version: Long {optimistic}"],
                   ["+ creditBalance()", "+ debitBalance()", "+ reserveEscrow()", "+ releaseEscrow()"],
                   border_color='#D97706', header_bg='#D97706')

    draw_uml_class(ax, 0.81, 0.025, 0.165, 0.225, "Notification", "notification-service",
                   ["- id: Long", "- recipient: String", "- type: String", "- message: String", "- status: String", "- orderId: Long", "- createdAt: LocalDateTime"],
                   ["+ sendInApp()", "+ sendEmail()", "+ markAsRead()"],
                   border_color='#D97706', header_bg='#D97706')

    # -------------------------------------------------------------
    # UML CONNECTIONS & ASSOCIATIONS
    # -------------------------------------------------------------
    # Farmer -> Crop
    ax.annotate('', xy=(0.215, 0.64), xytext=(0.195, 0.40),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2, linestyle='-'), zorder=5)
    ax.text(0.20, 0.52, "1..* posts", fontsize=6, color='#64748B', zorder=5)

    # Crop -> BiddingListing
    ax.annotate('', xy=(0.41, 0.64), xytext=(0.39, 0.64),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2, linestyle='-'), zorder=5)
    ax.text(0.395, 0.65, "1", fontsize=6, color='#64748B', zorder=5)

    # BiddingListing -> Bid (Composition)
    ax.annotate('', xy=(0.50, 0.51), xytext=(0.50, 0.53),
                arrowprops=dict(arrowstyle="<|-", color='#EA580C', lw=1.5), zorder=5)
    ax.text(0.51, 0.52, "1..* bids", fontsize=6, color='#EA580C', zorder=5)

    # Order connects Payment, Invoice, Delivery
    ax.annotate('', xy=(0.70, 0.46), xytext=(0.70, 0.48),
                arrowprops=dict(arrowstyle="->", color='#4F46E5', lw=1.2), zorder=5)
    ax.text(0.705, 0.465, "1:1 payment", fontsize=5.8, color='#4F46E5', zorder=5)

    ax.annotate('', xy=(0.81, 0.62), xytext=(0.79, 0.62),
                arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.2), zorder=5)
    ax.text(0.792, 0.63, "1:1 delivery", fontsize=5.8, color='#D97706', zorder=5)

    plt.tight_layout()
    plt.savefig('D:\\cropdealnaresh\\doc_gen\\class_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Class diagram generated successfully!")

if __name__ == '__main__':
    generate_class_diagram()
