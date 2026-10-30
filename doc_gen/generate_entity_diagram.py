import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.patches as mpatches

def draw_er_table(ax, x, y, w, h, table_name, columns, header_bg='#0F172A', border_color='#1E293B', category="ENTITY"):
    # Outer container
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.006",
                         facecolor='#FFFFFF', edgecolor=border_color, linewidth=1.2, zorder=3)
    ax.add_patch(box)

    # Header
    hdr_h = 0.024
    hdr_box = FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="round,pad=0,rounding_size=0.006",
                            facecolor=header_bg, edgecolor=border_color, linewidth=1, zorder=3.5)
    ax.add_patch(hdr_box)
    rect = Rectangle((x, y + h - hdr_h), w, hdr_h * 0.4, facecolor=header_bg, edgecolor='none', zorder=3.8)
    ax.add_patch(rect)

    ax.text(x + w * 0.5, y + h - 0.012, table_name.upper(), ha='center', va='center', fontsize=7.2, fontweight='bold', color='#FFFFFF', zorder=4)

    # Columns
    curr_y = y + h - hdr_h - 0.010
    row_h = (h - hdr_h - 0.008) / len(columns)
    
    for idx, (col_name, col_type, key_type) in enumerate(columns):
        cy = y + h - hdr_h - 0.008 - (idx + 0.5) * row_h
        # Key badge
        if key_type == 'PK':
            k_col = '#B91C1C'
            k_bg = '#FEE2E2'
        elif key_type == 'FK':
            k_col = '#1D4ED8'
            k_bg = '#DBEAFE'
        else:
            k_col = '#64748B'
            k_bg = '#F1F5F9'

        # Key label
        if key_type:
            ax.text(x + 0.006, cy, key_type, ha='left', va='center', fontsize=5.0, fontweight='bold', color=k_col, zorder=4)
        
        # Column name
        ax.text(x + 0.022, cy, col_name, ha='left', va='center', fontsize=5.8, color='#0F172A', fontfamily='monospace', zorder=4)
        # Column type
        ax.text(x + w - 0.006, cy, col_type, ha='right', va='center', fontsize=5.2, color='#64748B', fontfamily='monospace', zorder=4)

        # Subtle zebra striping
        if idx % 2 == 1:
            bg_strip = Rectangle((x + 0.002, cy - row_h*0.48), w - 0.004, row_h*0.96, facecolor='#F8FAFC', edgecolor='none', zorder=2.5)
            ax.add_patch(bg_strip)

