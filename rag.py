from app.config import CHROMA_DIR, EMBED_MODEL
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)
    return vs

def retrieve_context(query: str, k: int = 4) -> str:
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=k)
    return "\n\n".join([d.page_content for d in docs])

def get_rag_response(query: str, user_name: str = "User") -> str:
    context = retrieve_context(query)
    if not context:
        return "Sorry, I couldn’t find any information about that."

    model_name = "llama2"  # Replace with a valid Ollama model you have pulled
    try:
        llm = Ollama(model=model_name)
        prompt = f"""You are EduBot for a training institute. Use the context to answer:

User: {query}

Context:
{context}

Answer helpfully and concisely."""
        return llm(prompt) or "Sorry, I couldn’t generate a response."
    except Exception as e:
        return f"Error generating response: {e}\nHint: Make sure '{model_name}' is pulled with `ollama pull {model_name}`."
