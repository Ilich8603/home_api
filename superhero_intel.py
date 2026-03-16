import requests
from typing import Dict, Optional

TOKEN = "2619421814940190"
BASE_URL = f"https://superheroapi.com/api/{TOKEN}"
HERO_NAMES = ["Hulk", "Captain America", "Thanos"]


def get_intelligence(name: str) -> Optional[int]:
    """Возвращает intelligence героя по его имени или None, если не найден."""
    encoded_name = requests.utils.quote(name)  # Кодируем имя для URL (пробел -> %20)
    url = f"{BASE_URL}/search/{encoded_name}"

    try:
        resp = requests.get(url)
        data = resp.json()
    except Exception as e:
        print(f"Ошибка запроса для {name}: {e}")
        return None

    if data.get("response") == "error":
        print(f"API вернул ошибку для {name}: {data.get('error')}")
        return None

    results = data.get("results", [])
    # Ищем точное совпадение имени (с учётом регистра, как в API)
    for hero in results:
        if hero["name"] == name:
            int_str = hero["powerstats"]["intelligence"]
            # Некоторые значения могут быть "null" – в таком случае возвращаем 0
            return int(int_str) if int_str.isdigit() else 0

    print(f"Точное совпадение для {name} не найдено")
    return None


def main():
    intelligence_dict: Dict[str, int] = {}
    for name in HERO_NAMES:
        val = get_intelligence(name)
        if val is not None:
            intelligence_dict[name] = val
            print(f"{name}: intelligence = {val}")
        else:
            print(f"Не удалось получить intelligence для {name}")

    if intelligence_dict:
        smartest = max(intelligence_dict, key=intelligence_dict.get)
        print(f"\n Самый умный Супергерой: {smartest} (intelligence = {intelligence_dict[smartest]})")
    else:
        print("Не удалось определить интеллект ни для одного героя")


if __name__ == "__main__":
    main()
