import streamlit as st
from streamlit_ace import st_ace
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv, dotenv_values
import os

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {
                'role': 'user',
                'parts': ["You are a python developer and instructor. You will ask questions and you will answer if the user wants."]
            }
        ]
initialize_session_state()

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def run_python_code(code):
    try:
        # Run the code in a subprocess and capture the output
        result = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip()


def model_input(text):

    response = chat.send_message(text)
    
    st.session_state.messages.append({'role':'user',
                    'parts': [str(text)]})
    st.session_state.messages.append({'role':'model',
                    'parts': [str(response.text)]})

    return response



   
def main():
       
    
    with st.sidebar:
        st.subheader("Python Question Generator")
        text = st.text_area('Ask Your question from here.')     
        if st.button("send"):
            
            st.text(model_input(text=text).text)
    
            st.text(st.session_state.messages)

                
   
    st.subheader("Python Code Editor")
    # Code editor for user input with syntax highlighting and autocompletion
    code_input = st_ace(value="", language="python", height=300)

    # Custom button to run the code
    if st.button("Run Code"):
        with st.spinner("Running code..."):
            result = run_python_code(code_input)
        
        # Display the result
        st.subheader("Result:")
        if result:
            st.text(result)
            st.success("Code executed successfully!")
        else:
            st.error("An error occurred during code execution.")
    
if __name__ == "__main__":
    main()

