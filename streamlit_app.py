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
    page_title="Chronos | Time Intelligence",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================================
# COMPLETE MODERN REDESIGN WITH GLASSMORPHISM
# ============================================================================

st.markdown(
    """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&display=swap');
    
    * {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Theme Variables - Light Mode (Default) */
    :root {
        --bg-primary: #f0f4f8;
        --bg-secondary: #ffffff;
        --bg-glass: rgba(255, 255, 255, 0.85);
        --text-primary: #1a1a2e;
        --text-secondary: #4a5568;
        --text-muted: #718096;
        --border: #e2e8f0;
        --border-glow: rgba(79, 70, 229, 0.15);
        --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        --accent: #6366f1;
        --accent-dark: #4f46e5;
        --accent-glow: rgba(99, 102, 241, 0.2);
        --success: #10b981;
        --warning: #f59e0b;
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Dark Mode Styles */
    [data-theme="dark"] {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-glass: rgba(30, 41, 59, 0.85);
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border: #334155;
        --border-glow: rgba(99, 102, 241, 0.2);
        --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        --accent: #818cf8;
        --accent-dark: #6366f1;
        --accent-glow: rgba(129, 140, 248, 0.25);
    }
    
    /* Global Styles */
    .stApp {
        background: var(--bg-primary);
        transition: background 0.3s ease;
    }
    
    .block-container {
        max-width: 1400px !important;
        padding: 1.5rem 2rem !important;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Typography - Ensure all text is visible */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
    }
    
    p, span, div, label, .stMarkdown, .stCaption, .stText {
        color: var(--text-secondary) !important;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: var(--bg-glass) !important;
        backdrop-filter: blur(10px);
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 1rem 1.25rem !important;
        transition: all 0.3s ease !important;
        animation: scaleIn 0.4s ease-out forwards;
        opacity: 0;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: var(--accent) !important;
        box-shadow: 0 20px 35px -12px var(--accent-glow) !important;
    }
    
    div[data-testid="stMetricLabel"] p {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-muted) !important;
    }
    
    div[data-testid="stMetricValue"] p {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: var(--bg-glass) !important;
        backdrop-filter: blur(8px);
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        padding: 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Buttons */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px var(--accent-glow) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Tabs */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 0.5rem !important;
        background: var(--bg-glass) !important;
        backdrop-filter: blur(8px);
        border-radius: 60px !important;
        padding: 0.5rem !important;
        border: 1px solid var(--border) !important;
    }
    
    [data-testid="stTabs"] [role="tab"] {
        border-radius: 40px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stTabs"] [role="tab"]:hover {
        color: var(--accent) !important;
        background: rgba(99, 102, 241, 0.1) !important;
    }
    
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px var(--accent-glow) !important;
    }
    
    [data-testid="stTabs"] [role="tabpanel"] {
        animation: fadeInUp 0.4s ease-out;
        padding-top: 1.5rem;
    }
    
    /* Radio Buttons */
    [data-testid="stRadio"] {
        background: var(--bg-glass);
        backdrop-filter: blur(8px);
        border-radius: 60px;
        padding: 0.5rem;
        border: 1px solid var(--border);
        display: inline-flex;
    }
    
    [data-testid="stRadio"] label {
        border-radius: 40px !important;
        padding: 0.4rem 1.2rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stRadio"] label:hover {
        color: var(--accent) !important;
    }
    
    [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
        background-color: transparent !important;
    }
    
    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 16px !important;
        border: none !important;
        backdrop-filter: blur(8px);
        animation: fadeInLeft 0.3s ease-out !important;
    }
    
    div[data-testid="stAlert"]:has(svg[data-testid="stAlertInfo"]) {
        background: rgba(59, 130, 246, 0.15) !important;
        border-left: 4px solid #3b82f6 !important;
    }
    
    div[data-testid="stAlert"]:has(svg[data-testid="stAlertSuccess"]) {
        background: rgba(16, 185, 129, 0.15) !important;
        border-left: 4px solid #10b981 !important;
    }
    
    div[data-testid="stAlert"]:has(svg[data-testid="stAlertError"]) {
        background: rgba(239, 68, 68, 0.15) !important;
        border-left: 4px solid #ef4444 !important;
    }
    
    div[data-testid="stAlert"] p {
        color: var(--text-primary) !important;
    }
    
    /* Session Panel */
    .session-panel {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .session-card {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid var(--border);
        overflow: hidden;
        transition: all 0.3s ease;
        animation: fadeInUp 0.4s ease-out;
    }
    
    .session-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent);
    }
    
    .session-header {
        padding: 1rem 1.25rem;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid var(--border);
    }
    
    .session-header.work {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), transparent);
        color: #818cf8;
    }
    
    .session-header.break {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), transparent);
        color: #f59e0b;
    }
    
    .session-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1.25rem;
        border-bottom: 1px solid var(--border);
        transition: background 0.2s ease;
    }
    
    .session-item:hover {
        background: var(--accent-glow);
    }
    
    .session-item:last-child {
        border-bottom: none;
    }
    
    .session-time {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    .session-duration {
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    .session-duration.work { color: #818cf8; }
    .session-duration.break { color: #f59e0b; }
    
    .live-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        color: white;
        margin-left: 0.5rem;
        display: inline-block;
    }
    
    /* Hooray Banner */
    .hooray-banner {
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 20px;
        padding: 1rem 1.5rem;
        text-align: center;
        margin-top: 1rem;
        animation: pulse 0.6s ease-out;
    }
    
    .hooray-banner p {
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Summary Box */
    .summary-box {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid var(--border);
        padding: 1.25rem;
        margin-top: 1rem;
        line-height: 1.8;
    }
    
    .summary-box strong {
        color: var(--text-primary);
    }
    
    /* Caption */
    .stCaption {
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
    }
    
    /* Divider */
    hr {
        margin: 1rem 0;
        border-color: var(--border);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-dark);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Utility functions ──────────────────────────────────────────────────────────

def hms_to_seconds(hours: int, minutes: int, seconds: int) -> int:
    return (hours * 3_600) + (minutes * 60) + seconds


def format_short(total_seconds: int) -> str:
    total_seconds = max(total_seconds, 0)
    h = total_seconds // 3_600
    m = (total_seconds % 3_600) // 60
    s = total_seconds % 60
    return f"{h}h {m:02d}m {s:02d}s"


def format_clock(total_seconds: int) -> str:
    total_seconds = max(total_seconds, 0)
    h = total_seconds // 3_600
    m = (total_seconds % 3_600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def format_human(total_seconds: int) -> str:
    total_seconds = max(total_seconds, 0)
    h = total_seconds // 3_600
    m = (total_seconds % 3_600) // 60
    parts = []
    if h:
        parts.append(f"{h} hr{'s' if h != 1 else ''}")
    if m or not h:
        parts.append(f"{m} min{'s' if m != 1 else ''}")
    return " ".join(parts)


# ── Constants ──────────────────────────────────────────────────────────────────

DAY_FULL = "Full Day"
DAY_HALF = "Half Day"
DAY_TYPE_OPTIONS = (DAY_FULL, DAY_HALF)

MEMBER_THRESHOLDS: dict[str, int] = {
    DAY_FULL: hms_to_seconds(7, 30, 0),
    DAY_HALF: hms_to_seconds(4, 30, 0),
}
LEADER_THRESHOLDS: dict[str, int] = {
    DAY_FULL: hms_to_seconds(7, 0, 0),
    DAY_HALF: hms_to_seconds(4, 0, 0),
}
MEMBER_BREAK_TARGET = hms_to_seconds(1, 30, 0)


def member_threshold_seconds(day_type: str) -> int:
    return MEMBER_THRESHOLDS.get(day_type, MEMBER_THRESHOLDS[DAY_FULL])


def leader_threshold_seconds(day_type: str) -> int:
    return LEADER_THRESHOLDS.get(day_type, LEADER_THRESHOLDS[DAY_FULL])


def format_logout_at_display(first_entry: dt.datetime, deadline: dt.datetime) -> str:
    if deadline.date() == first_entry.date():
        return deadline.strftime("%I:%M %p").lstrip("0")
    return deadline.strftime("%d-%b %I:%M %p").lstrip("0")


def render_logout_eligibility_status(
    first_entry: dt.datetime, deadline: dt.datetime, now: dt.datetime
) -> None:
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    if now < deadline:
        at = format_logout_at_display(first_entry, deadline)
        st.info(f"🚀 You Need to Punch Out At :- **{at}**")
    else:
        st.markdown(
            '<div class="hooray-banner">'
            "<p>🎉 Target Completed! You're Free to Go!! 🎉</p>"
            "</div>",
            unsafe_allow_html=True,
        )


def render_summary(result: dict) -> None:
    total_work = result["total_work"] + result["ongoing_work"]
    total_break = result["total_break"]
    total_time = total_work + total_break
    num_breaks = len(result["break_sessions"])
    break_label = f"{num_breaks} break{'s' if num_breaks != 1 else ''} taken"

    st.markdown(
        f"""
        <div class="summary-box">
            🕐 &nbsp;<strong>Work Time:</strong> {format_human(total_work)}<br>
            ☕ &nbsp;<strong>Break Time:</strong> {format_human(total_break)}
            &nbsp;<span style="opacity:0.6;font-size:0.88em;">({break_label})</span><br>
            📊 &nbsp;<strong>Total Time in office:</strong> {format_human(total_time)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_session_panel(result: dict) -> None:
    work_data = result.get("work_sessions_data", [])
    break_data = result.get("break_sessions_data", [])

    def work_items_html() -> str:
        if not work_data:
            return '<div class="session-item"><span class="session-time">No sessions yet</span></div>'
        items = []
        for s in work_data:
            ongoing = '<span class="live-badge">LIVE</span>' if s.get("ongoing") else ""
            items.append(
                f'<div class="session-item">'
                f'<span class="session-time">{s["start"]} → {s["end"]}{ongoing}</span>'
                f'<span class="session-duration work">{s["human"]}</span>'
                f'</div>'
            )
        return "".join(items)

    def break_items_html() -> str:
        if not break_data:
            return '<div class="session-item"><span class="session-time">No breaks yet</span></div>'
        items = []
        for s in break_data:
            items.append(
                f'<div class="session-item">'
                f'<span class="session-time">{s["start"]} → {s["end"]}</span>'
                f'<span class="session-duration break">{s["human"]}</span>'
                f'</div>'
            )
        return "".join(items)

    st.markdown(
        f"""
        <div class="session-panel">
            <div class="session-card">
                <div class="session-header work">🕐 Work Sessions · {len(work_data)}</div>
                {work_items_html()}
            </div>
            <div class="session-card">
                <div class="session-header break">☕ Break Sessions · {len(break_data)}</div>
                {break_items_html()}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Dashboard renderers ────────────────────────────────────────────────────────

def render_team_member_dashboard(
    result: dict,
    day_type: str,
    first_entry: dt.datetime,
    now: dt.datetime,
) -> None:
    required_work_secs = member_threshold_seconds(day_type)
    total_work = result["total_work"] + result["ongoing_work"]
    total_break = result["total_break"]
    total_logged = total_work + total_break
    remaining_work = max(required_work_secs - total_work, 0)
    deadline = now + dt.timedelta(seconds=remaining_work)
    remaining_break = max(MEMBER_BREAK_TARGET - total_break, 0)

    st.caption(
        f"👤 Team Member · {day_type} · "
        f"Clocked in at {first_entry.strftime('%I:%M %p').lstrip('0')} on {first_entry.strftime('%d %b %Y')} · "
        f"Earliest logout at {format_logout_at_display(first_entry, deadline)}"
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Work Time", format_clock(total_work))
    c2.metric("Total Break Time", format_clock(total_break))
    c3.metric("Total Logged Time", format_clock(total_logged))
    c4.metric("Remaining Work", format_clock(remaining_work) if remaining_work > 0 else "—")
    c5.metric("Remaining Break", format_clock(remaining_break) if remaining_break > 0 else "—")

    if result["ongoing_work_text"]:
        label = "▲ Hide session breakdown" if st.session_state.member_session_panel_open else "▼ Active work session — tap to see breakdown"
        if st.button(label, key="btn_member_session_toggle", use_container_width=True):
            st.session_state.member_session_panel_open = not st.session_state.member_session_panel_open
        if st.session_state.member_session_panel_open:
            render_session_panel(result)

    render_logout_eligibility_status(first_entry, deadline, now)


def render_team_leader_dashboard(
    result: dict,
    day_type: str,
    first_entry: dt.datetime,
    now: dt.datetime,
) -> None:
    required_work_secs = leader_threshold_seconds(day_type)
    total_work = result["total_work"] + result["ongoing_work"]
    total_break = result["total_break"]
    total_time = total_work + total_break
    remaining_work = max(required_work_secs - total_work, 0)
    deadline = now + dt.timedelta(seconds=remaining_work)
    remaining_break = max(MEMBER_BREAK_TARGET - total_break, 0)

    st.caption(
        f"👑 Team Leader · {day_type} · "
        f"Clocked in at {first_entry.strftime('%I:%M %p').lstrip('0')} on {first_entry.strftime('%d %b %Y')} · "
        f"Earliest logout at {format_logout_at_display(first_entry, deadline)}"
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Work (login) Time", format_clock(total_work))
    c2.metric("Total Break Time", format_clock(total_break))
    c3.metric("Total Time", format_clock(total_time))
    c4.metric("Remaining Work", format_clock(remaining_work) if remaining_work > 0 else "—")
    c5.metric("Remaining Break", format_clock(remaining_break) if remaining_break > 0 else "—")

    if result["ongoing_work_text"]:
        label = "▲ Hide session breakdown" if st.session_state.leader_session_panel_open else "▼ Active work session — tap to see breakdown"
        if st.button(label, key="btn_leader_session_toggle", use_container_width=True):
            st.session_state.leader_session_panel_open = not st.session_state.leader_session_panel_open
        if st.session_state.leader_session_panel_open:
            render_session_panel(result)

    render_logout_eligibility_status(first_entry, deadline, now)


# ── Parsing ────────────────────────────────────────────────────────────────────

def extract_times(log_text: str) -> list[dt.datetime]:
    matches = re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", log_text)
    current_day = now_pune().date()
    points: list[dt.datetime] = []
    last_dt = None

    for item in matches:
        hh, mm = map(int, item.split(":"))
        candidate = dt.datetime.combine(current_day, dt.time(hh, mm))
        if last_dt and candidate < last_dt:
            current_day += dt.timedelta(days=1)
            candidate = dt.datetime.combine(current_day, dt.time(hh, mm))
        points.append(candidate)
        last_dt = candidate

    return points


@st.cache_data(ttl=0, show_spinner=False)
def normalize_paste_text(raw: str) -> str:
    return (raw or "").replace("\r\n", "\n")


def fresh_parse_biometric_log(log_text: str) -> tuple[dt.datetime, ...] | None:
    pts = extract_times(log_text)
    if len(pts) < 1:
        return None
    return tuple(pts)


def summarize_sessions(
    time_points: list[dt.datetime], current_time: dt.datetime | None = None
) -> dict:
    work_sessions: list[str] = []
    break_sessions: list[str] = []
    work_sessions_data: list[dict] = []
    break_sessions_data: list[dict] = []
    total_work = 0
    total_break = 0
    ongoing_work = 0
    ongoing_work_text = None

    for idx in range(len(time_points) - 1):
        start_dt = time_points[idx]
        end_dt = time_points[idx + 1]
        seconds = int((end_dt - start_dt).total_seconds())
        session_data = {
            "start": start_dt.strftime("%d-%b %H:%M"),
            "end": end_dt.strftime("%d-%b %H:%M"),
            "seconds": seconds,
            "human": format_human(seconds),
        }
        if idx % 2 == 0:
            work_sessions.append(str(session_data))
            work_sessions_data.append(session_data)
            total_work += seconds
        else:
            break_sessions.append(str(session_data))
            break_sessions_data.append(session_data)
            total_break += seconds

    if len(time_points) % 2 == 1:
        current_time = current_time or now_pune()
        if current_time < time_points[-1]:
            current_time += dt.timedelta(days=1)
        ongoing_work = int((current_time - time_points[-1]).total_seconds())
        ongoing_work_text = "(ongoing)"
        work_sessions_data.append({
            "start": time_points[-1].strftime("%d-%b %H:%M"),
            "end": current_time.strftime("%d-%b %H:%M"),
            "seconds": ongoing_work,
            "human": format_human(ongoing_work),
            "ongoing": True,
        })

    return {
        "work_sessions": work_sessions,
        "break_sessions": break_sessions,
        "work_sessions_data": work_sessions_data,
        "break_sessions_data": break_sessions_data,
        "total_work": total_work,
        "total_break": total_break,
        "ongoing_work": max(ongoing_work, 0),
        "ongoing_work_text": ongoing_work_text,
    }


# ── Session state persistence ──────────────────────────────────────────────────

def persist_member_day_query() -> None:
    st.session_state.member_day_type = st.session_state[MEMBER_DAY_WIDGET_KEY]
    st.query_params[MEMBER_DAY_QUERY] = st.session_state.member_day_type


def persist_leader_day_query() -> None:
    st.session_state.leader_day_type = st.session_state[LEADER_DAY_WIDGET_KEY]
    st.query_params[LEADER_DAY_QUERY] = st.session_state.leader_day_type


# ── Live dashboard fragments ──────────────────────────────────────────

@st.fragment(run_every="1s")
def member_live_dashboard() -> None:
    pts = st.session_state.get("member_biometric_points")
    if not pts:
        st.info("👈 Paste biometric log and click 'Calculate Times' to see live dashboard")
        return
    now = now_pune()
    result = summarize_sessions(pts, current_time=now)
    day_type = st.session_state.get(MEMBER_DAY_WIDGET_KEY, st.session_state.member_day_type)
    render_team_member_dashboard(result, day_type, pts[0], now)


@st.fragment(run_every="1s")
def leader_live_dashboard() -> None:
    pts = st.session_state.get("leader_biometric_points")
    if not pts:
        st.info("👈 Paste biometric log and click 'Calculate Times' to see live dashboard")
        return
    now = now_pune()
    result = summarize_sessions(pts, current_time=now)
    day_type = st.session_state.get(LEADER_DAY_WIDGET_KEY, st.session_state.leader_day_type)
    render_team_leader_dashboard(result, day_type, pts[0], now)


# ── Initialise session state ───────────────────────────────────────────────────

if "_chronos_cleared_caches" not in st.session_state:
    st.cache_data.clear()
    st.session_state._chronos_cleared_caches = True

if "member_day_type" not in st.session_state:
    mq = st.query_params.get(MEMBER_DAY_QUERY)
    st.session_state.member_day_type = mq if mq in DAY_TYPE_OPTIONS else DAY_FULL

if "leader_day_type" not in st.session_state:
    lq = st.query_params.get(LEADER_DAY_QUERY)
    st.session_state.leader_day_type = lq if lq in DAY_TYPE_OPTIONS else DAY_FULL

if "member_biometric_points" not in st.session_state:
    st.session_state.member_biometric_points = None

if "leader_biometric_points" not in st.session_state:
    st.session_state.leader_biometric_points = None

if "member_session_panel_open" not in st.session_state:
    st.session_state.member_session_panel_open = False

if "leader_session_panel_open" not in st.session_state:
    st.session_state.leader_session_panel_open = False

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"


# ── Page layout ───────────────────────────────────────────────────────────────

LOGO_SVG = """
<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
    <linearGradient id="logoGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ec4899"/>
      <stop offset="100%" stop-color="#f43f5e"/>
    </linearGradient>
  </defs>
  <circle cx="24" cy="24" r="22" fill="url(#logoGrad1)" opacity="0.15"/>
  <circle cx="24" cy="24" r="18" stroke="url(#logoGrad1)" stroke-width="2" fill="none"/>
  <circle cx="24" cy="24" r="12" fill="url(#logoGrad2)" opacity="0.8"/>
  <text x="24" y="30" text-anchor="middle" fill="white" font-size="16" font-weight="800" font-family="Arial, sans-serif">C</text>
</svg>
"""

# Inject theme attribute
theme_attr = 'data-theme="dark"' if st.session_state.theme_mode == "dark" else 'data-theme="light"'
st.markdown(f'<body {theme_attr}></body>', unsafe_allow_html=True)

# Scroll to top
st.markdown(
    """<script>
    (function() {
        function scrollTop() {
            var container = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
            if (container) container.scrollTop = 0;
            window.parent.document.documentElement.scrollTop = 0;
            window.parent.document.body.scrollTop = 0;
        }
        scrollTop();
        setTimeout(scrollTop, 100);
        setTimeout(scrollTop, 300);
    })();
    </script>""",
    unsafe_allow_html=True,
)

# Header
hdr_icon, hdr_title, hdr_spacer, hdr_toggle = st.columns([1, 9, 2, 2], vertical_alignment="center")

with hdr_icon:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)

with hdr_title:
    st.title("Chronos")

with hdr_toggle:
    _is_dark = st.session_state.theme_mode == "dark"
    toggle_label = "🌙 Dark" if not _is_dark else "☀️ Light"
    if st.button(toggle_label, key="btn_theme_toggle", use_container_width=True):
        st.session_state.theme_mode = "light" if _is_dark else "dark"
        st.rerun()

st.caption(
    "Paste biometric punches under the role that applies to you. "
    "Team Member and Team Leader each keep their own log, day type, and metrics."
)
st.caption(f"Pune time (IST): {now_pune().strftime('%d-%b-%Y %I:%M:%S %p')}")

st.markdown("**Biometric Log**")
tab_member_in, tab_leader_in = st.tabs(["👤  Team Member", "👑  Team Leader"])

with tab_member_in:
    st.radio(
        "Day Type",
        DAY_TYPE_OPTIONS,
        index=DAY_TYPE_OPTIONS.index(st.session_state.member_day_type),
        key=MEMBER_DAY_WIDGET_KEY,
        on_change=persist_member_day_query,
        horizontal=True,
        help="Min logout time: Full Day = 7h 30m | Half Day = 4h 30m",
    )
    with st.form(key="member_calc_form", clear_on_submit=False):
        st.text_area(
            "Team Member biometric log paste",
            height=170,
            label_visibility="collapsed",
            placeholder="Paste your biometric log here...\nExample:\n09:15\n13:00\n14:00\n18:30",
            key=MEMBER_PASTE_WIDGET_KEY,
        )
        member_submitted = st.form_submit_button("Calculate Times", use_container_width=True)
    if member_submitted:
        raw = normalize_paste_text(st.session_state.get(MEMBER_PASTE_WIDGET_KEY, ""))
        parsed = fresh_parse_biometric_log(raw)
        if parsed is None:
            st.error("Please enter at least one valid time in HH:MM format.")
            st.session_state.member_biometric_points = None
        else:
            st.session_state.member_biometric_points = list(parsed)
            st.success(f"✅ Successfully parsed {len(parsed)} time entries!")

    st.markdown("**Live Preview**")
    member_live_dashboard()

with tab_leader_in:
    st.radio(
        "Day Type",
        DAY_TYPE_OPTIONS,
        index=DAY_TYPE_OPTIONS.index(st.session_state.leader_day_type),
        key=LEADER_DAY_WIDGET_KEY,
        on_change=persist_leader_day_query,
        horizontal=True,
        help="Min login time: Full Day = 7h 00m | Half Day = 4h 00m",
    )
    with st.form(key="leader_calc_form", clear_on_submit=False):
        st.text_area(
            "Team Leader biometric log paste",
            height=170,
            label_visibility="collapsed",
            placeholder="Paste your biometric log here...\nExample:\n09:15\n13:00\n14:00\n18:30",
            key=LEADER_PASTE_WIDGET_KEY,
        )
        leader_submitted = st.form_submit_button("Calculate Times", use_container_width=True)
    if leader_submitted:
        raw = normalize_paste_text(st.session_state.get(LEADER_PASTE_WIDGET_KEY, ""))
        parsed = fresh_parse_biometric_log(raw)
        if parsed is None:
            st.error("Please enter at least one valid time in HH:MM format.")
            st.session_state.leader_biometric_points = None
        else:
            st.session_state.leader_biometric_points = list(parsed)
            st.success(f"✅ Successfully parsed {len(parsed)} time entries!")

    st.markdown("**Live Preview**")
    leader_live_dashboard()
