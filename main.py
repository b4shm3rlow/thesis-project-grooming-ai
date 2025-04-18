import requests, json
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaLLM
from gen_conversation import gen_partecipant_profile, gen_chat_as_step, gen_chat_complete
from gen_dataset_messages import gen_messages_phase
from prompt import PROMPT_PROFILE_GROOMER, PROMPT_PROFILE_VICTIM, SYSTEM_PROMPT, PROMPT_STEP_1, PROMPT_STEP_2, PROMPT_STEP_3, PROMPT_STEP_4, PROMPT_STEP_5, PROMPT_STEP_6, PROMPT_DATASET
from utils import parse_to_txt, get_last_lines, convert_json_to_string
from prompt import TARGETING, GAINING_TRUST, FULLFILLING_NEEDS, ISOLATION, SEXUALIZING_THE_RELATIONSHIP_AND_ABUSE, MAINTAINING_CONTROL
import time

PHASES = {
    "step_1": {"name": "Targeting and Gaining Trust", "prompt": PROMPT_STEP_1, "description": TARGETING},
    #"step_2": {"name": "Gaining trust and access", "prompt": PROMPT_STEP_2, "description": GAINING_TRUST},
    "step_3": {"name": "Fullfilling Needs", "prompt": PROMPT_STEP_3, "description": FULLFILLING_NEEDS},
    "step_4": {"name": "Isolation", "prompt": PROMPT_STEP_4, "description": ISOLATION},
    "step_5": {"name": "Sexualizing the relationship", "prompt": PROMPT_STEP_5, "description": SEXUALIZING_THE_RELATIONSHIP_AND_ABUSE},
    "step_6": {"name": "Maintaing control and Approach", "prompt": PROMPT_STEP_6, "description": MAINTAINING_CONTROL},
    }

def gen_chat_phase():
    '''response_g, response_v = gen_partecipant_profile(PROMPT_PROFILE_GROOMER, PROMPT_PROFILE_VICTIM)
    print(response_g)
    profile_g = json.loads(response_g)
    profile_v = json.loads(response_v)'''
    #desc_profile_g = f"name: {profile_g["name"]}, from {profile_g["provenience"]}, age {profile_g["age"]}, {profile_g["sex"]}; he's a {profile_g["profession"]}; in freetime do {profile_g["hobbies"]} "
    #desc_profile_v = f"name: {profile_v["name"]}, from {profile_v["provenience"]}, age {profile_v["age"]}, {profile_v["sex"]}; {profile_v["school"]}; in freetime do {profile_v["hobbies"]} "
    '''parse_to_txt(desc_profile_g, "profiles.txt")
    parse_to_txt(desc_profile_v, "profiles.txt")'''
    desc_profile_g = "name: Paul, from Tampa, florida, age 44, male; mechanic; in freetime do watch film, football"
    desc_profile_v = "name Alice from San francisco california, age 14, female; Middle School,in freetime do read anime, play videogames, drawing"

    chat_file = "test_generation/chat_11.txt"
    gen_output = "test_generation/chat_11_output.txt"

    step = "step_1"
    with open(chat_file, 'r', encoding='utf-8') as file:
        chat_log_history = get_last_lines(chat_file)
        print(f"chat_log_history: {chat_log_history}")
    
    response = gen_chat_as_step(prompt_step_template=PHASES[step]["prompt"], phase_name=PHASES[step]["name"], step_key=step, chat_log_history=chat_log_history, groomer_profile=desc_profile_g, victim_profile=desc_profile_v)
    parse_to_txt(response, gen_output)
    chat = convert_json_to_string(response)
    parse_to_txt(chat, chat_file)


if __name__ == "__main__":

    chat_file = "/home/jovyan/projects/thesis-project-grooming-ai/output/chat_5.txt"
    gen_output = "/home/jovyan/projects/thesis-project-grooming-ai/output/output_5.txt"
    #step = "step_1"
    #response = gen_messages_phase(phase_name=PHASES[step]["name"], phase_description=PHASES[step]["description"])
    #parse_to_txt(response=response, output_file="gen_messages.txt")
    #response_g = gen_partecipant_profile(PROMPT_PROFILE_GROOMER)
    #response_v = gen_partecipant_profile(PROMPT_PROFILE_VICTIM)
    #parse_to_txt(response_g, "test_generation/profiles.txt")
    #parse_to_txt(response_v, "test_generation/profiles.txt")
    desc_profile_g = "name: carl, from liverpool, UK, age 49, male"
    desc_profile_v = "name asya from brentford UK, age 13, female"
    start_time = time.time()
    gen_chat_complete(phases=PHASES,chat_file=chat_file, gen_output=gen_output, groomer_profile=desc_profile_g, victim_profile=desc_profile_v)
    tot_time = (time.time() - start_time) / 60
    print("--- %s minutes ---" % tot_time)