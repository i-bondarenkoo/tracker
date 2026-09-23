import os
from dotenv import load_dotenv
from langchain_gigachat import GigaChat

load_dotenv()
credentials = os.getenv("GIGACHAT_CREDENTIALS")
# print(credentials)

# объект большой языковой модели
# через который мы обращаемся с gigachat
llm_model = GigaChat(
    model="GigaChat-2",
    credentials=credentials,
    verify_ssl_certs=False,
)

response = llm_model.invoke("Привет! Кратко расскажи что такое FastAPI")
print(response.content)
