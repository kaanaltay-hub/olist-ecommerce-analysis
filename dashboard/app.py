from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# DARK THEME CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0D1B2A;
}

/* Sidebar — LOCKED OPEN, always visible, fixed width */
[data-testid="stSidebar"] {
    background-color: #1B263B !important;
    border-right: 1px solid #2E4057 !important;
    min-width: 218px !important;
    max-width: 218px !important;
    width: 218px !important;
    transform: none !important;
    margin-left: 0 !important;
    left: 0 !important;
    display: block !important;
    visibility: visible !important;
    position: relative !important;
}
/* Override Streamlit's collapse state entirely — no matter aria-expanded value */
[data-testid="stSidebar"][aria-expanded="false"],
[data-testid="stSidebar"][aria-expanded="true"] {
    min-width: 218px !important;
    max-width: 218px !important;
    width: 218px !important;
    transform: none !important;
    margin-left: 0 !important;
}
[data-testid="stSidebar"] > div {
    transform: none !important;
    margin-left: 0 !important;
    width: 218px !important;
}
[data-testid="stSidebar"] * {
    color: #c9d5e5 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #e5edf8 !important;
}

/* Sidebar - no scroll, compact fit */
[data-testid="stSidebar"] > div:first-child {
    overflow: hidden !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
}
[data-testid="stSidebar"] > div:first-child > div:first-child {
    overflow-y: hidden !important;
    flex: 1 !important;
    padding-bottom: 4px !important;
}
/* Compact radio options */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    padding-top: 2px !important;
    padding-bottom: 2px !important;
    font-size: 0.79rem !important;
    line-height: 1.3 !important;
}
[data-testid="stSidebar"] .stRadio {
    margin-bottom: 2px !important;
}
/* Constrain multiselect tag boxes to prevent overflow */
[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"] > div:first-child {
    max-height: 58px !important;
    overflow-y: auto !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    font-size: 0.60rem !important;
    padding: 0px 4px !important;
    height: 17px !important;
    line-height: 17px !important;
    margin: 1px !important;
}
[data-testid="stSidebar"] .stMultiSelect {
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {
    margin-bottom: 2px !important;
    font-size: 0.76rem !important;
}
/* Compact date input */
[data-testid="stSidebar"] [data-testid="stDateInput"] {
    margin-bottom: 0px !important;
}

/* ============================================================
   SIDEBAR TOGGLE BUTTONS — COMPLETELY HIDDEN
   Sidebar is locked permanently open, so toggle button is unnecessary.
   Hiding all known selectors across Streamlit versions:
   - Pre-1.38:  [data-testid="collapsedControl"]
   - 1.38+:     [data-testid="stSidebarCollapsedControl"] (closed state, edge)
   - 1.38+:     [data-testid="stSidebarCollapseButton"]  (open state, inside)
   - Generic:   button[kind="header"] / button[kind="headerNoPadding"]
   ============================================================ */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] button[kind="header"],
section[data-testid="stSidebar"] button[kind="headerNoPadding"],
section[data-testid="stSidebar"] > button {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Main layout */
.block-container {
    padding-top: 0.25rem !important;
    padding-bottom: 0.45rem !important;
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
    max-width: 100% !important;
}
main .block-container {
    padding-top: 0.2rem !important;
}

/* When sidebar is collapsed, ensure main area fills full width */
[data-testid="stSidebar"][aria-expanded="false"] ~ * .block-container,
[data-testid="stSidebar"][aria-expanded="false"] + section .block-container {
    padding-left: 0.75rem !important;
    margin-left: 0 !important;
}
section.main {
    transition: all 0.3s ease !important;
}

/* Keep header visible for sidebar toggle */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}
[data-testid="stToolbar"] {
    top: 0.08rem;
    right: 0.45rem;
}

/* General text */
label, .stCaption, .stMarkdown, .stText {
    color: #cfd9e8 !important;
}

/* Sidebar headings */
.sidebar-section-title {
    margin: 10px 0 8px 0;
    font-size: 0.62rem;
    color: #9fb0c7;
    text-transform: uppercase;
    letter-spacing: 1.15px;
    font-weight: 800;
}

