from bs4 import BeautifulSoup

# Чистим теги html
def clean_html(html) -> str:
    return BeautifulSoup(html, "html.parser").get_text()