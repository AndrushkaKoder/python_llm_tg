from config import LLM_NAME
from config import LLM_HOST
from ollama import AsyncClient

client = AsyncClient(host=LLM_HOST)


async def chat_message(user_input: str, data_from_database: str = '') -> str:
    req = await client.chat(
        model=LLM_NAME,
        messages=[
            {'role': 'user', 'content': prepare_prompt(user_input=user_input, search_data=data_from_database)},
        ], options={
            "temperature": 0.0,
            "top_p": 0.1,
            "num_ctx": 4096,
            "num_gpu": 99
        }
    )

    return req['message']['content']


def prepare_prompt(user_input: str, search_data: str) -> str:
    return f"""Ты — помощник по базе знаний. 
    Вот данные из Confluence по запросу '{user_input}':
    {search_data}

    Если есть подходящие ID, кратко ответь пользователю. 
    Если данных недостаточно, скажи об этом, или просто дай ссылку на страницу где искать."""
