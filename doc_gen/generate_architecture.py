import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, PathPatch
import matplotlib.patches as mpatches

def draw_rounded_box(ax, x, y, w, h, bg_color, border_color, title, subtitle=None, badge=None, items=None, box_radius=0.015, title_color='#FFFFFF', header_bg=None):
    # Main body
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0,rounding_size={box_radius}",
                         facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=2)
    ax.add_patch(box)
    
    # Header bar if specified
    if header_bg:
        header_h = h * 0.28 if items else h * 0.4
        header_box = FancyBboxPatch((x, y + h - header_h), w, header_h,
                                    boxstyle=f"round,pad=0,rounding_size={box_radius}",
                                    facecolor=header_bg, edgecolor=border_color, linewidth=1.5, zorder=3)
        ax.add_patch(header_box)
        # Fix bottom corners of header
        rect = Rectangle((x, y + h - header_h), w, header_h * 0.4, facecolor=header_bg, edgecolor='none', zorder=3.5)
        ax.add_patch(rect)
    
    # Title
    t_y = y + h - (header_h * 0.5 if header_bg else h * 0.3)
    ax.text(x + w * 0.5, t_y, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=title_color, zorder=4)
    
    # Subtitle or badge
    curr_y = t_y - 0.02
    if subtitle:
        ax.text(x + w * 0.5, curr_y, subtitle, ha='center', va='center', fontsize=7.5, color='#ECEFF1' if header_bg else '#546E7A', zorder=4)
        curr_y -= 0.025
        
    if badge:
        b_box = FancyBboxPatch((x + w*0.5 - 0.035, curr_y - 0.01), 0.07, 0.02,
                               boxstyle="round,pad=0,rounding_size=0.005",
                               facecolor='#E8F5E9', edgecolor='#4CAF50', linewidth=0.8, zorder=4)
        ax.add_patch(b_box)
        ax.text(x + w * 0.5, curr_y, badge, ha='center', va='center', fontsize=6.5, fontweight='bold', color='#2E7D32', zorder=5)
        curr_y -= 0.025
        
    # Items list
    if items:
        item_y = y + (h - (header_h if header_bg else h*0.35)) * 0.8
        step = (h - (header_h if header_bg else h*0.35)) / (len(items) + 1)
        for idx, itm in enumerate(items):
            ax.text(x + 0.012, y + (len(items) - idx) * step * 0.85 + 0.01, f"• {itm}", ha='left', va='center', fontsize=7.2, color='#263238', zorder=4)