def generate_entity_diagram():
    fig, ax = plt.subplots(figsize=(24, 16), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#F8FAFC')
    outer_border = FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0,rounding_size=0.015",
                                 facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=2, zorder=1)
    ax.add_patch(outer_border)

    # Header Banner
    header = FancyBboxPatch((0.02, 0.93), 0.96, 0.055, boxstyle="round,pad=0,rounding_size=0.008",
                           facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.04, 0.963, "CROPDEAL RELATIONAL DATABASE ENTITY SPECIFICATIONS (ER DIAGRAM)", fontsize=15, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(0.04, 0.942, "Entity Schemas, Relational Primary/Foreign Keys, Data Typing & Cardinalities Across Distributed Microservice Schemas", fontsize=9, color='#94A3B8', zorder=3)

    # Legend in header
    l_types = [("PK", "Primary Key", '#B91C1C'), ("FK", "Foreign Key", '#1D4ED8'), ("1:N", "One-to-Many", '#0F172A'), ("1:1", "One-to-One", '#059669')]
    for l_idx, (tag, desc, col) in enumerate(l_types):
        lx = 0.70 + l_idx * 0.07
        ax.text(lx, 0.952, f"[{tag}] {desc}", fontsize=7.2, fontweight='bold', color=col, zorder=4)

    # -------------------------------------------------------------
    # TABLES BY BUSINESS DOMAIN
    # -------------------------------------------------------------

    # COLUMN 1: USERS & PROFILES (x = 0.025)
    draw_er_table(ax, 0.025, 0.73, 0.165, 0.175, "users", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("email", "VARCHAR(255)", ""),
        ("username", "VARCHAR(100)", ""),
        ("password", "VARCHAR(255)", ""),
        ("role", "ENUM(FARMER..)", ""),
        ("status", "VARCHAR(50)", ""),
        ("auth_provider", "VARCHAR(50)", ""),
        ("created_at", "DATETIME", "")
    ], header_bg='#0284C7', border_color='#0284C7')

    draw_er_table(ax, 0.025, 0.51, 0.165, 0.19, "farmers", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("user_id", "BIGINT NOT NULL", "FK"),
        ("name", "VARCHAR(150)", ""),
        ("phone", "VARCHAR(20)", ""),
        ("address", "VARCHAR(255)", ""),
        ("farm_location", "VARCHAR(255)", ""),
        ("bank_details", "TEXT", ""),
        ("average_rating", "DOUBLE DEFAULT 0", ""),
        ("created_at", "DATETIME", "")
    ], header_bg='#0284C7', border_color='#0284C7')

    draw_er_table(ax, 0.025, 0.29, 0.165, 0.19, "dealers", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("user_id", "BIGINT NOT NULL", "FK"),
        ("name", "VARCHAR(150)", ""),
        ("phone", "VARCHAR(20)", ""),
        ("business_name", "VARCHAR(200)", ""),
        ("address", "VARCHAR(255)", ""),
        ("bank_details", "TEXT", ""),
        ("created_at", "DATETIME", "")
    ], header_bg='#0284C7', border_color='#0284C7')

    draw_er_table(ax, 0.025, 0.065, 0.165, 0.195, "delivery_partners", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("user_id", "BIGINT NOT NULL", "FK"),
        ("name", "VARCHAR(150)", ""),
        ("phone", "VARCHAR(20)", ""),
        ("vehicle_number", "VARCHAR(50)", ""),
        ("vehicle_type", "VARCHAR(50)", ""),
        ("driving_license", "VARCHAR(100)", ""),
        ("status", "VARCHAR(30)", "")
    ], header_bg='#0284C7', border_color='#0284C7')

    # COLUMN 2: CROPS, SUBSCRIPTIONS & MARKET PRICES (x = 0.215)
    draw_er_table(ax, 0.215, 0.67, 0.175, 0.235, "crops", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("farmer_id", "BIGINT NOT NULL", "FK"),
        ("commodity", "VARCHAR(100)", ""),
        ("state", "VARCHAR(100)", ""),
        ("district", "VARCHAR(100)", ""),
        ("grade", "VARCHAR(50)", ""),
        ("quantity", "DECIMAL(12,2)", ""),
        ("unit", "VARCHAR(20)", ""),
        ("price_per_unit", "DECIMAL(12,2)", ""),
        ("status", "VARCHAR(30)", ""),
        ("created_at", "DATETIME", "")
    ], header_bg='#16A34A', border_color='#16A34A')

    draw_er_table(ax, 0.215, 0.44, 0.175, 0.20, "crop_subscriptions", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("subscriber_id", "BIGINT NOT NULL", "FK"),
        ("commodity", "VARCHAR(100)", ""),
        ("state", "VARCHAR(100)", ""),
        ("district", "VARCHAR(100)", ""),
        ("grade", "VARCHAR(50)", ""),
        ("subscribed_at", "DATETIME", "")
    ], header_bg='#16A34A', border_color='#16A34A')

    draw_er_table(ax, 0.215, 0.19, 0.175, 0.22, "market_prices", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("state", "VARCHAR(100)", ""),
        ("district", "VARCHAR(100)", ""),
        ("market", "VARCHAR(150)", ""),
        ("commodity", "VARCHAR(100)", ""),
        ("variety", "VARCHAR(100)", ""),
        ("grade", "VARCHAR(50)", ""),
        ("min_price", "DECIMAL(10,2)", ""),
        ("max_price", "DECIMAL(10,2)", ""),
        ("modal_price", "DECIMAL(10,2)", ""),
        ("arrival_date", "DATE", "")
    ], header_bg='#16A34A', border_color='#16A34A')

    # COLUMN 3: BIDDING & AUCTIONS + NEGOTIATIONS (x = 0.415)
    draw_er_table(ax, 0.415, 0.69, 0.175, 0.215, "bidding_listings", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("crop_id", "BIGINT NOT NULL", "FK"),
        ("farmer_id", "BIGINT NOT NULL", "FK"),
        ("crop_name", "VARCHAR(100)", ""),
        ("quantity", "DECIMAL(12,2)", ""),
        ("base_price", "DECIMAL(12,2)", ""),
        ("current_highest_bid", "DECIMAL(12,2)", ""),
        ("current_winner_id", "BIGINT", "FK"),
        ("start_time", "DATETIME", ""),
        ("end_time", "DATETIME", ""),
        ("status", "VARCHAR(30)", "")
    ], header_bg='#EA580C', border_color='#EA580C')

    draw_er_table(ax, 0.415, 0.47, 0.175, 0.19, "bids", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("listing_id", "BIGINT NOT NULL", "FK"),
        ("dealer_id", "BIGINT NOT NULL", "FK"),
        ("bid_amount", "DECIMAL(12,2)", ""),
        ("status", "VARCHAR(30)", ""),
        ("bid_time", "DATETIME", "")
    ], header_bg='#EA580C', border_color='#EA580C')

    draw_er_table(ax, 0.415, 0.23, 0.175, 0.21, "negotiations", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("crop_id", "BIGINT NOT NULL", "FK"),
        ("buyer_id", "BIGINT NOT NULL", "FK"),
        ("seller_id", "BIGINT NOT NULL", "FK"),
        ("crop_name", "VARCHAR(100)", ""),
        ("quantity", "DECIMAL(12,2)", ""),
        ("target_price", "DECIMAL(12,2)", ""),
        ("agreed_price", "DECIMAL(12,2)", ""),
        ("status", "VARCHAR(30)", "")
    ], header_bg='#EA580C', border_color='#EA580C')

    draw_er_table(ax, 0.415, 0.04, 0.175, 0.165, "negotiation_offers", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("negotiation_id", "BIGINT NOT NULL", "FK"),
        ("offered_by_user_id", "BIGINT NOT NULL", "FK"),
        ("amount", "DECIMAL(12,2)", ""),
        ("message", "VARCHAR(255)", ""),
        ("status", "VARCHAR(30)", ""),
        ("created_at", "DATETIME", "")
    ], header_bg='#EA580C', border_color='#EA580C')

    # COLUMN 4: ORDERS, PAYMENTS & INVOICES (x = 0.615)
    draw_er_table(ax, 0.615, 0.67, 0.175, 0.235, "orders", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("farmer_id", "BIGINT NOT NULL", "FK"),
        ("dealer_id", "BIGINT NOT NULL", "FK"),
        ("crop_id", "BIGINT NOT NULL", "FK"),
        ("crop_name", "VARCHAR(100)", ""),
        ("quantity", "INT NOT NULL", ""),
        ("unit_price", "DECIMAL(12,2)", ""),
        ("total_amount", "DECIMAL(12,2)", ""),
        ("status", "VARCHAR(30)", ""),
        ("order_type", "VARCHAR(30)", ""),
        ("created_at", "DATETIME", "")
    ], header_bg='#4F46E5', border_color='#4F46E5')

    draw_er_table(ax, 0.615, 0.44, 0.175, 0.20, "payments", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("order_id", "BIGINT NOT NULL", "FK"),
        ("dealer_id", "BIGINT NOT NULL", "FK"),
        ("farmer_id", "BIGINT NOT NULL", "FK"),
        ("amount", "DECIMAL(12,2)", ""),
        ("payment_method", "VARCHAR(50)", ""),
        ("status", "VARCHAR(30)", ""),
        ("transaction_ref", "VARCHAR(100)", "")
    ], header_bg='#4F46E5', border_color='#4F46E5')

    draw_er_table(ax, 0.615, 0.23, 0.175, 0.18, "invoices", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("invoice_number", "VARCHAR(100)", ""),
        ("order_id", "BIGINT NOT NULL", "FK"),
        ("payment_id", "VARCHAR(100)", ""),
        ("farmer_id", "BIGINT NOT NULL", "FK"),
        ("dealer_id", "BIGINT NOT NULL", "FK"),
        ("subtotal", "DECIMAL(12,2)", ""),
        ("tax_amount", "DECIMAL(12,2)", ""),
        ("total_amount", "DECIMAL(12,2)", "")
    ], header_bg='#4F46E5', border_color='#4F46E5')

    draw_er_table(ax, 0.615, 0.04, 0.175, 0.165, "farmer_reviews", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("farmer_id", "BIGINT NOT NULL", "FK"),
        ("dealer_id", "BIGINT NOT NULL", "FK"),
        ("order_id", "BIGINT NOT NULL", "FK"),
        ("rating", "INT CHECK(1..5)", ""),
        ("comment", "TEXT", ""),
        ("created_at", "DATETIME", "")
    ], header_bg='#4F46E5', border_color='#4F46E5')

    # COLUMN 5: DELIVERIES, WALLET & NOTIFICATIONS (x = 0.815)
    draw_er_table(ax, 0.815, 0.73, 0.165, 0.175, "deliveries", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("order_id", "BIGINT NOT NULL", "FK"),
        ("delivery_agent_id", "BIGINT", "FK"),
        ("pickup_address", "VARCHAR(255)", ""),
        ("delivery_address", "VARCHAR(255)", ""),
        ("status", "VARCHAR(30)", ""),
        ("delivery_otp", "VARCHAR(10)", "")
    ], header_bg='#D97706', border_color='#D97706')

    draw_er_table(ax, 0.815, 0.52, 0.165, 0.18, "wallets", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("user_id", "BIGINT NOT NULL", "FK"),
        ("user_role", "VARCHAR(30)", ""),
        ("balance", "DECIMAL(12,2)", ""),
        ("reserved_balance", "DECIMAL(12,2)", ""),
        ("version", "BIGINT NOT NULL", ""),
        ("updated_at", "DATETIME", "")
    ], header_bg='#D97706', border_color='#D97706')

    draw_er_table(ax, 0.815, 0.31, 0.165, 0.18, "wallet_transactions", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("wallet_id", "BIGINT NOT NULL", "FK"),
        ("user_id", "BIGINT NOT NULL", "FK"),
        ("amount", "DECIMAL(12,2)", ""),
        ("type", "VARCHAR(30)", ""),
        ("reference_id", "VARCHAR(100)", ""),
        ("transaction_time", "DATETIME", "")
    ], header_bg='#D97706', border_color='#D97706')

    draw_er_table(ax, 0.815, 0.08, 0.165, 0.20, "notifications", [
        ("id", "BIGINT AUTO_INC", "PK"),
        ("recipient", "VARCHAR(100)", ""),
        ("type", "VARCHAR(50)", ""),
        ("message", "TEXT", ""),
        ("status", "VARCHAR(30)", ""),
        ("order_id", "BIGINT", "FK"),
        ("created_at", "DATETIME", "")
    ], header_bg='#D97706', border_color='#D97706')

    # -------------------------------------------------------------
    # RELATIONSHIP CONNECTORS (Cleanly routed)
    # -------------------------------------------------------------
    # users -> farmers (1:1)
    ax.annotate('', xy=(0.107, 0.70), xytext=(0.107, 0.73),
                arrowprops=dict(arrowstyle="->", color='#0284C7', lw=1.2), zorder=5)
    ax.text(0.113, 0.712, "1:1", fontsize=6, fontweight='bold', color='#0284C7', zorder=5)

    # farmers -> crops (1:N)
    ax.annotate('', xy=(0.215, 0.78), xytext=(0.190, 0.60),
                arrowprops=dict(arrowstyle="->", color='#16A34A', lw=1.2), zorder=5)
    ax.text(0.195, 0.70, "1:N", fontsize=6, fontweight='bold', color='#16A34A', zorder=5)

    # crops -> bidding_listings (1:N)
    ax.annotate('', xy=(0.415, 0.78), xytext=(0.390, 0.78),
                arrowprops=dict(arrowstyle="->", color='#EA580C', lw=1.2), zorder=5)
    ax.text(0.395, 0.79, "1:N", fontsize=6, fontweight='bold', color='#EA580C', zorder=5)

    # bidding_listings -> bids (1:N)
    ax.annotate('', xy=(0.502, 0.66), xytext=(0.502, 0.69),
                arrowprops=dict(arrowstyle="->", color='#EA580C', lw=1.2), zorder=5)
    ax.text(0.508, 0.672, "1:N", fontsize=6, fontweight='bold', color='#EA580C', zorder=5)

    # crops -> negotiations (1:N)
    ax.annotate('', xy=(0.415, 0.33), xytext=(0.390, 0.67),
                arrowprops=dict(arrowstyle="->", color='#EA580C', lw=1.2), zorder=5)
    ax.text(0.395, 0.48, "1:N", fontsize=6, fontweight='bold', color='#EA580C', zorder=5)

    # crops -> orders (1:N)
    ax.annotate('', xy=(0.615, 0.78), xytext=(0.390, 0.78),
                arrowprops=dict(arrowstyle="->", color='#4F46E5', lw=1.2, linestyle='--'), zorder=5)
    ax.text(0.595, 0.79, "1:N", fontsize=6, fontweight='bold', color='#4F46E5', zorder=5)

    # orders -> payments (1:1)
    ax.annotate('', xy=(0.702, 0.64), xytext=(0.702, 0.67),
                arrowprops=dict(arrowstyle="->", color='#4F46E5', lw=1.2), zorder=5)
    ax.text(0.708, 0.652, "1:1", fontsize=6, fontweight='bold', color='#4F46E5', zorder=5)

    # orders -> invoices (1:1)
    ax.annotate('', xy=(0.702, 0.41), xytext=(0.702, 0.44),
                arrowprops=dict(arrowstyle="->", color='#4F46E5', lw=1.2), zorder=5)
    ax.text(0.708, 0.422, "1:1", fontsize=6, fontweight='bold', color='#4F46E5', zorder=5)

    # orders -> deliveries (1:1)
    ax.annotate('', xy=(0.815, 0.81), xytext=(0.790, 0.81),
                arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.2), zorder=5)
    ax.text(0.795, 0.82, "1:1", fontsize=6, fontweight='bold', color='#D97706', zorder=5)

    # wallets -> wallet_transactions (1:N)
    ax.annotate('', xy=(0.897, 0.49), xytext=(0.897, 0.52),
                arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.2), zorder=5)
    ax.text(0.903, 0.502, "1:N", fontsize=6, fontweight='bold', color='#D97706', zorder=5)

    plt.tight_layout()
    plt.savefig('D:\\cropdealnaresh\\doc_gen\\entity_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Entity diagram generated successfully!")

if __name__ == '__main__':
    generate_entity_diagram()
