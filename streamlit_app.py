import datetime as dt
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "Icon.png"
PAGE_ICON = str(ICON_PATH) if ICON_PATH.exists() else "⏱️"
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
# CSS - Modern Minimal Design (less circular, more professional)
# ============================================================================

def get_theme_css():
    if st.session_state.theme_mode == "light":
        bg = "#f8fafc"
        surface = "#ffffff"
        surface_secondary = "#f1f5f9"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        border = "#e2e8f0"
        accent = "#3b82f6"
        accent_hover = "#2563eb"
        shadow = "0 1px 3px rgba(0,0,0,0.05)"
        shadow_hover = "0 4px 12px rgba(0,0,0,0.08)"
    else:
        bg = "#0f172a"
        surface = "#1e293b"
        surface_secondary = "#334155"
        text_primary = "#f1f5f9"
        text_secondary = "#94a3b8"
        border = "#334155"
        accent = "#3b82f6"
        accent_hover = "#60a5fa"
        shadow = "0 1px 3px rgba(0,0,0,0.3)"
        shadow_hover = "0 4px 12px rgba(0,0,0,0.4)"
    
    return f"""
    <style>
        /* Import */
        @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        
        .stApp {{
            background: {bg};
        }}
        
        /* Main container - no overflow */
        .main .block-container {{
            padding: 1.5rem 2rem;
            max-width: 1400px;
        }}
        
        /* Header - clean border */
        .modern-header {{
            background: {surface};
            border-radius: 12px;
            padding: 1.25rem 2rem;
            margin-bottom: 2rem;
            border: 1px solid {border};
            box-shadow: {shadow};
        }}
        
        h1 {{
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: {text_primary} !important;
            margin: 0 !important;
            letter-spacing: -0.02em;
        }}
        
        .caption {{
            color: {text_secondary};
            font-size: 0.85rem;
            margin-top: 4px;
        }}
        
        /* Stats grid using columns */
        div[data-testid="stMetric"] {{
            background: {surface};
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid {border};
            box-shadow: {shadow};
            transition: all 0.2s ease;
        }}
        
        div[data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: {shadow_hover};
        }}
        
        div[data-testid="stMetric"] label {{
            font-size: 0.7rem !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: {text_secondary} !important;
        }}
        
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
            font-size: 1.75rem !important;
            font-weight: 700;
            color: {text_primary} !important;
        }}
        
        /* Cards for forms */
        .card {{
            background: {surface};
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin: 1rem 0 1.5rem 0;
            border: 1px solid {border};
            box-shadow: {shadow};
        }}
        
        .card-title {{
            font-weight: 600;
            margin-bottom: 1rem;
            color: {text_primary};
            font-size: 0.9rem;
        }}
        
        /* Buttons - less rounded */
        .stButton > button {{
            background: {accent} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.25rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton > button:hover {{
            background: {accent_hover} !important;
            transform: translateY(-1px);
        }}
        
        /* Text area */
        .stTextArea textarea {{
            border-radius: 8px !important;
            border: 1px solid {border} !important;
            background: {surface} !important;
            color: {text_primary} !important;
            font-family: 'Inter', monospace !important;
            font-size: 0.85rem !important;
        }}
        
        .stTextArea textarea:focus {{
            border-color: {accent} !important;
            box-shadow: 0 0 0 2px {accent}30 !important;
        }}
        
        /* Radio buttons - normal, not pill-shaped */
        .stRadio > div {{
            display: flex;
            gap: 1.5rem;
            background: transparent;
        }}
        
        .stRadio label {{
            font-weight: 500;
            color: {text_primary};
        }}
        
        /* Tabs - underline style */
        [data-testid="stTabs"] [role="tablist"] {{
            border-bottom: 2px solid {border};
            gap: 2rem;
            background: transparent;
            padding: 0;
        }}
        
        [data-testid="stTabs"] [role="tab"] {{
            border-radius: 0 !important;
            padding: 0.5rem 0 !important;
            font-weight: 600 !important;
            color: {text_secondary} !important;
            border: none !important;
            background: transparent !important;
        }}
        
        [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
            color: {accent} !important;
            border-bottom: 2px solid {accent} !important;
            background: transparent !important;
        }}
        
        /* Session panels grid */
        .sessions-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
            margin: 1rem 0;
        }}
        
        .session-card {{
            background: {surface};
            border-radius: 12px;
            border: 1px solid {border};
            overflow: hidden;
        }}
        
        .session-header {{
            padding: 0.75rem 1rem;
            font-weight: 600;
            font-size: 0.8rem;
            letter-spacing: 0.3px;
            border-bottom: 1px solid {border};
            background: {surface_secondary};
            color: {text_primary};
        }}
        
        .session-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.6rem 1rem;
            border-bottom: 1px solid {border};
            font-size: 0.85rem;
        }}
        
        .session-time {{
            color: {text_secondary};
        }}
        
        .session-duration {{
            font-weight: 600;
            color: {accent};
        }}
        
        .live-badge {{
            background: #10b981;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.6rem;
            font-weight: 600;
            color: white;
            margin-left: 8px;
        }}
        
        /* Logout card */
        .logout-card {{
            background: {surface};
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin-top: 1rem;
            border: 1px solid {border};
        }}
        
        .logout-time {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {accent};
            font-family: monospace;
        }}
        
        .success-banner {{
            background: #10b981;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin-top: 1rem;
            color: white;
            font-weight: 600;
        }}
        
        hr {{
            margin: 1.5rem 0;
            border-color: {border};
        }}
        
        /* Theme toggle button special */
        div[data-testid="column"]:nth-child(3) .stButton > button {{
            background: {surface_secondary} !important;
            color: {text_primary} !important;
            border: 1px solid {border} !important;
        }}
        
        .section-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin: 1rem 0 0.5rem 0;
            color: {text_primary};
        }}
        
        /* Success/error */
        .stAlert {{
            border-radius: 8px;
            border: none;
        }}
    </style>
    """