/* Sidebar logo */
.sidebar-logo {
    text-align: center;
    padding: 5px 0 7px 0;
    border-bottom: 1px solid #2E4057;
    margin-bottom: 6px;
}
.logo-icon  { font-size: 1.35rem; }
.logo-title {
    font-size: 0.98rem;
    font-weight: 800;
    color: #eef4fb !important;
    letter-spacing: -0.2px;
}
.logo-sub {
    font-size: 0.66rem;
    color: #8fa6c6 !important;
    margin-top: 2px;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(145deg, #1B263B, #162033);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 10px 10px 9px 10px;
    text-align: center;
    position: relative;
    overflow: hidden;
    min-height: 78px;
}
.kpi-top-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.kpi-icon {
    font-size: 0.95rem;
    margin-bottom: 2px;
    line-height: 1;
}
.kpi-value {
    font-size: 1.08rem;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin: 1px 0;
    line-height: 1.05;
}
.kpi-label {
    font-size: 0.60rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    color: #8fa6c6 !important;
}

/* Section title */
.sec-title {
    font-size: 1rem;
    font-weight: 800;
    color: #eef4fb;
    letter-spacing: -0.3px;
    margin-bottom: 2px;
}
.sec-sub {
    font-size: 0.72rem;
    color: #9fb0c7;
    margin-bottom: 6px;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, #1e3a5f 0%, transparent 80%);
    margin: 8px 0;
}

/* Overview summary cards */
.summary-card {
    background: linear-gradient(145deg, #1B263B, #162033);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 10px 12px;
    min-height: 72px;
}
.summary-title {
    font-size: 1.15rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
}
.summary-main {
    color: #d8e2f0;
    font-size: 0.74rem;
    font-weight: 600;
    margin-top: 4px;
}
.summary-status {
    font-size: 0.68rem;
    font-weight: 800;
    margin-top: 6px;
}

/* Mini insight panels */
.mini-panel {
    background: linear-gradient(145deg, #1B263B, #162033);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 10px 10px 8px 10px;
}
.mini-panel-title {
    font-size: 0.72rem;
    font-weight: 800;
    margin-bottom: 4px;
}
.mini-note {
    font-size: 0.62rem;
    color: #9fb0c7;
    margin-bottom: 4px;
}

/* Compact widget sizing */
div[data-baseweb="select"] > div {
    min-height: 34px !important;
}
.stDateInput > div > div {
    min-height: 34px !important;
}
.stButton > button {
    min-height: 34px !important;
    border-radius: 8px !important;
}
.stMultiSelect [data-baseweb="tag"] {
    font-size: 0.70rem !important;
}

/* Hide default chrome except header */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* ===== OVERVIEW TARGET LAYOUT PATCH ===== */

.target-overview-title {
    margin-bottom: 6px;
    line-height: 1.02;
}
.target-overview-sub {
    font-size: 0.74rem;
    color: #9fb0c7;
}

.summary-card-wide,
.summary-card-small {
    background: linear-gradient(145deg, #1B263B, #162033);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 10px 12px;
    min-height: 74px;
}

.summary-card-wide-title {
    color: #eef4fb;
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 4px;
}
.summary-card-wide-text {
    color: #9fb0c7;
    font-size: 0.70rem;
    line-height: 1.35;
}

.summary-card-small-num {
    font-size: 1.22rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
}
.summary-card-small-title {
    color: #d6e0ee;
    font-size: 0.74rem;
    font-weight: 600;
    margin-bottom: 4px;
}
.summary-card-small-status {
    font-size: 0.68rem;
    font-weight: 800;
}

.overview-panel {
    background: linear-gradient(145deg, #1B263B, #162033);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 10px 10px 8px 10px;
}
.overview-panel-title {
    font-size: 0.72rem;
    font-weight: 800;
    margin-bottom: 4px;
}
.overview-panel-sub {
    font-size: 0.62rem;
    color: #9fb0c7;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PATHS & DATA
# ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_data():
    order_level = pd.read_csv(DATA_DIR / "olist_clean_order_level.csv")
    item_level = pd.read_csv(DATA_DIR / "olist_clean_item_level.csv")
    customer_level = pd.read_csv(DATA_DIR / "olist_clean_customer_level.csv")

    order_level["purchase_timestamp"] = pd.to_datetime(
        order_level["purchase_timestamp"], errors="coerce"
    )
    item_level["order_purchase_timestamp"] = pd.to_datetime(
        item_level["order_purchase_timestamp"], errors="coerce"
    )

    return order_level, item_level, customer_level

order_level, item_level, customer_level = load_data()

# ─────────────────────────────────────────────────────────────
# DESIGN TOKENS — Olist Brand Aligned (Rebrand 2024-2025)
# ─────────────────────────────────────────────────────────────
T            = "plotly_dark"
CH_OVERVIEW  = 205
CH_DETAIL    = 260

# ── Primary brand accents ────────────────────────────────────
CYAN         = "#1E88E5"   # Olist brand blue (primary accent)
INDIGO       = "#3B82F6"   # secondary blue tone
AMBER        = "#FFB703"   # warning / partial verdict
GREEN        = "#06D6A0"   # success / confirmed
RED          = "#EF476F"   # danger / rejected
VIOLET       = "#8338EC"   # category diversity
ORANGE       = "#FB5607"   # high-energy accent
TEAL         = "#00B4D8"   # secondary cyan

PALETTE      = [CYAN, GREEN, AMBER, RED, VIOLET, TEAL, ORANGE, INDIGO]

# ── Dark theme backgrounds (Olist navy base) ─────────────────
PAPER_BG = "rgba(0,0,0,0)"
PLOT_BG  = "rgba(13,27,42,0.9)"   # #0D1B2A (Olist navy)
GRID_C   = "#1B263B"              # subtle grid

def fl(fig, title="", h=CH_DETAIL):
    fig.update_layout(
        template=T,
        height=h,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        margin=dict(l=10, r=10, t=32, b=8),
        title=dict(
            text=title,
            font=dict(size=12, color="#d8e2f0", family="Inter"),
            x=0.02
        ),
        font=dict(color="#c0cede", family="Inter", size=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=9, color="#c0cede"),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        hovermode="x unified",
    )
    fig.update_xaxes(
        gridcolor=GRID_C,
        linecolor="#2E4057",
        zerolinecolor="#2E4057",
        tickfont=dict(color="#b3c1d3", size=9),
        title_font=dict(color="#d8e2f0", size=10)
    )
    fig.update_yaxes(
        gridcolor=GRID_C,
        linecolor="#2E4057",
        zerolinecolor="#2E4057",
        tickfont=dict(color="#b3c1d3", size=9),
        title_font=dict(color="#d8e2f0", size=10)
    )
    return fig

def kpi(icon, label, value, color=CYAN):
    return f"""
    <div class="kpi-card">
        <div class="kpi-top-bar" style="background:{color};"></div>
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>"""

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">📦</div>
        <div class="logo-title">Olist Analytics</div>
        <div class="logo-sub">E-Commerce · Brazil</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        options=[
            "📊  Overview",
            "🔬  H1 — Delay & Satisfaction",
            "📦  H2 — Category & Revenue",
            "🗺️  H3 — Location & Delivery",
            "🔄  H4 — Satisfaction & Repeat",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div class='sidebar-section-title'>Filters</div>", unsafe_allow_html=True)

    min_d = order_level["purchase_timestamp"].min().date()
    max_d = order_level["purchase_timestamp"].max().date()

    dr = st.date_input(
        "Date Range",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d
    )
    st.caption("📅 Date Range")

    if isinstance(dr, tuple) and len(dr) == 2:
        sd, ed = pd.to_datetime(dr[0]), pd.to_datetime(dr[1])
    else:
        sd, ed = pd.to_datetime(min_d), pd.to_datetime(max_d)

    all_cstates = sorted(order_level["customer_state"].dropna().unique())
    sel_states = st.multiselect(
        "Customer State",
        all_cstates,
        default=all_cstates,
        placeholder="All states"
    )

    all_cats = sorted(item_level["product_category_name_english"].dropna().unique())
    sel_cats = st.multiselect(
        "Category",
        all_cats,
        default=all_cats,
        placeholder="All categories"
    )

    if st.button("↺ Reset Filters", use_container_width=True):
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#8fa6c6; text-align:left; line-height:1.55;'>
        96,478 orders · 115,723 items<br>Sep 2016 – Oct 2018
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FILTERED DATA
# ─────────────────────────────────────────────────────────────
fo = order_level.copy()
fo = fo[(fo["purchase_timestamp"] >= sd) & (fo["purchase_timestamp"] <= ed)]
if sel_states:
    fo = fo[fo["customer_state"].isin(sel_states)]

fi = item_level.copy()
fi = fi[(fi["order_purchase_timestamp"] >= sd) & (fi["order_purchase_timestamp"] <= ed)]
if sel_states and "customer_state" in fi.columns:
    fi = fi[fi["customer_state"].isin(sel_states)]
if sel_cats:
    fi = fi[fi["product_category_name_english"].isin(sel_cats)]

fc = customer_level.copy()
if "customer_unique_id" in fo.columns:
    fc = fc[fc["customer_unique_id"].isin(fo["customer_unique_id"].dropna())]

# Global KPIs
total_orders  = fo["order_id"].nunique()
total_revenue = fo["total_revenue"].sum()
avg_review    = fo["review_score_final"].mean()
avg_delivery  = fo["delivery_time_days"].mean()
delay_rate    = (fo["delay_days"] > 0).mean()

# ══════════════════════════════════════════════════════════════
# PAGE ▶ OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "📊  Overview":

    st.markdown("""
    <div class='target-overview-title'>
        <span style='font-size:1.65rem; font-weight:800; color:#eef4fb;'>Olist E-Commerce</span>
        <span style='font-size:1.65rem; font-weight:300; color:#00d4ff;'> Dashboard</span><br>
        <span class='target-overview-sub'>Brazil · Sep 2016 – Oct 2018 · Hypothesis-driven analytics</span>
    </div>
    """, unsafe_allow_html=True)

    # KPI ROW
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(kpi("📦", "Total Orders", f"{total_orders:,}", CYAN), unsafe_allow_html=True)
    c2.markdown(kpi("💰", "Total Revenue", f"R$ {total_revenue/1e6:.2f}M", AMBER), unsafe_allow_html=True)
    c3.markdown(kpi("⭐", "Avg Review", f"{avg_review:.2f} / 5", VIOLET), unsafe_allow_html=True)
    c4.markdown(kpi("🚚", "Avg Delivery", f"{avg_delivery:.1f} days", INDIGO), unsafe_allow_html=True)
    c5.markdown(kpi("⚠️", "Delay Rate", f"{delay_rate:.1%}", RED), unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── TOP MAIN CHARTS ─────────────────────────────────────
    fo_t = fo.copy()
    fo_t["month"] = fo_t["purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    monthly = fo_t.groupby("month").agg(
        revenue=("total_revenue", "sum"),
        orders=("order_id", "nunique"),
    ).reset_index()

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(
        go.Bar(
            x=monthly["month"],
            y=monthly["revenue"],
            name="Revenue (R$)",
            marker_color=CYAN,
            opacity=0.82,
        ),
        secondary_y=False
    )
    fig_trend.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["orders"],
            name="Orders",
            mode="lines+markers",
            line=dict(color=AMBER, width=2.0),
            marker=dict(size=3),
        ),
        secondary_y=True
    )
    fig_trend.update_layout(
        template=T,
        height=180,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        margin=dict(l=10, r=10, t=28, b=6),
        title=dict(
            text="Monthly Revenue & Order Volume",
            font=dict(size=12, color="#d8e2f0"),
            x=0.02
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            y=1.02,
            x=0,
            font=dict(color="#c0cede", size=10)
        ),
        hovermode="x unified",
        font=dict(family="Inter", size=10, color="#c0cede"),
    )
    fig_trend.update_yaxes(gridcolor=GRID_C, secondary_y=False, tickfont=dict(color="#b3c1d3", size=10))
    fig_trend.update_yaxes(showgrid=False, secondary_y=True, tickfont=dict(color="#b3c1d3", size=10))
    fig_trend.update_xaxes(gridcolor=GRID_C, tickfont=dict(color="#b3c1d3", size=10))

    top_left, top_mid, top_right = st.columns([1.7, 0.9, 1.0])

    with top_left:
        st.plotly_chart(fig_trend, use_container_width=True, key="overview_trend_target")

    with top_mid:
        sr = (
            fo.groupby("customer_state")["total_revenue"].sum()
            .sort_values(ascending=True).tail(8).reset_index()
        )
        fig_s = go.Figure(go.Bar(
            x=sr["total_revenue"],
            y=sr["customer_state"],
            orientation="h",
            marker=dict(
                color=sr["total_revenue"],
                colorscale=[[0, "#2E4057"], [1, CYAN]]
            ),
            text=sr["total_revenue"].apply(lambda v: f"R$ {v/1e6:.1f}M"),
            textposition="outside",
            textfont=dict(color="#d8e2f0", size=9),
        ))
        fig_s.update_layout(showlegend=False)
        fig_s = fl(fig_s, "Revenue by Customer State (Top 8)", h=180)
        st.plotly_chart(fig_s, use_container_width=True, key="overview_state_target")

    with top_right:
        rd = fo["review_score_final"].dropna().value_counts().sort_index().reset_index()
        rd.columns = ["score", "cnt"]
        c_map = {1: RED, 2: ORANGE, 3: AMBER, 4: "#a3e635", 5: GREEN}

        fig_r = go.Figure([go.Bar(
            x=rd["score"],
            y=rd["cnt"],
            marker_color=[c_map.get(int(s), CYAN) for s in rd["score"]],
            text=rd["cnt"].apply(lambda v: f"{v/1000:.1f}k" if v >= 1000 else f"{v}"),
            textposition="outside",
            textfont=dict(color="#d8e2f0", size=9),
        )])
        fig_r.update_layout(showlegend=False)
        fig_r = fl(fig_r, "Review Score Distribution", h=180)
        st.plotly_chart(fig_r, use_container_width=True, key="overview_review_target")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── SUMMARY CARDS ROW ────────────────────────────────────
    st.markdown("<div class='sec-title'>Hypotheses at a Glance</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Click a section in the sidebar to explore each hypothesis in detail.</div>", unsafe_allow_html=True)

    s0, s1, s2, s3, s4 = st.columns([1.2, 0.8, 0.8, 0.8, 0.8])

    s0.markdown("""
    <div class="summary-card-wide">
        <div class="summary-card-wide-title">Hypotheses at a Glance</div>
        <div class="summary-card-wide-text">
            Executive snapshot of the four main analytical questions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    for col, num, title, verdict, color in [
        (s1, "H1", "Delay → Satisfaction", "✅ Confirmed", GREEN),
        (s2, "H2", "Category → Revenue", "✅ Confirmed", GREEN),
        (s3, "H3", "Location → Delivery", "✅ Confirmed", GREEN),
        (s4, "H4", "Satisfaction → Repeat", "⚠️ Partial", AMBER),
    ]:
        col.markdown(f"""
        <div class="summary-card-small">
            <div class="summary-card-small-num" style="color:{color};">{num}</div>
            <div class="summary-card-small-title">{title}</div>
            <div class="summary-card-small-status" style="color:{color};">{verdict}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── FOUR MINI PANELS ─────────────────────────────────────
    p1, p2, p3, p4 = st.columns(4)

    # H1 PANEL
    with p1:
        st.markdown("""
        <div class="overview-panel">
            <div class="overview-panel-title" style="color:#22c55e;">H1 — Delay & Satisfaction</div>
            <div class="overview-panel-sub">Avg Review Score by Delay Category</div>
        </div>
        """, unsafe_allow_html=True)

        h1_df = fo[["delay_days", "review_score_final"]].dropna().copy()
        h1_df["delay_bucket"] = pd.cut(
            h1_df["delay_days"],
            bins=[-999, -1, 0, 3, 7, 999],
            labels=["Early", "On-Time", "1-3d", "3-7d", "7+d"]
        )
        h1_bar = h1_df.groupby("delay_bucket", observed=False)["review_score_final"].mean().reset_index()

        fig_h1_bar = go.Figure(go.Bar(
            x=h1_bar["delay_bucket"],
            y=h1_bar["review_score_final"],
            marker_color=["#22c55e", "#3b82f6", "#f59e0b", "#fb923c", "#ef4444"],
            text=h1_bar["review_score_final"].round(2),
            textposition="outside",
            textfont=dict(color="#d8e2f0", size=8),
        ))
        fig_h1_bar.update_yaxes(range=[0, 5.2])
        fig_h1_bar = fl(fig_h1_bar, "", h=110)
        fig_h1_bar.update_layout(margin=dict(l=6, r=6, t=6, b=6))
        st.plotly_chart(fig_h1_bar, use_container_width=True, key="overview_h1_bar_final")

        st.markdown("<div class='overview-panel-sub'>Review Score vs Delay Days (Sampled)</div>", unsafe_allow_html=True)

        h1_sc = h1_df.sample(min(1500, len(h1_df)), random_state=42)
        fig_h1_sc = px.scatter(
            h1_sc,
            x="delay_days",
            y="review_score_final",
            opacity=0.18,
            color_discrete_sequence=[CYAN],
            trendline="lowess",
            trendline_color_override=AMBER,
        )
        fig_h1_sc.update_yaxes(range=[0, 5.2])
        fig_h1_sc = fl(fig_h1_sc, "", h=105)
        fig_h1_sc.update_layout(margin=dict(l=6, r=6, t=6, b=6), showlegend=False)
        st.plotly_chart(fig_h1_sc, use_container_width=True, key="overview_h1_sc_final")

    # H2 PANEL
    with p2:
        st.markdown("""
        <div class="overview-panel">
            <div class="overview-panel-title" style="color:#22c55e;">H2 — Category & Revenue</div>
            <div class="overview-panel-sub">Revenue Share — Top 6 Categories</div>
        </div>
        """, unsafe_allow_html=True)

        cat_all = (
            fi.groupby("product_category_name_english")
            .agg(
                total_orders=("order_id", "nunique"),
                total_revenue=("revenue_line", "sum"),
                avg_price=("price", "mean")
            )
            .reset_index()
            .dropna()
            .sort_values("total_revenue", ascending=False)
        )

        cat_top6 = cat_all.head(6)

        fig_h2_pie = px.pie(
            cat_top6,
            values="total_revenue",
            names="product_category_name_english",
            hole=0.52,
            color_discrete_sequence=PALETTE
        )
        fig_h2_pie.update_traces(textinfo="percent", textfont_color="#eef4fb", textfont_size=8)
        fig_h2_pie.update_layout(
            template=T,
            height=110,
            paper_bgcolor=PAPER_BG,
            margin=dict(l=4, r=4, t=4, b=4),
            showlegend=False,
            font=dict(color="#c0cede", size=8)
        )
        st.plotly_chart(fig_h2_pie, use_container_width=True, key="overview_h2_pie_final")

        st.markdown("<div class='overview-panel-sub'>Pareto Chart — Revenue Concentration (Top 20)</div>", unsafe_allow_html=True)

        cat20 = cat_all.head(20).copy()
        total_rev = cat20["total_revenue"].sum()
        cat20["rank"] = range(1, len(cat20) + 1)
        cat20["cum_ratio"] = cat20["total_revenue"].cumsum() / total_rev

        fig_h2_par = make_subplots(specs=[[{"secondary_y": True}]])
        fig_h2_par.add_trace(
            go.Bar(
                x=cat20["rank"],
                y=cat20["total_revenue"],
                marker_color="#3b82f6",
                name="Revenue"
            ),
            secondary_y=False
        )
        fig_h2_par.add_trace(
            go.Scatter(
                x=cat20["rank"],
                y=cat20["cum_ratio"],
                mode="lines+markers",
                line=dict(color=AMBER, width=1.8),
                marker=dict(size=3),
                name="Cumulative %"
            ),
            secondary_y=True
        )
        fig_h2_par.update_layout(
            template=T,
            height=105,
            paper_bgcolor=PAPER_BG,
            plot_bgcolor=PLOT_BG,
            margin=dict(l=6, r=6, t=6, b=6),
            showlegend=True,
            legend=dict(font=dict(size=7), orientation="h", y=1.02, x=0),
            font=dict(color="#c0cede", size=8)
        )
        fig_h2_par.update_yaxes(showgrid=True, gridcolor=GRID_C, secondary_y=False, tickfont=dict(size=8))
        fig_h2_par.update_yaxes(showgrid=False, secondary_y=True, tickformat=".0%", tickfont=dict(size=8))
        fig_h2_par.update_xaxes(showgrid=False, tickfont=dict(size=8))
        st.plotly_chart(fig_h2_par, use_container_width=True, key="overview_h2_pareto_final")

    # H3 PANEL
    with p3:
        st.markdown("""
        <div class="overview-panel">
            <div class="overview-panel-title" style="color:#22c55e;">H3 — Location & Delivery</div>
            <div class="overview-panel-sub">Same-State vs Cross-State Delivery</div>
        </div>
        """, unsafe_allow_html=True)

        h3_df = fo.dropna(subset=["seller_state", "customer_state", "delivery_time_days", "delay_days"]).copy()
        h3_df["same"] = h3_df["seller_state"] == h3_df["customer_state"]

        same_avg = h3_df.loc[h3_df["same"], "delivery_time_days"].mean()
        cross_avg = h3_df.loc[~h3_df["same"], "delivery_time_days"].mean()
        same_delay = (h3_df.loc[h3_df["same"], "delay_days"] > 0).mean() * 100
        cross_delay = (h3_df.loc[~h3_df["same"], "delay_days"] > 0).mean() * 100

        cmp_df = pd.DataFrame({
            "Metric": ["Delivery", "Delay %"],
            "Same": [same_avg, same_delay],
            "Cross": [cross_avg, cross_delay]
        })

        fig_h3_cmp = go.Figure()
        fig_h3_cmp.add_bar(
            name="Same",
            x=cmp_df["Metric"],
            y=cmp_df["Same"],
            marker_color=GREEN,
            text=cmp_df["Same"].round(1),
            textposition="outside",
            textfont=dict(color="#d8e2f0", size=8)
        )
        fig_h3_cmp.add_bar(
            name="Cross",
            x=cmp_df["Metric"],
            y=cmp_df["Cross"],
            marker_color=RED,
            text=cmp_df["Cross"].round(1),
            textposition="outside",
            textfont=dict(color="#d8e2f0", size=8)
        )
        fig_h3_cmp.update_layout(barmode="group", showlegend=True)
        fig_h3_cmp = fl(fig_h3_cmp, "", h=110)
        fig_h3_cmp.update_layout(margin=dict(l=6, r=6, t=6, b=6), legend=dict(font=dict(size=7), orientation="h", y=1.02, x=0))
        st.plotly_chart(fig_h3_cmp, use_container_width=True, key="overview_h3_cmp_final")

        lower_left, lower_right = st.columns(2)

        with lower_left:
            st.markdown("<div class='overview-panel-sub'>Avg Delivery Time by Seller State</div>", unsafe_allow_html=True)
            sp = (
                h3_df.groupby("seller_state")
                .agg(avg_delivery=("delivery_time_days", "mean"))
                .reset_index()
                .sort_values("avg_delivery")
                .head(8)
            )
            fig_h3_sp = go.Figure(go.Bar(
                x=sp["seller_state"],
                y=sp["avg_delivery"],
                marker_color=["#9acd32","#8bc34a","#7cb342","#fbc02d","#f9a825","#fb8c00","#f4511e","#e53935"][:len(sp)],
            ))
            fig_h3_sp = fl(fig_h3_sp, "", h=95)
            fig_h3_sp.update_layout(margin=dict(l=6, r=6, t=6, b=6), showlegend=False)
            st.plotly_chart(fig_h3_sp, use_container_width=True, key="overview_h3_sp_final")

        with lower_right:
            st.markdown("<div class='overview-panel-sub'>Delay Rate by Customer State</div>", unsafe_allow_html=True)
            cd = (
                h3_df.groupby("customer_state")
                .agg(delay_rate=("delay_days", lambda x: (x > 0).mean()))
                .reset_index()
                .sort_values("delay_rate", ascending=False)
                .head(8)
            )
            fig_h3_cd = go.Figure(go.Bar(
                x=cd["customer_state"],
                y=cd["delay_rate"],
                marker_color=["#22c55e","#65a30d","#eab308","#f59e0b","#f97316","#ef4444","#dc2626","#b91c1c"][:len(cd)],
            ))
            fig_h3_cd.update_yaxes(tickformat=".0%")
            fig_h3_cd = fl(fig_h3_cd, "", h=95)
            fig_h3_cd.update_layout(margin=dict(l=6, r=6, t=6, b=6), showlegend=False)
            st.plotly_chart(fig_h3_cd, use_container_width=True, key="overview_h3_cd_final")

    # H4 PANEL
    with p4:
        st.markdown("""
        <div class="overview-panel">
            <div class="overview-panel-title" style="color:#f59e0b;">H4 — Satisfaction & Repeat</div>
            <div class="overview-panel-sub">Repeat Purchase Rate by Review Segment</div>
        </div>
        """, unsafe_allow_html=True)

        h4_df = fc.dropna(subset=["avg_review_score", "is_repeat_customer"]).copy()
        h4_df["review_bucket"] = pd.cut(
            h4_df["avg_review_score"],
            bins=[0, 2, 3, 4, 5],
            labels=["1-2", "2-3", "3-4", "4-5"]
        )
        rr_mini = (
            h4_df.groupby("review_bucket", observed=False)
            .agg(rate=("is_repeat_customer", "mean"))
            .reset_index()
        )

        fig_h4_rr = go.Figure(go.Bar(
            x=rr_mini["review_bucket"],
            y=rr_mini["rate"],
            marker_color=[RED, ORANGE, CYAN, GREEN],
            text=rr_mini["rate"].apply(lambda v: f"{v:.1%}"),
            textposition="outside",
            textfont=dict(color="#d8e2f0", size=8),
        ))
        fig_h4_rr.update_yaxes(tickformat=".0%")
        fig_h4_rr = fl(fig_h4_rr, "", h=110)
        fig_h4_rr.update_layout(margin=dict(l=6, r=6, t=6, b=6))
        st.plotly_chart(fig_h4_rr, use_container_width=True, key="overview_h4_rr_final")

        lower1, lower2 = st.columns(2)

        with lower1:
            if "avg_order_value" in h4_df.columns:
                st.markdown("<div class='overview-panel-sub'>Avg Order Value: One-Time vs Repeat</div>", unsafe_allow_html=True)
                h4_df["group"] = h4_df["is_repeat_customer"].map({0: "One-Time", 1: "Repeat"})
                fig_h4_box = px.box(
                    h4_df,
                    x="group",
                    y="avg_order_value",
                    color="group",
                    color_discrete_map={"One-Time": INDIGO, "Repeat": GREEN},
                    points=False,
                )
                fig_h4_box.update_layout(showlegend=False)
                fig_h4_box = fl(fig_h4_box, "", h=95)
                fig_h4_box.update_layout(margin=dict(l=6, r=6, t=6, b=6))
                st.plotly_chart(fig_h4_box, use_container_width=True, key="overview_h4_box_final")

        with lower2:
            st.markdown("<div class='overview-panel-sub'>Avg Review Score by # of Orders</div>", unsafe_allow_html=True)
            h4_df["order_bucket"] = pd.cut(
                h4_df["total_orders"],
                bins=[0, 1, 2, 3, 100],
                labels=["1", "2", "3", "4+"]
            )
            ob = (
                h4_df.groupby("order_bucket", observed=False)
                .agg(avg_review=("avg_review_score", "mean"))
                .reset_index()
            )
            fig_h4_ob = go.Figure(go.Bar(
                x=ob["order_bucket"],
                y=ob["avg_review"],
                marker_color=[INDIGO, "#3b82f6", "#22c55e", "#16a34a"],
                text=ob["avg_review"].round(2),
                textposition="outside",
                textfont=dict(color="#d8e2f0", size=8),
            ))
            fig_h4_ob.update_yaxes(range=[0, 5.2])
            fig_h4_ob = fl(fig_h4_ob, "", h=95)
            fig_h4_ob.update_layout(margin=dict(l=6, r=6, t=6, b=6))
            st.plotly_chart(fig_h4_ob, use_container_width=True, key="overview_h4_ob_final")

# ══════════════════════════════════════════════════════════════
# PAGE ▶ H1 — DELAY & SATISFACTION
# ══════════════════════════════════════════════════════════════
elif page == "🔬  H1 — Delay & Satisfaction":

    st.markdown("""
    <div class="hyp-card">
        <div class="hyp-tag">Hypothesis 1</div>
        <div class="hyp-text">
            Orders with longer delivery delays receive significantly lower customer review scores.
        </div>
    </div>""", unsafe_allow_html=True)

    h1 = fo[["delay_days", "review_score_final", "delivery_time_days"]].dropna().copy()

    on_time_score = h1[h1["delay_days"] <= 0]["review_score_final"].mean()
    delayed_score = h1[h1["delay_days"] > 0]["review_score_final"].mean()
    score_drop = on_time_score - delayed_score
    delayed_n = int((h1["delay_days"] > 0).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("✅", "On-Time Avg Score", f"{on_time_score:.2f}", GREEN), unsafe_allow_html=True)
    c2.markdown(kpi("🚨", "Delayed Avg Score", f"{delayed_score:.2f}", RED), unsafe_allow_html=True)
    c3.markdown(kpi("📉", "Score Drop", f"▼ {score_drop:.2f}", AMBER), unsafe_allow_html=True)
    c4.markdown(kpi("📦", "Delayed Orders", f"{delayed_n:,}", INDIGO), unsafe_allow_html=True)

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        h1["delay_bucket"] = pd.cut(
            h1["delay_days"],
            bins=[-999, -1, 0, 3, 7, 999],
            labels=["Early", "On-Time", "1–3 Days", "3–7 Days", "7+ Days"]
        )
        bkt = (h1.groupby("delay_bucket", observed=False)["review_score_final"]
               .mean().reset_index())
        bkt.columns = ["bucket", "avg"]

        fig_b = go.Figure(go.Bar(
            x=bkt["bucket"],
            y=bkt["avg"],
            marker_color=[GREEN, "#3b82f6", AMBER, ORANGE, RED],
            text=bkt["avg"].round(2),
            textposition="outside",
            textfont=dict(color="#c9d5e5", size=11),
        ))
        fig_b.add_hline(
            y=avg_review,
            line_dash="dot",
            line_color="#5a6c86",
            annotation_text=f"Overall avg {avg_review:.2f}",
            annotation_font_color="#cbd5e1"
        )
        fig_b.update_yaxes(range=[0, 5.8])
        fig_b = fl(fig_b, "Avg Review Score by Delay Category", h=325)
        st.plotly_chart(fig_b, use_container_width=True, key="h1_bar")

    with col2:
        samp = h1.sample(min(4000, len(h1)), random_state=42)
        fig_sc = px.scatter(
            samp,
            x="delay_days",
            y="review_score_final",
            opacity=0.18,
            color_discrete_sequence=[CYAN],
            trendline="lowess",
            trendline_color_override=AMBER,
            labels={"delay_days": "Delay (Days)", "review_score_final": "Review Score"},
        )
        fig_sc.update_yaxes(range=[0, 5.5])
        fig_sc = fl(fig_sc, "Review Score vs Delay Days (Sampled, with LOWESS trend)", h=325)
        st.plotly_chart(fig_sc, use_container_width=True, key="h1_scatter")

    col3, col4 = st.columns(2)

    with col3:
        corr = fo[["delivery_time_days", "delay_days", "review_score_final"]].dropna().corr()
        fig_hm = px.imshow(
            corr.round(3),
            text_auto=True,
            color_continuous_scale=[[0, RED], [0.5, "#2E4057"], [1, CYAN]],
            zmin=-1,
            zmax=1,
        )
        fig_hm = fl(fig_hm, "Correlation Matrix — Delivery & Satisfaction", h=325)
        st.plotly_chart(fig_hm, use_container_width=True, key="h1_heatmap")

    with col4:
        h1["group"] = h1["delay_days"].apply(
            lambda x: "On-Time / Early" if x <= 0 else "Delayed"
        )
        fig_bx = px.box(
            h1,
            x="group",
            y="review_score_final",
            color="group",
            color_discrete_map={"On-Time / Early": GREEN, "Delayed": RED},
            points=False,
            labels={"group": "", "review_score_final": "Review Score"},
        )
        fig_bx.update_layout(showlegend=False)
        fig_bx = fl(fig_bx, "Score Distribution: Delayed vs On-Time", h=325)
        st.plotly_chart(fig_bx, use_container_width=True, key="h1_box")

    st.markdown("""
    <div class="verdict verdict-confirmed">
        <strong>✅ H1 CONFIRMED</strong> — Delayed orders score on average
        <strong>0.8–1.2 points lower</strong> than on-time orders. The longer the delay, the satisfaction drop becomes stronger.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE ▶ H2 — CATEGORY & REVENUE
# ══════════════════════════════════════════════════════════════
elif page == "📦  H2 — Category & Revenue":

    st.markdown("""
    <div class="hyp-card">
        <div class="hyp-tag">Hypothesis 2</div>
        <div class="hyp-text">
            A small number of product categories account for a disproportionately large share
            of total revenue — consistent with the Pareto principle.
        </div>
    </div>""", unsafe_allow_html=True)

    cat = (
        fi.groupby("product_category_name_english")
        .agg(
            total_orders=("order_id", "nunique"),
            total_revenue=("revenue_line", "sum"),
            avg_price=("price", "mean")
        )
        .reset_index()
        .dropna(subset=["product_category_name_english"])
        .sort_values("total_revenue", ascending=False)
        .reset_index(drop=True)
    )
    cat["cum_ratio"] = cat["total_revenue"].cumsum() / cat["total_revenue"].sum()
    cat["rank"] = range(1, len(cat) + 1)

    top5_share = cat["total_revenue"].head(5).sum() / cat["total_revenue"].sum()
    top20_share = cat["total_revenue"].head(20).sum() / cat["total_revenue"].sum()
    top_cat = cat.iloc[0]["product_category_name_english"]

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("📂", "Total Categories", f"{len(cat)}", CYAN), unsafe_allow_html=True)
    c2.markdown(kpi("🏆", "Top 5 Revenue Share", f"{top5_share:.0%}", AMBER), unsafe_allow_html=True)
    c3.markdown(kpi("📊", "Top 20 Share", f"{top20_share:.0%}", INDIGO), unsafe_allow_html=True)
    c4.markdown(kpi("💎", "Leader Category", top_cat[:16] + "…" if len(top_cat) > 16 else top_cat, GREEN), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2.6, 1.4])

    with col1:
        t10 = cat.head(10).sort_values("total_revenue", ascending=True)
        fig_h2 = go.Figure(go.Bar(
            x=t10["total_revenue"],
            y=t10["product_category_name_english"],
            orientation="h",
            marker=dict(
                color=t10["total_revenue"],
                colorscale=[[0, "#2E4057"], [1, CYAN]]
            ),
            text=t10["total_revenue"].apply(lambda v: f"R$ {v/1e6:.2f}M"),
            textposition="outside",
            textfont=dict(color="#c9d5e5", size=10),
        ))
        fig_h2.update_coloraxes(showscale=False)
        fig_h2 = fl(fig_h2, "Top 10 Categories by Total Revenue", h=220)
        st.plotly_chart(fig_h2, use_container_width=True, key="h2_top10")

    with col2:
        fig_pie = px.pie(
            cat.head(8),
            values="total_revenue",
            names="product_category_name_english",
            hole=0.55,
            color_discrete_sequence=PALETTE,
        )
        fig_pie.update_traces(textinfo="percent", textfont_color="#eef4fb", textfont_size=10)
        fig_pie.update_layout(
            template=T,
            height=220,
            paper_bgcolor=PAPER_BG,
            margin=dict(l=12, r=12, t=34, b=8),
            title=dict(
                text="Revenue Share — Top 8 Categories",
                font=dict(size=12, color="#cbd5e1"),
                x=0.02
            ),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, color="#b8c4d6")),
            font=dict(family="Inter", size=10, color="#b8c4d6"),
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="h2_pie")

    p20 = cat.head(20)
    fig_par = make_subplots(specs=[[{"secondary_y": True}]])
    fig_par.add_trace(go.Bar(
        x=p20["rank"], y=p20["total_revenue"],
        name="Revenue", marker_color=CYAN, opacity=0.8,
    ), secondary_y=False)
    fig_par.add_trace(go.Scatter(
        x=p20["rank"], y=p20["cum_ratio"],
        name="Cumulative %",
        mode="lines+markers",
        line=dict(color=AMBER, width=2.0), marker=dict(size=4),
    ), secondary_y=True)
    fig_par.add_hline(
        y=0.8, line_dash="dot", line_color=RED,
        annotation_text="80%",
        annotation_font_color="#ffb4b4",
        secondary_y=True
    )
    fig_par.update_layout(
        template=T,
        height=240,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        margin=dict(l=12, r=12, t=34, b=8),
        title=dict(
            text="Pareto Chart — Revenue Concentration (Top 20 Categories)",
            font=dict(size=12, color="#cbd5e1"),
            x=0.02
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#b8c4d6")),
        hovermode="x unified",
        font=dict(family="Inter", size=11, color="#b8c4d6"),
        xaxis_title="Category Rank",
    )
    fig_par.update_yaxes(gridcolor=GRID_C, secondary_y=False, title_text="Revenue (R$)", tickfont=dict(color="#aebcd0"))
    fig_par.update_yaxes(showgrid=False, secondary_y=True, tickformat=".0%", title_text="Cumulative Share", tickfont=dict(color="#aebcd0"))
    fig_par.update_xaxes(gridcolor=GRID_C, tickfont=dict(color="#aebcd0"))
    st.plotly_chart(fig_par, use_container_width=True, key="h2_pareto")

    fig_bub = px.scatter(
        cat,
        x="total_orders",
        y="total_revenue",
        size="avg_price",
        hover_name="product_category_name_english",
        color="total_revenue",
        color_continuous_scale=[[0, "#2E4057"], [1, CYAN]],
        size_max=28,
        labels={
            "total_orders": "Total Orders",
            "total_revenue": "Total Revenue",
            "avg_price": "Avg Price"
        },
    )
    fig_bub.update_coloraxes(showscale=False)
    fig_bub = fl(fig_bub, "Category Performance — Volume vs Revenue vs Avg Price", h=210)
    st.plotly_chart(fig_bub, use_container_width=True, key="h2_bubble")

    st.markdown("""
    <div class="verdict verdict-confirmed">
        <strong>✅ H2 CONFIRMED</strong> — The top 5 categories account for
        <strong>~40% of total revenue</strong>. Top 20 categories cover over 75% of all sales.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE ▶ H3 — LOCATION & DELIVERY
# ══════════════════════════════════════════════════════════════
elif page == "🗺️  H3 — Location & Delivery":

    st.markdown("""
    <div class="hyp-card">
        <div class="hyp-tag">Hypothesis 3</div>
        <div class="hyp-text">
            Orders where the seller and customer are in the same state are delivered significantly faster
            and have a lower delay rate compared to cross-state orders.
        </div>
    </div>""", unsafe_allow_html=True)

    h3 = fo.dropna(subset=["seller_state", "customer_state", "delivery_time_days", "delay_days"]).copy()
    h3["same"] = h3["seller_state"] == h3["customer_state"]
    h3["label"] = h3["same"].map({True: "Same State", False: "Cross State"})

    same = h3[h3["same"]]
    cross = h3[~h3["same"]]

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("🏠", "Same-State Delivery", f"{same['delivery_time_days'].mean():.1f} days", GREEN), unsafe_allow_html=True)
    c2.markdown(kpi("✈️", "Cross-State Delivery", f"{cross['delivery_time_days'].mean():.1f} days", RED), unsafe_allow_html=True)
    c3.markdown(kpi("📉", "Same-State Delay %", f"{(same['delay_days']>0).mean():.1%}", AMBER), unsafe_allow_html=True)
    c4.markdown(kpi("📈", "Cross-State Delay %", f"{(cross['delay_days']>0).mean():.1%}", INDIGO), unsafe_allow_html=True)

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cdf = pd.DataFrame({
            "Metric": ["Avg Delivery (days)", "Delay Rate (%)"],
            "Same State": [
                same["delivery_time_days"].mean(),
                (same["delay_days"] > 0).mean() * 100
            ],
            "Cross State": [
                cross["delivery_time_days"].mean(),
                (cross["delay_days"] > 0).mean() * 100
            ],
        })
        fig_cmp = go.Figure()
        fig_cmp.add_bar(
            name="Same State", x=cdf["Metric"], y=cdf["Same State"],
            marker_color=GREEN,
            text=cdf["Same State"].round(1),
            textposition="outside",
            textfont=dict(color="#c9d5e5")
        )
        fig_cmp.add_bar(
            name="Cross State", x=cdf["Metric"], y=cdf["Cross State"],
            marker_color=RED,
            text=cdf["Cross State"].round(1),
            textposition="outside",
            textfont=dict(color="#c9d5e5")
        )
        fig_cmp.update_layout(barmode="group")
        fig_cmp = fl(fig_cmp, "Same State vs Cross State — Delivery Metrics", h=325)
        fig_cmp.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.12,
                xanchor="center",
                x=0.5,
                font=dict(size=10, color="#c0cede")
            ),
            margin=dict(l=10, r=10, t=36, b=42)
        )
        st.plotly_chart(fig_cmp, use_container_width=True, key="h3_compare")

    with col2:
        fig_bx3 = px.box(
            h3,
            x="label",
            y="delivery_time_days",
            color="label",
            color_discrete_map={"Same State": GREEN, "Cross State": RED},
            points=False,
            labels={"label": "", "delivery_time_days": "Delivery Time (Days)"},
        )
        fig_bx3.update_layout(showlegend=False)
        fig_bx3 = fl(fig_bx3, "Delivery Time Distribution — Same vs Cross State", h=325)
        st.plotly_chart(fig_bx3, use_container_width=True, key="h3_box")

    col3, col4 = st.columns(2)

    with col3:
        sp = (
            h3.groupby("seller_state")
            .agg(
                avg_delivery=("delivery_time_days", "mean"),
                orders=("order_id", "count"),
                delay_rate=("delay_days", lambda x: (x > 0).mean())
            )
            .reset_index()
            .sort_values("avg_delivery")
            .head(15)
        )
        fig_sp = px.bar(
            sp,
            x="seller_state",
            y="avg_delivery",
            color="delay_rate",
            color_continuous_scale=[[0, GREEN], [0.5, AMBER], [1, RED]],
            text="avg_delivery",
            labels={
                "seller_state": "Seller State",
                "avg_delivery": "Avg Delivery (Days)",
                "delay_rate": "Delay Rate"
            },
        )
        fig_sp.update_traces(
            texttemplate="%{text:.1f}d",
            textposition="outside",
            textfont=dict(color="#c9d5e5")
        )
        fig_sp = fl(fig_sp, "Avg Delivery Time by Seller State (color = delay risk)", h=315)
        st.plotly_chart(fig_sp, use_container_width=True, key="h3_seller_perf")

    with col4:
        cd = (
            h3.groupby("customer_state")
            .agg(delay_rate=("delay_days", lambda x: (x > 0).mean()))
            .reset_index()
            .sort_values("delay_rate", ascending=True)
        )
        fig_cd = go.Figure(go.Bar(
            x=cd["delay_rate"],
            y=cd["customer_state"],
            orientation="h",
            marker=dict(
                color=cd["delay_rate"],
                colorscale=[[0, GREEN], [0.5, AMBER], [1, RED]]
            ),
            text=cd["delay_rate"].apply(lambda v: f"{v:.0%}"),
            textposition="outside",
            textfont=dict(color="#c9d5e5", size=10),
        ))
        fig_cd.update_coloraxes(showscale=False)
        fig_cd.update_xaxes(tickformat=".0%")
        fig_cd = fl(fig_cd, "Delay Rate by Customer State", h=315)
        st.plotly_chart(fig_cd, use_container_width=True, key="h3_customer_delay")

    st.markdown("""
    <div class="verdict verdict-confirmed">
        <strong>✅ H3 CONFIRMED</strong> — Same-state orders arrive faster and show a lower delay rate than cross-state orders.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE ▶ H4 — SATISFACTION & REPEAT
# ══════════════════════════════════════════════════════════════
elif page == "🔄  H4 — Satisfaction & Repeat":

    st.markdown("""
    <div class="hyp-card">
        <div class="hyp-tag">Hypothesis 4</div>
        <div class="hyp-text">
            Customers with higher satisfaction scores are more likely to make repeat purchases
            on the Olist platform.
        </div>
    </div>""", unsafe_allow_html=True)

    repeat_rate = fc["is_repeat_customer"].mean()
    repeat_n = int(fc["is_repeat_customer"].sum())
    seg_n = fc["customer_segment"].nunique() if "customer_segment" in fc.columns else "—"

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("👥", "Total Customers", f"{len(fc):,}", CYAN), unsafe_allow_html=True)
    c2.markdown(kpi("🔄", "Repeat Customers", f"{repeat_n:,}", INDIGO), unsafe_allow_html=True)
    c3.markdown(kpi("📊", "Repeat Rate", f"{repeat_rate:.1%}", AMBER), unsafe_allow_html=True)
    c4.markdown(kpi("🎯", "Segments", f"{seg_n}", GREEN), unsafe_allow_html=True)

    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        h4 = fc.dropna(subset=["avg_review_score", "is_repeat_customer"]).copy()
        h4["review_bucket"] = pd.cut(
            h4["avg_review_score"],
            bins=[0, 2, 3, 4, 5],
            labels=["Very Low\n(1–2)", "Low\n(2–3)", "Medium\n(3–4)", "High\n(4–5)"]
        )
        rr = (
            h4.groupby("review_bucket", observed=False)
            .agg(
                rate=("is_repeat_customer", "mean"),
                cnt=("customer_unique_id", "count")
            )
            .reset_index()
        )
        fig_rr = go.Figure(go.Bar(
            x=rr["review_bucket"],
            y=rr["rate"],
            marker_color=[RED, ORANGE, INDIGO, GREEN],
            text=rr["rate"].apply(lambda v: f"{v:.1%}"),
            textposition="outside",
            textfont=dict(color="#c9d5e5", size=11),
        ))
        fig_rr.add_hline(
            y=repeat_rate, line_dash="dot", line_color="#5a6c86",
            annotation_text=f"Avg {repeat_rate:.1%}",
            annotation_font_color="#cbd5e1"
        )
        fig_rr.update_yaxes(tickformat=".0%")
        fig_rr = fl(fig_rr, "Repeat Purchase Rate by Review Score Segment", h=325)
        st.plotly_chart(fig_rr, use_container_width=True, key="h4_repeat_rate")

    with col2:
        if "customer_segment" in fc.columns:
            seg = (
                fc.groupby("customer_segment")
                .agg(
                    count=("customer_unique_id", "count"),
                    avg_review=("avg_review_score", "mean"),
                    avg_order_value=("avg_order_value", "mean"),
                    rate=("is_repeat_customer", "mean")
                )
                .reset_index()
            )
            fig_seg = px.scatter(
                seg,
                x="avg_review",
                y="rate",
                size="count",
                color="customer_segment",
                color_discrete_sequence=PALETTE,
                hover_name="customer_segment",
                size_max=45,
                text="customer_segment",
                labels={"avg_review": "Avg Review Score", "rate": "Repeat Rate"},
            )
            fig_seg.update_traces(
                textposition="top center",
                textfont=dict(size=9, color="#c9d5e5")
            )
            fig_seg.update_yaxes(tickformat=".0%")
            fig_seg = fl(fig_seg, "Customer Segments — Satisfaction vs Repeat Rate", h=325)
            fig_seg.update_layout(
                legend=dict(
                    title_text="",
                    orientation="h",
                    yanchor="top",
                    y=-0.18,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10, color="#c0cede")
                ),
                margin=dict(l=10, r=10, t=36, b=48)
            )
            st.plotly_chart(fig_seg, use_container_width=True, key="h4_segment")

    col3, col4 = st.columns(2)

    with col3:
        h4["group"] = h4["is_repeat_customer"].map({0: "One-Time", 1: "Repeat"})
        fig_ov = px.box(
            h4,
            x="group",
            y="avg_order_value",
            color="group",
            color_discrete_map={"One-Time": INDIGO, "Repeat": GREEN},
            points=False,
            labels={"group": "", "avg_order_value": "Avg Order Value (R$)"},
        )
        fig_ov.update_layout(showlegend=False)
        fig_ov = fl(fig_ov, "Avg Order Value: One-Time vs Repeat Customers", h=315)
        st.plotly_chart(fig_ov, use_container_width=True, key="h4_order_value")

    with col4:
        h4["order_bucket"] = pd.cut(
            h4["total_orders"],
            bins=[0, 1, 2, 3, 100],
            labels=["1 Order", "2 Orders", "3 Orders", "4+ Orders"]
        )
        ob = (
            h4.groupby("order_bucket", observed=False)
            .agg(
                avg_review=("avg_review_score", "mean"),
                cnt=("customer_unique_id", "count")
            )
            .reset_index()
        )
        fig_ob = go.Figure(go.Bar(
            x=ob["order_bucket"],
            y=ob["avg_review"],
            marker_color=PALETTE[:4],
            text=ob["avg_review"].round(2),
            textposition="outside",
            textfont=dict(color="#c9d5e5", size=11),
        ))
        fig_ob.update_yaxes(range=[0, 5.5])
        fig_ob = fl(fig_ob, "Avg Review Score by Number of Orders Placed", h=315)
        st.plotly_chart(fig_ob, use_container_width=True, key="h4_avg_review_orders")

    st.markdown(f"""
    <div class="verdict verdict-partial">
        <strong>⚠️ H4 PARTIALLY CONFIRMED</strong> — High satisfaction alone is not a reliable
        predictor of repeat purchases. The overall repeat rate is very low (~{repeat_rate:.1%}),
        indicating Olist functions primarily as a <strong>one-time purchase platform</strong>.
    </div>""", unsafe_allow_html=True)