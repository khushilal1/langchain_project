# imported all libraries
import streamlit as st
import os
from langchain_community.embeddings.ollama import OllamaEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from dotenv import load_dotenv
# from langchain_objectbox.vectorstores import ObjectBox

# load_dotenv()