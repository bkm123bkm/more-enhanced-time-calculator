import datetime as dt
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "Icon.png"
PAGE_ICON = str(ICON_PATH) if ICON_PATH.exists() else "💎"
PUNE_TZ = ZoneInfo("Asia/Kolkata")

def now_pune() -> dt.datetime:
    return dt.datetime.now(PUNE_TZ).replace(tzinfo=None)

st.set_page_config(
    page_title="TimeTrack Pro",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None
if "member_day_type" not in st.session_state:
    st.session_state.member_day_type = "Full Day"
if "leader_day_type" not in st.session_state:
    st.session_state.leader_day_type = "Full Day"
if "show_member_sessions" not in st.session_state:
    st.session_state.show_member_sessions = False
if "show_leader_sessions" not in st.session_state:
    st.session_state.show_leader_sessions = False

# ============================================================================
# CSS - Modern Glass-morphism (fixed for no overlap)
# ============================================================================

def inject_css():
    """Inject theme-specific CSS with high specificity to avoid overlap"""
    if st.session_state.theme_mode == "light":
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #e9edf2 100%)"
        card_bg = "rgba(255, 255, 255, 0.85)"
        card_bg_hover = "rgba(255, 255, 255, 0.95)"
        text_primary = "#1e293b"
        text_secondary = "#5a6e7c"
        accent = "#2563eb"
        accent_gradient = "linear-gradient(135deg, #1e2b3c 0%, #2c3e50 100%)"
        border = "rgba(0, 0, 0, 0.08)"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.05)"
    else:
        bg_gradient = "linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%)"
        card_bg = "rgba(30, 30, 45, 0.8)"
        card_bg_hover = "rgba(40, 40, 58, 0.9)"
        text_primary = "#e0e0e0"
        text_secondary = "#8a8a9e"
        accent = "#60a5fa"
        accent_gradient = "linear-gradient(135deg, #3a3a5a 0%, #2a2a44 100%)"
        border = "rgba(255, 255, 255, 0.08)"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.2)"
    
    css = f"""
    <style>
        /* Global reset & fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        .stApp {{
            background: {bg_gradient};
        }}
        
        /* Main container padding - prevent overlapping */
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}
        
        /* Glass header */
        .glass-header {{
            background: {card_bg};
            backdrop-filter: blur(12px);
            border-radius: 28px;
            padding: 1.25rem 2rem;
            margin-bottom: 2rem;
            border: 1px solid {border};
            box-shadow: {shadow};
        }}
        
        h1 {{
            font-size: 2rem !important;
            font-weight: 700 !important;
            background: {accent_gradient};
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
            letter-spacing: -0.02em;
            margin: 0 !important;
        }}
        
        .caption-text {{
            color: {text_secondary} !important;
            font-size: 0.85rem !important;
        }}
        
        /* Stats using native columns + custom metric styling */
        div[data-testid="stMetric"] {{
            background: {card_bg};
            backdrop-filter: blur(8px);
            border-radius: 24px;
            padding: 1rem;
            border: 1px solid {border};
            transition: all 0.3s ease;
            text-align: center;
        }}
        
        div[data-testid="stMetric"]:hover {{
            transform: translateY(-3px);
            background: {card_bg_hover};
            box-shadow: {shadow};
        }}
        
        div[data-testid="stMetric"] label {{
            font-size: 0.7rem !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            color: {text_secondary} !important;
        }}
        
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
            font-size: 1.75rem !important;
            font-weight: 700;
            font-family: 'Inter', monospace;
            background: {accent_gradient};
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        
        /* Session panels - use CSS grid for proper layout */
        .sessions-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
            margin: 1.5rem 0;
        }}
        
        .session-card {{
            background: {card_bg};
            backdrop-filter: blur(8px);
            border-radius: 24px;
            border: 1px solid {border};
            overflow: hidden;
        }}
        
        .session-header {{
            padding: 0.9rem 1.25rem;
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            border-bottom: 1px solid {border};
        }}
        
        .session-header.work {{
            background: rgba(59, 130, 246, 0.08);
            color: {accent};
        }}
        
        .session-header.break {{
            background: rgba(245, 158, 11, 0.08);
            color: #f59e0b;
        }}
        
        .session-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1.25rem;
            border-bottom: 1px solid {border};
        }}
        
        .session-time {{
            color: {text_secondary};
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .session-duration {{
            font-weight: 700;
            font-size: 0.9rem;
        }}
        
        .session-duration.work {{
            color: {accent};
        }}
        
        .session-duration.break {{
            color: #f59e0b;
        }}
        
        .live-badge {{
            background: linear-gradient(135deg, #10b981, #059669);
            padding: 2px 10px;
            border-radius: 30px;
            font-size: 0.6rem;
            font-weight: 600;
            color: white;
            margin-left: 10px;
            display: inline-block;
        }}
        
        /* Logout card */
        .logout-card {{
            background: {card_bg};
            border-radius: 24px;
            padding: 1.25rem;
            text-align: center;
            margin-top: 1.5rem;
            border: 1px solid {border};
        }}
        
        .logout-time {{
            font-size: 1.8rem;
            font-weight: 800;
            background: {accent_gradient};
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-family: monospace;
        }}
        
        .success-banner {{
            background: linear-gradient(135deg, #10b981, #059669);
            border-radius: 24px;
            padding: 1.25rem;
            text-align: center;
            margin-top: 1.5rem;
            animation: slideUp 0.4s ease;
        }}
        
        .success-banner p {{
            color: white !important;
            font-weight: 600;
            margin: 0;
        }}
        
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Form cards */
        .form-card {{
            background: {card_bg};
            backdrop-filter: blur(8px);
            border-radius: 28px;
            padding: 1.25rem 1.5rem;
            margin: 1rem 0 1.5rem 0;
            border: 1px solid {border};
        }}
        
        /* Buttons */
        .stButton > button {{
            background: {accent_gradient} !important;
            color: white !important;
            border: none !important;
            border-radius: 40px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }}
        
        /* Text area */
        .stTextArea textarea {{
            border-radius: 20px !important;
            border: 1px solid {border} !important;
            background: {card_bg} !important;
            color: {text_primary} !important;
            font-family: monospace !important;
        }}
        
        /* Radio group */
        .stRadio > div {{
            gap: 0.5rem;
            background: {card_bg};
            padding: 0.4rem;
            border-radius: 60px;
            display: inline-flex;
            border: 1px solid {border};
        }}
        
        .stRadio label {{
            padding: 0.4rem 1.2rem !important;
            border-radius: 40px !important;
            font-weight: 500 !important;
        }}
        
        /* Tabs */
        [data-testid="stTabs"] [role="tablist"] {{
            gap: 0.5rem;
            background: {card_bg};
            border-radius: 60px;
            padding: 0.4rem;
            border: 1px solid {border};
            margin-bottom: 1.5rem;
        }}
        
        [data-testid="stTabs"] [role="tab"] {{
            border-radius: 40px !important;
            padding: 0.4rem 1.2rem !important;
            font-weight: 500 !important;
        }}
        
        [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
            background: {accent_gradient} !important;
            color: white !important;
        }}
        
        hr {{
            margin: 1.5rem 0;
            border: none;
            height: 1px;
            background: {border};
        }}
        
        .section-header {{
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            background: {accent_gradient};
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        
        /* Override Streamlit default column gap to prevent overlap */
        .row-widget.stHorizontal {{
            gap: 1rem;
        }}
        
        /* Fix for theme toggle button alignment */
        div[data-testid="column"]:nth-child(3) .stButton > button {{
            background: {card_bg} !important;
            color: {text_primary} !important;
            border: 1px solid {border} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Inject CSS on every rerun (theme changes)
inject_css()

# ============================================================================
# Utility functions (unchanged, but included for completeness)
# ============================================================================

def format_clock(seconds: int) -> str:
    seconds = max(seconds, 0)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_human(seconds: int) -> str:
    seconds = max(seconds, 0)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"

# Constants
DAY_FULL = "Full Day"
DAY_HALF = "Half Day"
DAY_TYPE_OPTIONS = (DAY_FULL, DAY_HALF)

MEMBER_THRESHOLDS = {DAY_FULL: 27000, DAY_HALF: 16200}
LEADER_THRESHOLDS = {DAY_FULL: 25200, DAY_HALF: 14400}
BREAK_TARGET = 5400

def member_threshold(day_type: str) -> int:
    return MEMBER_THRESHOLDS.get(day_type, 27000)

def leader_threshold(day_type: str) -> int:
    return LEADER_THRESHOLDS.get(day_type, 25200)

def extract_times(log_text: str) -> list[dt.datetime]:
    matches = re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", log_text)
    today = now_pune().date()
    points = []
    last = None
    for m in matches:
        h, min_val = map(int, m.split(":"))
        candidate = dt.datetime.combine(today, dt.time(h, min_val))
        if last and candidate < last:
            today += dt.timedelta(days=1)
            candidate = dt.datetime.combine(today, dt.time(h, min_val))
        points.append(candidate)
        last = candidate
    return points

def normalize_paste_text(raw: str) -> str:
    return (raw or "").replace("\r\n", "\n")

def parse_log(log_text: str) -> list[dt.datetime] | None:
    pts = extract_times(log_text)
    return pts if len(pts) >= 1 else None

def analyze_sessions(points: list[dt.datetime], current: dt.datetime = None) -> dict:
    if current is None:
        current = now_pune()
    
    work_sessions = []
    break_sessions = []
    total_work = 0
    total_break = 0
    
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        duration = int((end - start).total_seconds())
        session = {
            "start": start.strftime("%I:%M %p").lstrip("0"),
            "end": end.strftime("%I:%M %p").lstrip("0"),
            "duration": duration,
            "human": format_human(duration)
        }
        if i % 2 == 0:
            work_sessions.append(session)
            total_work += duration
        else:
            break_sessions.append(session)
            total_break += duration
    
    ongoing = 0
    has_ongoing = False
    if len(points) % 2 == 1:
        last = points[-1]
        if current < last:
            current += dt.timedelta(days=1)
        ongoing = int((current - last).total_seconds())
        has_ongoing = True
        work_sessions.append({
            "start": last.strftime("%I:%M %p").lstrip("0"),
            "end": current.strftime("%I:%M %p").lstrip("0"),
            "duration": ongoing,
            "human": format_human(ongoing),
            "ongoing": True
        })
    
    return {
        "work_sessions": work_sessions,
        "break_sessions": break_sessions,
        "total_work": total_work,
        "total_break": total_break,
        "ongoing_work": ongoing,
        "has_ongoing": has_ongoing
    }

# ============================================================================
# Dashboard Components (using native st.metric to avoid overlap)
# ============================================================================

def render_stats_grid(stats: dict):
    cols = st.columns(5)
    metrics = [
        ("💼 Total Work", stats["total_work"]),
        ("☕ Break Time", stats["total_break"]),
        ("⏱️ Total Time", stats["total_work"] + stats["total_break"]),
        ("⏳ Remaining Work", stats["remaining_work"]),
        ("🍵 Remaining Break", stats["remaining_break"])
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            display = format_clock(value) if value > 0 else "✓" if "Remaining" in label and value == 0 else format_clock(value)
            st.metric(label, display)

def render_sessions_panel(work: list, breaks: list):
    st.markdown('<div class="sessions-grid">', unsafe_allow_html=True)
    # Work column
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header work">🎯 WORK SESSIONS · {len(work)}</div>', unsafe_allow_html=True)
    if work:
        for s in work:
            live = '<span class="live-badge">LIVE</span>' if s.get("ongoing") else ""
            st.markdown(
                f'<div class="session-row">'
                f'<span class="session-time">{s["start"]} → {s["end"]}{live}</span>'
                f'<span class="session-duration work">{s["human"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="session-row"><span class="session-time">— No work sessions —</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # Break column
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header break">✨ BREAK SESSIONS · {len(breaks)}</div>', unsafe_allow_html=True)
    if breaks:
        for s in breaks:
            st.markdown(
                f'<div class="session-row">'
                f'<span class="session-time">{s["start"]} → {s["end"]}</span>'
                f'<span class="session-duration break">{s["human"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="session-row"><span class="session-time">— No breaks —</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_logout_status(deadline: dt.datetime, first: dt.datetime, now: dt.datetime):
    if now < deadline:
        time_str = deadline.strftime("%I:%M %p").lstrip("0")
        if deadline.date() != first.date():
            time_str = deadline.strftime("%d %b, %I:%M %p").lstrip("0")
        st.markdown(
            f'<div class="logout-card">'
            f'<div style="font-size:0.7rem; letter-spacing:1px; margin-bottom:6px;">🚀 EARLIEST LOGOUT</div>'
            f'<div class="logout-time">{time_str}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="success-banner">'
            '<p>✨ TARGET ACHIEVED! You\'re Free to Go! ✨</p>'
            '</div>',
            unsafe_allow_html=True
        )

# Dashboard functions
def member_dashboard(points: list, day_type: str):
    now = now_pune()
    result = analyze_sessions(points, now)
    required = member_threshold(day_type)
    total_work = result["total_work"] + result["ongoing_work"]
    remaining = max(required - total_work, 0)
    deadline = now + dt.timedelta(seconds=remaining)
    remaining_break = max(BREAK_TARGET - result["total_break"], 0)
    stats = {
        "total_work": total_work,
        "total_break": result["total_break"],
        "remaining_work": remaining,
        "remaining_break": remaining_break
    }
    st.caption(f"👤 First punch: {points[0].strftime('%I:%M %p').lstrip('0')} • {points[0].strftime('%d %b %Y')}")
    render_stats_grid(stats)
    # Session toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if result["has_ongoing"]:
            btn_label = "📋 Hide Details" if st.session_state.show_member_sessions else "📋 Show Session Details"
            if st.button(btn_label, key="member_session_toggle", use_container_width=True):
                st.session_state.show_member_sessions = not st.session_state.show_member_sessions
                st.rerun()
    if st.session_state.show_member_sessions:
        render_sessions_panel(result["work_sessions"], result["break_sessions"])
    render_logout_status(deadline, points[0], now)

def leader_dashboard(points: list, day_type: str):
    now = now_pune()
    result = analyze_sessions(points, now)
    required = leader_threshold(day_type)
    total_work = result["total_work"] + result["ongoing_work"]
    remaining = max(required - total_work, 0)
    deadline = now + dt.timedelta(seconds=remaining)
    remaining_break = max(BREAK_TARGET - result["total_break"], 0)
    stats = {
        "total_work": total_work,
        "total_break": result["total_break"],
        "remaining_work": remaining,
        "remaining_break": remaining_break
    }
    st.caption(f"👑 First punch: {points[0].strftime('%I:%M %p').lstrip('0')} • {points[0].strftime('%d %b %Y')}")
    render_stats_grid(stats)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if result["has_ongoing"]:
            btn_label = "📋 Hide Details" if st.session_state.show_leader_sessions else "📋 Show Session Details"
            if st.button(btn_label, key="leader_session_toggle", use_container_width=True):
                st.session_state.show_leader_sessions = not st.session_state.show_leader_sessions
                st.rerun()
    if st.session_state.show_leader_sessions:
        render_sessions_panel(result["work_sessions"], result["break_sessions"])
    render_logout_status(deadline, points[0], now)

# Live fragments
@st.fragment(run_every="1s")
def member_live():
    if st.session_state.member_points:
        member_dashboard(st.session_state.member_points, st.session_state.member_day_type)

@st.fragment(run_every="1s")
def leader_live():
    if st.session_state.leader_points:
        leader_dashboard(st.session_state.leader_points, st.session_state.leader_day_type)

# ============================================================================
# Header
# ============================================================================
st.markdown('<div class="glass-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 6, 2])
with col1:
    st.markdown('<span style="font-size: 2.5rem;">💎</span>', unsafe_allow_html=True)
with col2:
    st.title("TimeTrack Pro")
    st.markdown('<span class="caption-text">Intelligent time analytics with live tracking</span>', unsafe_allow_html=True)
with col3:
    theme_label = "🌙 Dark Mode" if st.session_state.theme_mode == "light" else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"
        st.rerun()
st.markdown(f'<span class="caption-text" style="display: block; margin-top: 8px;">📍 Pune, India (IST) • {now_pune().strftime("%A, %d %B %Y • %I:%M:%S %p")}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# Tabs
# ============================================================================
tab1, tab2 = st.tabs(["👤 TEAM MEMBER", "👑 TEAM LEADER"])

with tab1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 1rem; font-weight: 600;">📅 Day Configuration</div>', unsafe_allow_html=True)
    day_type = st.radio(
        "Select shift type",
        DAY_TYPE_OPTIONS,
        index=0 if st.session_state.member_day_type == DAY_FULL else 1,
        horizontal=True,
        key="member_day_radio",
        label_visibility="collapsed"
    )
    st.session_state.member_day_type = day_type
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 1rem; font-weight: 600;">📝 Biometric Log Input</div>', unsafe_allow_html=True)
    with st.form("member_form"):
        log = st.text_area(
            "Paste your punch times",
            height=140,
            placeholder="09:15\n13:00\n14:00\n18:30",
            key="member_input",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("✨ Analyze & Track", use_container_width=True)
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.member_points = pts
            st.success(f"✓ Successfully parsed {len(pts)} time entries")
        else:
            st.error("✗ Please enter valid times in HH:MM format (e.g., 09:15)")
            st.session_state.member_points = None
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📊 Live Dashboard</div>', unsafe_allow_html=True)
    member_live()

with tab2:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 1rem; font-weight: 600;">📅 Day Configuration</div>', unsafe_allow_html=True)
    day_type = st.radio(
        "Select shift type",
        DAY_TYPE_OPTIONS,
        index=0 if st.session_state.leader_day_type == DAY_FULL else 1,
        horizontal=True,
        key="leader_day_radio",
        label_visibility="collapsed"
    )
    st.session_state.leader_day_type = day_type
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 1rem; font-weight: 600;">📝 Biometric Log Input</div>', unsafe_allow_html=True)
    with st.form("leader_form"):
        log = st.text_area(
            "Paste your punch times",
            height=140,
            placeholder="09:15\n13:00\n14:00\n18:30",
            key="leader_input",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("✨ Analyze & Track", use_container_width=True)
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.leader_points = pts
            st.success(f"✓ Successfully parsed {len(pts)} time entries")
        else:
            st.error("✗ Please enter valid times in HH:MM format (e.g., 09:15)")
            st.session_state.leader_points = None
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📊 Live Dashboard</div>', unsafe_allow_html=True)
    leader_live()
