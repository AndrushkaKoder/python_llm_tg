# logging.basicConfig(level=logging.INFO)
#
# conf = Confluence(
#     url="https://your-domain.atlassian.net", username="email", password="API_TOKEN"
# )
#
# # Хранилище истории: {chat_id: [messages]}
# chat_histories = {}
#
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_confluence_content",
#             "description": "Найти и прочитать страницу в Confluence по названию или теме",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {
#                         "type": "string",
#                         "description": "Название стандарта или темы",
#                     },
#                 },
#                 "required": ["query"],
#             },
#         },
#     }
# ]
#
#
# def get_confluence_content(query):
#     try:
#         logging.info(f"Запрос к Confluence: {query}")
#         search = conf.search(f'text ~ "{query}"', limit=1)
#         if search and "content" in search:
#             page_id = search["content"]["id"]
#             page = conf.get_page_by_id(page_id, expand="body.storage")
#             content = page["body"]["storage"]["value"]
#             return content[:5000]  # Берем первые 5к символов
#         return "Информации по этому запросу в Confluence не найдено."
#     except Exception as e:
#         logging.error(f"Ошибка Confluence: {e}")
#         return f"Произошла ошибка при обращении к базе знаний: {e}"
#
#
# @bot.message_handler(func=lambda message: True)
# def handle_ai_chat(message):
#     chat_id = message.chat.id
#
#     if chat_id not in chat_histories:
#         chat_histories[chat_id] = [
#             {
#                 "role": "system",
#                 "content": "Ты корпоративный ассистент. Отвечай кратко и только на основе данных из инструментов.",
#             }
#         ]
#
#     try:
#         res = ollama.chat(
#             model="llama3.1", tools=tools, messages=chat_histories[chat_id]
#         )
#
#         # ШАГ 2: Проверка на вызов инструмента
#         if res.get("message", {}).get("tool_calls"):
#             for tool in res["message"]["tool_calls"]:
#                 fn_name = tool["function"]["name"]
#                 arguments = tool["function"]["arguments"]
#
#                 bot.send_chat_action(chat_id, "find_location")  # Анимация "ищет"
#                 context = get_confluence_content(arguments.get("query"))
#
#                 # ШАГ 3: Получаем финальный ответ от Ollama
#                 final_res = ollama.chat(
#                     model="llama3.1", messages=chat_histories[chat_id]
#                 )
#                 answer = final_res["message"]["content"]
#         else:
#             answer = res["message"]["content"]
#
#         bot.reply_to(message, answer)
#
#     except Exception as e:
#         logging.error(f"Глобальная ошибка: {e}")
#         bot.reply_to(message, "⚠️ Извини, я сломался. Попробуй позже.")
#
#
# bot.infinity_polling()