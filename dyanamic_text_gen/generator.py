import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

# Load environment variables if necessary
from dotenv import load_dotenv

load_dotenv()

# Streamlit framework
st.title("Dynamic Text Generation: Poems, Stories, and Essays Based on User Prompts")
option = st.selectbox("Select one to generate", ("poem", "essay", "story"))
topic = st.text_input("Enter the topic")
No_of_word = st.number_input("Enter the number of words", min_value=1, step=1)

if st.button("Generate"):
    # LLaMA2 model
    llm = Ollama(model="mistral")

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        "Write a {option} about {topic} for {no_of_word} words"
    )

    # Combine the prompt, model, and parser into a chain
    # Note: The chain should be prompt -> model -> parser
    chain = prompt | llm | StrOutputParser()

    # Generate the input dictionary
    input_dict = {"option": option, "topic": topic, "no_of_word": No_of_word}

    # Calling the model
    try:
        # Use the chain to process the input and get the result
        # generating the reponse
        with st.spinner("Generating response...."):
            result = chain.stream(input_dict)
            st.write(result)

    except Exception as e:
        st.error(f"An error occurred: {e}")
