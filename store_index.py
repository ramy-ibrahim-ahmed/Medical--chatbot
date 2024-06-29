import os
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from src.helper import load_pfd, text_split, download_hugging_face_embeddings

load_dotenv()
os.environ.get("PINECONE_API_KEY")
index_name = "medical-chatbot"

extracted_data = load_pfd(r"data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
# vectorstore.from_texts(
#     [chunk.page_content for chunk in text_chunks],
#     index_name=index_name,
#     embedding=embeddings,
# )