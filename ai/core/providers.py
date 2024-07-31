from django.conf import settings
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

llm_chat = AzureChatOpenAI(
    azure_deployment=settings.OPENAI_CHAT_DEPLOYMENT,
    openai_api_version=settings.OPENAI_API_VERSION,
    openai_api_key=settings.OPENAI_KEY,
    azure_endpoint=settings.OPENAI_ENDPOINT,
)

llm_embeddings = AzureOpenAIEmbeddings(
    azure_deployment=settings.OPENAI_EMBEDDINGS_DEPLOYMENT,
    openai_api_version=settings.OPENAI_API_VERSION,
    openai_api_key=settings.OPENAI_KEY,
    azure_endpoint=settings.OPENAI_ENDPOINT,
)

if __name__ == "__main__":
    print(llm_chat.predict("Hello, how are you?"))
