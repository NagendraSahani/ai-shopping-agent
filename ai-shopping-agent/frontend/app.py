import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ============================================================
# CONFIG (Backend unchanged)
# ============================================================
API_URL = "https://ai-shopping-agent-1-4ihn.onrender.com/agent/shopping"

st.set_page_config(
    page_title="AI Shopping Agent",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE
# ============================================================
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []

if "result" not in st.session_state:
    st.session_state.result = None

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "query_input" not in st.session_state:
    st.session_state.query_input = ""

if "trigger_search" not in st.session_state:
    st.session_state.trigger_search = False


def set_query_and_search(q):
    st.session_state.query_input = q
    st.session_state.trigger_search = True


# ============================================================
# CUSTOM CSS — Premium Dark Theme (Amazon x Apple x ChatGPT)
# ============================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
    --bg-primary:#0b0d12;
    --bg-secondary:#12151c;
    --bg-card:#161a23;
    --bg-card-hover:#1c212c;
    --border-color:#242938;
    --accent-1:#7c5cff;
    --accent-2:#22d3ee;
    --accent-3:#f97316;
    --success:#22c55e;
    --danger:#ef4444;
    --text-primary:#f5f6fa;
    --text-secondary:#9aa2b1;
    --text-muted:#5c6474;
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif !important;
    color:var(--text-primary);
}

