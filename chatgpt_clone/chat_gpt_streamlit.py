from langchain_community.chat_models import ChatOllama
from langchain_community.llms import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st



# getting the va
llm = ChatOllama(model="mistral")

# template of the prompt
template = """
You are a helpful assistant.
Answer thr folllowing question considering the history of the conversation:
chat history:{chat_history}
User question:{user_question}

"""

# creating the promtp
prompt = ChatPromptTemplate.from_template(template)

# making the chain
chain = prompt | llm | StrOutputParser()
# invoking the prompt
print(
    chain.invoke(
        {"chat_history": "", "user_question": "what  is Artificial Intelligence?"}
    )
)


# # setting the page
# st.set_page_config(page_title="ChatBot")
# st.title("ChatGpt-like clone")

#getting the inpt



