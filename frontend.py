import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load local .env file (for local testing)
load_dotenv()

# 2. Page Configuration
st.set_page_config(page_title="Sports AI Expert", page_icon="🏆")
st.title("🏆 Sports AI Agent")
st.markdown("Ask me anything about **Football, Basketball, Tennis, or Cricket**!")

# 3. Securely Get API Key
# This looks in Streamlit Cloud Secrets first, then your local .env
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key not found! Please add it to your .env file locally or Streamlit Secrets in the cloud.")
    st.stop()

# 4. Initialize AI Logic
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

    prompt = ChatPromptTemplate.from_template(
        "You are a specialized sports assistant. "
        "Only answer questions related to Football, Basketball, Tennis, and Cricket. "
        "If the user asks about anything else (politics, weather, other sports, etc.), "
        "politely inform them that you are a specialized sports expert for those four sports only."
        "\n\nUser Question: {topic}"
    )

    # Creating the chain
    chain = prompt | llm | StrOutputParser()

except Exception as e:
    st.error(f"Failed to initialize AI: {e}")

# 5. User Interface
user_input = st.text_input("Enter your sports question here:", placeholder="Who won the last Champions League?")

if st.button("Ask Expert"):
    if user_input:
        with st.spinner("Analyzing sports data..."):
            try:
                response = chain.invoke({"topic": user_input})
                st.success("### Expert Response:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please type a question first!")

# 6. Footer
st.divider()
st.caption("Powered by Google Gemini & LangChain")