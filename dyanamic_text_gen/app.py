from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()


# getting the key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# fastapi
app = FastAPI(title="Lanchain Server", version="1.0", description="A simple API server")

# making routes
add_routes(app, ChatOpenAI(), path="/openai")

# model
model = ChatOpenAI()

# llam2 model
llm = Ollama(model="llama2")
# prompt
# prompt1 = ChatPromptTemplate.from_template("Write essay about {topic} with ¨ words")
prompt2 = ChatPromptTemplate.from_template(
    "Write {option} about {topic} for  {no_of_word} words"
)

# adding routes as api
# add_routes(app, prompt1 | model, path="/essay")


# adding other routes as api
add_routes(app, prompt2 | llm, path="/poem")


# starting of the app or end point of the app
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
