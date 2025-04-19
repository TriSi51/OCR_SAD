import os

from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
from.pdf_qa_db import get_pdf_by_id

from dotenv import load_dotenv
load_dotenv(override=True)

Settings.llm= OpenAI(model="gpt-3.5-turbo",api_key=os.getenv("OPENAI_API_KEY"))
Settings.embed_model= OpenAIEmbedding(model="text-embedding-3-small")
Settings.node_parser= SentenceSplitter(chunk_size= 512, chunk_overlap=20)
Settings.num_output= 512
Settings.context_window=3900

VECTOR_DB_DIR= "storage/vector_store_index"

def get_pdf_from_db(pdf_id: int) -> str:
    pdf_data= get_pdf_by_id(pdf_id)
    if not pdf_data:
        raise ValueError(f"PDF with id {pdf_id} are not found in database")
    binary= pdf_data['content']
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp:
        tmp.write(binary)
        tmp_path= tmp.name
    import fitz
    doc=fitz.open(tmp_path)
    print(f"doc: {len(doc)}")
    full_text= "\n".join([page.get_text("text") for page in doc])
    doc.close()
    return full_text

def build_index_from_text(pdf_id: int):
    text= get_pdf_from_db(pdf_id)

    print(f"pdf text: {text}")
    documents =Document(text=text, metadata={"pdf_id": str(pdf_id)})
    index=VectorStoreIndex.from_documents([documents])
    storage_path= os.path.join(VECTOR_DB_DIR,f"pdf_{pdf_id}")

    index.storage_context.persist(persist_dir=storage_path)


def query_pdf(pdf_id: int, question:str) ->str:
    storage_path= os.path.join(VECTOR_DB_DIR, f"pdf_{pdf_id}")
    if not os.path.exists(storage_path):
        raise ValueError(f"No index found for PDF id: {pdf_id}")
    storage_context= StorageContext.from_defaults(persist_dir= storage_path)
    index= load_index_from_storage(storage_context=storage_context)
    query_engine = index.as_query_engine()
    response= query_engine.query(question)
    return str(response)
