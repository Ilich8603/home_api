import requests
import datetime

def get_python_questions_last_two_days():
    """Выводит все вопросы с StackOverflow с тегом 'Python' за последние два дня."""
    base_url = "https://api.stackexchange.com/2.3/questions"

    # Вычисляем timestamp для двух дней назад
    two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
    fromdate_timestamp = int(two_days_ago.timestamp())

    params = {
        'site': 'stackoverflow',
        'tagged': 'python',
        'sort': 'creation',
        'order': 'desc',
        'fromdate': fromdate_timestamp,
        'filter': 'withbody' # Получаем тело вопроса для более полной информации
    }

    print(f"Searching for Python questions created after: {two_days_ago.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Вызовет исключение для ошибок HTTP (4xx или 5xx)
        data = response.json()

        if data['items']:
            print(f"\nFound {len(data['items'])} Python questions in the last two days:")
            for i, question in enumerate(data['items']):
                creation_date = datetime.datetime.fromtimestamp(question['creation_date'])
                print(f"\n{i+1}. Title: {question['title']}")
                print(f"   Link: {question['link']}")
                print(f"   Created: {creation_date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Tags: {', '.join(question['tags'])}")

        else:
            print("No Python questions found in the last two days.")

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        if response is not None and hasattr(response, 'text'):
            print(f"Response content: {response.text}")

if __name__ == '__main__':
    get_python_questions_last_two_days()