import os
from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_community.llms import CTransformers
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from src.prompt import *

load_dotenv()
os.environ.get("PINECONE_API_KEY")
index_name = "medical-chatbot"

embeddings = download_hugging_face_embeddings()

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)


PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


llm = CTransformers(
    model=r"model\llama-2-7b-chat.ggmlv3.q4_0.bin",
    model_type="llama",
    config={
        "max_new_tokens": 512,
        "temperature": 0.8,
    },
)


qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    msg = request.json["message"]
    result = qa.invoke({"query": msg})
    return jsonify({"response": str(result["result"])})


if __name__ == "__main__":
    app.run(debug=True)