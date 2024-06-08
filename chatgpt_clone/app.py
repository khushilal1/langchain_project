from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage


def get_response(user_query, chat_history):
    # Initializing the LLM with the model
    llm = ChatOllama(model="mistral")

    # Template of the prompt
    template = """
    You are a helpful assistant.
    Answer the following question considering the history of the conversation:
    chat history: {chat_history}
    User question: {user_question}
    """

    # Creating the prompt
    prompt = ChatPromptTemplate.from_template(template)

    # Making the chain
    chain = prompt | llm | StrOutputParser()

    # Streaming the response
    return chain.stream({"chat_history": chat_history, "user_question": user_query})


# Setting the page
st.set_page_config(page_title="ChatBot")
st.title("ChatGpt-like clone")

# Initializing session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="I'm an AI Assistant. How can I help you?")
    ]

# Displaying chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# Query of user
user_query = st.chat_input("Type your message here...")

if user_query:
    # Append user query to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    # Get response from AI
    response_parts = get_response(user_query, st.session_state.chat_history)

    # Initialize an empty string for the full response
    full_response = ""

    # Placeholder for AI message
    ai_message_placeholder = st.empty()

    # Collecting and displaying the streamed response
    for part in response_parts:
        full_response += part
        ai_message_placeholder.markdown(full_response)

    # Append AI response to chat history
    st.session_state.chat_history.append(AIMessage(content=full_response))
