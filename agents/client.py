import os
from dotenv import load_dotenv
from langchain_gigachat import GigaChat
from langchain.agents import create_agent
from agents.tools import tools

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

system_prompt = """
Ты помощник приложения для учёта расходов.

Если пользователь спрашивает свой ID,
используй инструмент get_my_id.

После получения результата сообщи пользователю его ID.
"""

agent = create_agent(
    llm_model,
    tools=tools,
    system_prompt=system_prompt,
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Какой у меня ID?",
            }
        ]
    }
)
# response = llm_model.invoke("Назови 3 любых фрукта")
print(response["messages"][-1].content)
