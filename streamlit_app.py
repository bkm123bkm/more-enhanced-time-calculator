import streamlit as st
import datetime as dt
import re
from zoneinfo import ZoneInfo

# ---------------- CONFIG ----------------
st.set_page_config(layout="wide", page_title="TimeTrack Pro")

PUNE = ZoneInfo("Asia/Kolkata")

# ---------------- STATE ----------------
if "member_points" not in st.session_state:
    st.session_state.member_points = None
if "leader_points" not in st.session_state:
    st.session_state.leader_points = None
if "member_day" not in st.session_state:
    st.session_state.member_day = "Full Day"
if "leader_day" not in st.session_state:
    st.session_state.leader_day = "Full Day"

# ---------------- CSS (FULL REDESIGN) ----------------
st.markdown("""
<style>

body, .stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Glass Card */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Header */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:20px;
}

.title {
    font-size:28px;
    font-weight:700;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    border:none;
    color:white;
    border-radius:12px;
    padding:10px;
    font-weight:600;
}

/* Textarea */
textarea {
    background:#020617 !important;
    color:white !important;
}

/* Stats */
.stats {
    display:grid;
    grid-template-columns: repeat(5,1fr);
    gap:15px;
    margin-top:20px;
}

.stat {
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:16px;
    text-align:center;
}

.stat h3 {
    font-size:12px;
    color:#94a3b8;
}

.stat p {
    font-size:20px;
    font-weight:700;
}

/* Sessions */
.session {
    margin-top:20px;
    padding:15px;
    border-radius:16px;
    background: rgba(255,255,255,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def now():
    return dt.datetime.now(PUNE).replace(tzinfo=None)

def parse(text):
    matches = re.findall(r"\b\d{1,2}:\d{2}\b", text)
    today = now().date()
    pts = []
    last = None

    for m in matches:
        h,mn = map(int,m.split(":"))
        t = dt.datetime.combine(today, dt.time(h,mn))

        if last and t < last:
            today += dt.timedelta(days=1)
            t = dt.datetime.combine(today, dt.time(h,mn))

        pts.append(t)
        last = t

    return pts if pts else None

def format_time(sec):
    h = sec//3600
    m = (sec%3600)//60
    s = sec%60
    return f"{h:02d}:{m:02d}:{s:02d}"

# ---------------- ANALYSIS ----------------
def analyze(points):
    work = 0
    brk = 0

    for i in range(len(points)-1):
        d = int((points[i+1]-points[i]).total_seconds())
        if i%2==0:
            work += d
        else:
            brk += d

    if len(points)%2==1:
        work += int((now()-points[-1]).total_seconds())

    return work, brk

# ---------------- HEADER ----------------
col1, col2 = st.columns([6,2])

with col1:
    st.markdown('<div class="title">✨ TimeTrack Pro</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f"<div style='text-align:right'>{now().strftime('%d %b %Y • %I:%M:%S %p')}</div>", unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["👤 Member", "👑 Leader"])

# ---------------- MEMBER ----------------
with tab1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.session_state.member_day = st.radio(
        "Day Type",
        ["Full Day","Half Day"],
        horizontal=True,
        key="member_radio"
    )

    log = st.text_area("Log Input", height=120, key="member_log")

    if st.button("Analyze", key="member_btn"):
        pts = parse(log)
        if pts:
            st.session_state.member_points = pts

    if st.session_state.member_points:
        work, brk = analyze(st.session_state.member_points)

        st.markdown('<div class="stats">', unsafe_allow_html=True)
        for label, val in [
            ("Work", work),
            ("Break", brk),
            ("Total", work+brk),
            ("Remain Work", max(27000-work,0)),
            ("Remain Break", max(5400-brk,0))
        ]:
            st.markdown(f"""
            <div class="stat">
            <h3>{label}</h3>
            <p>{format_time(val)}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LEADER ----------------
with tab2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.session_state.leader_day = st.radio(
        "Day Type",
        ["Full Day","Half Day"],
        horizontal=True,
        key="leader_radio"
    )

    log = st.text_area("Log Input", height=120, key="leader_log")

    if st.button("Analyze", key="leader_btn"):
        pts = parse(log)
        if pts:
            st.session_state.leader_points = pts

    if st.session_state.leader_points:
        work, brk = analyze(st.session_state.leader_points)

        st.markdown('<div class="stats">', unsafe_allow_html=True)
        for label, val in [
            ("Work", work),
            ("Break", brk),
            ("Total", work+brk),
            ("Remain Work", max(25200-work,0)),
            ("Remain Break", max(5400-brk,0))
        ]:
            st.markdown(f"""
            <div class="stat">
            <h3>{label}</h3>
            <p>{format_time(val)}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
