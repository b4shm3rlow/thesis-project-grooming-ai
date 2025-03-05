from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from config import OLLAMA_URL, MODEL_3_1_8B_Q4KM_GUFF
import os

examples = {
    "step_1": {"file_path": "rag/targeting_examples.txt"},
    "step_2": {"file_path": "rag/gaining_trust_access_examples.txt"},
    "step_3": {"file_path": "rag/fullfilling_needs_examples.txt"},
    "step_4": {"file_path": "rag/isolation_examples.txt"},
    "step_5": {"file_path": "rag/sexualize_relationship_abuse_example.txt"},
    "step_5": {"file_path": "rag/mantaining_control.txt"},
}


def load_knowledge(step_key):

    '''embed_model = OllamaEmbeddings(
    model=MODEL_NAME,
    base_url=OLLAMA_URL
    )'''
    model_name = "sentence-transformers/all-mpnet-base-v2"  
    model_kwargs = {'device': 'cpu'}  
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for key, values in examples.items():

        if key == step_key:

            file_path = values["file_path"]
            if not os.path.exists(file_path):
                raise FileNotFoundError(
                    f"The file {file_path} does not exist. Please check the path."
                )

            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
            # Check if the text file exists


    text = text_splitter.split_text(file_content)
    vector_store = Chroma.from_texts(text, embeddings)

    return vector_store

