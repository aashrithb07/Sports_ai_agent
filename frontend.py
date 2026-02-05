import streamlit as st
import requests

st.title("Sports AI")

user_input = st.text_input("Ask a sports question (Football, Basketball, Tennis, Cricket):")

if st.button("Ask Question"):
    if user_input:
        with st.spinner("Thinking..."):
            try:
                # 🚨 CRITICAL: The key must be "query" to match your ChatRequest schema
                # 🚨 CRITICAL: Use json=, NOT data=
                payload = {"query": user_input}
                
                response = requests.post(
                    "http://127.0.0.1:8000/chat", 
                    json=payload
                )

                if response.status_code == 200:
                    result = response.json()
                    # According to our ChatResponse schema, the answer is in 'data'
                    st.success(result["data"])
                else:
                    st.error(f"Backend error: {response.status_code}")
                    # This helps us see WHY it's 422
                    st.json(response.json()) 
                    
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")
    else:
        st.warning("Please enter a question first.")