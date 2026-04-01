from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import os

#load the env environment:
load_dotenv()
groq_api_key =os.getenv("GROQ_API_KEY")
gemini_api_key=os.getenv("GEMINI_API_KEY")

#streamlit page setup: 
st.set_page_config(
    page_title="Chatbot",
    page_icon="🚀",
    layout="centered",
)

st.title("🤖 My First Chatbot")

#initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# provider= st.selectbox("Choose provider:", ["Groq", "Gemini"] )

# if provider =="Groq": 
#         llm = ChatGroq(
#             model="llama-3.1-8b-instant",
#             temperature=0.0,
#             api_key=groq_api_key
#         )
# elif provider=="Gemini":
#      llm=ChatGoogleGenerativeAI(
#           model="gemini-2.5-flash",
#           temperature=0.0,
#           google_api_key=gemini_api_key
#      )

with st.sidebar:
     st.header("Settings")
     provider=st.selectbox("Choose provider:", ["Groq", "Gemini"] )
     if provider =="Groq":
          model=st.selectbox(
               "choose model",["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
          )
          llm = ChatGroq(
               model=model,
               temperature=0.0,
               api_key=groq_api_key
          )
     elif provider=="Gemini":
           model=st.selectbox(
               "choose model",[ "gemini-2.5-flash"]
          )
           llm = ChatGoogleGenerativeAI(
               model=model,
               temperature=0.0,
               google_api_key=gemini_api_key
          )

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()


user_prompt=st.chat_input("Ask Chatbot ....")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({
         "role":"user",
         "content": user_prompt
         })

    with st.spinner("Thinking..."):
         response=llm.invoke(
         input=[{"role":"system", "content":"you are a helpful assistant"},
                *st.session_state.chat_history]
        )

    assistant_response= response.content
    st.session_state.chat_history.append({"role": "assistant","content": assistant_response})

    with st.chat_message("assistant"):
         st.markdown(assistant_response)

    