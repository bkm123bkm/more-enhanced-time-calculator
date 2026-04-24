import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# REMOVE default Streamlit padding completely
st.markdown("""
<style>
.block-container {
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# === YOUR FULL HTML UI ===
html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">

<style>
body {
    margin:0;
    font-family:'Outfit', sans-serif;
    background: linear-gradient(135deg,#0f172a,#020617);
    color:white;
}

/* Glass */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border-radius:20px;
    padding:20px;
    margin:20px;
}

/* Header */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
}

/* Button */
.btn {
    background:linear-gradient(135deg,#6366f1,#818cf8);
    border:none;
    padding:10px 20px;
    border-radius:12px;
    color:white;
    cursor:pointer;
}

/* Tabs */
.tabs {
    display:flex;
    gap:10px;
    margin:20px;
}
.tab {
    padding:10px 20px;
    border-radius:10px;
    background:#1e293b;
    cursor:pointer;
}
.active {
    background:#6366f1;
}

/* Cards */
.card {
    background:#1e293b;
    padding:20px;
    border-radius:20px;
    margin:20px;
}

/* Textarea */
textarea {
    width:100%;
    height:120px;
    border-radius:10px;
    padding:10px;
    background:#020617;
    color:white;
    border:none;
}

/* Stats */
.stats {
    display:flex;
    gap:20px;
}
.stat {
    flex:1;
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    text-align:center;
}
</style>
</head>

<body>

<div class="glass header">
    <h2>✨ TimeTrack Pro</h2>
    <button class="btn" onclick="toggleTheme()">🌙 Dark Mode</button>
</div>

<div class="tabs">
    <div class="tab active">👤 Member</div>
    <div class="tab">👑 Leader</div>
</div>

<div class="card">
    <h3>📋 Paste Log</h3>
    <textarea placeholder="09:15\n13:00\n14:00\n18:30"></textarea>
    <br><br>
    <button class="btn">Analyze</button>
</div>

<div class="stats">
    <div class="stat">
        <h4>Work</h4>
        <p>05:20:00</p>
    </div>
    <div class="stat">
        <h4>Break</h4>
        <p>01:10:00</p>
    </div>
    <div class="stat">
        <h4>Remaining</h4>
        <p>02:10:00</p>
    </div>
</div>

<script>
function toggleTheme(){
    document.body.style.background =
        document.body.style.background.includes("0f172a")
        ? "linear-gradient(135deg,#f3f4f6,#e5e7eb)"
        : "linear-gradient(135deg,#0f172a,#020617)";
}
</script>

</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
