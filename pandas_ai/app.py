from pandasai.llm.local_llm import LocalLLM
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe


model = LocalLLM(
    api_base="http://localhost:11434/v1", model="mistral"
)  # using the local host devcie


st.title("Data Analysis With PandasAI and LLM")

# uploded fule
uploader_file = st.file_uploader("upload a csv file", type=["csv", "txt"])

if uploader_file is not None:
    data = pd.read_csv(uploader_file)
    st.write(data.head())

    df = SmartDataframe(data, config={"llm": model})
    prompt = st.text_area("Enter your prompt:")

    # generate button
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response...."):
                st.write(f"The answer of prompt be:{df.chat(prompt)}")