def generate_architecture():
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#F8FAFC')
    
    # Outer Border
    border = FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0,rounding_size=0.02",
                            facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=2, zorder=1)
    ax.add_patch(border)

    # Header Banner
    header = FancyBboxPatch((0.02, 0.91), 0.96, 0.07, boxstyle="round,pad=0,rounding_size=0.01",
                           facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.04, 0.955, "CROPDEAL MICROSERVICES PLATFORM", fontsize=16, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(0.04, 0.925, "System Architecture & Runtime Communication Topology | Spring Boot 3.3.13 • Spring Cloud 2023.0.6 • Docker Compose", fontsize=9.5, color='#94A3B8', zorder=3)
    
    # Metadata badges in header
    badges = ["Eureka Discovery", "Spring Cloud Gateway", "RabbitMQ Bus", "Distributed MySQL", "Angular 17 UI"]
    for i, b in enumerate(badges):
        bx = 0.58 + i * 0.078
        bb = FancyBboxPatch((bx, 0.93), 0.072, 0.03, boxstyle="round,pad=0,rounding_size=0.005",
                            facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1, zorder=3)
        ax.add_patch(bb)
        ax.text(bx + 0.036, 0.945, b, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#38BDF8', zorder=4)

    # -------------------------------------------------------------
    # 1. CLIENT LAYER (Top)
    # -------------------------------------------------------------
    client_group = FancyBboxPatch((0.03, 0.79), 0.94, 0.10, boxstyle="round,pad=0,rounding_size=0.01",
                                 facecolor='#F1F5F9', edgecolor='#94A3B8', linewidth=1.2, linestyle='--', zorder=2)
    ax.add_patch(client_group)
    ax.text(0.04, 0.875, "1. PRESENTATION & CLIENT CONSUMER LAYER", fontsize=10, fontweight='bold', color='#334155', zorder=3)
    
    clients = [
        ("Farmer Portal (Angular)", "Crop catalog, bids review, negotiations", ":4200/farmer", '#0284C7'),
        ("Dealer Portal (Angular)", "Browse crops, live auctions, payments", ":4200/dealer", '#0284C7'),
        ("Delivery App (Mobile/Web)", "Order dispatch, OTP delivery proof", ":4200/delivery", '#0284C7'),
        ("Admin Console (Angular)", "Platform audit, user KYC, reports", ":4200/admin", '#0284C7'),
        ("Swagger UI Docs", "OpenAPI aggregated interactive console", ":8080/swagger-ui.html", '#0D9488')
    ]
    for i, (title, sub, port, col) in enumerate(clients):
        cx = 0.04 + i * 0.185
        draw_rounded_box(ax, cx, 0.805, 0.175, 0.065, '#FFFFFF', col, title, sub, badge=port, box_radius=0.008, title_color='#0F172A')

    # Arrow from Clients to API Gateway
    ax.annotate('', xy=(0.50, 0.74), xytext=(0.50, 0.80),
                arrowprops=dict(arrowstyle="-|>", color='#0284C7', lw=2.5, mutation_scale=15), zorder=5)
    ax.text(0.51, 0.765, "HTTPS / REST (Single Entry Point)", fontsize=8, fontweight='bold', color='#0284C7', zorder=5)

    # -------------------------------------------------------------
    # 2. EDGE GATEWAY & INFRASTRUCTURE GOVERNANCE LAYER
    # -------------------------------------------------------------
    infra_group = FancyBboxPatch((0.03, 0.62), 0.94, 0.155, boxstyle="round,pad=0,rounding_size=0.01",
                                facecolor='#EFF6FF', edgecolor='#BFDBFE', linewidth=1.2, zorder=2)
    ax.add_patch(infra_group)
    ax.text(0.04, 0.755, "2. EDGE GATEWAY & SERVICE GOVERNANCE INFRASTRUCTURE", fontsize=10, fontweight='bold', color='#1E40AF', zorder=3)

    # API Gateway Box (Wide)
    gw_box = FancyBboxPatch((0.04, 0.635), 0.44, 0.105, boxstyle="round,pad=0,rounding_size=0.01",
                            facecolor='#FFFFFF', edgecolor='#2563EB', linewidth=2, zorder=3)
    ax.add_patch(gw_box)
    # Header of Gateway
    gw_hdr = FancyBboxPatch((0.04, 0.705), 0.44, 0.035, boxstyle="round,pad=0,rounding_size=0.01",
                            facecolor='#1E40AF', edgecolor='#2563EB', linewidth=1.5, zorder=3.5)
    ax.add_patch(gw_hdr)
    ax.text(0.26, 0.722, "SPRING CLOUD API GATEWAY (Port 8080)", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF', zorder=4)
    
    gw_features = [
        "Dynamic lb:// Service Routing",
        "JWT Security & Token Verification",
        "OpenAPI Docs Aggregation Hub",
        "CORS & Rate Limiting Filter"
    ]
    for idx, f in enumerate(gw_features):
        col_idx = idx % 2
        row_idx = idx // 2
        fx = 0.055 + col_idx * 0.21
        fy = 0.68 - row_idx * 0.032
        fb = FancyBboxPatch((fx, fy - 0.012), 0.195, 0.024, boxstyle="round,pad=0,rounding_size=0.004",
                            facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1, zorder=4)
        ax.add_patch(fb)
        ax.text(fx + 0.01, fy, f"✔ {f}", va='center', fontsize=7.2, color='#334155', zorder=5)

    # Eureka Server Box
    draw_rounded_box(ax, 0.51, 0.635, 0.22, 0.105, '#FFFFFF', '#059669', "EUREKA SERVICE DISCOVERY",
                     subtitle="Spring Cloud Netflix (Port 8761)",
                     badge="DYNAMIC REGISTRY",
                     items=["Client-Side Round-Robin LB", "Real-time Heartbeat Monitor", "Auto-Registration of 15 Services"],
                     box_radius=0.01, title_color='#FFFFFF', header_bg='#059669')

    # Config Server Box
    draw_rounded_box(ax, 0.75, 0.635, 0.21, 0.105, '#FFFFFF', '#7C3AED', "CONFIG SERVER",
                     subtitle="Spring Cloud Config (Port 8888)",
                     badge="100% CENTRALIZED CONFIG",
                     items=["Git/File Property Storage", "Runtime Environment Profiles", "Single Source of Truth"],
                     box_radius=0.01, title_color='#FFFFFF', header_bg='#7C3AED')

    # Arrows between Gateway, Eureka, Config Server
    ax.annotate('', xy=(0.51, 0.68), xytext=(0.48, 0.68),
                arrowprops=dict(arrowstyle="<|-|>", color='#059669', lw=2, mutation_scale=12), zorder=5)
    ax.text(0.482, 0.695, "Registry\nLookup", ha='center', fontsize=6.8, fontweight='bold', color='#059669', zorder=5)

    ax.annotate('', xy=(0.75, 0.68), xytext=(0.73, 0.68),
                arrowprops=dict(arrowstyle="<|-", color='#7C3AED', lw=1.5, mutation_scale=10), zorder=5)

    # -------------------------------------------------------------
    # 3. CORE BUSINESS MICROSERVICES DOMAIN LAYER
    # -------------------------------------------------------------
    services_group = FancyBboxPatch((0.03, 0.25), 0.94, 0.355, boxstyle="round,pad=0,rounding_size=0.01",
                                    facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.5, zorder=2)
    ax.add_patch(services_group)
    ax.text(0.04, 0.585, "3. BUSINESS MICROSERVICES DOMAIN MESH (15 DEDICATED DOMAINS)", fontsize=10, fontweight='bold', color='#0F172A', zorder=3)

    # Functional Domain Columns/Boxes
    domains = [
        # (title, color, x, y, w, h, services_list)
        ("IDENTITY & USERS", "#0284C7", 0.04, 0.265, 0.14, 0.305, [
            ("auth-service", ":8081", ["JWT Token Provider", "Role Auth (Farmer/Dealer)", "OAuth2 Google Login"]),
            ("user-service", ":8082", ["Farmer & Dealer Profiles", "Delivery Partner KYC", "Farmer Rating/Reviews"])
        ]),
        ("CATALOG & MARKET PRICING", "#16A34A", 0.19, 0.265, 0.18, 0.305, [
            ("crop-service", ":8083", ["Crop Postings & Units", "Status: Active/Sold", "Crop Subscriptions"]),
            ("price-service", ":8084", ["Mandi Market Prices", "Live MSP Benchmark", "Historical Trend Sync"]),
            ("price-alert-service", ":8094", ["Dealer Buying Requests", "Target Price Watcher", "Threshold Alerts"])
        ]),
        ("B2B TRADE & AUCTIONS", "#EA580C", 0.38, 0.265, 0.18, 0.305, [
            ("bidding-service", ":8086", ["Live Auction Listings", "Real-time Bid Engine", "Highest Bid Winner"]),
            ("negotiation-service", ":8085", ["Farmer-Dealer Chat/Offer", "Counter-Offer Engine", "Agreed Price Contract"])
        ]),
        ("ORDER EXECUTION & FINANCE", "#4F46E5", 0.57, 0.265, 0.19, 0.305, [
            ("order-service", ":8088", ["Direct/Bid/Neg Orders", "Order State Machine", "Cancel/Refund Hook"]),
            ("payment-service", ":8089", ["Gateway/Wallet Interop", "Transaction Audit", "Refund Management"]),
            ("wallet-service", ":8087", ["Escrow Fund Hold/Release", "Balance Credit/Debit", "Double-Spend Guard"]),
            ("invoice-service", ":8090", ["Automated Tax/GST Calc", "Itemized Line Items", "PDF Bill Generator"])
        ]),
        ("LOGISTICS & INTELLIGENCE", "#D97706", 0.77, 0.265, 0.19, 0.305, [
            ("delivery-service", ":8091", ["Delivery Assignment", "OTP Proof of Delivery", "Driver Status Updates"]),
            ("notification-service", ":8092", ["RabbitMQ Consumer", "In-App/Email/SMS Alerts", "Order/Bid Dispatcher"]),
            ("chatbot-service", ":8096", ["Advisory AI Assistant", "Crop Query Resolution"]),
            ("report-service", ":8095", ["Revenue & Sales Analytics", "Performance Reports"])
        ])
    ]

    for d_title, d_col, dx, dy, dw, dh, svc_list in domains:
        # Domain container
        d_box = FancyBboxPatch((dx, dy), dw, dh, boxstyle="round,pad=0,rounding_size=0.008",
                               facecolor='#FFFFFF', edgecolor=d_col, linewidth=1.5, zorder=3)
        ax.add_patch(d_box)
        # Domain Header
        dh_box = FancyBboxPatch((dx, dy + dh - 0.03), dw, 0.03, boxstyle="round,pad=0,rounding_size=0.008",
                                facecolor=d_col, edgecolor=d_col, linewidth=1, zorder=3.5)
        ax.add_patch(dh_box)
        ax.text(dx + dw*0.5, dy + dh - 0.015, d_title, ha='center', va='center', fontsize=7.8, fontweight='bold', color='#FFFFFF', zorder=4)

        # Microservice Cards inside domain
        n_svc = len(svc_list)
        card_h = (dh - 0.045) / n_svc
        for s_idx, (s_name, s_port, s_items) in enumerate(svc_list):
            sy = dy + dh - 0.038 - (s_idx + 1) * card_h + 0.005
            sc_box = FancyBboxPatch((dx + 0.006, sy), dw - 0.012, card_h - 0.008, boxstyle="round,pad=0,rounding_size=0.005",
                                    facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1, zorder=4)
            ax.add_patch(sc_box)
            ax.text(dx + 0.012, sy + card_h - 0.018, s_name, fontsize=7.5, fontweight='bold', color='#0F172A', zorder=5)
            ax.text(dx + dw - 0.015, sy + card_h - 0.018, s_port, ha='right', fontsize=6.8, fontweight='bold', color=d_col, zorder=5)
            for itm_idx, itm in enumerate(s_items[:2]):
                ax.text(dx + 0.012, sy + card_h - 0.028 - itm_idx * 0.011, f"• {itm}", fontsize=6.2, color='#475569', zorder=5)

    # Arrow from Gateway down to Microservices
    ax.annotate('', xy=(0.26, 0.57), xytext=(0.26, 0.635),
                arrowprops=dict(arrowstyle="-|>", color='#2563EB', lw=2.5, mutation_scale=15), zorder=5)
    ax.text(0.27, 0.605, "lb://service-id (Load Balanced REST)", fontsize=7.5, fontweight='bold', color='#2563EB', zorder=5)

    # -------------------------------------------------------------
    # 4. ASYNCHRONOUS MESSAGING BUS (RabbitMQ)
    # -------------------------------------------------------------
    event_group = FancyBboxPatch((0.03, 0.13), 0.94, 0.105, boxstyle="round,pad=0,rounding_size=0.01",
                                 facecolor='#FFF7ED', edgecolor='#FDBA74', linewidth=1.5, zorder=2)
    ax.add_patch(event_group)
    ax.text(0.04, 0.218, "4. ASYNCHRONOUS EVENT-DRIVEN MESSAGING BACKBONE (RabbitMQ Broker :5672 / :15672)", fontsize=9.5, fontweight='bold', color='#C2410C', zorder=3)

    # Exchange Box
    draw_rounded_box(ax, 0.04, 0.142, 0.22, 0.068, '#FFFFFF', '#EA580C', "cropdeal.exchange",
                     subtitle="Direct & Topic Exchanges", badge="AMQP BROKER", box_radius=0.008, title_color='#FFFFFF', header_bg='#EA580C')

    # Queues Box
    queues = [
        ("notification.queue", "Real-time push, email, SMS notifications"),
        ("price.alert.queue", "Price matches against farmer crop postings"),
        ("order.events.queue", "Order placement, payment success, fulfillment"),
        ("delivery.status.queue", "Driver dispatch & real-time delivery status updates")
    ]
    for q_idx, (q_name, q_desc) in enumerate(queues):
        qx = 0.28 + q_idx * 0.17
        qb = FancyBboxPatch((qx, 0.142), 0.16, 0.068, boxstyle="round,pad=0,rounding_size=0.006",
                            facecolor='#FFFFFF', edgecolor='#FB923C', linewidth=1.2, zorder=3)
        ax.add_patch(qb)
        ax.text(qx + 0.08, 0.192, q_name, ha='center', fontsize=7.5, fontweight='bold', color='#C2410C', zorder=4)
        ax.text(qx + 0.08, 0.162, q_desc, ha='center', fontsize=6.2, color='#64748B', wrap=True, zorder=4)

    # Arrows Microservices <--> RabbitMQ
    ax.annotate('', xy=(0.15, 0.21), xytext=(0.28, 0.265),
                arrowprops=dict(arrowstyle="-|>", color='#EA580C', lw=1.8, mutation_scale=12), zorder=5)
    ax.text(0.20, 0.23, "Publish Events", fontsize=6.8, fontweight='bold', color='#EA580C', zorder=5)

    ax.annotate('', xy=(0.86, 0.265), xytext=(0.75, 0.21),
                arrowprops=dict(arrowstyle="-|>", color='#EA580C', lw=1.8, mutation_scale=12), zorder=5)
    ax.text(0.81, 0.23, "Consume Events", fontsize=6.8, fontweight='bold', color='#EA580C', zorder=5)

    # -------------------------------------------------------------
    # 5. DATA PERSISTENCE LAYER (MySQL)
    # -------------------------------------------------------------
    db_group = FancyBboxPatch((0.03, 0.025), 0.94, 0.09, boxstyle="round,pad=0,rounding_size=0.01",
                              facecolor='#F0FDF4', edgecolor='#BBF7D0', linewidth=1.2, zorder=2)
    ax.add_patch(db_group)
    ax.text(0.04, 0.098, "5. RELATIONAL DATA PERSISTENCE LAYER (Containerized MySQL Database Engine :3306)", fontsize=9.5, fontweight='bold', color='#166534', zorder=3)

    db_schemas = [
        ("auth_db", "Users, Roles, Providers", '#166534'),
        ("user_db", "Farmers, Dealers, KYC", '#166534'),
        ("crop_db", "Crops, Varieties, Units", '#166534'),
        ("bidding_db", "Listings, Bids, Rules", '#166534'),
        ("negotiation_db", "Offers, Counter-Offers", '#166534'),
        ("order_db", "Orders, Status Machine", '#166534'),
        ("payment_db", "Payments, Refunds", '#166534'),
        ("wallet_db", "Balances, Escrow Holds", '#166534'),
        ("invoice_db", "Invoices, Tax Items", '#166534'),
        ("delivery_db", "Deliveries, Fleet Tracking", '#166534')
    ]
    for db_idx, (schema_name, desc, col) in enumerate(db_schemas):
        dbx = 0.04 + db_idx * 0.092
        db_box = FancyBboxPatch((dbx, 0.035), 0.086, 0.052, boxstyle="round,pad=0,rounding_size=0.005",
                                facecolor='#FFFFFF', edgecolor=col, linewidth=1.2, zorder=3)
        ax.add_patch(db_box)
        # Cylinder top indicator
        cyl = FancyBboxPatch((dbx + 0.005, 0.072), 0.076, 0.01, boxstyle="round,pad=0,rounding_size=0.003",
                             facecolor='#DCFCE7', edgecolor=col, linewidth=0.8, zorder=4)
        ax.add_patch(cyl)
        ax.text(dbx + 0.043, 0.058, schema_name, ha='center', fontsize=7.2, fontweight='bold', color='#14532D', zorder=5)
        ax.text(dbx + 0.043, 0.042, desc, ha='center', fontsize=5.8, color='#64748B', zorder=5)

    plt.tight_layout()
    plt.savefig('D:\\cropdealnaresh\\doc_gen\\architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Architecture diagram generated successfully!")

if __name__ == '__main__':
    generate_architecture()
