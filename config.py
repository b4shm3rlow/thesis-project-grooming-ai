import os
from dotenv import load_dotenv

try:
    load_dotenv(".env")
except ImportError:
    print("dotenv not installed, skipping...")


WEBUI_URL = os.getenv("WEBUI_URL")
OLLAMA_URL = os.getenv("OLLAMA_URL")
TOKEN_API = os.getenv("TOKEN_API")
MODEL_3_2_UNC = os.getenv("MODEL_3_2_UNC")
MODEL_3_2_ABL = os.getenv("MODEL_3_2_ABL")
MODEL_3_1_8B = os.getenv("MODEL_3_1_8B")
MODEL_3_1_8B_ABL = os.getenv("MODEL_3_1_8B_ABL")
MODEL_3_1_8B_Q4KM_GUFF = os.getenv("MODEL_3_1_8B_Q4KM_GUFF")
MODEL_DEEPSEEK_Q4KM_GUFF = os.getenv("MODEL_DEEPSEEK_Q4KM_GUFF")
MODEL_DEEPSEEK_LLAMA_IQ4XS_GUFF = os.getenv("MODEL_DEEPSEEK_LLAMA_IQ4XS_GUFF")