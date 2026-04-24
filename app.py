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

def now_pune() -> dt.datetime:
    return dt.datetime.now(PUNE_TZ).replace(tzinfo=None)

st.set_page_config(
    page_title="TimeTrack Pro",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------ Theme & Session ------------------------
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

# ------------------------ Custom CSS ------------------------
st.markdown("""
<style>
/* GENERAL */
* { font-family: 'Segoe UI', sans-serif; }
.stApp { background: #f3f4f6; padding: 1rem; }
@media (prefers-color-scheme: dark) { .stApp { background: #0f172a; } }

/* HEADER */
h1 { 
    font-size: 2.5rem !important; 
    font-weight: 800 !important; 
    background: linear-gradient(90deg,#4f46e5,#3b82f6); 
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.stCaption { color: #64748b !important; }
@media (prefers-color-scheme: dark) { .stCaption { color: #94a3b8 !important; } }

/* BUTTONS */
.stButton>button { 
    border-radius: 50px !important; 
    font-weight: 600 !important; 
    padding: 0.6rem 1.8rem !important; 
    color: white !important; 
    background: linear-gradient(90deg,#3b82f6,#6366f1) !important;
    transition: all 0.2s ease;
    width: 100% !important;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }

/* CARDS */
.card { 
    border-radius: 1rem; 
    padding: 1rem; 
    background: white; 
    box-shadow: 0 3px 10px rgba(0,0,0,0.05); 
    margin-bottom: 1rem;
}
@media (prefers-color-scheme: dark) { .card { background: #1e293b; box-shadow: none; } }
.card-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem; }
.card-value { font-size: 1.6rem; font-weight: 800; font-family: monospace; }

/* GRID */
.grid { display: grid; gap: 1rem; margin: 1rem 0; }
.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-5 { grid-template-columns: repeat(5, 1fr); }

/* SESSION PANEL */
.session-panel { border-radius: 1rem; overflow: hidden; }
.session-header { padding: 0.6rem 1rem; font-weight: 600; color: white; }
.session-work { background: #3b82f6; }
.session-break { background: #f59e0b; }
.session-row { display: flex; justify-content: space-between; padding: 0.5rem 1rem; border-bottom: 1px solid #e2e8f0; }
@media (prefers-color-scheme: dark) { .session-row { border-color: #334155; } }
.session-duration.work { color: #dbeafe; font-weight: 600; }
.session-duration.break { color: #ffedd5; font-weight: 600; }
.live-badge { background: #10b981; color: white; font-size: 0.6rem; font-weight: 600; padding: 2px 8px; border-radius: 20px; margin-left: 0.5rem; }

/* SUCCESS BANNER */
.success-banner { 
    background: linear-gradient(90deg,#10b981,#059669); 
    color: white; 
    text-align: center; 
    padding: 1rem; 
    border-radius: 1rem; 
    font-weight: 700; 
}
</style>
""", unsafe_allow_html=True)

# ------------------------ UTILITY ------------------------
def format_clock(seconds: int) -> str:
    seconds = max(seconds, 0)
    h = seconds // 3600; m = (seconds % 3600) // 60; s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_human(seconds: int) -> str:
    seconds = max(seconds, 0)
    h = seconds // 3600; m = (seconds % 3600) // 60
    return f"{h}h {m}m" if h else f"{m}m"

# ------------------------ DAY TYPES & THRESHOLDS ------------------------
DAY_FULL = "Full Day"
DAY_HALF = "Half Day"
DAY_TYPE_OPTIONS = (DAY_FULL, DAY_HALF)
MEMBER_THRESHOLDS = {DAY_FULL: 27000, DAY_HALF: 16200}
LEADER_THRESHOLDS = {DAY_FULL: 25200, DAY_HALF: 14400}
BREAK_TARGET = 5400

def member_threshold(day_type: str) -> int: return MEMBER_THRESHOLDS.get(day_type, 27000)
def leader_threshold(day_type: str) -> int: return LEADER_THRESHOLDS.get(day_type, 25200)

# ------------------------ LOG PARSING ------------------------
def extract_times(log_text: str) -> list[dt.datetime]:
    matches = re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", log_text)
    today = now_pune().date(); points=[]; last=None
    for m in matches:
        h, min_val = map(int, m.split(":"))
        candidate = dt.datetime.combine(today, dt.time(h, min_val))
        if last and candidate < last: today += dt.timedelta(days=1); candidate = dt.datetime.combine(today, dt.time(h, min_val))
        points.append(candidate); last = candidate
    return points

def normalize_paste_text(raw: str) -> str: return (raw or "").replace("\r\n", "\n")
def parse_log(log_text: str) -> list[dt.datetime] | None:
    pts = extract_times(log_text); return pts if len(pts)>=1 else None

def analyze_sessions(points: list[dt.datetime], current: dt.datetime = None) -> dict:
    current = current or now_pune()
    work_sessions=[]; break_sessions=[]; total_work=0; total_break=0
    for i in range(len(points)-1):
        start, end = points[i], points[i+1]; duration = int((end-start).total_seconds())
        session={"start":start.strftime("%I:%M %p").lstrip("0"),"end":end.strftime("%I:%M %p").lstrip("0"),"duration":duration,"human":format_human(duration)}
        if i%2==0: work_sessions.append(session); total_work+=duration
        else: break_sessions.append(session); total_break+=duration
    ongoing=0; has_ongoing=False
    if len(points)%2==1:
        last=points[-1]; ongoing=int((current-last).total_seconds()); has_ongoing=True
        work_sessions.append({"start":last.strftime("%I:%M %p").lstrip("0"),"end":current.strftime("%I:%M %p").lstrip("0"),"duration":ongoing,"human":format_human(ongoing),"ongoing":True})
    return {"work_sessions":work_sessions,"break_sessions":break_sessions,"total_work":total_work,"total_break":total_break,"ongoing_work":ongoing,"has_ongoing":has_ongoing}

# ------------------------ DASHBOARD COMPONENTS ------------------------
def render_stats_grid(stats: dict):
    st.markdown('<div class="grid grid-5">', unsafe_allow_html=True)
    labels = ["Total Work","Break Time","Total Time","Remaining Work","Remaining Break"]
    values = [stats["total_work"], stats["total_break"], stats["total_work"]+stats["total_break"], stats["remaining_work"], stats["remaining_break"]]
    for label, value in zip(labels, values):
        st.markdown(f'<div class="card"><div class="card-title">{label}</div><div class="card-value">{format_clock(value)}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_sessions_panel(work: list, breaks: list):
    st.markdown('<div class="grid grid-2">', unsafe_allow_html=True)
    for sessions, s_type in [(work,'work'),(breaks,'break')]:
        st.markdown(f'<div class="session-panel card"><div class="session-header session-{s_type}">{"🕐 WORK" if s_type=="work" else "☕ BREAK"} SESSIONS · {len(sessions)}</div>', unsafe_allow_html=True)
        if sessions:
            for s in sessions:
                live = '<span class="live-badge">LIVE</span>' if s.get("ongoing") else ''
                st.markdown(f'<div class="session-row"><span>{s["start"]} → {s["end"]}{live}</span><span class="session-duration {s_type}">{s["human"]}</span></div>', unsafe_allow_html=True)
        else: st.markdown('<div class="session-row"><span>No sessions</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_logout_status(deadline: dt.datetime, first: dt.datetime, now: dt.datetime):
    if now < deadline:
        time_str = deadline.strftime("%I:%M %p").lstrip("0")
        if deadline.date() != first.date(): time_str = deadline.strftime("%d %b, %I:%M %p").lstrip("0")
        st.markdown(f'<div class="card"><div class="card-title">⏰ Earliest Logout</div><div class="card-value">{time_str}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-banner">🎉 TARGET COMPLETED! You\'re Free to Go! 🎉</div>', unsafe_allow_html=True)

def dashboard(points, day_type, is_leader=False):
    now = now_pune(); result = analyze_sessions(points, now)
    required = leader_threshold(day_type) if is_leader else member_threshold(day_type)
    total_work = result["total_work"]+result["ongoing_work"]
    remaining = max(required-total_work,0)
    deadline = now + dt.timedelta(seconds=remaining)
    remaining_break = max(BREAK_TARGET - result["total_break"],0)
    stats={"total_work":total_work,"total_break":result["total_break"],"remaining_work":remaining,"remaining_break":remaining_break}
    st.caption(f"{'👑 Leader' if is_leader else '👤 Member'} Clocked in: {points[0].strftime('%I:%M %p').lstrip('0')} on {points[0].strftime('%d %b %Y')}")
    render_stats_grid(stats)
    render_sessions_panel(result["work_sessions"], result["break_sessions"])
    render_logout_status(deadline, points[0], now)

# ------------------------ HEADER ------------------------
col1,col2,col3 = st.columns([1,8,2])
with col1: st.markdown('<span style="font-size:2.5rem;">⏱️</span>', unsafe_allow_html=True)
with col2: st.title("TimeTrack Pro"); st.caption("Intelligent Biometric Time Analysis")
with col3:
    theme_label = "🌙 Dark Mode" if st.session_state.theme_mode=="light" else "☀️ Light Mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode=="light" else "light"; st.rerun()
st.caption(f"📍 Pune, India (IST) • {now_pune().strftime('%A, %d %B %Y • %I:%M:%S %p')}")

# ------------------------ MAIN TABS ------------------------
tab1, tab2 = st.tabs(["👤 TEAM MEMBER","👑 TEAM LEADER"])

with tab1:
    day_type = st.radio("Day Type", DAY_TYPE_OPTIONS, index=0 if st.session_state.member_day_type==DAY_FULL else 1, horizontal=True)
    st.session_state.member_day_type = day_type
    with st.form("member_form"):
        log = st.text_area("Biometric Log", height=150, placeholder="Paste log here...", key="member_input")
        if st.form_submit_button("🔍 Calculate & Track", use_container_width=True):
            pts = parse_log(normalize_paste_text(log))
            if pts: st.session_state.member_points=pts; st.success(f"✅ Parsed {len(pts)} entries")
            else: st.session_state.member_points=None; st.error("❌ Invalid times (HH:MM)")
    if st.session_state.member_points: dashboard(st.session_state.member_points, day_type)

with tab2:
    day_type = st.radio("Day Type", DAY_TYPE_OPTIONS, index=0 if st.session_state.leader_day_type==DAY_FULL else 1, horizontal=True)
    st.session_state.leader_day_type = day_type
    with st.form("leader_form"):
        log = st.text_area("Biometric Log", height=150, placeholder="Paste log here...", key="leader_input")
        if st.form_submit_button("🔍 Calculate & Track", use_container_width=True):
            pts = parse_log(normalize_paste_text(log))
            if pts: st.session_state.leader_points=pts; st.success(f"✅ Parsed {len(pts)} entries")
            else: st.session_state.leader_points=None; st.error("❌ Invalid times (HH:MM)")
    if st.session_state.leader_points: dashboard(st.session_state.leader_points, day_type, is_leader=True)
