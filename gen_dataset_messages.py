from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, BasePromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaLLM
from ollama import chat, generate
from ollama import Client
from utils import parse_to_txt
from config import OLLAMA_URL, MODEL_3_2_UNC, MODEL_3_2_ABL, MODEL_3_1_8B, MODEL_3_1_8B_Q4KM_GUFF, MODEL_DEEPSEEK_Q4KM_GUFF
from rag import load_knowledge
from prompt import PROMPT_DATASET
  
def gen_messages_phase(phase_name, phase_description):

    template = """Question: {question}"""

    prompt = ChatPromptTemplate.from_template(template)

    model = Ollama(model=MODEL_DEEPSEEK_Q4KM_GUFF, base_url=OLLAMA_URL)

    chain = prompt | model

    answer=""
    while len(answer) <= 300:
        response = chain.invoke({"question": PROMPT_DATASET, "phase_name": phase_name, "phase_description": phase_description})
        answer = response


    return answer
