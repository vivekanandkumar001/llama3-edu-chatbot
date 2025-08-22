# app/ingest.py
from pathlib import Path
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import DATA_DIR, CHROMA_DIR, EMBED_MODEL, STORAGE_DIR

def maybe_write_sample():
    # create data dir & sample files if not present
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    courses_fp = DATA_DIR / "courses.json"
    faq_fp = DATA_DIR / "faq.json"
    if not courses_fp.exists():
        sample_courses = [
            {
                "course_name": "Python Full Stack Development",
                "duration": "6 months",
                "fees": "₹12,000",
                "trainer": "Mr. Ramesh Kumar",
                "highlights": ["HTML","CSS","JavaScript","Flask","Django","Projects"],
                "enrollment_url": "https://example.com/python-full-stack"
            },
            {
                "course_name": "Data Science & AI Mastery",
                "duration": "8 months",
                "fees": "₹18,000",
                "trainer": "Dr. Priya Sharma",
                "highlights": ["Python","Pandas","Machine Learning","Deep Learning","AI Projects"],
                "enrollment_url": "https://example.com/data-science-ai"
            }
        ]
        courses_fp.write_text(json.dumps(sample_courses, ensure_ascii=False, indent=2), encoding="utf-8")
    if not faq_fp.exists():
        sample_faq = [
            {"question":"Do you provide placement assistance?","answer":"Yes — resume workshops, mock interviews, placement drives."},
            {"question":"Are there installment options for fees?","answer":"Yes — 2 or 3 installments are available."}
        ]
        faq_fp.write_text(json.dumps(sample_faq, ensure_ascii=False, indent=2), encoding="utf-8")

def load_documents():
    docs = []
    for p in sorted(DATA_DIR.glob("*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(j, list):
            for item in j:
                docs.append(Document(page_content=json.dumps(item, ensure_ascii=False), metadata={"source": p.name}))
        else:
            docs.append(Document(page_content=json.dumps(j, ensure_ascii=False), metadata={"source": p.name}))
    return docs

def run_ingest():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    maybe_write_sample()
    docs = load_documents()
    if not docs:
        print("No JSON data files found in data/. Add courses.json and faq.json")
        return
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    print(f"Preparing {len(chunks)} chunks for embeddings...")
    embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = Chroma.from_documents(chunks, embedding=embed, persist_directory=str(CHROMA_DIR))
    vs.persist()
    print("Ingest complete. Chroma index written to:", CHROMA_DIR)

if __name__ == "__main__":
    run_ingest()
