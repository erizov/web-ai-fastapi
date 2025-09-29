import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

#print ("OPENAI_API_KEY", OPENAI_API_KEY)
#print ("OPENAI_API_BASE", OPENAI_API_BASE)