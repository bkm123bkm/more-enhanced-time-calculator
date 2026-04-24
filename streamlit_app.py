import datetime as dt
import re
from zoneinfo import ZoneInfo
import streamlit as st

# ------------------- SETTINGS -------------------
PUNE_TZ = ZoneInfo("Asia/Kolkata")
DAY_FULL = "Full Day"
DAY_HALF = "Half Day"
DAY_TYPE_OPTIONS = (DAY_FULL, DAY_HALF)
MEMBER_THRESHOLDS = {DAY_FULL: 27000, DAY_HALF: 16200}
LEADER_THRESHOLDS = {DAY_FULL: 25200, DAY_HALF: 14400}
BREAK_TARGET = 5400

# ------------------- SESSION STATE -------------------
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None

# ------------------- UTILITY FUNCTIONS -------------------
def now_pune() -> dt.datetime:
    return dt.datetime.now(PUNE_TZ).replace(tzinfo=None)

def format_clock(seconds: int) -> str:
    h, m, s = seconds//3600, (seconds%3600)//60, seconds%60
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_human(seconds: int) -> str:
    h, m = seconds//3600, (seconds%3600)//60
    return f"{h}h {m}m" if h>0 else f"{m}m"

def extract_times(log_text: str):
    matches = re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", log_text)
    today = now_pune().date()
    points = []
    last = None
    for m in matches:
        h, mi = map(int, m.split(":"))
        candidate = dt.datetime.combine(today, dt.time(h, mi))
        if last and candidate < last:
            today += dt.timedelta(days=1)
            candidate = dt.datetime.combine(today, dt.time(h, mi))
        points.append(candidate)
        last = candidate
    return points

def parse_log(log_text: str):
    pts = extract_times(log_text)
    return pts if pts else None

def analyze_sessions(points: list[dt.datetime], current=None):
    if current is None: current = now_pune()
    work_sessions, break_sessions, total_work, total_break = [], [], 0, 0
    for i in range(len(points)-1):
        start, end = points[i], points[i+1]
        dur = int((end-start).total_seconds())
        s = {"start": start.strftime("%I:%M %p").lstrip("0"), "end": end.strftime("%I:%M %p").lstrip("0"),
             "duration": dur, "human": format_human(dur)}
        if i%2==0: work_sessions.append(s); total_work+=dur
        else: break_sessions.append(s); total_break+=dur
    ongoing, has_ongoing = 0, False
    if len(points)%2==1:
        last = points[-1]
        ongoing = int((current-last).total_seconds())
        has_ongoing = True
        work_sessions.append({"start": last.strftime("%I:%M %p").lstrip("0"),
                              "end": current.strftime("%I:%M %p").lstrip("0"),
                              "duration": ongoing, "human": format_human(ongoing), "ongoing": True})
    return {"work_sessions": work_sessions, "break_sessions": break_sessions,
            "total_work": total_work, "total_break": total_break,
            "ongoing_work": ongoing, "has_ongoing": has_ongoing}

def threshold(day_type, leader=False):
    return LEADER_THRESHOLDS[day_type] if leader else MEMBER_THRESHOLDS[day_type]

def normalize_text(text: str):
    return (text or "").replace("\r\n","\n")

# ------------------- CSS -------------------
st.markdown("""
<style>
/* General */
body, .stApp { font-family: 'Segoe UI', sans-serif; background:#f5f7fb; }
@media (prefers-color-scheme: dark){.stApp{background:#0f172a;}}

/* Header */
h1 { font-size:2rem;font-weight:700; background: linear-gradient(135deg,#3b82f6,#8b5cf6); -webkit-background-clip: text; color:transparent;}

/* Stats cards */
.stats-grid { display:flex; gap:1rem; margin:1rem 0;}
.card { background:white; flex:1; border-radius:15px; padding:1rem; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.05);}
.card-title { font-weight:600; color:#64748b; font-size:0.8rem; }
.card-value { font-size:1.5rem; font-weight:700; margin-top:0.3rem; color:#1e293b;}
@media (prefers-color-scheme: dark){.card{background:#1e293b;}.card-value{color:#f1f5f9;}}

/* Buttons */
.stButton>button{background:linear-gradient(135deg,#3b82f6,#2563eb);color:white;border-radius:40px;padding:0.5rem 1.5rem;font-weight:600;transition:all 0.2s;}
.stButton>button:hover{transform:translateY(-1px); box-shadow:0 4px 12px rgba(59,130,246,0.3);}

/* Session panels timeline */
.session-panel{background:white; border-radius:15px; padding:1rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(0,0,0,0.05);}
.session-header{font-weight:600;margin-bottom:0.5rem;}
.session-row{display:flex; justify-content:space-between; padding:0.5rem 0;border-top:1px solid #e2e8f0;}
.session-row:first-child{border-top:none;}
.session-duration.work{color:#3b82f6;font-weight:600;}
.session-duration.break{color:#f59e0b;font-weight:600;}
.live-badge{background:#10b981;color:white;padding:2px 8px;border-radius:20px;font-size:0.7rem;margin-left:8px;}
@media (prefers-color-scheme: dark){
    .session-panel{background:#1e293b;border-color:#334155;}
    .session-row{border-color:#334155;}
}

/* Logout/Success */
.logout-card{background:white;border-radius:15px;padding:1rem;text-align:center;margin-top:1rem;box-shadow:0 2px 8px rgba(0,0,0,0.05);}
.logout-time{font-size:1.5rem;font-weight:700;color:#3b82f6;font-family:monospace;}
.success-banner{background:linear-gradient(135deg,#10b981,#059669);border-radius:15px;padding:1rem;text-align:center;color:white;font-weight:600;margin-top:1rem;}
</style>
""", unsafe_allow_html=True)

