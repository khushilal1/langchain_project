import requests
import streamlit as st


# # getting open ai reponse
# def get_openai_reponse(input_text):
#     response = requests.post(
#         "http://localhost:8000/essay/invoke", json={"input": {"topic": input_text}}
#     )

#     return response.json()["output"]["content"]


# getting the ollama2 reonse
def get_llama2_response(input_text, No_of_word, option):
    response = requests.post(
        "http://localhost:8000/poem/invoke",
        json={
            "input": {"topic": input_text, "no_of_word": No_of_word, "option": option}
        },
    )

    return response.json()["output"]


# streamlit framework
st.title("Langchain Demo with LLAMA2 API")
# input_text = st.text_input("Write an essay  using Openai API on")
input_text1 = st.text_input("write a poem  using Llama2 API on")
No_of_word = st.number_input("write no of words")
option = st.selectbox("Select one to generate", ("poem", "essay", "story"))


# if input_text:
#     st.write(get_openai_reponse(input_text))

if st.button("Generate"):

    if input_text1 and No_of_word:
        st.write(get_llama2_response(input_text1, No_of_word, option))
