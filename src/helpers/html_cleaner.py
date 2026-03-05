import html2text

# Чистим теги html
def clean_html(raw_html) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(raw_html)