# Apply CSS
st.markdown(get_theme_css(), unsafe_allow_html=True)

# ============================================================================
# Helper functions
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
# UI Components
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
    # Work
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header">📋 WORK SESSIONS ({len(work)})</div>', unsafe_allow_html=True)
    if work:
        for s in work:
            live = '<span class="live-badge">LIVE</span>' if s.get("ongoing") else ""
            st.markdown(
                f'<div class="session-row">'
                f'<span class="session-time">{s["start"]} → {s["end"]}{live}</span>'
                f'<span class="session-duration">{s["human"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="session-row"><span class="session-time">None</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # Breaks
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header">☕ BREAK SESSIONS ({len(breaks)})</div>', unsafe_allow_html=True)
    if breaks:
        for s in breaks:
            st.markdown(
                f'<div class="session-row">'
                f'<span class="session-time">{s["start"]} → {s["end"]}</span>'
                f'<span class="session-duration">{s["human"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="session-row"><span class="session-time">None</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_logout_status(deadline: dt.datetime, first: dt.datetime, now: dt.datetime):
    if now < deadline:
        time_str = deadline.strftime("%I:%M %p").lstrip("0")
        if deadline.date() != first.date():
            time_str = deadline.strftime("%d %b, %I:%M %p").lstrip("0")
        st.markdown(
            f'<div class="logout-card">'
            f'<div style="font-size:0.7rem; color:#64748b;">Earliest logout</div>'
            f'<div class="logout-time">{time_str}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="success-banner">✓ Target completed! You\'re free to go.</div>', unsafe_allow_html=True)

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
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if result["has_ongoing"]:
            btn_label = "Hide Details" if st.session_state.show_member_sessions else "Show Session Details"
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
            btn_label = "Hide Details" if st.session_state.show_leader_sessions else "Show Session Details"
            if st.button(btn_label, key="leader_session_toggle", use_container_width=True):
                st.session_state.show_leader_sessions = not st.session_state.show_leader_sessions
                st.rerun()
    if st.session_state.show_leader_sessions:
        render_sessions_panel(result["work_sessions"], result["break_sessions"])
    render_logout_status(deadline, points[0], now)

@st.fragment(run_every="1s")
def member_live():
    if st.session_state.member_points:
        member_dashboard(st.session_state.member_points, st.session_state.member_day_type)

@st.fragment(run_every="1s")
def leader_live():
    if st.session_state.leader_points:
        leader_dashboard(st.session_state.leader_points, st.session_state.leader_day_type)

# ============================================================================
# App Layout
# ============================================================================

# Header
st.markdown('<div class="modern-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 5, 2])
with col1:
    st.markdown('<span style="font-size: 2rem;">⏱️</span>', unsafe_allow_html=True)
with col2:
    st.title("TimeTrack Pro")
    st.markdown('<div class="caption">Intelligent time analytics with live tracking</div>', unsafe_allow_html=True)
with col3:
    theme_label = "🌙 Dark Mode" if st.session_state.theme_mode == "light" else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"
        st.rerun()
st.markdown(f'<div class="caption">📍 Pune, India (IST) • {now_pune().strftime("%A, %d %B %Y • %I:%M:%S %p")}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["TEAM MEMBER", "TEAM LEADER"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📅 Day Configuration</div>', unsafe_allow_html=True)
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
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 Biometric Log Input</div>', unsafe_allow_html=True)
    with st.form("member_form"):
        log = st.text_area(
            "Paste punch times (HH:MM format)",
            height=120,
            placeholder="09:15\n13:00\n14:00\n18:30",
            key="member_input",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("Analyze & Track", use_container_width=True)
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.member_points = pts
            st.success(f"✓ Parsed {len(pts)} time entries")
        else:
            st.error("✗ Invalid format. Use HH:MM (e.g., 09:15)")
            st.session_state.member_points = None
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📊 Live Dashboard</div>', unsafe_allow_html=True)
    member_live()

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📅 Day Configuration</div>', unsafe_allow_html=True)
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
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 Biometric Log Input</div>', unsafe_allow_html=True)
    with st.form("leader_form"):
        log = st.text_area(
            "Paste punch times (HH:MM format)",
            height=120,
            placeholder="09:15\n13:00\n14:00\n18:30",
            key="leader_input",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("Analyze & Track", use_container_width=True)
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.leader_points = pts
            st.success(f"✓ Parsed {len(pts)} time entries")
        else:
            st.error("✗ Invalid format. Use HH:MM (e.g., 09:15)")
            st.session_state.leader_points = None
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📊 Live Dashboard</div>', unsafe_allow_html=True)
    leader_live()