# ------------------- DASHBOARD RENDER -------------------
def render_stats(stats):
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    for label, value in stats.items():
        st.markdown(f'<div class="card"><div class="card-title">{label.replace("_"," ").title()}</div><div class="card-value">{format_clock(value)}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_sessions(work, breaks):
    for s_type, sessions in [("work", work),("break", breaks)]:
        st.markdown(f'<div class="session-panel"><div class="session-header">{"🕐 Work Sessions" if s_type=="work" else "☕ Break Sessions"} · {len(sessions)}</div>', unsafe_allow_html=True)
        for s in sessions:
            live = '<span class="live-badge">LIVE</span>' if s.get("ongoing") else ''
            st.markdown(f'<div class="session-row"><span>{s["start"]} → {s["end"]}{live}</span><span class="session-duration {s_type}">{s["human"]}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_logout(deadline, first, now):
    if now<deadline:
        t_str = deadline.strftime("%I:%M %p").lstrip("0")
        st.markdown(f'<div class="logout-card"><div>⏰ Earliest Logout</div><div class="logout-time">{t_str}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-banner">🎉 TARGET COMPLETED! You\'re Free to Go! 🎉</div>', unsafe_allow_html=True)

def dashboard(points, day_type, leader=False):
    now = now_pune()
    result = analyze_sessions(points, now)
    req = threshold(day_type, leader)
    total_work = result["total_work"] + result["ongoing_work"]
    remaining = max(req-total_work,0)
    deadline = now + dt.timedelta(seconds=remaining)
    remaining_break = max(BREAK_TARGET - result["total_break"],0)
    stats = {"Total Work": total_work, "Break Time": result["total_break"], "Remaining Work": remaining, "Remaining Break": remaining_break}
    st.caption(f"⏱ Clocked in: {points[0].strftime('%I:%M %p').lstrip('0')} on {points[0].strftime('%d %b %Y')}")
    render_stats(stats)
    if result["has_ongoing"]:
        if st.button("📋 Show/Hide Sessions", key=f"{'leader' if leader else 'member'}_toggle"):
            st.session_state[f"show_sessions_{'leader' if leader else 'member'}"] = not st.session_state.get(f"show_sessions_{'leader' if leader else 'member'}", False)
        if st.session_state.get(f"show_sessions_{'leader' if leader else 'member'}", False):
            render_sessions(result["work_sessions"], result["break_sessions"])
    render_logout(deadline, points[0], now)

# ------------------- HEADER -------------------
col1, col2, col3 = st.columns([1,8,2])
with col1: st.markdown('<span style="font-size:2.5rem;">⏱️</span>', unsafe_allow_html=True)
with col2: st.title("TimeTrack Pro"); st.caption("Intelligent Biometric Time Analysis")
with col3:
    theme_label = "🌙 Dark Mode" if st.session_state.theme_mode=="light" else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle"): 
        st.session_state.theme_mode = "dark" if st.session_state.theme_mode=="light" else "light"; st.experimental_rerun()
st.caption(f"📍 Pune, India • {now_pune().strftime('%A, %d %B %Y • %I:%M:%S %p')}")

# ------------------- TABS -------------------
tab1, tab2 = st.tabs(["👤 TEAM MEMBER", "👑 TEAM LEADER"])

with tab1:
    day_type = st.radio("Day Type", DAY_TYPE_OPTIONS, index=0, horizontal=True, key="member_day_radio")
    st.session_state.member_day_type = day_type
    with st.form("member_form"):
        log = st.text_area("Biometric Log", height=150, placeholder="Paste your biometric log...", key="member_input")
        submitted = st.form_submit_button("🔍 Calculate & Track", key="member_submit")
        if submitted:
            pts = parse_log(normalize_text(log))
            if pts: st.session_state.member_points=pts; st.success(f"✅ Parsed {len(pts)} entries")
            else: st.error("❌ Invalid times"); st.session_state.member_points=None
    st.markdown("---")
    if st.session_state.member_points: dashboard(st.session_state.member_points, day_type, leader=False)

with tab2:
    day_type = st.radio("Day Type", DAY_TYPE_OPTIONS, index=0, horizontal=True, key="leader_day_radio")
    st.session_state.leader_day_type = day_type
    with st.form("leader_form"):
        log = st.text_area("Biometric Log", height=150, placeholder="Paste your biometric log...", key="leader_input")
        submitted = st.form_submit_button("🔍 Calculate & Track", key="leader_submit")
        if submitted:
            pts = parse_log(normalize_text(log))
            if pts: st.session_state.leader_points=pts; st.success(f"✅ Parsed {len(pts)} entries")
            else: st.error("❌ Invalid times"); st.session_state.leader_points=None
    st.markdown("---")
    if st.session_state.leader_points: dashboard(st.session_state.leader_points, day_type, leader=True)
