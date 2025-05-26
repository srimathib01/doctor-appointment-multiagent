import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Set the GROQ_API_KEY environment variable
os.environ["GROQ_API_KEY"] = api_key

class LLMModel:
    def __init__(self, model_name="llama3-70b"):
        if not model_name:
            raise ValueError("Model is not defined.")
        self.model_name = model_name
        self.llama_model = ChatGroq(model=self.model_name)

    def get_model(self):
        return self.llama_model

if __name__ == "__main__":
    llm_instance = LLMModel()
    llm_model = llm_instance.get_model()
    response = llm_model.invoke("hi")

    print(response)
