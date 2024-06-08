import streamlit as st
import os
from langchain_groq import ChatGroq

# readig the cntexr from website
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS
import time


load_dotenv()


##load the graoq api key
groq_api_key = os.getenv("GROQ_API_KEY")

#
if "vector" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings()
    st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
    # loading the data of web page

    st.session_state.docs = st.session_state.loader.load()
    # getting the chunk doucmemt
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    #
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(
        st.session_state.docs[:1]
    )

    st.session_state.vectors = FAISS.from_documents(
        st.session_state.final_documents, st.session_state.embeddings
    )

# detail about the web app
st.title("ChatGraq Demo")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma-7b-It")

# pompt
prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on the provided contex only.
    Please provide the most accurate reponse based on the question
    <context>
    {context}
    </context>
    
    
    """
)

documment_chain = create_stuff_documents_chain(llm, prompt)
# retiver chain
retriver = st.session_state.vector.as_retriever()
retriver_chain = create_retrieval_chain(retriver, documment_chain)
#
prompt = st.text_input("Enter your prompt")

if prompt:
    start = time.process_time()
    response = retriver_chain.invoke({"input": prompt})
    print("Response time:", time.process_time - start)
    st.write(response["answer"])

    # streamlit expander
    with st.expander("Document similarity search"):
        # find the relevant chunk
        for i, doc in enumerate(response["answer"]):
            st.write(doc.page_content)
            st.write("------------------------------------")