.stApp{
    background:radial-gradient(circle at 10% 0%, #171b2e 0%, #0b0d12 45%, #0b0d12 100%);
}

#MainMenu, footer, header{visibility:hidden;}

/* ---------- HERO ---------- */
.hero-container{
    padding:48px 40px;
    border-radius:24px;
    background:linear-gradient(120deg, #6d28d9 0%, #7c5cff 35%, #22d3ee 100%);
    margin-bottom:32px;
    box-shadow:0 20px 60px -20px rgba(124,92,255,0.55);
    position:relative;
    overflow:hidden;
}
.hero-container::after{
    content:"";
    position:absolute;
    top:-60px;right:-60px;
    width:220px;height:220px;
    background:rgba(255,255,255,0.12);
    border-radius:50%;
}
.hero-title{
    font-size:2.6rem;
    font-weight:900;
    color:#ffffff;
    margin:0;
    letter-spacing:-1px;
}
.hero-subtitle{
    font-size:1.05rem;
    color:rgba(255,255,255,0.9);
    margin-top:8px;
    font-weight:500;
}
.hero-badges{margin-top:18px;}
.hero-badge{
    display:inline-block;
    background:rgba(255,255,255,0.18);
    backdrop-filter:blur(6px);
    color:#fff;
    padding:6px 14px;
    border-radius:999px;
    font-size:0.78rem;
    font-weight:600;
    margin-right:8px;
    border:1px solid rgba(255,255,255,0.25);
}

/* ---------- SEARCH BOX ---------- */
div[data-testid="stTextInput"] input{
    background:var(--bg-card) !important;
    border:2px solid var(--border-color) !important;
    border-radius:16px !important;
    color:var(--text-primary) !important;
    padding:18px 20px !important;
    font-size:1.05rem !important;
    font-weight:500 !important;
    transition:all 0.25s ease;
}
div[data-testid="stTextInput"] input:focus{
    border-color:var(--accent-1) !important;
    box-shadow:0 0 0 4px rgba(124,92,255,0.25) !important;
}

/* ---------- BUTTONS ---------- */
.stButton>button{
    background:linear-gradient(90deg, var(--accent-1), var(--accent-2));
    color:#fff;
    border:none;
    border-radius:14px;
    padding:14px 22px;
    font-weight:700;
    font-size:1rem;
    width:100%;
    transition:all 0.25s ease;
    box-shadow:0 8px 24px -8px rgba(124,92,255,0.6);
}
.stButton>button:hover{
    transform:translateY(-2px);
    box-shadow:0 12px 28px -6px rgba(124,92,255,0.75);
}

a[data-testid="stLinkButton"] > button, .stLinkButton>a{
    background:linear-gradient(90deg,#f97316,#fb923c) !important;
    color:#fff !important;
    border-radius:14px !important;
    font-weight:800 !important;
    border:none !important;
    box-shadow:0 8px 22px -8px rgba(249,115,22,0.7) !important;
    transition:all 0.25s ease !important;
}
a[data-testid="stLinkButton"] > button:hover, .stLinkButton>a:hover{
    transform:translateY(-2px);
}

/* ---------- CARDS ---------- */
.premium-card{
    background:var(--bg-card);
    border:1px solid var(--border-color);
    border-radius:20px;
    padding:26px;
    transition:all 0.25s ease;
}
.premium-card:hover{
    border-color:var(--accent-1);
    background:var(--bg-card-hover);
}

.ai-pick-wrapper{
    background:linear-gradient(145deg, rgba(124,92,255,0.14), rgba(34,211,238,0.08));
    border:1.5px solid rgba(124,92,255,0.45);
    border-radius:26px;
    padding:30px;
    margin-bottom:10px;
    box-shadow:0 20px 50px -25px rgba(124,92,255,0.5);
}
.ai-pick-tag{
    display:inline-block;
    background:linear-gradient(90deg, var(--accent-1), var(--accent-2));
    color:#fff;
    padding:6px 16px;
    border-radius:999px;
    font-size:0.75rem;
    font-weight:800;
    letter-spacing:1px;
    text-transform:uppercase;
    margin-bottom:14px;
}
.product-name{
    font-size:1.5rem;
    font-weight:800;
    color:var(--text-primary);
    margin:6px 0 14px 0;
    line-height:1.3;
}
.info-row{
    font-size:0.98rem;
    color:var(--text-secondary);
    margin:6px 0;
    font-weight:500;
}
.info-row b{color:var(--text-primary);}
.price-tag{
    font-size:1.8rem;
    font-weight:900;
    color:var(--success);
    margin:4px 0 10px 0;
}

/* ---------- SMALL PRODUCT GRID CARDS ---------- */
.grid-card{
    background:var(--bg-card);
    border:1px solid var(--border-color);
    border-radius:18px;
    padding:16px;
    height:100%;
    transition:all 0.2s ease;
}
.grid-card:hover{
    border-color:var(--accent-2);
    transform:translateY(-4px);
    box-shadow:0 14px 30px -14px rgba(34,211,238,0.45);
}
.grid-title{
    font-size:0.92rem;
    font-weight:700;
    color:var(--text-primary);
    margin:10px 0 6px 0;
    min-height:42px;
    line-height:1.3;
}
.grid-price{
    font-size:1.15rem;
    font-weight:800;
    color:var(--success);
}
.grid-meta{
    font-size:0.8rem;
    color:var(--text-secondary);
    margin:2px 0;
}
.rank-badge{
    display:inline-block;
    background:rgba(124,92,255,0.18);
    color:var(--accent-1);
    font-weight:800;
    font-size:0.72rem;
    padding:3px 10px;
    border-radius:999px;
    margin-bottom:6px;
}

/* ---------- SECTION HEADERS ---------- */
.section-header{
    display:flex;
    align-items:center;
    gap:10px;
    font-size:1.4rem;
    font-weight:800;
    color:var(--text-primary);
    margin:8px 0 18px 0;
    border-left:5px solid var(--accent-1);
    padding-left:14px;
}

/* ---------- VERDICT / PROS / CONS ---------- */
.verdict-card{
    background:linear-gradient(135deg, rgba(34,211,238,0.12), rgba(124,92,255,0.08));
    border:1px solid rgba(34,211,238,0.35);
    border-radius:18px;
    padding:22px;
    font-size:1rem;
    color:var(--text-primary);
    font-weight:500;
    line-height:1.6;
}
.pros-card{
    background:rgba(34,197,94,0.08);
    border:1px solid rgba(34,197,94,0.35);
    border-radius:18px;
    padding:20px;
    height:100%;
}
.cons-card{
    background:rgba(239,68,68,0.08);
    border:1px solid rgba(239,68,68,0.35);
    border-radius:18px;
    padding:20px;
    height:100%;
}
.pros-card h4{color:var(--success); margin-top:0;}
.cons-card h4{color:var(--danger); margin-top:0;}
.pros-card ul, .cons-card ul{padding-left:18px; margin:0;}
.pros-card li, .cons-card li{margin-bottom:8px; color:var(--text-secondary); font-weight:500;}

/* ---------- AI RECOMMENDATION CARDS ---------- */
.reco-card{
    background:var(--bg-card);
    border:1px solid var(--border-color);
    border-radius:16px;
    padding:18px 20px;
    margin-bottom:10px;
}
.reco-key{
    font-size:0.72rem;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1px;
    color:var(--accent-2);
    margin-bottom:6px;
}
.reco-value{
    font-size:0.98rem;
    color:var(--text-primary);
    font-weight:500;
    line-height:1.5;
}

/* ---------- CONFIDENCE BAR LABEL ---------- */
.confidence-label{
    font-size:0.85rem;
    font-weight:700;
    color:var(--text-secondary);
    margin-bottom:2px;
}
div[data-testid="stProgress"] > div > div{
    background:linear-gradient(90deg, var(--accent-1), var(--accent-2)) !important;
}

/* ---------- METRIC CARDS ---------- */
div[data-testid="stMetric"]{
    background:var(--bg-card);
    border:1px solid var(--border-color);
    border-radius:16px;
    padding:16px 10px;
    text-align:center;
}
div[data-testid="stMetricValue"]{
    color:var(--accent-2) !important;
    font-weight:800 !important;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"]{
    background:var(--bg-secondary);
    border-right:1px solid var(--border-color);
}
.sidebar-title{
    font-size:1.1rem;
    font-weight:800;
    color:var(--text-primary);
    margin-bottom:10px;
}
.sidebar-sub{
    font-size:0.8rem;
    color:var(--text-muted);
    margin-bottom:18px;
}

/* ---------- FOOTER ---------- */
.footer{
    margin-top:60px;
    padding:28px 10px 10px 10px;
    border-top:1px solid var(--border-color);
    text-align:center;
    color:var(--text-muted);
    font-size:0.85rem;
}
.tech-badge{
    display:inline-block;
    background:var(--bg-card);
    border:1px solid var(--border-color);
    color:var(--text-secondary);
    padding:6px 14px;
    border-radius:999px;
    font-size:0.78rem;
    font-weight:600;
    margin:4px;
}

/* ---------- DATAFRAME ---------- */
div[data-testid="stDataFrame"]{
    border:1px solid var(--border-color);
    border-radius:16px;
    overflow:hidden;
}

/* ---------- RESPONSIVE ---------- */
@media (max-width: 768px){
    .hero-title{font-size:1.8rem;}
    .hero-container{padding:28px 20px;}
    .product-name{font-size:1.2rem;}
    .price-tag{font-size:1.4rem;}
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================


def fetch_data(user_query: str):
    """Calls the existing FastAPI backend. Backend contract unchanged."""
    resp = requests.post(API_URL, params={"query": user_query}, timeout=120)
    resp.raise_for_status()
    return resp.json()


def render_confidence_bar(confidence):
    try:
        val = float(confidence)
    except (TypeError, ValueError):
        val = 0
    val = max(0, min(100, val))
    st.markdown(
        f'<div class="confidence-label">🎯 AI Confidence Score — {val:.0f}%</div>',
        unsafe_allow_html=True,
    )
    st.progress(val / 100)


def render_best_product(best: dict):
    st.markdown('<div class="ai-pick-wrapper">', unsafe_allow_html=True)
    st.markdown('<span class="ai-pick-tag">🤖 AI Top Pick</span>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        thumbnail = best.get("thumbnail", "")
        if thumbnail:
            st.image(thumbnail, use_container_width=True)
        else:
            st.info("No Image Available")

    with col2:
        st.markdown(f'<div class="product-name">{best.get("name", "Unnamed Product")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price-tag">₹{best.get("price", 0)}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="info-row">🏪 Platform: <b>{best.get("platform", "N/A")}</b></div>'
            f'<div class="info-row">⭐ Rating: <b>{best.get("rating", "N/A")}</b></div>'
            f'<div class="info-row">📝 Reviews: <b>{best.get("reviews", "N/A")}</b></div>',
            unsafe_allow_html=True,
        )

        st.write("")
        render_confidence_bar(best.get("confidence", 0))
        st.write("")

        if best.get("buy_link"):
            st.link_button("🛒 Buy Now", best["buy_link"], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_score_breakdown(score_breakdown):
    if not score_breakdown:
        st.info("No score breakdown available.")
        return

    if isinstance(score_breakdown, dict):
        keys = list(score_breakdown.keys())
        cols = st.columns(min(len(keys), 5) or 1)
        for i, k in enumerate(keys):
            v = score_breakdown[k]
            with cols[i % len(cols)]:
                st.metric(label=k.replace("_", " ").title(), value=v)
    else:
        st.json(score_breakdown)


def render_ai_recommendation(ai_rec):
    if not ai_rec:
        st.info("No AI recommendation available.")
        return

    if isinstance(ai_rec, dict):
        for key, value in ai_rec.items():
            pretty_key = str(key).replace("_", " ").title()
            if isinstance(value, (list, tuple)):
                value_html = "<br>".join([f"• {v}" for v in value])
            elif isinstance(value, dict):
                value_html = "<br>".join([f"<b>{k}</b>: {v}" for k, v in value.items()])
            else:
                value_html = str(value)

            st.markdown(
                f"""
                <div class="reco-card">
                    <div class="reco-key">{pretty_key}</div>
                    <div class="reco-value">{value_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif isinstance(ai_rec, list):
        for item in ai_rec:
            st.markdown(
                f'<div class="reco-card"><div class="reco-value">• {item}</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f'<div class="reco-card"><div class="reco-value">{ai_rec}</div></div>',
            unsafe_allow_html=True,
        )


def _extract_list(value):
    """Normalize a pros/cons style field into a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        # split on newlines or semicolons if it's one big string
        parts = [p.strip("-• \n") for p in value.replace(";", "\n").split("\n") if p.strip()]
        return parts if parts else [value]
    return [str(value)]


def render_review(review):
    if not review:
        st.info("No review summary available.")
        return

    pros, cons, verdict = [], [], ""

    if isinstance(review, dict):
        lower_map = {str(k).lower(): k for k in review.keys()}

        for candidate in ["pros", "positives", "advantages"]:
            if candidate in lower_map:
                pros = _extract_list(review[lower_map[candidate]])
                break

        for candidate in ["cons", "negatives", "disadvantages", "drawbacks"]:
            if candidate in lower_map:
                cons = _extract_list(review[lower_map[candidate]])
                break

        for candidate in ["verdict", "summary", "conclusion", "final_thoughts"]:
            if candidate in lower_map:
                verdict = review[lower_map[candidate]]
                break

        if not (pros or cons or verdict):
            # unknown dict shape — render generic cards
            render_ai_recommendation(review)
            return
    else:
        # plain string review — try to detect labeled sections
        text = str(review)
        verdict = text

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        pros_html = "".join([f"<li>{p}</li>" for p in pros]) if pros else "<li>Not specified</li>"
        st.markdown(
            f'<div class="pros-card"><h4>✅ Pros</h4><ul>{pros_html}</ul></div>',
            unsafe_allow_html=True,
        )

    with col2:
        cons_html = "".join([f"<li>{c}</li>" for c in cons]) if cons else "<li>Not specified</li>"
        st.markdown(
            f'<div class="cons-card"><h4>⚠️ Cons</h4><ul>{cons_html}</ul></div>',
            unsafe_allow_html=True,
        )

    if verdict:
        st.write("")
        st.markdown(
            f'<div class="verdict-card">🧠 <b>Verdict:</b><br>{verdict}</div>',
            unsafe_allow_html=True,
        )


def render_comparison_table(table_data):
    try:
        df = pd.DataFrame(table_data)
        if df.empty:
            st.info("No comparison data available.")
            return
        st.dataframe(
            df.style.background_gradient(cmap="Purples", axis=0) if df.select_dtypes("number").shape[1] else df,
            use_container_width=True,
            height=min(50 + 38 * len(df), 500),
        )
    except Exception:
        st.dataframe(pd.DataFrame(table_data), use_container_width=True)


def render_product_grid(products, heading, icon="🛍️", max_items=10, cols_per_row=5, show_rank=False):
    if not products:
        return

    st.markdown(f'<div class="section-header">{icon} {heading}</div>', unsafe_allow_html=True)

    items = products[:max_items]
    rows = [items[i : i + cols_per_row] for i in range(0, len(items), cols_per_row)]

    rank = 1
    for row in rows:
        cols = st.columns(len(row), gap="medium")
        for col, product in zip(cols, row):
            with col:
                st.markdown('<div class="grid-card">', unsafe_allow_html=True)

                thumbnail = product.get("thumbnail", "")
                if thumbnail:
                    st.image(thumbnail, use_container_width=True)

                if show_rank:
                    st.markdown(f'<span class="rank-badge">#{rank}</span>', unsafe_allow_html=True)

                name = product.get("name", "Unnamed Product")
                short_name = name if len(name) <= 60 else name[:57] + "..."
                st.markdown(f'<div class="grid-title">{short_name}</div>', unsafe_allow_html=True)

                st.markdown(
                    f'<div class="grid-price">₹{product.get("price", 0)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="grid-meta">⭐ {product.get("rating", "N/A")} &nbsp;|&nbsp; 🏪 {product.get("platform", "N/A")}</div>',
                    unsafe_allow_html=True,
                )

                conf = product.get("confidence", None)
                if conf is not None:
                    try:
                        st.progress(max(0, min(100, float(conf))) / 100)
                    except (TypeError, ValueError):
                        pass

                if product.get("buy_link"):
                    st.link_button("Buy", product["buy_link"], use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)
                rank += 1
        st.write("")


def render_footer():
    st.markdown(
        """
        <div class="footer">
            <div>
                <span class="tech-badge">🧠 LangGraph</span>
                <span class="tech-badge">✨ Gemini</span>
                <span class="tech-badge">🔎 Tavily</span>
                <span class="tech-badge">🛰️ SerpAPI</span>
                <span class="tech-badge">⚡ FastAPI</span>
                <span class="tech-badge">🎨 Streamlit</span>
            </div>
            <div style="margin-top:14px;">Built with ❤️ — AI Shopping Agent · Premium UI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🕘 Recent Searches</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Tap any search to run it again</div>', unsafe_allow_html=True)

    if st.session_state.recent_searches:
        for q in reversed(st.session_state.recent_searches[-10:]):
            st.button(f"🔁 {q}", key=f"recent_{q}", on_click=set_query_and_search, args=(q,), use_container_width=True)
    else:
        st.caption("No searches yet. Your history will show up here.")

    st.divider()
    st.markdown('<div class="sidebar-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.caption(
        "This AI Shopping Agent compares products across platforms, "
        "scores them, and recommends the best pick using an autonomous "
        "LangGraph agent pipeline."
    )

# ============================================================
# HERO SECTION
# ============================================================
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🛒 AI Shopping Agent</div>
        <div class="hero-subtitle">Your autonomous AI-powered assistant for finding the best product, at the best price, from the best seller.</div>
        <div class="hero-badges">
            <span class="hero-badge">⚡ LangGraph</span>
            <span class="hero-badge">✨ Gemini</span>
            <span class="hero-badge">🔎 Tavily</span>
            <span class="hero-badge">🛰️ SerpAPI</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SEARCH SECTION
# ============================================================
search_col, button_col = st.columns([4, 1], gap="medium")

with search_col:
    query = st.text_input(
        "Search Product",
        placeholder="e.g. Laptop under 50000",
        key="query_input",
        label_visibility="collapsed",
    )

with button_col:
    search_clicked = st.button("🔍 Search Now", use_container_width=True)

do_search = search_clicked or st.session_state.trigger_search
st.session_state.trigger_search = False

# ============================================================
# SEARCH EXECUTION
# ============================================================
if do_search:
    current_query = st.session_state.query_input.strip()

    if current_query == "":
        st.warning("⚠️ Please enter a product name.")
        st.stop()

    with st.spinner("🤖 Agent is searching across platforms, comparing prices & analyzing reviews..."):
        try:
            data = fetch_data(current_query)
        except requests.exceptions.RequestException as e:
            st.error("❌ Cannot connect to FastAPI backend. Make sure it's running on port 8000.")
            st.code(str(e))
            st.stop()
        except ValueError:
            st.error("❌ Backend did not return valid JSON.")
            st.stop()

    st.session_state.result = data
    st.session_state.last_query = current_query

    if current_query not in st.session_state.recent_searches:
        st.session_state.recent_searches.append(current_query)

# ============================================================
# RENDER RESULTS (persists across reruns)
# ============================================================
data = st.session_state.result

if data:
    st.success(f"✅ Best match found for **\"{st.session_state.last_query}\"**")

    best = data.get("best_product", {})

    st.write("")
    render_best_product(best)

    st.write("")
    st.markdown('<div class="section-header">📊 Score Breakdown</div>', unsafe_allow_html=True)
    render_score_breakdown(best.get("score_breakdown", {}))

    st.write("")
    st.markdown('<div class="section-header">🤖 AI Recommendation</div>', unsafe_allow_html=True)
    render_ai_recommendation(data.get("ai_recommendation", {}))

    st.write("")
    st.markdown('<div class="section-header">📝 Review Summary</div>', unsafe_allow_html=True)
    render_review(data.get("review", ""))

    if data.get("comparison_table"):
        st.write("")
        st.markdown('<div class="section-header">📋 Comparison Table</div>', unsafe_allow_html=True)
        render_comparison_table(data["comparison_table"])

    if data.get("all_products"):
        st.write("")
        render_product_grid(
            data["all_products"],
            heading="Top Products",
            icon="🏆",
            max_items=10,
            cols_per_row=5,
            show_rank=True,
        )

    if data.get("alternatives"):
        st.write("")
        render_product_grid(
            data["alternatives"],
            heading="Alternative Products",
            icon="🥈",
            max_items=10,
            cols_per_row=5,
            show_rank=False,
        )

else:
    st.info("👆 Enter a product above and hit **Search Now** to let the AI agent find your best match.")

render_footer()
