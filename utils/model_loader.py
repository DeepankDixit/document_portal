import os
import sys
import json
from dotenv import load_dotenv
from utils.config_loader import load_config

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    def __init__(self, config_path: str = 'config/config.yaml'):
        load_dotenv()  # Load environment variables from .env file
        self._validate_env()
        self.config = load_config() #imported from utils.config_loader.py
        log.info("Configuration loaded successfully.", config_keys=list(self.config.keys()))

    def _validate_env(self):
        """
        Validate required environment variables.
        Ensure API keys exist.
        """
        required_vars = ['GOOGLE_API_KEY', 'GROQ_API_KEY']
        self.api_keys = {key: os.getenv(key) for key in required_vars}
        missing_keys = [key for key, value in self.api_keys.items() if not value]
        if missing_keys:
            log.error("Missing environment variables", missing_keys=missing_keys)
            raise DocumentPortalException(f"Missing required API keys: {', '.join(missing_keys)}")
        log.info("All required API keys are set.")

    def load_embedding_model(self):
        """
        Load and return embedding model from Google Generative AI.
        """
        try:
            log.info("Loading embedding model...")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name,
                                                google_api_key=self.api_keys.get("GOOGLE_API_KEY"))
        except Exception as e:
            log.error("Error loading embedding model", error=str(e))
            raise DocumentPortalException("Failed to load embedding model", sys)

    def load_llm_model(self):
        """
        Load and return the configured LLM model.
        """
        llm_block = self.config["llm"]
        provider_key = os.getenv("LLM_PROVIDER", "groq") #default to groq if not set

        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider=provider_key)
            raise ValueError(f"LLM provider '{provider_key}' not found in config")

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)

        log.info("Loading LLM", provider=provider, model=model_name)

        if provider == "google":
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=self.api_keys.get("GOOGLE_API_KEY"),
                temperature=temperature,
                max_output_tokens=max_tokens
            )

        elif provider == "groq":
            return ChatGroq(
                model=model_name,
                api_key=self.api_keys.get("GROQ_API_KEY"), #type: ignore
                temperature=temperature,
            )

        # elif provider == "openai":
        #     return ChatOpenAI(
        #         model=model_name,
        #         api_key=self.api_keys.get("OPENAI_API_KEY"),
        #         temperature=temperature,
        #         max_tokens=max_tokens
        #     )

        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
if __name__ == "__main__":
    loader = ModelLoader()
    embedding_model = loader.load_embedding_model()
    llm_model = loader.load_llm_model()
    log.info("Models loaded successfully", embedding_model=str(embedding_model), llm_model=str(llm_model))

    #test the ModelLoader
    result = llm_model.invoke("Hello, how are you?")
    print(result)
    result_emb = embedding_model.embed_query("Hello, how are you?")
    print(result_emb)
