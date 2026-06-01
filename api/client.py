import requests

class ZRQApiClient:
    def __init__(self, base_url: str):
        # Пример URL: "https://your-project.vercel.app"
        self.base_url = base_url.rstrip("/")

    def register(self, username: str, password: str) -> dict:
        """
        Отправляет запрос на регистрацию нового аккаунта.
        Возвращает словарь с результатом или вызывает исключение с описанием.
        """
        url = f"{self.base_url}/api/auth/register"
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 201:
                return {"success": True, "data": response.json()}
            else:
                # Извлекаем детали ошибки, переданные FastAPI бэкендом
                error_detail = response.json().get("detail", "Неизвестная ошибка регистрации")
                return {"success": False, "error": error_detail}
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Ошибка сети при подключении к ZRQ Server: {str(e)}"}

    def login(self, username: str, password: str) -> dict:
        """
        Отправляет запрос на авторизацию.
        Если данные неверны, бэкенд вернет 401, а метод вернет 'Invalid credentials'.
        """
        url = f"{self.base_url}/api/auth/login"
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            elif response.status_code == 401:
                # Четкое разграничение ошибки по вашему ТЗ
                return {"success": False, "error": "Invalid credentials"}
            else:
                error_detail = response.json().get("detail", "Ошибка авторизации сервера")
                return {"success": False, "error": error_detail}
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Ошибка сети при авторизации: {str(e)}"}
