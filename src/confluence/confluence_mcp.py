from mcp.server.fastmcp import FastMCP
from atlassian import Confluence
from helpers.html_cleaner import clean_html

import config

mcp = FastMCP('local')

confluence = Confluence(
    url=config.CONFLUENCE_HOST,
    username=config.CONFLUENCE_USER,
    password=config.CONFLUENCE_TOKEN
)


@mcp.tool()
def mcp_request(query: str) -> str:
    """  Поиск страниц в Confluence по ключевым словам в заголовке или тексте. """
    cql = f'text ~ "{query}" OR title ~ "{query}"'

    try:
        response = confluence.cql(cql=cql, limit=3)

        if not response.get('results'):
            return "Ничего не найдено по этому запросу."

        page_id = response['results'][0]['content']['id']
        title = response['results'][0]['title']

        if page_id is None:
            raise Exception('Id страницы не получен')

        page_data = confluence.get_page_by_id(page_id=page_id, expand='body.storage')

        raw_text = page_data['body']['storage']['value']

        prepare_text = clean_html(raw_text)

        return f"[{page_id}] Страница: {title}\nСодержание:\n{prepare_text[:4000]}"

    except Exception as e:
        return "Ошибка поиска в конфлюенсе: " + str(e)[:200]


def get_tools_definition():
    return [
        {
            'type': 'function',
            'function': {
                'name': 'mcp_request',
                'description': 'Поиск страниц в Confluence по ключевым словам и получение их содержания.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'Тема поиска или ключевые слова (например, "Онбординг")',
                        },
                    },
                    'required': ['query'],
                },
            },
        },
    ]