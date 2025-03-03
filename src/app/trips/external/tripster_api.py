import requests

class TripsterAPI:
    BASE_URL = "https://experience.tripster.ru/api/"

    def __init__(self, token: str):
        """
        Инициализирует API клиент с переданным токеном.
        
        :param token: API токен Tripster.
        """
        self.token = token
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

    def get(self, resource: str, params: dict = None) -> dict:
        """
        Отправляет GET-запрос к API.
        
        :param resource: Название ресурса API (например, "experiences").
        :param params: Параметры запроса (dict).
        :return: Данные в формате JSON.
        """
        url = f"{self.BASE_URL}{resource}/"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Ошибка Tripster API: {response.status_code} - {response.text}")

        return response.json()

    def get_all(self, resource: str, params: dict = None) -> list:
        """
        Получает все страницы результата, обрабатывая пагинацию.
        
        :param resource: Название ресурса API.
        :param params: Параметры запроса.
        :return: Полный список результатов.
        """
        results = []
        params = params or {}
        params.setdefault("page_size", 100)
        page = 1

        while True:
            params["page"] = page
            data = self.get(resource, params)
            results.extend(data.get("results", []))

            if not data.get("next"):
                break

            page += 1

        return results