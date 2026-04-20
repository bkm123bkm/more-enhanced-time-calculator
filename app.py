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


# ============================================================================
# BEAUTIFUL MODERN UI WITH WORKING DARK/LIGHT MODE
# ============================================================================

# Theme initialization
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

# Apply theme class to body
theme_class = "dark-mode" if st.session_state.theme_mode == "dark" else "light-mode"

st.markdown(
    f"""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
    }}
    
    /* Light Mode Variables */
    .light-mode {{
        --bg-primary: #f8fafc;
        --bg-secondary: #ffffff;
        --bg-tertiary: #f1f5f9;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --primary: #3b82f6;
        --primary-dark: #2563eb;
        --primary-light: #dbeafe;
        --success: #10b981;
        --success-light: #d1fae5;
        --warning: #f59e0b;
        --danger: #ef4444;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }}
    
    /* Dark Mode Variables */
    .dark-mode {{
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --border: #334155;
        --border-light: #1e293b;
        --primary: #60a5fa;
        --primary-dark: #3b82f6;
        --primary-light: #1e3a8a;
        --success: #34d399;
        --success-light: #064e3b;
        --warning: #fbbf24;
        --danger: #f87171;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }}
    
    /* Apply variables */
    .stApp {{
        background: var(--bg-primary);
        transition: all 0.3s ease;
    }}
    
    .block-container {{
        max-width: 1400px !important;
        padding: 2rem !important;
    }}
    
    /* Typography */
    h1, h2, h3 {{
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}
    
    h1 {{
        font-size: 2.2rem !important;
        background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
    }}
    
    p, .stMarkdown, .stCaption, label {{
        color: var(--text-secondary) !important;
    }}
    
    /* Header Section */
    .header-section {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border);
    }}
    
    .logo-area {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .logo-icon {{
        font-size: 3rem;
        background: linear-gradient(135deg, var(--primary), #8b5cf6);
        border-radius: 20px;
        padding: 0.5rem;
        display: inline-block;
    }}
    
    /* Stats Grid */
    .stats-container {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }}
    
    .stat-box {{
        background: var(--bg-secondary);
        border-radius: 20px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }}
    
    .stat-box:hover {{
        transform: translateY(-4px);
        border-color: var(--primary);
        box-shadow: var(--shadow-lg);
    }}
    
    .stat-label {{
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }}
    
    .stat-value {{
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--text-primary);
        font-family: 'Monaco', monospace;
    }}
    
    /* Session Cards */
    .sessions-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }}
    
    .session-box {{
        background: var(--bg-secondary);
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }}
    
    .session-box:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl);
    }}
    
    .session-title {{
        padding: 1rem 1.25rem;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 2px solid var(--border);
    }}
    
    .session-title.work {{
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), transparent);
        color: var(--primary);
    }}
    
    .session-title.break {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), transparent);
        color: var(--warning);
    }}
    
    .session-item {{
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 1.25rem;
        border-bottom: 1px solid var(--border-light);
        transition: background 0.2s ease;
    }}
    
    .session-item:hover {{
        background: var(--bg-tertiary);
    }}
    
    .session-time {{
        color: var(--text-secondary);
        font-size: 0.85rem;
    }}
    
    .session-duration {{
        font-weight: 700;
        font-size: 0.85rem;
    }}
    
    .session-duration.work {{
        color: var(--primary);
    }}
    
    .session-duration.break {{
        color: var(--warning);
    }}
    
    .live-tag {{
        background: var(--success);
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.6rem;
        font-weight: 700;
        color: white;
        margin-left: 0.5rem;
        display: inline-block;
    }}
    
    /* Logout Card */
    .logout-card {{
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border-radius: 20px;
        padding: 1.25rem;
        text-align: center;
        margin-top: 1.5rem;
        border: 1px solid var(--border);
    }}
    
    .logout-label {{
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }}
    
    .logout-time {{
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--primary);
        font-family: monospace;
    }}
    
    .success-card {{
        background: linear-gradient(135deg, var(--success), #059669);
        border-radius: 20px;
        padding: 1.25rem;
        text-align: center;
        margin-top: 1.5rem;
        animation: pulse 0.5s ease-out;
    }}
    
    .success-card p {{
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 0;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(0.95); opacity: 0; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    /* Text Area */
    .stTextArea textarea {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
        font-family: 'Monaco', monospace !important;
    }}
    
    .stTextArea textarea:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }}
    
    /* Theme Toggle Button */
    .theme-btn {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 40px !important;
        padding: 0.5rem 1.2rem !important;
        font-size: 0.85rem !important;
    }}
    
    /* Radio Buttons - Day Type */
    .stRadio > div {{
        gap: 0.75rem;
        background: var(--bg-secondary);
        padding: 0.5rem;
        border-radius: 60px;
        border: 1px solid var(--border);
        display: inline-flex;
    }}
    
    .stRadio label {{
        background: transparent !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 40px !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
    }}
    
    .stRadio label:hover {{
        color: var(--primary) !important;
    }}
    
    /* Tabs */
    [data-testid="stTabs"] [role="tablist"] {{
        gap: 0.5rem;
        background: var(--bg-secondary);
        border-radius: 60px;
        padding: 0.5rem;
        border: 1px solid var(--border);
    }}
    
    [data-testid="stTabs"] [role="tab"] {{
        border-radius: 40px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
    }}
    
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
        background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
        color: white !important;
    }}
    
    [data-testid="stTabs"] [role="tabpanel"] {{
        padding-top: 1.5rem;
    }}
    
    /* Alerts */
    .stAlert {{
        border-radius: 16px !important;
        border: none !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-tertiary);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--primary);
        border-radius: 10px;
    }}
    
    /* Divider */
    hr {{
        margin: 1.5rem 0;
        border-color: var(--border);
    }}
    
    /* Info text */
    .info-text {{
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
    }}
    </style>
    
    <script>
        document.body.className = '{theme_class}';
    </script>
    """,
    unsafe_allow_html=True,
)


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
    st.markdown(
        f"""
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-label">Total Work</div>
                <div class="stat-value">{format_clock(stats['total_work'])}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Break Time</div>
                <div class="stat-value">{format_clock(stats['total_break'])}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Time</div>
                <div class="stat-value">{format_clock(stats['total_work'] + stats['total_break'])}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Remaining Work</div>
                <div class="stat-value">{format_clock(stats['remaining_work']) if stats['remaining_work'] > 0 else "✓"}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Remaining Break</div>
                <div class="stat-value">{format_clock(stats['remaining_break']) if stats['remaining_break'] > 0 else "✓"}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sessions_panel(work: list, breaks: list):
    # Build work HTML
    work_html = ""
    for s in work:
        live_tag = '<span class="live-tag">LIVE</span>' if s.get("ongoing") else ""
        work_html += f'''
            <div class="session-item">
                <span class="session-time">{s["start"]} → {s["end"]}{live_tag}</span>
                <span class="session-duration work">{s["human"]}</span>
            </div>
        '''
    
    if not work_html:
        work_html = '<div class="session-item"><span class="session-time">No work sessions</span></div>'
    
    # Build break HTML
    break_html = ""
    for s in breaks:
        break_html += f'''
            <div class="session-item">
                <span class="session-time">{s["start"]} → {s["end"]}</span>
                <span class="session-duration break">{s["human"]}</span>
            </div>
        '''
    
    if not break_html:
        break_html = '<div class="session-item"><span class="session-time">No breaks taken</span></div>'
    
    st.markdown(
        f"""
        <div class="sessions-grid">
            <div class="session-box">
                <div class="session-title work">🕐 WORK SESSIONS · {len(work)}</div>
                {work_html}
            </div>
            <div class="session-box">
                <div class="session-title break">☕ BREAK SESSIONS · {len(breaks)}</div>
                {break_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_logout_status(deadline: dt.datetime, first: dt.datetime, now: dt.datetime):
    if now < deadline:
        time_str = deadline.strftime("%I:%M %p").lstrip("0")
        if deadline.date() != first.date():
            time_str = deadline.strftime("%d %b, %I:%M %p").lstrip("0")
        st.markdown(
            f"""
            <div class="logout-card">
                <div class="logout-label">⏰ Earliest Logout Time</div>
                <div class="logout-time">{time_str}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return True
    else:
        st.markdown(
            '<div class="success-card"><p>🎉 TARGET COMPLETED! You\'re Free to Go! 🎉</p></div>',
            unsafe_allow_html=True
        )
        return False


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
    
    # Show/hide sessions button - always show when there's an active session
    show_key = f"show_member_sessions_{id(points)}"
    if result["has_ongoing"]:
        if st.button("📋 Show/Hide Session Details", use_container_width=True, key=show_key):
            st.session_state[show_key] = not st.session_state.get(show_key, False)
        
        if st.session_state.get(show_key, False):
            render_sessions_panel(result["work_sessions"], result["break_sessions"])
    
    # Logout status
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
    
    # Show/hide sessions button - always show when there's an active session
    show_key = f"show_leader_sessions_{id(points)}"
    if result["has_ongoing"]:
        if st.button("📋 Show/Hide Session Details", use_container_width=True, key=show_key):
            st.session_state[show_key] = not st.session_state.get(show_key, False)
        
        if st.session_state.get(show_key, False):
            render_sessions_panel(result["work_sessions"], result["break_sessions"])
    
    # Logout status
    render_logout_status(deadline, points[0], now)


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


# ─── Session State Initialization ─────────────────────────────────────────────

if "member_day_type" not in st.session_state:
    st.session_state.member_day_type = DAY_FULL
if "leader_day_type" not in st.session_state:
    st.session_state.leader_day_type = DAY_FULL
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None


# ─── Header ───────────────────────────────────────────────────────────────────

col1, col2, col3 = st.columns([1, 8, 2])

with col1:
    st.markdown('<div class="logo-icon">⏱️</div>', unsafe_allow_html=True)

with col2:
    st.markdown(
        """
        <h1>TimeTrack Pro</h1>
        <p style="margin-top: -8px;">Intelligent Biometric Time Analysis</p>
        """,
        unsafe_allow_html=True
    )

with col3:
    theme_label = "🌙 Dark Mode" if st.session_state.theme_mode == "light" else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"
        st.rerun()

st.caption(f"📍 Pune, India (IST) • {now_pune().strftime('%A, %d %B %Y • %I:%M:%S %p')}")


# ─── Main Tabs ────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["👤 TEAM MEMBER", "👑 TEAM LEADER"])

# ==================== TEAM MEMBER TAB ====================
with tab1:
    # Day Type Selection
    member_day = st.radio(
        "Select Day Type",
        DAY_TYPE_OPTIONS,
        index=0 if st.session_state.member_day_type == DAY_FULL else 1,
        horizontal=True,
        key="member_day_radio",
        label_visibility="collapsed"
    )
    if member_day != st.session_state.member_day_type:
        st.session_state.member_day_type = member_day
        st.query_params[MEMBER_DAY_QUERY] = member_day
    
    # Input Form
    with st.form("member_form"):
        log = st.text_area(
            "Biometric Log",
            height=150,
            placeholder="Paste your biometric log here...\n\nExample:\n09:15\n13:00\n14:00\n18:30",
            key="member_input",
            label_visibility="collapsed"
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


# ==================== TEAM LEADER TAB ====================
with tab2:
    # Day Type Selection
    leader_day = st.radio(
        "Select Day Type",
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
            placeholder="Paste your biometric log here...\n\nExample:\n09:15\n13:00\n14:00\n18:30",
            key="leader_input",
            label_visibility="collapsed"
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
