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
