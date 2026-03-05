from ollama import AsyncClient
import config
from confluence.confluence_mcp import get_tools_definition, mcp_request
from helpers.prompts import get_system_prompt

client = AsyncClient(host=config.LLM_HOST)


async def send_message(user_input: str) -> str:
    response = await client.chat(
        model=config.LLM_NAME,
        messages=[
            {'role': 'system', 'content': get_system_prompt()},
            {'role': 'user', 'content': user_input},
        ],
        options={
            "temperature": 0.0,
            "num_ctx": 8192,
        },
        tools=get_tools_definition()
    )
    if response['message'].get('tool_calls'):
        print("ОНА ПРОСИТ MCP!")
        messages = [
            {'role': 'user', 'content': user_input},
            response['message'],
        ]

        for tool in response['message']['tool_calls']:
            if tool['function']['name'] == 'mcp_request':
                query = tool['function']['arguments']['query']
                print(f"🛠 Модель вызвала поиск по запросу: {query}")

                search_data = mcp_request(query)

                messages.append({
                    'role': 'tool',
                    'content': search_data,
                    'name': 'mcp_request'
                })

        final_response = await client.chat(
            model=config.LLM_NAME,
            messages=messages
        )
        return final_response['message']['content']

    return response['message']['content']
