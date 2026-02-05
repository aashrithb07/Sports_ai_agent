import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Page Configuration
st.set_page_config(page_title="Sports AI Expert", page_icon="🏆")

# 2. Hide Streamlit Branding (Footer/Menus)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Securely Get API Key
# Looks for Streamlit Cloud Secrets first, then local environment
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key not found! Please add it to Streamlit Secrets.")
    st.stop()

# 4. Initialize AI Logic
try:
    # Using 1.5-flash for the 1,500 requests/day free quota
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

    prompt = ChatPromptTemplate.from_template(
        "You are a specialized sports assistant. "
        "Only answer questions related to Football, Basketball, Tennis, and Cricket. "
        "If the user asks about anything else, politely inform them you are a specialized expert for these four sports only."
        "\n\nUser Question: {topic}"
    )

    # Creating the chain
    chain = prompt | llm | StrOutputParser()

except Exception as e:
    st.error(f"Failed to initialize AI: {e}")

# 5. User Interface
st.title("🏆 Sports AI Agent")
st.markdown("Ask me anything about **Football, Basketball, Tennis, or Cricket**!")

user_input = st.text_input("Enter your sports question here:")

if st.button("Ask"):
    if user_input:
        try:
            # Display a chat-style bubble for the response
            with st.chat_message("assistant"):
                # chain.stream allows the text to appear word-by-word
                response = st.write_stream(chain.stream({"topic": user_input}))
        
        except Exception as e:
            # Friendly error handling for rate limits
            if "429" in str(e) or "resource_exhausted" in str(e).lower():
                st.error("⏳ The AI is busy right now! Please wait 60 seconds and try again.")
            else:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please type a question first!")

# The divider and caption were removed as requested for a clean look.