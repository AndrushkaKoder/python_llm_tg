from atlassian import Confluence
import config
import logging
import strip_tags

confluence = Confluence(url=config.CONFLUENCE_HOST, username=config.CONFLUENCE_USER, password=config.CONFLUENCE_TOKEN)

def get_spaces(space: str = None) -> dict | None:
    if space:
        return confluence.get_space(space)

    return confluence.get_all_spaces()


def get_confluence_info(query: str, space: str = None) -> str:
    try:
        logging.info(f"Запрос к Confluence: {query}")
        result = ''

        if space:
            query = f'text ~ "{query}" and space = "{space}" and type = "page"'
        else:
            query =  f'text ~ "{query}" and type = "page"'

        res = confluence.cql(query, limit=5, expand='body.storage')

        for item in res['results']:
            print(item)
            html_body = item['content']['body']['storage']['value']

            result = strip_tags.strip_tags(html_body)

        return result[:500]
    except Exception as e:
        logging.error(f"Ошибка Confluence: {e}")
        return f"Произошла ошибка при обращении к базе знаний: {e}"
