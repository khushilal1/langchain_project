import streamlit as st
import pandas as pd
from langchain_community.llms import Ollama
from pandasai import SmartDataframe


llm = Ollama(model="mistral")


st.title("Data Analysis With Generative AI")

uploader_file = st.file_uploader("Upload a CSV file", type=["csv", "txt"])

if uploader_file:
    data = pd.read_csv(uploader_file)
    st.write(data.head())
    # convert into same
    df = SmartDataframe(data, config={"llm": llm})
    # prompt
    prompt = st.text_area("Ask me anything about uploaded data")

    #
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response......."):
                st.write(df.chat(prompt))
        else:
            st.warning("Please enter a prompt!")



