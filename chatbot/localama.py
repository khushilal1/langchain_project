from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()  # initialize



## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
#lanchain api key
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")





# prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant.Please reponse to the user queries"),
        ("user", "Questions:{questions}"),
    ]
)


# for streamlit framework
st.title("Langchain Demo with OPENAI API")
input_text = st.text_input("Ask me anything")


# CALLING  ollama
llm = Ollama(model="llama2")
output_parser = StrOutputParser()


# making the chain
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"questions": input_text}))
