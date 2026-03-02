from config import LLM_NAME
from config import LLM_HOST
from ollama import AsyncClient


client = AsyncClient(host=LLM_HOST)

async def handle_user_request(base_prompt: str) -> str:
    req = await client.chat(
        model=LLM_NAME,
        messages=[
            {'role': 'user', 'content': prepare_prompt(user_input=base_prompt)}
        ]
    )

    return req['message']['content']


def prepare_prompt(user_input: str) -> str:
    return f'Ты юрист. Отвечай только на юридические вопросы. Кратко и по делу. На остальные вопросы отвечай - "Я не обсуждаю другие темы.". Вопрос: {user_input}'
