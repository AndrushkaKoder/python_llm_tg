from core import run_bot

if __name__ == '__main__':
    try:
        run_bot()
    except Exception as e:
        exit('Ошибка запуска Бота: ' + str(e))
