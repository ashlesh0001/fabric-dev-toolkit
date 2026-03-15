import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "./chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"


@st.cache_resource(show_spinner="Loading embedding model (one-time, ~90 MB)…")
def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def index_documents(content: str) -> tuple:
    """
    Split content into chunks, embed with HuggingFace, and store in Chroma.
    Returns (vectorstore, chunk_count).
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(content)
    embeddings = get_embedding_model()
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vectorstore, len(chunks)


def retrieve_context(question: str, vectorstore: Chroma) -> list[str]:
    """Retrieve top 5 most relevant chunks for a question."""
    docs = vectorstore.similarity_search(question, k=5)
    return [doc.page_content for doc in docs]


def build_rag_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    return f"Context from Lakehouse metadata:\n\n{context}\n\n---\n\nQuestion: {question}"
