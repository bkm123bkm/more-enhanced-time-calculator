import datetime as dt
from pathlib import Path
import re
from zoneinfo import ZoneInfo

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "Icon.png"
PAGE_ICON = str(ICON_PATH) if ICON_PATH.exists() else "⏱️"
PUNE_TZ = ZoneInfo("Asia/Kolkata")

# Widget keys (Streamlit-owned). Never assign programmatically to these keys.
MEMBER_DAY_WIDGET_KEY = "_ui_member_day_type"
LEADER_DAY_WIDGET_KEY = "_ui_leader_day_type"
MEMBER_PASTE_WIDGET_KEY = "_ui_member_paste"
LEADER_PASTE_WIDGET_KEY = "_ui_leader_paste"
MEMBER_DAY_QUERY = "member_day"
LEADER_DAY_QUERY = "leader_day"


def now_pune() -> dt.datetime:
    return dt.datetime.now(PUNE_TZ).replace(tzinfo=None)


st.set_page_config(
    page_title="More Enhanced Time Calculator",
    page_icon=PAGE_ICON,
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --accent-gold: #d4af72;
        --accent-gold-hover: #c49c5f;
        --accent-gold-soft: #f2ddbb;
        --card-topline: #1e3a8a;
    }

    .stApp {
        background: var(--background-color);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2.2rem;
    }

    h1, h2, h3 {
        color: var(--text-color) !important;
        letter-spacing: 0.3px;
        font-weight: 700;
        text-wrap: balance;
    }

    h1 {
        font-size: 3rem !important;
        margin-bottom: 0.2rem;
        font-family: "Georgia", "Times New Roman", serif;
    }

    p, label, .stCaption {
        color: color-mix(in srgb, var(--text-color) 70%, transparent) !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(
            180deg,
            color-mix(in srgb, var(--secondary-background-color) 95%, transparent) 0%,
            color-mix(in srgb, var(--secondary-background-color) 85%, transparent) 100%
        );
        border: 1px solid color-mix(in srgb, var(--accent-gold) 22%, var(--text-color));
        border-radius: 16px;
        padding: 14px;
        box-shadow: 0 12px 26px color-mix(in srgb, black 20%, transparent);
        backdrop-filter: blur(2px);
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--card-topline) 50%, transparent 100%);
        opacity: 0.85;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted) !important;
    }

    div[data-testid="stMetricValue"] {
        color: var(--text-color) !important;
        font-weight: 700 !important;
    }

    .stTextArea textarea {
        border: 1px solid color-mix(in srgb, var(--accent-gold) 22%, var(--text-color));
        border-radius: 12px;
        background: var(--secondary-background-color);
        color: var(--text-color);
        box-shadow: inset 0 1px 0 color-mix(in srgb, white 8%, transparent);
    }

    .stTextArea textarea:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent-gold) 28%, transparent) !important;
    }

    /* Hide "Press Ctrl+Enter to apply" hint */
    .stTextArea [data-testid="InputInstructions"],
    .stTextArea small {
        display: none !important;
    }

    /* Disable all hyperlinks — plain non-clickable text */
    a, a:hover, a:visited, a:active, a:focus {
        pointer-events: none !important;
        cursor: default !important;
        text-decoration: none !important;
        color: inherit !important;
    }

    /* Hide Streamlit anchor link icons */
    a[data-testid="stMarkdownAnchorLink"],
    .st-anchor-link,
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(180deg, #e2c18a 0%, var(--accent-gold) 100%);
        color: #1a1308 !important;
        border-radius: 12px;
        border: 1px solid color-mix(in srgb, #fff 22%, var(--accent-gold));
        font-weight: 700;
        transition: all 0.15s ease;
        box-shadow: 0 10px 22px rgba(212, 175, 114, 0.28);
        opacity: 1 !important;
        min-height: 2.8rem;
    }

    .stButton > button:hover:not(:disabled),
    .stFormSubmitButton > button:hover:not(:disabled) {
        background: linear-gradient(180deg, #edd2a5 0%, var(--accent-gold-hover) 100%);
        transform: translateY(-1px) scale(1.01);
        box-shadow: 0 14px 30px rgba(212, 175, 114, 0.34);
    }

    .stButton > button:disabled {
        background-color: #6f634f !important;
        color: #d7c9b2 !important;
        opacity: 0.7 !important;
        cursor: not-allowed;
        box-shadow: none;
    }

    .stMarkdown, .stText {
        color: var(--text-color);
    }

    hr {
        border-color: color-mix(in srgb, var(--accent-gold) 25%, transparent);
    }

    /* Disable all hyperlinks globally — plain non-clickable text */
    a, a:hover, a:visited, a:active, a:focus {
        pointer-events: none !important;
        cursor: default !important;
        text-decoration: none !important;
        color: inherit !important;
    }

    div[data-testid="stAlert"] {
        border: 1px solid color-mix(in srgb, var(--accent-gold) 28%, var(--text-color));
        border-radius: 12px;
        background: color-mix(in srgb, var(--secondary-background-color) 90%, transparent);
    }

    /* Tab switch: fade + slide animation */
    @keyframes more_enhanced_time_calculator-tab-reveal {
        from { opacity: 0; transform: translateX(14px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    [data-testid="stTabs"] [role="tabpanel"],
    [data-testid="stTabs"] [data-baseweb="tab-panel"] {
        transition: opacity 0.28s ease, transform 0.28s ease;
    }

    [data-testid="stTabs"] [role="tabpanel"]:not([aria-hidden="true"]),
    [data-testid="stTabs"] [data-baseweb="tab-panel"]:not([hidden]) {
        animation: more_enhanced_time_calculator-tab-reveal 0.38s cubic-bezier(0.22, 1, 0.36, 1) both;
    }

    .more_enhanced_time_calculator-hooray-banner {
        background: linear-gradient(180deg, #1f6b3a 0%, #145a2e 100%);
        color: #ffffff !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.35);
        padding: 14px 18px;
        border-radius: 12px;
        border: 1px solid color-mix(in srgb, #34d399 55%, #14532d);
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        box-shadow: 0 10px 28px color-mix(in srgb, #22c55e 35%, transparent);
        margin-top: 0.35rem;
    }

    .more_enhanced_time_calculator-hooray-banner,
    .more_enhanced_time_calculator-hooray-banner p,
    .more_enhanced_time_calculator-hooray-banner span {
        color: #ffffff !important;
    }

    .more_enhanced_time_calculator-summary-box {
        background: color-mix(in srgb, var(--secondary-background-color) 80%, transparent);
        border: 1px solid color-mix(in srgb, var(--accent-gold) 22%, var(--text-color));
        border-radius: 14px;
        padding: 16px 20px;
        margin-top: 0.6rem;
        line-height: 2.2;
        user-select: none;
        -webkit-user-select: none;
    }

    .more_enhanced_time_calculator-summary-box *::selection {
        background: transparent;
    }

    .more_enhanced_time_calculator-summary-box *::-moz-selection {
        background: transparent;
    }

    @media (prefers-color-scheme: dark) {
        :root { --card-topline: var(--accent-gold-soft); }

        .stApp {
            background:
                radial-gradient(circle at 14% -10%, rgba(148,137,121,0.10), transparent 34%),
                radial-gradient(circle at 86% 0%, rgba(57,62,70,0.20), transparent 32%),
                #1e2229;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, #323840 0%, #272c34 100%);
            border: 1px solid #424850;
            box-shadow: 0 16px 30px rgba(0, 0, 0, 0.50);
        }

        .stTextArea textarea {
            background: #272c34;
            border-color: #3a3f48;
        }

        .more_enhanced_time_calculator-hooray-banner {
            background: linear-gradient(180deg, #166534 0%, #0f3d1f 100%);
            border-color: #22c55e;
            box-shadow: 0 12px 32px rgba(34, 197, 94, 0.22);
        }

        .more_enhanced_time_calculator-summary-box {
            background: #272c34;
            border-color: #3a3f48;
        }

        .stButton > button,
        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: #000000 !important;
            text-shadow: none !important;
        }
        .stApp .stButton > button {
            color: #000000 !important;
        }
    }

    /* ── Session panel ── */
    .ee-session-panel {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 14px;
    }

    .ee-session-col {
        background: color-mix(in srgb, var(--secondary-background-color) 80%, transparent);
        border: 1px solid color-mix(in srgb, var(--accent-gold) 20%, var(--text-color));
        border-radius: 14px;
        padding: 16px 18px 12px;
        position: relative;
        overflow: hidden;
    }

    .ee-session-col::before {
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 2px;
    }

    .ee-session-col.work::before {
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
    }

    .ee-session-col.brk::before {
        background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
    }

    .ee-col-header {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .ee-col-header.work { color: #60a5fa; }
    .ee-col-header.brk  { color: var(--accent-gold); }

    .ee-col-count {
        font-size: 0.68rem;
        padding: 2px 7px;
        border-radius: 20px;
        font-weight: 700;
        letter-spacing: 0;
    }

    .ee-col-header.work .ee-col-count { background: rgba(59,130,246,0.18); color: #93c5fd; }
    .ee-col-header.brk  .ee-col-count { background: rgba(212,175,114,0.18); color: var(--accent-gold); }

    .ee-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        padding: 7px 0;
        border-bottom: 1px solid color-mix(in srgb, var(--text-color) 8%, transparent);
        gap: 8px;
        font-size: 0.82rem;
    }

    .ee-row:last-child { border-bottom: none; }

    .ee-row-label {
        color: color-mix(in srgb, var(--text-color) 55%, transparent);
        white-space: nowrap;
        flex-shrink: 0;
        font-size: 0.78rem;
    }

    .ee-row-range {
        color: color-mix(in srgb, var(--text-color) 80%, transparent);
        font-size: 0.8rem;
        text-align: center;
        flex: 1;
    }

    .ee-row-dur {
        font-weight: 700;
        white-space: nowrap;
        font-size: 0.84rem;
    }

    .ee-row-dur.work { color: #60a5fa; }
    .ee-row-dur.brk  { color: var(--accent-gold); }

    .ee-ongoing-badge {
        font-size: 0.65rem;
        background: rgba(34,197,94,0.18);
        color: #4ade80;
        border-radius: 10px;
        padding: 1px 6px;
        font-weight: 700;
        letter-spacing: 0.06em;
        vertical-align: middle;
        margin-left: 4px;
    }

    @media (prefers-color-scheme: dark) {
        .ee-session-col {
            background: #272c34;
            border-color: #3a3f48;
        }
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


def format_hours_minutes(total_seconds: int) -> str:
    total_seconds = max(total_seconds, 0)
    h = total_seconds // 3_600
    m = (total_seconds % 3_600) // 60
    return f"{h}h {m:02d}m"


def format_human(total_seconds: int) -> str:
    """Plain English duration: '8 hrs 50 mins'"""
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

# Team Member: minimum total logged time (work + breaks on site)
MEMBER_THRESHOLDS: dict[str, int] = {
    DAY_FULL: hms_to_seconds(7, 30, 0),
    DAY_HALF: hms_to_seconds(4, 30, 0),
}
# Team Leader: minimum login / work time
LEADER_THRESHOLDS: dict[str, int] = {
    DAY_FULL: hms_to_seconds(7, 0, 0),
    DAY_HALF: hms_to_seconds(4, 0, 0),
}
# Break allowance for Team Member
MEMBER_BREAK_TARGET = hms_to_seconds(1, 30, 0)


# ── Threshold helpers ──────────────────────────────────────────────────────────

def member_threshold_seconds(day_type: str) -> int:
    return MEMBER_THRESHOLDS.get(day_type, MEMBER_THRESHOLDS[DAY_FULL])


def leader_threshold_seconds(day_type: str) -> int:
    return LEADER_THRESHOLDS.get(day_type, LEADER_THRESHOLDS[DAY_FULL])


def min_duration_from_first_entry(day_type: str, *, role: str) -> dt.timedelta:
    if role == "member":
        sec = member_threshold_seconds(day_type)
    else:
        sec = leader_threshold_seconds(day_type)
    return dt.timedelta(seconds=sec)


def format_logout_at_display(first_entry: dt.datetime, deadline: dt.datetime) -> str:
    """12hr format; adds date if logout rolls past first-entry calendar day."""
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
            '<div class="more_enhanced_time_calculator-hooray-banner">'
            "🎉 Target Completed! You’re Free to Go!!"
            "</div>",
            unsafe_allow_html=True,
        )


def render_summary(result: dict) -> None:
    """Human-readable work & break summary box."""
    total_work = result["total_work"] + result["ongoing_work"]
    total_break = result["total_break"]
    total_time = total_work + total_break
    num_breaks = len(result["break_sessions"])
    break_label = f"{num_breaks} break{'s' if num_breaks != 1 else ''} taken"

    st.markdown(
        f"""
        <div class="more_enhanced_time_calculator-summary-box">
            🕐 &nbsp;<b>Work Time:</b> {format_human(total_work)}<br>
            ☕ &nbsp;<b>Break Time:</b> {format_human(total_break)}
            &nbsp;<span style="opacity:0.6;font-size:0.88em;">({break_label})</span><br>
            📊 &nbsp;<b>Total Time in office:</b> {format_human(total_time)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_session_panel(result: dict) -> None:
    """Premium side-by-side work & break session breakdown."""
    work_data = result.get("work_sessions_data", [])
    break_data = result.get("break_sessions_data", [])

    def work_rows_html() -> str:
        if not work_data:
            return '<div class="ee-row"><span class="ee-row-label" style="opacity:0.45">No sessions yet</span></div>'
        rows = []
        for i, s in enumerate(work_data, 1):
            ongoing_badge = '<span class="ee-ongoing-badge">LIVE</span>' if s.get("ongoing") else ""
            rows.append(
                f'<div class="ee-row">'
                f'<span class="ee-row-label">Session {i}</span>'
                f'<span class="ee-row-range">{s["start"]} → {s["end"]}{ongoing_badge}</span>'
                f'<span class="ee-row-dur work">{s["human"]}</span>'
                f'</div>'
            )
        return "".join(rows)

    def break_rows_html() -> str:
        if not break_data:
            return '<div class="ee-row"><span class="ee-row-label" style="opacity:0.45">No breaks yet</span></div>'
        rows = []
        for i, s in enumerate(break_data, 1):
            rows.append(
                f'<div class="ee-row">'
                f'<span class="ee-row-label">Break {i}</span>'
                f'<span class="ee-row-range">{s["start"]} → {s["end"]}</span>'
                f'<span class="ee-row-dur brk">{s["human"]}</span>'
                f'</div>'
            )
        return "".join(rows)

    st.markdown(
        f"""
        <div class="ee-session-panel">
            <div class="ee-session-col work">
                <div class="ee-col-header work">
                    🕐 Work Sessions
                    <span class="ee-col-count">{len(work_data)}</span>
                </div>
                {work_rows_html()}
            </div>
            <div class="ee-session-col brk">
                <div class="ee-col-header brk">
                    ☕ Break Sessions
                    <span class="ee-col-count">{len(break_data)}</span>
                </div>
                {break_rows_html()}
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
    """Team Member: logout when net work time (excluding breaks) >= threshold."""
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
    """Team Leader: logout when net work time (excluding breaks) >= threshold."""
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
        session_text = (
            f"{start_dt.strftime('%Y-%m-%d %H:%M')} -> "
            f"{end_dt.strftime('%Y-%m-%d %H:%M')} - {format_short(seconds)}"
        )
        session_data = {
            "start": start_dt.strftime("%d-%b %H:%M"),
            "end": end_dt.strftime("%d-%b %H:%M"),
            "seconds": seconds,
            "human": format_human(seconds),
        }
        if idx % 2 == 0:
            work_sessions.append(session_text)
            work_sessions_data.append(session_data)
            total_work += seconds
        else:
            break_sessions.append(session_text)
            break_sessions_data.append(session_data)
            total_break += seconds

    # Odd number of punches = active work session ongoing
    if len(time_points) % 2 == 1:
        current_time = current_time or now_pune()
        if current_time < time_points[-1]:
            current_time += dt.timedelta(days=1)
        ongoing_work = int((current_time - time_points[-1]).total_seconds())
        ongoing_work_text = (
            f"{time_points[-1].strftime('%Y-%m-%d %H:%M')} -> "
            f"{current_time.strftime('%Y-%m-%d %H:%M')} - {format_short(ongoing_work)} "
            "(ongoing)"
        )
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


# ── Live dashboard fragments (auto-refresh every 1s) ──────────────────────────

@st.fragment(run_every="1s")
def member_live_dashboard() -> None:
    pts = st.session_state.get("member_biometric_points")
    if not pts:
        return
    now = now_pune()
    result = summarize_sessions(pts, current_time=now)
    day_type = st.session_state.get(MEMBER_DAY_WIDGET_KEY, st.session_state.member_day_type)
    render_team_member_dashboard(result, day_type, pts[0], now)


@st.fragment(run_every="1s")
def leader_live_dashboard() -> None:
    pts = st.session_state.get("leader_biometric_points")
    if not pts:
        return
    now = now_pune()
    result = summarize_sessions(pts, current_time=now)
    day_type = st.session_state.get(LEADER_DAY_WIDGET_KEY, st.session_state.leader_day_type)
    render_team_leader_dashboard(result, day_type, pts[0], now)


# ── Initialise session state ───────────────────────────────────────────────────

if "_more_enhanced_time_calculator_cleared_caches" not in st.session_state:
    st.cache_data.clear()
    st.session_state._more_enhanced_time_calculator_cleared_caches = True

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

# Premium animated SVG clock icon with pulse animation
CLOCK_SVG = """
<svg width="58" height="58" viewBox="0 0 58 58" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="faceGrad" cx="50%" cy="38%" r="55%">
      <stop offset="0%" stop-color="#f5e6c8"/>
      <stop offset="100%" stop-color="#c9a96e"/>
    </radialGradient>
    <radialGradient id="rimGrad" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#e8c97a"/>
      <stop offset="60%" stop-color="#b8892a"/>
      <stop offset="100%" stop-color="#7a5510"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#00000055"/>
    </filter>
  </defs>
  <!-- Outer gold rim -->
  <circle cx="29" cy="29" r="27" fill="url(#rimGrad)" filter="url(#shadow)"/>
  <!-- Inner highlight ring -->
  <circle cx="29" cy="29" r="23.5" fill="none" stroke="#f0d080" stroke-width="0.7" opacity="0.5"/>
  <!-- Clock face -->
  <circle cx="29" cy="29" r="22" fill="url(#faceGrad)"/>
  <!-- Hour markers -->
  <g stroke="#7a5510" stroke-width="1.5" stroke-linecap="round">
    <line x1="29" y1="9"  x2="29" y2="12"/>
    <line x1="29" y1="46" x2="29" y2="49"/>
    <line x1="9"  y1="29" x2="12" y2="29"/>
    <line x1="46" y1="29" x2="49" y2="29"/>
  </g>
  <!-- Minor tick marks -->
  <g stroke="#b8892a" stroke-width="0.8" stroke-linecap="round" opacity="0.6">
    <line x1="38.2" y1="10.5"  x2="36.9" y2="12.8"/>
    <line x1="19.8" y1="10.5"  x2="21.1" y2="12.8"/>
    <line x1="47.5" y1="19.8" x2="45.2" y2="21.1"/>
    <line x1="47.5" y1="38.2" x2="45.2" y2="36.9"/>
    <line x1="38.2" y1="47.5" x2="36.9" y2="45.2"/>
    <line x1="19.8" y1="47.5" x2="21.1" y2="45.2"/>
    <line x1="10.5" y1="38.2" x2="12.8" y2="36.9"/>
    <line x1="10.5" y1="19.8" x2="12.8" y2="21.1"/>
  </g>
  <!-- Hour hand (pointing ~10) -->
  <line x1="29" y1="29" x2="21" y2="17" stroke="#3b2a0e" stroke-width="2.4" stroke-linecap="round"/>
  <!-- Minute hand (pointing ~2) -->
  <line x1="29" y1="29" x2="38.5"   y2="18.5" stroke="#3b2a0e" stroke-width="1.6" stroke-linecap="round"/>
  <!-- Second hand -->
  <line x1="29" y1="29" x2="32.5"   y2="43" stroke="#c0392b" stroke-width="1" stroke-linecap="round"/>
  <!-- Center jewel -->
  <circle cx="29" cy="29" r="2.2" fill="#7a5510"/>
  <circle cx="29" cy="29" r="1.1" fill="#f0d080"/>
  <animateTransform attributeName="transform" type="rotate" from="0 29 29" to="360 29 29" dur="60s" repeatCount="indefinite"/>
</svg>
"""

# Theme-aware CSS injection
_tm = st.session_state.theme_mode
_is_dark = _tm == "dark"

# ── Animated botanical SVG wallpaper patterns ─────────────────────────────────
# Dark: deep indigo/violet leaves with subtle floating animation
# Light: soft sage/mint botanical illustration with gentle movement
DARK_BG_SVG = """url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22800%22%20height%3D%22800%22%3E%0A%3Crect%20width%3D%22800%22%20height%3D%22800%22%20fill%3D%22%231e2229%22%2F%3E%0A%3Cstyle%3E.la%7Bfill%3A%233a3428%7D.lb%7Bfill%3A%232e2a22%7D.lc%7Bfill%3A%2346403a%7D.v%7Bstroke%3A%236b5f48%3Bstroke-width%3A0.8%3Bfill%3Anone%3Bopacity%3A0.55%7D.v2%7Bstroke%3A%238a7a60%3Bstroke-width%3A0.5%3Bfill%3Anone%3Bopacity%3A0.35%7D%0A@keyframes%20drift%20%7B0%25%7Btransform%3Atranslate(0%2C0)%7D100%25%7Btransform%3Atranslate(30px%2C20px)%7D%7D%0A.g1%7Banimation%3Adrift%2020s%20ease-in-out%20infinite%20alternate%3B%7D%0A.g2%7Banimation%3Adrift%2025s%20ease-in-out%20infinite%20alternate-reverse%3B%7D%0A.g3%7Banimation%3Adrift%2018s%20ease-in-out%20infinite%20alternate%3B%7D%3C%2Fstyle%3E%0A%3Cg%20class%3D%22g1%22%20transform%3D%22translate(120%2C170)%20rotate(-42)%22%3E%3Cpath%20d%3D%22M0%2C0%20C12%2C-55%2052%2C-85%2072%2C-88%20C90%2C-90%20105%2C-75%2095%2C-45%20C82%2C-10%2045%2C18%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.82%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C30%2C-44%2065%2C-68%2095%2C-45%22%20class%3D%22v%22%2F%3E%3Cpath%20d%3D%22M20%2C-18%20C32%2C-36%2050%2C-50%2070%2C-56%22%20class%3D%22v2%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g2%22%20transform%3D%22translate(480%2C195)%20rotate(38)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-10%2C-52%20-48%2C-82%20-70%2C-84%20C-88%2C-86%20-102%2C-70%20-92%2C-42%20C-80%2C-10%20-44%2C20%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.78%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C-22%2C-42%20-60%2C-65%20-92%2C-42%22%20class%3D%22v%22%2F%3E%3Cpath%20d%3D%22M-20%2C-18%20C-30%2C-34%20-46%2C-50%20-62%2C-58%22%20class%3D%22v2%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g3%22%20transform%3D%22translate(295%2C440)%20rotate(-8)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-14%2C-58%20-56%2C-88%20-82%2C-90%20C-104%2C-92%20-118%2C-74%20-106%2C-44%20C-92%2C-10%20-50%2C24%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.80%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C-30%2C-48%20-70%2C-72%20-106%2C-44%22%20class%3D%22v%22%2F%3E%3Cpath%20d%3D%22M-25%2C-22%20C-36%2C-40%20-54%2C-58%20-72%2C-68%22%20class%3D%22v2%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g1%22%20transform%3D%22translate(720%2C170)%20rotate(-42)%22%3E%3Cpath%20d%3D%22M0%2C0%20C12%2C-55%2052%2C-85%2072%2C-88%20C90%2C-90%20105%2C-75%2095%2C-45%20C82%2C-10%2045%2C18%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.82%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C30%2C-44%2065%2C-68%2095%2C-45%22%20class%3D%22v%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g2%22%20transform%3D%22translate(-120%2C195)%20rotate(38)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-10%2C-52%20-48%2C-82%20-70%2C-84%20C-88%2C-86%20-102%2C-70%20-92%2C-42%20C-80%2C-10%20-44%2C20%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.78%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g3%22%20transform%3D%22translate(300%2C728)%20rotate(10)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-12%2C-52%20-50%2C-80%20-74%2C-82%20C-94%2C-84%20-108%2C-68%20-96%2C-40%20C-82%2C-8%20-44%2C22%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.72%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C-28%2C-44%20-64%2C-66%20-96%2C-40%22%20class%3D%22v%22%2F%3E%3C%2Fg%3E%0A%3C%2Fsvg%3E")"""

LIGHT_BG_SVG = """url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22800%22%20height%3D%22800%22%3E%0A%3Crect%20width%3D%22800%22%20height%3D%22800%22%20fill%3D%22%23eef7f2%22%2F%3E%0A%3Cstyle%3E.la%7Bfill%3A%236abf8a%7D.lb%7Bfill%3A%2386c9a0%7D.lc%7Bfill%3A%234caf78%7D.v%7Bstroke%3A%232d8a58%3Bstroke-width%3A0.8%3Bfill%3Anone%3Bopacity%3A0.38%7D.v2%7Bstroke%3A%233aaa6a%3Bstroke-width%3A0.5%3Bfill%3Anone%3Bopacity%3A0.26%7D%0A@keyframes%20drift%20%7B0%25%7Btransform%3Atranslate(0%2C0)%7D100%25%7Btransform%3Atranslate(20px%2C15px)%7D%7D%0A.g1%7Banimation%3Adrift%2022s%20ease-in-out%20infinite%20alternate%3B%7D%0A.g2%7Banimation%3Adrift%2028s%20ease-in-out%20infinite%20alternate-reverse%3B%7D%0A.g3%7Banimation%3Adrift%2019s%20ease-in-out%20infinite%20alternate%3B%7D%3C%2Fstyle%3E%0A%3Cg%20class%3D%22g1%22%20transform%3D%22translate(120%2C170)%20rotate(-42)%22%3E%3Cpath%20d%3D%22M0%2C0%20C12%2C-55%2052%2C-85%2072%2C-88%20C90%2C-90%20105%2C-75%2095%2C-45%20C82%2C-10%2045%2C18%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.42%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C30%2C-44%2065%2C-68%2095%2C-45%22%20class%3D%22v%22%2F%3E%3Cpath%20d%3D%22M20%2C-18%20C32%2C-36%2050%2C-50%2070%2C-56%22%20class%3D%22v2%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g2%22%20transform%3D%22translate(480%2C195)%20rotate(38)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-10%2C-52%20-48%2C-82%20-70%2C-84%20C-88%2C-86%20-102%2C-70%20-92%2C-42%20C-80%2C-10%20-44%2C20%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.41%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C-22%2C-42%20-60%2C-65%20-92%2C-42%22%20class%3D%22v%22%2F%3E%3Cpath%20d%3D%22M-20%2C-18%20C-30%2C-34%20-46%2C-50%20-62%2C-58%22%20class%3D%22v2%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g3%22%20transform%3D%22translate(295%2C440)%20rotate(-8)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-14%2C-58%20-56%2C-88%20-82%2C-90%20C-104%2C-92%20-118%2C-74%20-106%2C-44%20C-92%2C-10%20-50%2C24%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.42%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C-30%2C-48%20-70%2C-72%20-106%2C-44%22%20class%3D%22v%22%2F%3E%3Cpath%20d%3D%22M-25%2C-22%20C-36%2C-40%20-54%2C-58%20-72%2C-68%22%20class%3D%22v2%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g1%22%20transform%3D%22translate(720%2C170)%20rotate(-42)%22%3E%3Cpath%20d%3D%22M0%2C0%20C12%2C-55%2052%2C-85%2072%2C-88%20C90%2C-90%20105%2C-75%2095%2C-45%20C82%2C-10%2045%2C18%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.42%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C30%2C-44%2065%2C-68%2095%2C-45%22%20class%3D%22v%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g2%22%20transform%3D%22translate(-120%2C195)%20rotate(38)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-10%2C-52%20-48%2C-82%20-70%2C-84%20C-88%2C-86%20-102%2C-70%20-92%2C-42%20C-80%2C-10%20-44%2C20%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.41%22%2F%3E%3C%2Fg%3E%0A%3Cg%20class%3D%22g3%22%20transform%3D%22translate(300%2C728)%20rotate(10)%22%3E%3Cpath%20d%3D%22M0%2C0%20C-12%2C-52%20-50%2C-80%20-74%2C-82%20C-94%2C-84%20-108%2C-68%20-96%2C-40%20C-82%2C-8%20-44%2C22%200%2C0%20Z%22%20class%3D%22la%22%20opacity%3D%220.37%22%2F%3E%3Cpath%20d%3D%22M0%2C0%20C-28%2C-44%20-64%2C-66%20-96%2C-40%22%20class%3D%22v%22%2F%3E%3C%2Fg%3E%0A%3C%2Fsvg%3E")"""

# Complete theme CSS with animations
THEME_CSS = f"""
<style>
/* ── Global animations ─────────────────────────────────────────── */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes glowPulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(212,175,114,0.4); }}
    70% {{ box-shadow: 0 0 0 10px rgba(212,175,114,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(212,175,114,0); }}
}}

@keyframes metricPop {{
    0% {{ transform: scale(0.95); opacity: 0; }}
    80% {{ transform: scale(1.02); }}
    100% {{ transform: scale(1); opacity: 1; }}
}}

/* ── Wallpaper background with parallax effect ──────────────────── */
.stApp {{
    background-image: {DARK_BG_SVG if _is_dark else LIGHT_BG_SVG} !important;
    background-size: 800px 800px !important;
    background-repeat: repeat !important;
    background-attachment: fixed !important;
    transition: background-image 0.5s ease !important;
}}

/* Frosted overlay with blur */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: {"rgba(20,22,28,0.65)" if _is_dark else "rgba(238,247,242,0.72)"};
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    pointer-events: none;
    z-index: 0;
    transition: background 0.3s ease;
}}

.block-container {{
    position: relative;
    z-index: 1;
    animation: fadeInUp 0.6s ease-out;
}}

/* ── Typography with subtle glow ────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {{
    color: {"#f5ebd6" if _is_dark else "#0f2a1a"} !important;
    text-shadow: {"0 2px 12px rgba(212,175,114,0.25)" if _is_dark else "0 1px 4px rgba(100,140,80,0.15)"} !important;
    letter-spacing: -0.02em;
}}

h1 {{
    background: linear-gradient(135deg, {"#f5e6c8" if _is_dark else "#1a4a2a"}, {"#d4af72" if _is_dark else "#3a8a5a"});
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    text-shadow: none;
}}

/* ── Animated Metric Cards ─────────────────────────────────────── */
div[data-testid="stMetric"] {{
    animation: metricPop 0.5s cubic-bezier(0.34, 1.2, 0.64, 1) forwards;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    background: {"linear-gradient(135deg,rgba(57,62,70,0.92) 0%,rgba(38,43,52,0.96) 100%)" if _is_dark else "linear-gradient(135deg,rgba(255,255,255,0.85) 0%,rgba(230,250,238,0.92) 100%)"} !important;
    border: {"1px solid rgba(212,175,114,0.35)" if _is_dark else "1px solid rgba(80,170,110,0.5)"} !important;
    border-radius: 20px !important;
    backdrop-filter: blur(12px) !important;
}}

div[data-testid="stMetric"]:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: {"0 20px 40px rgba(0,0,0,0.5)" if _is_dark else "0 20px 40px rgba(60,140,80,0.2)"} !important;
    transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
}}

div[data-testid="stMetricValue"] > div {{
    font-size: 1.8rem !important;
    background: linear-gradient(135deg, {"#f5e6c8" if _is_dark else "#1a4a2a"}, {"#d4af72" if _is_dark else "#3a8a5a"});
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}}

/* ── Text Areas with focus animation ───────────────────────────── */
.stTextArea textarea {{
    transition: all 0.3s ease !important;
    background: {"rgba(38,43,52,0.92)" if _is_dark else "rgba(240,252,245,0.9)"} !important;
    border-radius: 16px !important;
    font-family: 'JetBrains Mono', monospace !important;
}}

.stTextArea textarea:focus {{
    transform: scale(1.01);
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 3px rgba(212,175,114,0.3) !important;
}}

/* ── Buttons with ripple effect ────────────────────────────────── */
.stButton > button {{
    position: relative;
    overflow: hidden;
    transition: all 0.25s cubic-bezier(0.34, 1.2, 0.64, 1) !important;
    border-radius: 40px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em;
}}

.stButton > button::after {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
    transform: translate(-50%, -50%);
    transition: width 0.4s, height 0.4s;
}}

.stButton > button:active::after {{
    width: 200px;
    height: 200px;
    opacity: 0;
}}

.stButton > button:hover {{
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 15px 35px rgba(212,175,114,0.35) !important;
}}

/* ── Tabs with elegant animation ───────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {{
    gap: 8px !important;
    background: transparent !important;
}}

[data-testid="stTabs"] [role="tab"] {{
    transition: all 0.25s ease !important;
    border-radius: 40px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    backdrop-filter: blur(8px);
}}

[data-testid="stTabs"] [role="tab"]:hover {{
    transform: translateY(-2px);
    background: {"rgba(212,175,114,0.12)" if _is_dark else "rgba(80,170,110,0.1)"} !important;
}}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background: {"linear-gradient(135deg,rgba(212,175,114,0.2),rgba(212,175,114,0.05))" if _is_dark else "linear-gradient(135deg,rgba(80,170,110,0.15),rgba(80,170,110,0.05))"} !important;
    border-bottom: none !important;
    box-shadow: {"0 4px 15px rgba(212,175,114,0.2)" if _is_dark else "0 4px 15px rgba(80,170,110,0.15)"} !important;
}}

/* ── Session panel with slide-in animation ─────────────────────── */
.ee-session-col {{
    transition: all 0.3s ease !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 20px !important;
}}

.ee-session-col:hover {{
    transform: translateY(-3px);
    box-shadow: {"0 15px 35px rgba(0,0,0,0.3)" if _is_dark else "0 15px 35px rgba(80,170,110,0.15)"} !important;
}}

.ee-row {{
    transition: all 0.2s ease !important;
}}

.ee-row:hover {{
    background: {"rgba(212,175,114,0.08)" if _is_dark else "rgba(80,170,110,0.06)"};
    border-radius: 8px;
    padding-left: 8px;
}}

/* ── Hooray banner with bounce animation ───────────────────────── */
@keyframes gentleBounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-5px); }}
}}

.more_enhanced_time_calculator-hooray-banner {{
    animation: gentleBounce 0.6s ease-out, glowPulse 2s infinite;
    backdrop-filter: blur(12px);
    background: linear-gradient(135deg, #1f6b3a, #0f4a2a) !important;
}}

/* ── Info alerts with slide-in ─────────────────────────────────── */
div[data-testid="stAlert"] {{
    animation: fadeInUp 0.4s ease-out;
    backdrop-filter: blur(12px);
    border-radius: 16px !important;
}}

/* ── Clock icon pulse animation ────────────────────────────────── */
@keyframes clockPulse {{
    0% {{ transform: scale(1); opacity: 1; }}
    50% {{ transform: scale(1.05); opacity: 0.9; }}
    100% {{ transform: scale(1); opacity: 1; }}
}}

/* ── Custom scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: {"rgba(57,62,70,0.5)" if _is_dark else "rgba(200,220,210,0.5)"};
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb {{
    background: {"#d4af72" if _is_dark else "#3a8a5a"};
    border-radius: 10px;
    transition: background 0.2s;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {"#e8c87a" if _is_dark else "#2a6a4a"};
}}

/* ── Loading spinner animation ─────────────────────────────────── */
@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

.stSpinner > div {{
    animation: spin 1s linear infinite !important;
    border-top-color: var(--accent-gold) !important;
}}

/* ── Smooth transitions for all interactive elements ───────────── */
button, div[data-testid="stMetric"], .stTextArea textarea, [role="tab"] {{
    transition: all 0.25s cubic-bezier(0.2, 0.9, 0.4, 1.1) !important;
}}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

# Scroll to top on every page load/refresh
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

# ── Header row: icon | title | spacer | theme toggle ──────────────────────────
hdr_icon, hdr_title, hdr_spacer, hdr_toggle = st.columns([1, 9, 2, 2], vertical_alignment="center")

with hdr_icon:
    st.markdown(CLOCK_SVG, unsafe_allow_html=True)

with hdr_title:
    st.title("More Enhanced Time Calculator")

with hdr_toggle:
    toggle_label = "☀️  Light" if _is_dark else "🌙  Dark"
    st.markdown(
        f"""
        <style>
        @keyframes ee-toggle-pulse {{
            0%   {{ box-shadow: {"0 0 0 0 rgba(212,175,114,0.35)" if _is_dark else "0 0 0 0 rgba(180,140,60,0.28)"}; }}
            70%  {{ box-shadow: {"0 0 0 7px rgba(212,175,114,0)" if _is_dark else "0 0 0 7px rgba(180,140,60,0)"}; }}
            100% {{ box-shadow: {"0 0 0 0 rgba(212,175,114,0)" if _is_dark else "0 0 0 0 rgba(180,140,60,0)"}; }}
        }}

        div[data-testid="column"]:last-child .stButton > button {{
            background: {"linear-gradient(145deg,#2a2318 0%,#1a1610 50%,#221d14 100%)" if _is_dark else "linear-gradient(145deg,#fffdf5 0%,#f7e8c0 50%,#f0d898 100%)"} !important;
            color: {"#d4af72" if _is_dark else "#6b4a0e"} !important;
            border: {"1px solid rgba(212,175,114,0.35)" if _is_dark else "1px solid rgba(180,130,40,0.45)"} !important;
            border-radius: 40px !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            padding: 0.45rem 1.3rem !important;
            min-height: 2.4rem !important;
            position: relative !important;
            overflow: hidden !important;
            box-shadow: {
                "0 2px 8px rgba(0,0,0,0.55), 0 1px 2px rgba(0,0,0,0.4), inset 0 1px 0 rgba(212,175,114,0.18), inset 0 -1px 0 rgba(0,0,0,0.3)"
                if _is_dark else
                "0 2px 8px rgba(160,120,40,0.22), 0 1px 2px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.9), inset 0 -1px 0 rgba(160,120,40,0.15)"
            } !important;
            transition: all 0.22s cubic-bezier(0.34,1.56,0.64,1) !important;
            backdrop-filter: blur(8px) !important;
        }}

        div[data-testid="column"]:last-child .stButton > button::after {{
            content: "" !important;
            position: absolute !important;
            inset: 0 !important;
            background: {"linear-gradient(180deg,rgba(212,175,114,0.08) 0%,transparent 60%)" if _is_dark else "linear-gradient(180deg,rgba(255,255,255,0.55) 0%,transparent 60%)"} !important;
            border-radius: inherit !important;
            pointer-events: none !important;
        }}

        div[data-testid="column"]:last-child .stButton > button:hover {{
            background: {"linear-gradient(145deg,#342b1e 0%,#241e14 50%,#2c2518 100%)" if _is_dark else "linear-gradient(145deg,#fff9e8 0%,#f5e0a8 50%,#edcf80 100%)"} !important;
            color: {"#e8c87a" if _is_dark else "#5a3c08"} !important;
            border-color: {"rgba(232,200,122,0.55)" if _is_dark else "rgba(160,110,20,0.6)"} !important;
            transform: translateY(-2px) scale(1.03) !important;
            box-shadow: {
                "0 6px 20px rgba(0,0,0,0.5), 0 2px 6px rgba(0,0,0,0.35), inset 0 1px 0 rgba(232,200,122,0.25), 0 0 12px rgba(212,175,114,0.18)"
                if _is_dark else
                "0 6px 18px rgba(160,120,40,0.3), 0 2px 6px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.95), 0 0 12px rgba(200,160,60,0.2)"
            } !important;
        }}

        div[data-testid="column"]:last-child .stButton > button:active {{
            transform: translateY(0px) scale(0.98) !important;
            transition: all 0.08s ease !important;
            box-shadow: {
                "0 1px 4px rgba(0,0,0,0.6), inset 0 2px 4px rgba(0,0,0,0.3)"
                if _is_dark else
                "0 1px 4px rgba(160,120,40,0.2), inset 0 2px 4px rgba(160,120,40,0.1)"
            } !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.button(toggle_label, key="btn_theme_toggle"):
        st.session_state.theme_mode = "light" if _is_dark else "dark"
        st.rerun()

st.caption(
    "Paste biometric punches under the role that applies to you. "
    "Team Member and Team Leader each keep their own log, day type, and metrics."
)
st.caption(f"Pune time (IST): {now_pune().strftime('%d-%b-%Y %I:%M:%S %p')}")

st.markdown("**Biometric log**")
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
            placeholder="Biometric.\n01:55\nBiometric.\n01:56\nBiometric.\n01:58\n...",
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

    st.markdown("**Live preview**")
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
            placeholder="Biometric.\n01:55\nBiometric.\n01:56\nBiometric.\n01:58\n...",
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

    st.markdown("**Live preview**")
    leader_live_dashboard()

st.markdown("---")
st.markdown("#### Feedback")


def submit_feedback_to_sheets(feedback_text: str) -> bool:
    """Append feedback + timestamp to the configured Google Sheet."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(st.secrets["feedback_sheet"]["sheet_id"])
        worksheet = sheet.worksheet(st.secrets["feedback_sheet"].get("worksheet", "Sheet1"))
        timestamp = now_pune().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([timestamp, feedback_text])
        return True
    except Exception as e:
        st.error(f"Could not save feedback: {e}")
        return False


# Use a counter-based key so we can reset the widget by changing its key
if "feedback_reset_counter" not in st.session_state:
    st.session_state.feedback_reset_counter = 0
if "feedback_saved" not in st.session_state:
    st.session_state.feedback_saved = False

# Show success banner BEFORE text area (persists after rerun)
if st.session_state.feedback_saved:
    st.success("❤️ Thank you for your valuable feedback! Our team is actively working to make your experience even better.")
    st.session_state.feedback_saved = False

with st.form(key="feedback_form", clear_on_submit=True):
    feedback_text = st.text_area(
        "Share your feedback",
        label_visibility="collapsed",
        placeholder=(
            "Want a new feature? Share it in the feedback form and include your Name/Email so our team can notify you once it’s implemented."
        ),
        height=100,
    )
    submitted = st.form_submit_button("Submit Feedback", use_container_width=True)

if submitted:
    stripped = (feedback_text or "").strip()
    if not stripped:
        st.warning("Please write something before submitting.")
    else:
        with st.spinner("Saving your feedback…"):
            ok = submit_feedback_to_sheets(stripped)
        if ok:
            st.session_state.feedback_saved = True
            st.rerun()
        else:
            st.error("❌ Could not save feedback. Please try again.")
