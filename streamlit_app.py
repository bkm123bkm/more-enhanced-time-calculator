import datetime as dt
from pathlib import Path
import re
from zoneinfo import ZoneInfo
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "Icon.png"
PAGE_ICON = str(ICON_PATH) if ICON_PATH.exists() else "⏱️"
PUNE_TZ = ZoneInfo("Asia/Kolkata")

DAY_FULL = "Full Day"
DAY_HALF = "Half Day"
DAY_TYPE_OPTIONS = (DAY_FULL, DAY_HALF)

MEMBER_THRESHOLDS = {DAY_FULL: 27000, DAY_HALF: 16200}
LEADER_THRESHOLDS = {DAY_FULL: 25200, DAY_HALF: 14400}
BREAK_TARGET = 5400


def now_pune() -> dt.datetime:
    return dt.datetime.now(PUNE_TZ).replace(tzinfo=None)


# -------------------- SESSION STATE --------------------
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None
if "member_day_type" not in st.session_state:
    st.session_state.member_day_type = DAY_FULL
if "leader_day_type" not in st.session_state:
    st.session_state.leader_day_type = DAY_FULL

st.set_page_config(
    page_title="TimeTrack Pro",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- CSS STYLE --------------------
st.markdown("""
<style>
/* Global */
* { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.stApp { background: #f5f7fb; padding: 0.5rem; }
@media (prefers-color-scheme: dark) { .stApp { background: #0f172a; } }

/* Header */
h1 { font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; background-clip: text; color: transparent; }

/* Metric Cards */
.stat-card { background:white; border-radius:1rem; padding:1rem; text-align:center; box-shadow:0 2px 5px rgba(0,0,0,0.1); border:1px solid #e2e8f0; }
@media (prefers-color-scheme: dark) { .stat-card { background:#1e293b; border-color:#334155; } }
.stat-label { font-size:0.75rem; text-transform:uppercase; color:#64748b; margin-bottom:0.5rem; }
.stat-value { font-size:1.5rem; font-weight:700; color:#1e293b; font-family: monospace; }
@media (prefers-color-scheme: dark) { .stat-value { color:#f1f5f9; } }

/* Session Panel */
.sessions-panel { display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin:1rem 0; }
.session-card { background:white; border-radius:1rem; border:1px solid #e2e8f0; overflow:hidden; }
@media (prefers-color-scheme: dark) { .session-card { background:#1e293b; border-color:#334155; } }
.session-header { padding:0.75rem 1rem; font-weight:600; border-bottom:1px solid #e2e8f0; }
.session-header.work { background: rgba(59, 130, 246, 0.1); color:#3b82f6; }
.session-header.break { background: rgba(245, 158, 11, 0.1); color:#f59e0b; }
.session-row { display:flex; justify-content:space-between; padding:0.75rem 1rem; border-bottom:1px solid #e2e8f0; }
.session-duration.work { color:#3b82f6; font-weight:600; }
.session-duration.break { color:#f59e0b; font-weight:600; }
.live-badge { background:#10b981; padding:2px 8px; border-radius:20px; font-size:0.6rem; font-weight:600; color:white; margin-left:8px; }

/* Logout Card */
.logout-card { background:white; border-radius:1rem; padding:1rem; text-align:center; border:1px solid #e2e8f0; margin-top:1rem; }
@media (prefers-color-scheme: dark) { .logout-card { background:#1e293b; border-color:#334155; } }
.logout-time { font-size:1.5rem; font-weight:700; color:#3b82f6; font-family: monospace; }
.success-banner { background: linear-gradient(135deg,#10b981,#059669); border-radius:1rem; padding:1rem; text-align:center; margin-top:1rem; }
.success-banner p { color:white !important; font-weight:600; margin:0; }

/* Buttons */
.stButton > button { background: linear-gradient(135deg,#3b82f6,#2563eb)!important; color:white!important; border:none!important; border-radius:40px!important; padding:0.5rem 1.5rem!important; font-weight:600!important; width:100%!important; }
.stButton > button:hover { transform:translateY(-1px); box-shadow:0 4px 12px rgba(59,130,246,0.3); }
</style>
""", unsafe_allow_html=True)

# -------------------- UTILITIES --------------------
def format_clock(seconds:int) -> str:
    seconds=max(seconds,0)
    h=seconds//3600
    m=(seconds%3600)//60
    s=seconds%60
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_human(seconds:int) -> str:
    seconds=max(seconds,0)
    h=seconds//3600
    m=(seconds%3600)//60
    return f"{h}h {m}m" if h>0 else f"{m}m"

def threshold(day_type:str, leader=False) -> int:
    if leader: return LEADER_THRESHOLDS.get(day_type, 25200)
    return MEMBER_THRESHOLDS.get(day_type, 27000)

def extract_times(log_text:str) -> list[dt.datetime]:
    matches = re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", log_text)
    today = now_pune().date()
    points = []
    last = None
    for m in matches:
        h, mi = map(int,m.split(":"))
        candidate = dt.datetime.combine(today, dt.time(h,mi))
        if last and candidate<last:
            today += dt.timedelta(days=1)
            candidate = dt.datetime.combine(today, dt.time(h,mi))
        points.append(candidate)
        last = candidate
    return points

def parse_log(text:str):
    pts = extract_times(text)
    return pts if len(pts)>=1 else None

def normalize_text(raw:str) -> str:
    return (raw or "").replace("\r\n","\n")

def analyze_sessions(points:list[dt.datetime], current=None):
    if current is None: current=now_pune()
    work_sessions, break_sessions = [], []
    total_work, total_break = 0,0
    for i in range(len(points)-1):
        start, end = points[i], points[i+1]
        duration = int((end-start).total_seconds())
        session={"start":start.strftime("%I:%M %p").lstrip("0"),
                 "end":end.strftime("%I:%M %p").lstrip("0"),
                 "duration":duration,
                 "human":format_human(duration)}
        if i%2==0:
            work_sessions.append(session)
            total_work += duration
        else:
            break_sessions.append(session)
            total_break += duration
    ongoing, has_ongoing = 0, False
    if len(points)%2==1:
        last=points[-1]
        if current<last: current+=dt.timedelta(days=1)
        ongoing=int((current-last).total_seconds())
        has_ongoing=True
        work_sessions.append({"start":last.strftime("%I:%M %p").lstrip("0"),
                              "end":current.strftime("%I:%M %p").lstrip("0"),
                              "duration":ongoing,"human":format_human(ongoing),
                              "ongoing":True})
    return {"work_sessions":work_sessions,"break_sessions":break_sessions,
            "total_work":total_work,"total_break":total_break,
            "ongoing_work":ongoing,"has_ongoing":has_ongoing}

# -------------------- RENDER --------------------
def render_stats(stats:dict):
    cols = st.columns(len(stats))
    for col,(label,value) in zip(cols, stats.items()):
        with col:
                        st.markdown(f'<div class="stat-card"><div class="stat-label">{label}</div>'
                        f'<div class="stat-value">{format_clock(value) if isinstance(value,int) else value}</div></div>',
                        unsafe_allow_html=True)

def render_sessions(work:list, breaks:list):
    st.markdown('<div class="sessions-panel">', unsafe_allow_html=True)
    
    # Work Sessions
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header work">🕐 WORK SESSIONS · {len(work)}</div>', unsafe_allow_html=True)
    if work:
        for s in work:
            live = '<span class="live-badge">LIVE</span>' if s.get("ongoing") else ""
            st.markdown(f'<div class="session-row"><span>{s["start"]} → {s["end"]}{live}</span>'
                        f'<span class="session-duration work">{s["human"]}</span></div>',
                        unsafe_allow_html=True)
    else:
        st.markdown('<div class="session-row">No work sessions</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Break Sessions
    st.markdown('<div class="session-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="session-header break">☕ BREAK SESSIONS · {len(breaks)}</div>', unsafe_allow_html=True)
    if breaks:
        for s in breaks:
            st.markdown(f'<div class="session-row"><span>{s["start"]} → {s["end"]}</span>'
                        f'<span class="session-duration break">{s["human"]}</span></div>',
                        unsafe_allow_html=True)
    else:
        st.markdown('<div class="session-row">No breaks taken</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_logout(deadline:dt.datetime, first:dt.datetime, now:dt.datetime):
    if now<deadline:
        time_str = deadline.strftime("%I:%M %p").lstrip("0")
        if deadline.date()!=first.date():
            time_str = deadline.strftime("%d %b, %I:%M %p").lstrip("0")
        st.markdown(f'<div class="logout-card"><div style="font-size:0.8rem;color:#64748b;">⏰ Earliest Logout Time</div>'
                    f'<div class="logout-time">{time_str}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-banner"><p>🎉 TARGET COMPLETED! You\'re Free to Go! 🎉</p></div>', unsafe_allow_html=True)

def dashboard(points:list, day_type:str, leader=False):
    now = now_pune()
    result = analyze_sessions(points, now)
    required = threshold(day_type, leader)
    total_work = result["total_work"] + result["ongoing_work"]
    remaining = max(required - total_work,0)
    deadline = now + dt.timedelta(seconds=remaining)
    remaining_break = max(BREAK_TARGET - result["total_break"],0)
    
    stats = {
        "Total Work": total_work,
        "Break Time": result["total_break"],
        "Total Time": total_work + result["total_break"],
        "Remaining Work": remaining,
        "Remaining Break": remaining_break
    }
    
    st.caption(f"{'👑 Leader' if leader else '👤 Member'} Clocked in: {points[0].strftime('%I:%M %p').lstrip('0')} on {points[0].strftime('%d %b %Y')}")
    
    render_stats(stats)
    
    if result["has_ongoing"]:
        if st.button("📋 Show/Hide Session Details", key=f"{'leader' if leader else 'member'}_toggle"):
            st.session_state[f"show_{'leader' if leader else 'member'}_sessions"] = not st.session_state.get(f"show_{'leader' if leader else 'member'}_sessions", False)
        if st.session_state.get(f"show_{'leader' if leader else 'member'}_sessions", False):
            render_sessions(result["work_sessions"], result["break_sessions"])
    
    render_logout(deadline, points[0], now)

# -------------------- HEADER --------------------
col1, col2, col3 = st.columns([1,8,2])
with col1: st.markdown('<span style="font-size:2.5rem;">⏱️</span>', unsafe_allow_html=True)
with col2:
    st.title("TimeTrack Pro")
    st.caption("Intelligent Biometric Time Analysis")
with col3:
    theme_label = "🌙 Dark Mode" if st.session_state.theme_mode=="light" else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle"):
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode=="light" else "light"
        st.experimental_rerun()

st.caption(f"📍 Pune, India (IST) • {now_pune().strftime('%A, %d %B %Y • %I:%M:%S %p')}")

# -------------------- TABS --------------------
tab1, tab2 = st.tabs(["👤 TEAM MEMBER", "👑 TEAM LEADER"])

with tab1:
    day_type = st.radio("Day Type", DAY_TYPE_OPTIONS, index=0 if st.session_state.member_day_type==DAY_FULL else 1, horizontal=True, key="member_day_radio")
    st.session_state.member_day_type = day_type
    with st.form("member_form"):
        log = st.text_area("Biometric Log", height=150, placeholder="Paste your biometric log here...\nExample:\n09:15\n13:00\n14:00\n18:30", key="member_input")
        submitted = st.form_submit_button("🔍 Calculate & Track")
    if submitted:
        pts = parse_log(normalize_text(log))
        if pts:
            st.session_state.member_points = pts
            st.success(f"✅ Successfully parsed {len(pts)} time entries")
        else:
            st.session_state.member_points = None
            st.error("❌ Please enter valid times in HH:MM format")
    if st.session_state.member_points: dashboard(st.session_state.member_points, day_type, leader=False)

with tab2:
    day_type = st.radio("Day Type", DAY_TYPE_OPTIONS, index=0 if st.session_state.leader_day_type==DAY_FULL else 1, horizontal=True, key="leader_day_radio")
    st.session_state.leader_day_type = day_type
    with st.form("leader_form"):
        log = st.text_area("Biometric Log", height=150, placeholder="Paste your biometric log here...\nExample:\n09:15\n13:00\n14:00\n18:30", key="leader_input")
        submitted = st.form_submit_button("🔍 Calculate & Track")
    if submitted:
        pts = parse_log(normalize_text(log))
        if pts:
            st.session_state.leader_points = pts
            st.success(f"✅ Successfully parsed {len(pts)} time entries")
        else:
            st.session_state.leader_points = None
            st.error("❌ Please enter valid times in HH:MM format")
    if st.session_state.leader_points: dashboard(st.session_state.leader_points, day_type, leader=True)
