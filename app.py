import datetime as dt
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "Icon.png"
PAGE_ICON = str(ICON_PATH) if ICON_PATH.exists() else "⏱️"
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


# Theme initialization
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None
if "member_day_type" not in st.session_state:
    st.session_state.member_day_type = "Full Day"
if "leader_day_type" not in st.session_state:
    st.session_state.leader_day_type = "Full Day"


# ============================================================================
# CSS - Using triple quotes to avoid f-string issues
# ============================================================================

st.markdown("""
<style>
* {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Light mode */
.stApp {
    background: #f5f7fb;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .stApp {
        background: #0f172a;
    }
}

/* Header */
h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}

/* Stats grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin: 1rem 0;
}

.stat-card {
    background: white;
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    .stat-card {
        background: #1e293b;
        border-color: #334155;
    }
}

.stat-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.5rem;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    font-family: monospace;
    color: #1e293b;
}

@media (prefers-color-scheme: dark) {
    .stat-value {
        color: #f1f5f9;
    }
}

/* Session panels */
.sessions-panel {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1rem 0;
}

.session-card {
    background: white;
    border-radius: 1rem;
    border: 1px solid #e2e8f0;
    overflow: hidden;
}

@media (prefers-color-scheme: dark) {
    .session-card {
        background: #1e293b;
        border-color: #334155;
    }
}

.session-header {
    padding: 0.75rem 1rem;
    font-weight: 600;
    border-bottom: 1px solid #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    .session-header {
        border-color: #334155;
    }
}

.session-header.work {
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
}

.session-header.break {
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
}

.session-row {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    .session-row {
        border-color: #334155;
    }
}

.session-time {
    color: #475569;
}

@media (prefers-color-scheme: dark) {
    .session-time {
        color: #94a3b8;
    }
}

.session-duration {
    font-weight: 600;
}

.session-duration.work {
    color: #3b82f6;
}

.session-duration.break {
    color: #f59e0b;
}

.live-badge {
    background: #10b981;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 0.6rem;
    font-weight: 600;
    color: white;
    margin-left: 8px;
}

/* Logout card */
.logout-card {
    background: white;
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
    margin-top: 1rem;
    border: 1px solid #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    .logout-card {
        background: #1e293b;
        border-color: #334155;
    }
}

.logout-time {
    font-size: 1.5rem;
    font-weight: 700;
    color: #3b82f6;
    font-family: monospace;
}

.success-banner {
    background: linear-gradient(135deg, #10b981, #059669);
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
    margin-top: 1rem;
    animation: pulse 0.5s ease;
}

.success-banner p {
    color: white !important;
    font-weight: 600;
    margin: 0;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 40px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Text area */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    font-family: monospace !important;
}

@media (prefers-color-scheme: dark) {
    .stTextArea textarea {
        background: #1e293b !important;
        border-color: #334155 !important;
        color: white !important;
    }
}

/* Radio buttons */
.stRadio > div {
    gap: 0.5rem;
    background: white;
    padding: 0.5rem;
    border-radius: 60px;
    border: 1px solid #e2e8f0;
    display: inline-flex;
}

@media (prefers-color-scheme: dark) {
    .stRadio > div {
        background: #1e293b;
        border-color: #334155;
    }
}

.stRadio label {
    padding: 0.4rem 1.2rem !important;
    border-radius: 40px !important;
    font-weight: 500 !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0.5rem;
    background: white;
    border-radius: 60px;
    padding: 0.5rem;
    border: 1px solid #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    [data-testid="stTabs"] [role="tablist"] {
        background: #1e293b;
        border-color: #334155;
    }
}

[data-testid="stTabs"] [role="tab"] {
    border-radius: 40px !important;
    padding: 0.4rem 1.2rem !important;
    font-weight: 500 !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: white !important;
}

/* Caption */
.stCaption {
    color: #64748b !important;
}

@media (prefers-color-scheme: dark) {
    .stCaption {
        color: #94a3b8 !important;
    }
}

/* Divider */
hr {
    margin: 1rem 0;
    border-color: #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    hr {
        border-color: #334155;
    }
}
</style>
""", unsafe_allow_html=True)


# ── Utility functions ──────────────────────────────────────────────────────────

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

MEMBER_THRESHOLDS = {DAY_FULL: 27000, DAY_HALF: 16200}
LEADER_THRESHOLDS = {DAY_FULL: 25200, DAY_HALF: 14400}
BREAK_TARGET = 5400


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


# ── Dashboard Render Functions ─────────────────────────────────────────────────

def render_stats_grid(stats: dict):
    cols = st.columns(5)
    
    labels = ["Total Work", "Break Time", "Total Time", "Remaining Work", "Remaining Break"]
    values = [
        stats["total_work"],
        stats["total_break"],
        stats["total_work"] + stats["total_break"],
        stats["remaining_work"],
        stats["remaining_break"]
    ]
    
    for col, label, value in zip(cols, labels, values):
        with col:
            display = format_clock(value) if value > 0 else "✓" if "Remaining" in label and value == 0 else format_clock(value)
            st.metric(label, display)


