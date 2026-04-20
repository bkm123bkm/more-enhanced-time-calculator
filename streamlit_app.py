import datetime as dt
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "Icon.png"
PAGE_ICON = str(ICON_PATH) if ICON_PATH.exists() else "⚡"
PUNE_TZ = ZoneInfo("Asia/Kolkata")

# Widget keys
MEMBER_DAY_WIDGET_KEY = "_ui_member_day_type"
LEADER_DAY_WIDGET_KEY = "_ui_leader_day_type"
MEMBER_PASTE_WIDGET_KEY = "_ui_member_paste"
LEADER_PASTE_WIDGET_KEY = "_ui_leader_paste"
MEMBER_DAY_QUERY = "member_day"
LEADER_DAY_QUERY = "leader_day"


def now_pune() -> dt.datetime:
    return dt.datetime.now(PUNE_TZ).replace(tzinfo=None)


st.set_page_config(
    page_title="TimeTrack Pro",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================================
# BRAND NEW UI DESIGN - MINIMALIST MODERN
# ============================================================================

st.markdown(
    """
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', system-ui, sans-serif !important;
    }
    
    /* Light Theme */
    [data-theme="light"] {
        --bg: #f5f7fb;
        --surface: #ffffff;
        --surface-2: #f8f9fc;
        --text: #1a1f36;
        --text-2: #4a5568;
        --text-3: #a0aec0;
        --border: #e2e8f0;
        --primary: #3b82f6;
        --primary-dark: #2563eb;
        --primary-glow: rgba(59, 130, 246, 0.15);
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --card-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 10px 25px -5px rgba(0,0,0,0.05);
        --hover-shadow: 0 20px 25px -5px rgba(0,0,0,0.08), 0 10px 10px -5px rgba(0,0,0,0.02);
    }
    
    /* Dark Theme */
    [data-theme="dark"] {
        --bg: #0a0c10;
        --surface: #14161c;
        --surface-2: #1a1d24;
        --text: #e2e8f0;
        --text-2: #94a3b8;
        --text-3: #64748b;
        --border: #2d3748;
        --primary: #60a5fa;
        --primary-dark: #3b82f6;
        --primary-glow: rgba(96, 165, 250, 0.15);
        --success: #34d399;
        --warning: #fbbf24;
        --danger: #f87171;
        --card-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 10px 25px -5px rgba(0,0,0,0.2);
        --hover-shadow: 0 20px 25px -5px rgba(0,0,0,0.3), 0 10px 10px -5px rgba(0,0,0,0.1);
    }
    
    /* Base */
    .stApp {
        background: var(--bg);
        transition: all 0.2s ease;
    }
    
    .block-container {
        max-width: 1300px !important;
        padding: 2rem !important;
    }
    
    /* Typography */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        margin-bottom: 0.25rem !important;
        letter-spacing: -0.02em !important;
    }
    
    p, .stMarkdown, .stCaption {
        color: var(--text-2) !important;
    }
    
    /* Custom Card */
    .card {
        background: var(--surface);
        border-radius: 24px;
        border: 1px solid var(--border);
        padding: 1.5rem;
        transition: all 0.2s ease;
        box-shadow: var(--card-shadow);
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: var(--hover-shadow);
    }
    
    /* Role Header */
    .role-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid var(--primary);
    }
    
    .role-icon {
        font-size: 32px;
    }
    
    .role-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text);
    }
    
    /* Day Type Toggle */
    .day-toggle {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .day-option {
        flex: 1;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        background: var(--surface-2);
        border: 1px solid var(--border);
        color: var(--text-2);
        font-weight: 500;
    }
    
    .day-option.active {
        background: var(--primary);
        border-color: var(--primary);
        color: white;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin: 20px 0;
    }
    
    .stat-card {
        background: var(--surface-2);
        border-radius: 20px;
        padding: 16px;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary);
    }
    
    .stat-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-3);
        margin-bottom: 8px;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        font-family: monospace;
    }
    
    /* Session Panel */
    .session-panel {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 20px;
    }
    
    .session-card {
        background: var(--surface-2);
        border-radius: 20px;
        border: 1px solid var(--border);
        overflow: hidden;
    }
    
    .session-header {
        padding: 12px 16px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid var(--border);
    }
    
    .session-header.work {
        background: rgba(59, 130, 246, 0.1);
        color: var(--primary);
    }
    
    .session-header.break {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning);
    }
    
    .session-row {
        display: flex;
        justify-content: space-between;
        padding: 10px 16px;
        border-bottom: 1px solid var(--border);
        font-size: 0.85rem;
    }
    
    .session-row:last-child {
        border-bottom: none;
    }
    
    .session-time {
        color: var(--text-2);
    }
    
    .session-duration {
        font-weight: 600;
    }
    
    .session-duration.work { color: var(--primary); }
    .session-duration.break { color: var(--warning); }
    
    .live-badge {
        background: var(--success);
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.6rem;
        font-weight: 600;
        color: white;
        margin-left: 8px;
    }
    
    /* Logout Info */
    .logout-info {
        background: var(--surface);
        border-radius: 16px;
        padding: 16px;
        margin-top: 20px;
        text-align: center;
        border: 1px solid var(--border);
    }
    
    .logout-time {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    .success-banner {
        background: linear-gradient(135deg, var(--success), #059669);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        color: white;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: var(--text) !important;
        font-size: 0.85rem !important;
        font-family: monospace !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-glow) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-1px);
    }
    
    /* Toggle Button */
    .theme-toggle {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 40px !important;
        padding: 8px 20px !important;
        font-size: 0.85rem !important;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        gap: 8px;
    }
    
    .stRadio label {
        background: var(--surface-2);
        padding: 8px 20px;
        border-radius: 40px;
        border: 1px solid var(--border);
        color: var(--text-2);
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface-2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Utility functions ──────────────────────────────────────────────────────────

def hms_to_seconds(hours: int, minutes: int, seconds: int) -> int:
    return (hours * 3600) + (minutes * 60) + seconds


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


# ── Constants ──────────────────────────────────────────────────────────────────

DAY_FULL = "Full Day"
DAY_HALF = "Half Day"
DAY_TYPE_OPTIONS = (DAY_FULL, DAY_HALF)

MEMBER_THRESHOLDS = {DAY_FULL: 27000, DAY_HALF: 16200}  # 7h30m, 4h30m
LEADER_THRESHOLDS = {DAY_FULL: 25200, DAY_HALF: 14400}  # 7h, 4h
BREAK_TARGET = 5400  # 1h30m


def member_threshold(day_type: str) -> int:
    return MEMBER_THRESHOLDS.get(day_type, 27000)


def leader_threshold(day_type: str) -> int:
    return LEADER_THRESHOLDS.get(day_type, 25200)


# ── Parsing ────────────────────────────────────────────────────────────────────

def extract_times(log_text: str) -> list[dt.datetime]:
    matches = re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", log_text)
    today = now_pune().date()
    points = []
    last = None
    
    for m in matches:
        h, m = map(int, m.split(":"))
        candidate = dt.datetime.combine(today, dt.time(h, m))
        if last and candidate < last:
            today += dt.timedelta(days=1)
            candidate = dt.datetime.combine(today, dt.time(h, m))
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
    ongoing_text = None
    
    if len(points) % 2 == 1:
        last = points[-1]
        if current < last:
            current += dt.timedelta(days=1)
        ongoing = int((current - last).total_seconds())
        ongoing_text = "ongoing"
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
        "has_ongoing": ongoing_text is not None
    }


# ── Dashboard Components ───────────────────────────────────────────────────────

def render_stats(stats: dict):
    cols = st.columns(5)
    
    metrics = [
        ("Total Work", stats["total_work"]),
        ("Break Time", stats["total_break"]),
        ("Total Time", stats["total_work"] + stats["total_break"]),
        ("Remaining Work", stats["remaining_work"]),
        ("Remaining Break", stats["remaining_break"])
    ]
    
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{format_clock(value) if value > 0 else "—"}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_sessions(work: list, breaks: list):
    work_html = "".join([
        f'<div class="session-row"><span class="session-time">{s["start"]} → {s["end"]}{" <span class="live-badge">LIVE</span>" if s.get("ongoing") else ""}</span><span class="session-duration work">{s["human"]}</span></div>'
        for s in work
    ]) or '<div class="session-row"><span class="session-time">No sessions</span></div>'
    
    break_html = "".join([
        f'<div class="session-row"><span class="session-time">{s["start"]} → {s["end"]}</span><span class="session-duration break">{s["human"]}</span></div>'
        for s in breaks
    ]) or '<div class="session-row"><span class="session-time">No breaks</span></div>'
    
    st.markdown(
        f"""
        <div class="session-panel">
            <div class="session-card">
                <div class="session-header work">🕐 WORK · {len(work)} sessions</div>
                {work_html}
            </div>
            <div class="session-card">
                <div class="session-header break">☕ BREAK · {len(breaks)} sessions</div>
                {break_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_logout(deadline: dt.datetime, first: dt.datetime, now: dt.datetime):
    if now < deadline:
        time_str = deadline.strftime("%I:%M %p").lstrip("0")
        if deadline.date() != first.date():
            time_str = deadline.strftime("%d %b, %I:%M %p").lstrip("0")
        st.markdown(
            f"""
            <div class="logout-info">
                <div style="margin-bottom: 4px; font-size: 0.8rem; color: var(--text-3);">Earliest Logout Time</div>
                <div class="logout-time">{time_str}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="success-banner">🎉 Target Completed! You\'re Free to Go! 🎉</div>',
            unsafe_allow_html=True
        )


# ── Role Dashboard ────────────────────────────────────────────────────────────

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
    
    st.caption(f"Clocked in: {points[0].strftime('%I:%M %p').lstrip('0')} on {points[0].strftime('%d %b %Y')}")
    
    render_stats(stats)
    
    if result["has_ongoing"]:
        if st.button("📊 Show/Hide Session Details", use_container_width=True, key=f"toggle_{id(points)}"):
            st.session_state[f"show_sessions_{id(points)}"] = not st.session_state.get(f"show_sessions_{id(points)}", False)
        
        if st.session_state.get(f"show_sessions_{id(points)}", False):
            render_sessions(result["work_sessions"], result["break_sessions"])
    
    render_logout(deadline, points[0], now)


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
    
    st.caption(f"Clocked in: {points[0].strftime('%I:%M %p').lstrip('0')} on {points[0].strftime('%d %b %Y')}")
    
    render_stats(stats)
    
    if result["has_ongoing"]:
        if st.button("📊 Show/Hide Session Details", use_container_width=True, key=f"toggle_leader_{id(points)}"):
            st.session_state[f"show_leader_sessions_{id(points)}"] = not st.session_state.get(f"show_leader_sessions_{id(points)}", False)
        
        if st.session_state.get(f"show_leader_sessions_{id(points)}", False):
            render_sessions(result["work_sessions"], result["break_sessions"])
    
    render_logout(deadline, points[0], now)


# ── Live Fragments ────────────────────────────────────────────────────────────

@st.fragment(run_every="1s")
def member_live():
    points = st.session_state.get("member_points")
    if points:
        member_dashboard(points, st.session_state.member_day_type)


@st.fragment(run_every="1s")
def leader_live():
    points = st.session_state.get("leader_points")
    if points:
        leader_dashboard(points, st.session_state.leader_day_type)


# ─── Session State ────────────────────────────────────────────────────────────

if "member_day_type" not in st.session_state:
    st.session_state.member_day_type = DAY_FULL
if "leader_day_type" not in st.session_state:
    st.session_state.leader_day_type = DAY_FULL
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None
if "theme" not in st.session_state:
    st.session_state.theme = "light"


# ─── Theme ─────────────────────────────────────────────────────────────────────

theme_attr = f'data-theme="{st.session_state.theme}"'
st.markdown(f'<body {theme_attr}></body>', unsafe_allow_html=True)


# ─── Header ───────────────────────────────────────────────────────────────────

col1, col2, col3 = st.columns([1, 8, 2])

with col1:
    st.markdown('<span style="font-size: 42px;">⏱️</span>', unsafe_allow_html=True)

with col2:
    st.markdown('<h1>TimeTrack Pro</h1><p style="margin-top: -8px;">Biometric Time Intelligence</p>', unsafe_allow_html=True)

with col3:
    theme_label = "🌙 Dark" if st.session_state.theme == "light" else "☀️ Light"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

st.caption(f"📍 Pune, IST • {now_pune().strftime('%A, %d %b %Y • %I:%M:%S %p')}")


# ─── Main Tabs ────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["👤 TEAM MEMBER", "👑 TEAM LEADER"])

# ==================== TEAM MEMBER TAB ====================
with tab1:
    # Day Type Selection
    col_a, col_b = st.columns([1, 1])
    with col_a:
        full_active = "active" if st.session_state.member_day_type == DAY_FULL else ""
        half_active = "active" if st.session_state.member_day_type == DAY_HALF else ""
        st.markdown(
            f"""
            <div class="day-toggle">
                <div class="day-option {full_active}" onclick="parent.postMessage({{type: 'streamlit:setComponentValue', key: 'member_day_full', value: 'Full Day'}}, '*')">📅 Full Day<br><span style="font-size: 0.7rem;">7h 30m</span></div>
                <div class="day-option {half_active}" onclick="parent.postMessage({{type: 'streamlit:setComponentValue', key: 'member_day_half', value: 'Half Day'}}, '*')">📆 Half Day<br><span style="font-size: 0.7rem;">4h 30m</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Radio fallback
    day_type = st.radio(
        "Day Type",
        DAY_TYPE_OPTIONS,
        index=0 if st.session_state.member_day_type == DAY_FULL else 1,
        horizontal=True,
        key="member_day_radio",
        label_visibility="collapsed"
    )
    if day_type != st.session_state.member_day_type:
        st.session_state.member_day_type = day_type
        st.query_params[MEMBER_DAY_QUERY] = day_type
    
    # Input Form
    with st.form("member_form"):
        log = st.text_area(
            "Biometric Log",
            height=150,
            placeholder="Paste your biometric log here...\n\n09:15\n13:00\n14:00\n18:30",
            key="member_input",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("🔍 Calculate & Track", use_container_width=True)
    
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.member_points = pts
            st.success(f"✅ Parsed {len(pts)} time entries")
        else:
            st.error("❌ Please enter valid times (HH:MM format)")
            st.session_state.member_points = None
    
    # Live Dashboard
    st.markdown("---")
    st.markdown("### 📊 Live Dashboard")
    member_live()


# ==================== TEAM LEADER TAB ====================
with tab2:
    # Day Type Selection
    full_active = "active" if st.session_state.leader_day_type == DAY_FULL else ""
    half_active = "active" if st.session_state.leader_day_type == DAY_HALF else ""
    st.markdown(
        f"""
        <div class="day-toggle">
            <div class="day-option {full_active}">📅 Full Day<br><span style="font-size: 0.7rem;">7h 00m</span></div>
            <div class="day-option {half_active}">📆 Half Day<br><span style="font-size: 0.7rem;">4h 00m</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Radio fallback
    leader_day = st.radio(
        "Day Type",
        DAY_TYPE_OPTIONS,
        index=0 if st.session_state.leader_day_type == DAY_FULL else 1,
        horizontal=True,
        key="leader_day_radio",
        label_visibility="collapsed"
    )
    if leader_day != st.session_state.leader_day_type:
        st.session_state.leader_day_type = leader_day
        st.query_params[LEADER_DAY_QUERY] = leader_day
    
    # Input Form
    with st.form("leader_form"):
        log = st.text_area(
            "Biometric Log",
            height=150,
            placeholder="Paste your biometric log here...\n\n09:15\n13:00\n14:00\n18:30",
            key="leader_input",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("🔍 Calculate & Track", use_container_width=True)
    
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.leader_points = pts
            st.success(f"✅ Parsed {len(pts)} time entries")
        else:
            st.error("❌ Please enter valid times (HH:MM format)")
            st.session_state.leader_points = None
    
    # Live Dashboard
    st.markdown("---")
    st.markdown("### 📊 Live Dashboard")
    leader_live()
