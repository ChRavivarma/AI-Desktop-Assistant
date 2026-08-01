import streamlit as st
from PIL import ImageGrab
import numpy as np
import cv2
from assistant import ask_ai

st.set_page_config(
    page_title="Desktop AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

col1, col2 = st.columns([8,2])

with col1:
    st.markdown(
        "<div class='title'>Desktop AI Assistant</div>",
        unsafe_allow_html=True
    )

with col2:
    st.success("🟢 LIVE")

# ---------------- CSS ---------------- #

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background:#0F172A;
    color:white;
}

[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #334155;
}

.block-container{
    padding-top:1rem;
}

.title{
    font-size:34px;
    font-weight:700;
}

.subtitle{
    color:#94A3B8;
    margin-bottom:25px;
}

.card{

    background:#1E293B;
    border-radius:18px;

    padding:20px;

    border:1px solid #334155;

    height:100%;
}

.status{

    color:#22C55E;
    font-weight:bold;
}

.chatbox{

    height:420px;
    overflow-y:auto;
}

.user{

    background:#2563EB;

    padding:12px;

    border-radius:12px;

    margin-bottom:12px;

}

.ai{

    background:#334155;

    padding:12px;

    border-radius:12px;

    margin-bottom:12px;

}

</style>
""",unsafe_allow_html=True)

# ---------------- Sidebar ---------------- #

st.sidebar.title("🤖 Desktop AI")

st.sidebar.success("Connected")

st.sidebar.divider()

st.sidebar.write("### Provider")

st.sidebar.info("Gemini")

st.sidebar.write("### Voice")

st.sidebar.success("Listening")

st.sidebar.write("### Screenshot")

st.sidebar.success("Enabled")

st.sidebar.write("### Webcam")

st.sidebar.success("Enabled")

st.sidebar.divider()

st.sidebar.caption("Version 1.0")

# ---------------- Header ---------------- #

st.markdown("<div class='title'>Desktop AI Assistant</div>",unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Real-time Multimodal Desktop Assistant</div>",unsafe_allow_html=True)

# ---------------- Layout ---------------- #

left, right = st.columns([2, 1])

with left:

# ---------------- Chat ---------------- #

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:

        role = msg["role"]

        css = "user" if role == "user" else "ai"

        st.markdown(
            f"<div class='{css}'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

    prompt = st.chat_input("Ask about anything on your screen...")

    if prompt:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        with st.spinner("Thinking..."):

            answer = ask_ai(prompt)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

        st.rerun()

    with right:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("🖥 Live Desktop")

        screenshot = ImageGrab.grab()
        screenshot = np.array(screenshot)

        st.image(
            screenshot,
            channels="RGB",
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("📷 Live Camera")

        camera = cv2.VideoCapture(0)

        success, frame = camera.read()

        if success:

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB,
            )

            st.image(
                frame,
                channels="RGB",
                use_container_width=True,
            )

        camera.release()

        st.markdown("</div>", unsafe_allow_html=True)
