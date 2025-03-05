from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, BasePromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaLLM
from ollama import chat, generate
from ollama import Client
from utils import parse_to_txt, validate_json
from config import OLLAMA_URL, MODEL_3_2_UNC, MODEL_3_2_ABL, MODEL_3_1_8B, MODEL_3_1_8B_Q4KM_GUFF, MODEL_DEEPSEEK_Q4KM_GUFF, MODEL_DEEPSEEK_LLAMA_IQ4XS_GUFF
from rag import load_knowledge
from prompt import SYSTEM_PROMPT, RAG_PROMPT, OUTPUT_FORMAT, OUTPUT_JSON_SCHEMA
import json

def gen_partecipant_profile(prompt_profile_g, prompt_profile_v):

    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = ChatPromptTemplate.from_template(template)

    model = Ollama(model=MODEL_DEEPSEEK_LLAMA_IQ4XS_GUFF, base_url=OLLAMA_URL, system=SYSTEM_PROMPT, format='json')

    chain = prompt | model

    response_g = chain.invoke({"question": prompt_profile_g})
    response_v = chain.invoke({"question": prompt_profile_v})


    return response_g , response_v

def gen_chat_as_step(prompt_step_template, phase_name, step_key, chat_log_history, groomer_profile, victim_profile):

    llm = Ollama(model=MODEL_DEEPSEEK_LLAMA_IQ4XS_GUFF, base_url=OLLAMA_URL, system=SYSTEM_PROMPT, format='json')

    #rag_template = ChatPromptTemplate.from_template(RAG_PROMPT)
    #rag_prompt = rag_template.format(phase_name=phase_name)

    q_template = ChatPromptTemplate.from_template(prompt_step_template)
    if step_key == "step_1":
        q_prompt = q_template.format(chat_log_history=chat_log_history, groomer_profile=groomer_profile, victim_profile=victim_profile, output_format=OUTPUT_FORMAT)
    else:
        q_prompt = q_template.format(chat_log_history=chat_log_history, output_format=OUTPUT_FORMAT)

    vector_store = load_knowledge(step_key)
    
    retriever = vector_store.as_retriever()

    docs = retriever.get_relevant_documents(q_prompt)
    context = "\n".join([doc.page_content for doc in docs])

    rag_template = ChatPromptTemplate.from_template(RAG_PROMPT)
    #rag_prompt = rag_template.format(phase_name=phase_name, context=context)

    chain = rag_template | llm

    answer= ""
    while True:
        '''response = generate(
            model=MODEL_3_1_8B_ABL,
            messages=[
                {'role': 'system', 'content': rag_prompt},
                {'role': 'user', 'content': q_prompt},
            ],
            system=SYSTEM_PROMPT,
            #stream=True,
            options={'num_ctx': 2048, 'seed': 42}
            )'''
        response = chain.invoke({"question": q_prompt, "context": context , "phase_name": phase_name})
        response_str = json.dumps(response)
        answer = response
        print(f"Lunghezza risposta: {len(response_str)}")
        if len(response_str) >= 900 and validate_json(json.loads(response), OUTPUT_JSON_SCHEMA):
            #answer = response['message']['content']
            #answer = response
            print(phase_name)
            print(f"Lunghezza risposta: {len(response_str)}")

            return answer

def gen_chat_complete(phases, groomer_profile=None, victim_profile=None):

    #generate profile humans
    #response_groomer = gen_partecipant_profile(PROMPT_PROFILE_GROOMER)
    #response_victim = gen_partecipant_profile(PROMPT_PROFILE_VICTIM)
    #groomer = json.loads(response_groomer)
    #victim = json.loads(response_victim)
    #groomer_profile = f"name: {groomer["firstname"]}, nickname: {groomer["nickname"]}, from {groomer["provenience"]}, age {groomer["age"]}, {groomer["sex"]}; he's a {groomer["profession"]}; he like in freetime to do {groomer["hobbies"]} "
    #victim_profile = f"name: {victim["firstname"]}, nickname: {victim["nickname"]}, from {victim["provenience"]}, age {victim["age"]}, {victim["sex"]}; he's a {victim["profession"]}; he like in freetime to do {victim["hobbies"]} "
    
    chat_history_log = ""
    #generate chat for step
    for step_key, step_values in phases.items():

        response_chat_step = gen_chat_as_step(prompt_step_template=step_values["prompt"], phase_name=step_values["name"], step_key=step_key, groomer_profile=groomer_profile, victim_profile=victim_profile, chat_log_history=chat_history_log)

        chat_history_log += response_chat_step
        parse_to_txt(chat_history_log, "test_llama/chat6.txt")

    return chat_history_log
