import datetime as dt
import re
from zoneinfo import ZoneInfo
import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TimeTrack Pro", page_icon="⏱️", layout="wide")

PUNE_TZ = ZoneInfo("Asia/Kolkata")

DAY_FULL = "Full Day"
DAY_HALF = "Half Day"
DAY_TYPE_OPTIONS = (DAY_FULL, DAY_HALF)

MEMBER_THRESHOLDS = {DAY_FULL: 27000, DAY_HALF: 16200}
LEADER_THRESHOLDS = {DAY_FULL: 25200, DAY_HALF: 14400}
BREAK_TARGET = 5400

# ---------------- STATE ----------------
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None

# ---------------- UTILS ----------------
def now_pune():
    return dt.datetime.now(PUNE_TZ).replace(tzinfo=None)

def format_clock(sec):
    sec = max(sec, 0)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_human(sec):
    sec = max(sec, 0)
    h = sec // 3600
    m = (sec % 3600) // 60
    return f"{h}h {m}m" if h else f"{m}m"

def extract_times(text):
    matches = re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", text)
    today = now_pune().date()
    pts = []
    last = None

    for m in matches:
        h, mi = map(int, m.split(":"))
        t = dt.datetime.combine(today, dt.time(h, mi))
        if last and t < last:
            today += dt.timedelta(days=1)
            t = dt.datetime.combine(today, dt.time(h, mi))
        pts.append(t)
        last = t

    return pts

def analyze(points):
    now = now_pune()
    work, breaks = [], []
    tw, tb = 0, 0

    for i in range(len(points) - 1):
        d = int((points[i+1] - points[i]).total_seconds())
        s = {
            "start": points[i].strftime("%I:%M %p").lstrip("0"),
            "end": points[i+1].strftime("%I:%M %p").lstrip("0"),
            "dur": d,
            "human": format_human(d)
        }
        if i % 2 == 0:
            work.append(s)
            tw += d
        else:
            breaks.append(s)
            tb += d

    ongoing = 0
    if len(points) % 2 == 1:
        last = points[-1]
        ongoing = int((now - last).total_seconds())
        work.append({
            "start": last.strftime("%I:%M %p").lstrip("0"),
            "end": now.strftime("%I:%M %p").lstrip("0"),
            "human": format_human(ongoing),
            "ongoing": True
        })

    return work, breaks, tw, tb, ongoing

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {background:#f5f7fb;}
h1 {background:linear-gradient(90deg,#3b82f6,#8b5cf6);
-webkit-background-clip:text;color:transparent;}

.card {
background:white;
padding:1rem;
border-radius:15px;
text-align:center;
box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

.session {
background:white;
padding:1rem;
border-radius:15px;
margin-top:1rem;
}

.success {
background:linear-gradient(135deg,#10b981,#059669);
color:white;
padding:1rem;
border-radius:15px;
text-align:center;
font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- RENDER ----------------
def render_dashboard(points, day_type, leader=False):
    work, breaks, tw, tb, ongoing = analyze(points)

    req = LEADER_THRESHOLDS[day_type] if leader else MEMBER_THRESHOLDS[day_type]
    total = tw + ongoing
    rem = max(req - total, 0)

    st.markdown("### 📊 Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f'<div class="card">Work<br><b>{format_clock(total)}</b></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card">Break<br><b>{format_clock(tb)}</b></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card">Remaining<br><b>{format_clock(rem)}</b></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="card">Sessions<br><b>{len(work)}</b></div>', unsafe_allow_html=True)

    st.markdown("### 🧠 Sessions")

    for s in work:
        live = " 🔴 LIVE" if s.get("ongoing") else ""
        st.markdown(f'<div class="session">🕐 {s["start"]} → {s["end"]}{live} | {s["human"]}</div>', unsafe_allow_html=True)

    for s in breaks:
        st.markdown(f'<div class="session">☕ {s["start"]} → {s["end"]} | {s["human"]}</div>', unsafe_allow_html=True)

    if rem == 0:
        st.markdown('<div class="success">🎉 TARGET COMPLETE</div>', unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("⏱️ TimeTrack Pro")
st.caption(f"📍 IST • {now_pune().strftime('%A %d %B %Y %I:%M:%S %p')}")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["👤 Member", "👑 Leader"])

# MEMBER
with tab1:
    d = st.radio("Day Type", DAY_TYPE_OPTIONS, horizontal=True, key="m_day")

    with st.form("m_form"):
        txt = st.text_area("Paste Log", key="m_txt")
        sub = st.form_submit_button("Calculate")

    if sub:
        pts = extract_times(txt)
        if pts:
            st.session_state.member_points = pts
        else:
            st.error("Invalid input")

    if st.session_state.member_points:
        render_dashboard(st.session_state.member_points, d)

# LEADER
with tab2:
    d = st.radio("Day Type", DAY_TYPE_OPTIONS, horizontal=True, key="l_day")

    with st.form("l_form"):
        txt = st.text_area("Paste Log", key="l_txt")
        sub = st.form_submit_button("Calculate")

    if sub:
        pts = extract_times(txt)
        if pts:
            st.session_state.leader_points = pts
        else:
            st.error("Invalid input")

    if st.session_state.leader_points:
        render_dashboard(st.session_state.leader_points, d, leader=True)
