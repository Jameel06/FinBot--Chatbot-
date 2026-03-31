import streamlit as st
from chatbot import get_response

# Page config
st.set_page_config(
    page_title="FinBot - AI Finance Assistant",
    page_icon="💰",
    layout="centered"
)

# ---- Custom CSS for blinking red dot ----
st.markdown("""
<style>
.blink {
    animation: blinker 1s linear infinite;
    color: red;
    font-weight: bold;
}
@keyframes blinker {
    50% { opacity: 0; }
}
.signature {
    font-size: 12px;
    color: gray;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("💰 FinBot - AI Finance Assistant")
st.caption("Your personal AI assistant for Mutual Funds, Stocks, Tax, Budgeting & more!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "OH,hi! 👋 I'm FinBot, your personal finance assistant. Ask me anything about Mutual Funds, SIP, Stocks, Tax, Budgeting or any finance topic!"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# User input
if prompt := st.chat_input("Ask me about finance... e.g. What is SIP?"):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(st.session_state.messages[1:])

            # ✅ Add signature line
            response_with_signature = response + """
<div class="signature">
❤️ Made with love by <b>MOHD JAMEEL</b> | FinBot
</div>
"""
            st.markdown(response_with_signature, unsafe_allow_html=True)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_with_signature
    })

# Sidebar
with st.sidebar:

    # ✅ Live Price blinking indicator
    st.markdown("""
    <div>
        <span class="blink">●</span> Live Price Updates
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("💡 Try asking:")
    st.write("• What is SIP and how does it work?")
    st.write("• How to save tax under 80C?")
    st.write("• Difference between stocks and mutual funds?")
    st.write("• How to make a monthly budget?")
    st.write("• What is PPF?")
    st.write("• How does GST work?")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("⚠️ Disclaimer: This is for educational purposes only. Not financial advice.")