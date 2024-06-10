import os
from langchain_community.llms import Ollama
import streamlit as st
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationBufferMemory

# streamlit framework

st.title("Langchain Demo with Ollama")
# model

st.title("Celebrity Search Results")
# input text
input_text = st.text_input("Search the topic")
# first template

llm = Ollama(model="mistral")

# first template
first_input_prompt = PromptTemplate(
    input_variables=["name"], template="Tell me about {name}"
)

# memroy
person_memory = ConversationBufferMemory(input_key="name", memory_key="chat_history")
dob_memory = ConversationBufferMemory(input_key="person", memory_key="chat_history")
desc_memory = ConversationBufferMemory(
    input_key="dob", memory_key="descritpion_history"
)


# making the chain1
chain1 = LLMChain(
    llm=llm,
    prompt=first_input_prompt,
    verbose=True,
    output_key="person",
    memory=person_memory,
)


# second tmeplate
second_input_prompt = PromptTemplate(
    input_variables=["person"], template="when was  {person} born"
)

# making second 2 chain
chain2 = LLMChain(
    llm=llm,
    prompt=second_input_prompt,
    verbose=True,
    output_key="dob",
    memory=dob_memory,
)


# third pompt
third_input_prompt = PromptTemplate(
    input_variables=["dob"],
    template="Mentions some evenr happended around{dob} in the world",
    memrory=desc_memory,
)


# third chain
chain3 = LLMChain(
    llm=llm, prompt=third_input_prompt, verbose=True, output_key="description"
)
# parent chain
prarent_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    verbose=True,
    input_variables=["name"],
    output_variables=["person", "dob", "description"],
)


# generating the reponse
if st.button("Generate"):
    if input_text:
        with st.spinner("Generating response...."):
            st.write(prarent_chain({"name": input_text}))
    else:
        st.warning("Please enter a prompt!")

    with st.expander("Person Name"):
        st.info(person_memory.buffer)

    with st.expander("Major Events"):
        st.info(desc_memory.buffer)