def render_sessions_panel(work: list, breaks: list):
    st.markdown('<div class="sessions-panel">', unsafe_allow_html=True)
    
    # Work sessions column
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header work">🕐 WORK SESSIONS · {len(work)}</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="session-row"><span class="session-time">No work sessions</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Break sessions column
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header break">☕ BREAK SESSIONS · {len(breaks)}</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="session-row"><span class="session-time">No breaks taken</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_logout_status(deadline: dt.datetime, first: dt.datetime, now: dt.datetime):
    if now < deadline:
        time_str = deadline.strftime("%I:%M %p").lstrip("0")
        if deadline.date() != first.date():
            time_str = deadline.strftime("%d %b, %I:%M %p").lstrip("0")
        st.markdown(
            f'<div class="logout-card">'
            f'<div style="font-size:0.8rem;color:#64748b;">⏰ Earliest Logout Time</div>'
            f'<div class="logout-time">{time_str}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="success-banner">'
            '<p>🎉 TARGET COMPLETED! You\'re Free to Go! 🎉</p>'
            '</div>',
            unsafe_allow_html=True
        )


# ── Dashboard Components ───────────────────────────────────────────────────────

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
    
    st.caption(f"👤 Clocked in: {points[0].strftime('%I:%M %p').lstrip('0')} on {points[0].strftime('%d %b %Y')}")
    
    render_stats_grid(stats)
    
    # Session toggle button
    if result["has_ongoing"]:
        if st.button("📋 Show/Hide Session Details", key="member_session_toggle", use_container_width=True):
            st.session_state.show_member_sessions = not st.session_state.get("show_member_sessions", False)
        
        if st.session_state.get("show_member_sessions", False):
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
    
    st.caption(f"👑 Clocked in: {points[0].strftime('%I:%M %p').lstrip('0')} on {points[0].strftime('%d %b %Y')}")
    
    render_stats_grid(stats)
    
    # Session toggle button
    if result["has_ongoing"]:
        if st.button("📋 Show/Hide Session Details", key="leader_session_toggle", use_container_width=True):
            st.session_state.show_leader_sessions = not st.session_state.get("show_leader_sessions", False)
        
        if st.session_state.get("show_leader_sessions", False):
            render_sessions_panel(result["work_sessions"], result["break_sessions"])
    
    render_logout_status(deadline, points[0], now)


# ── Live Fragments ────────────────────────────────────────────────────────────

@st.fragment(run_every="1s")
def member_live():
    if st.session_state.member_points:
        member_dashboard(st.session_state.member_points, st.session_state.member_day_type)


@st.fragment(run_every="1s")
def leader_live():
    if st.session_state.leader_points:
        leader_dashboard(st.session_state.leader_points, st.session_state.leader_day_type)


# ─── Header ───────────────────────────────────────────────────────────────────

col1, col2, col3 = st.columns([1, 8, 2])

with col1:
    st.markdown('<span style="font-size: 2.5rem;">⏱️</span>', unsafe_allow_html=True)

with col2:
    st.title("TimeTrack Pro")
    st.caption("Intelligent Biometric Time Analysis")

with col3:
    theme_label = "🌙 Dark Mode" if st.session_state.theme_mode == "light" else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"
        st.rerun()

st.caption(f"📍 Pune, India (IST) • {now_pune().strftime('%A, %d %B %Y • %I:%M:%S %p')}")


# ─── Main Tabs ────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["👤 TEAM MEMBER", "👑 TEAM LEADER"])

# TEAM MEMBER TAB
with tab1:
    day_type = st.radio(
        "Day Type",
        DAY_TYPE_OPTIONS,
        index=0 if st.session_state.member_day_type == DAY_FULL else 1,
        horizontal=True,
        key="member_day_radio"
    )
    st.session_state.member_day_type = day_type
    
    with st.form("member_form"):
        log = st.text_area(
            "Biometric Log",
            height=150,
            placeholder="Paste your biometric log here...\n\nExample:\n09:15\n13:00\n14:00\n18:30",
            key="member_input"
        )
        submitted = st.form_submit_button("🔍 Calculate & Track", use_container_width=True)
    
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.member_points = pts
            st.success(f"✅ Successfully parsed {len(pts)} time entries")
        else:
            st.error("❌ Please enter valid times in HH:MM format")
            st.session_state.member_points = None
    
    st.markdown("---")
    st.markdown("### 📊 Live Dashboard")
    member_live()


# TEAM LEADER TAB
with tab2:
    day_type = st.radio(
        "Day Type",
        DAY_TYPE_OPTIONS,
        index=0 if st.session_state.leader_day_type == DAY_FULL else 1,
        horizontal=True,
        key="leader_day_radio"
    )
    st.session_state.leader_day_type = day_type
    
    with st.form("leader_form"):
        log = st.text_area(
            "Biometric Log",
            height=150,
            placeholder="Paste your biometric log here...\n\nExample:\n09:15\n13:00\n14:00\n18:30",
            key="leader_input"
        )
        submitted = st.form_submit_button("🔍 Calculate & Track", use_container_width=True)
    
    if submitted:
        raw = normalize_paste_text(log)
        pts = parse_log(raw)
        if pts:
            st.session_state.leader_points = pts
            st.success(f"✅ Successfully parsed {len(pts)} time entries")
        else:
            st.error("❌ Please enter valid times in HH:MM format")
            st.session_state.leader_points = None
    
    st.markdown("---")
    st.markdown("### 📊 Live Dashboard")
    leader_live()
