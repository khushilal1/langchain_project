# imported all libraries
import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv

load_dotenv()

##load the api key and ollama
groq_api_key = os.getenv("GROQ_API_KEY")  # FOR GRAQ API KEY
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # FOR OEN AI KEY

##
st.title("Chat graq with llama3 Demo")

##llm
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# designint the prompt
prompt = ChatPromptTemplate.from_template(
    """
                                        
                                  Answer the question based on the provided context only.
                                  Please provide the most accurate response based on the question
                                  <context>
                                  {context}
                                  </context>
                                  Questions:{input}
                                        
                                        """
)


# defiing the vectro embdeeing
def vector_embedding():
    if "vectors" not in st.session_state:

        # function to convert into vector of pdf
        st.session_state.embeddings = OllamaEmbeddings()
        # loading the pdf
        st.session_state.loader = PyPDFDirectoryLoader(
            "./us_census"
        )  # data ingestion step
        # stores as document
        st.session_state.docs = st.session_state.loader.load()  # docuent loading

        # text splitting as initlaizing the etxsplitter character function
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10, chunk_overlap=2
        )  # chubk creation

        # getting the first 50 document
        st.session_state.final_document = (
            st.session_state.text_splitter.split_documents(st.session_state.docs[:2])
        )
        # convertig the all document into vector
        st.session_state.vectors = FAISS.from_documents(
            st.session_state.final_document, st.session_state.embeddings
        )  # vector stores


# field as asking the question
prompt1 = st.text_input("Enter your Questions from documnets")

if st.button("Document Embedding"):
    vector_embedding()
    st.write("Vector Store Database is ready")


# calculting the timing
import time
if prompt1:
    document_chain = create_stuff_documents_chain(llm, prompt)  # creating the documnet
    # creating the retirver for getting the exatct value as relaibale one also

    retriever = st.session_state.vectors.as_retreiver()
    # rereival chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)  # last chai
    # invkking the retrieval chain
    start = time.process_time()
    response = retrieval_chain.invoke({"input": prompt1})
    print("Response time:", time.process_time() - start)
    # writing the reponse
    st.write(response["answer"])

    # with  srreamlit expande

    with st.expander("Document similarity search"):
        # find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("----------------------------------------------")
