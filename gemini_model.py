import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv, dotenv_values
import os
from llama_index.llms import Gemini

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

llm = Gemini(model="modelels/gemini")
genai.configure(api_key=API_KEY)


text = st.text_area('Write sth')

if st.button('send'):
    response = llm.predict(text)
    st.text(response)