import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from supabase import create_client, Client
from passlib.context import CryptContext

# Инициализация FastAPI
app = FastAPI(title="ZRQ Corp API Gateway")

# Контекст для хеширования паролей (используем Argon2)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Инициализация клиента Supabase (Берется из переменных окружения Vercel)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Важно: используем Service Role Key только на бэкенде!

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Критические переменные окружения Supabase не настроены.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Схемы валидации данных (Pydantic)
class AuthModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

# --- ЭНДПОИНТ РЕГИСТРАЦИИ ---
@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: AuthModel):
    # Проверяем, существует ли уже такой пользователь
    existing_user = supabase.table("users").select("username").eq("username", user_data.username).execute()
    
    if existing_user.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже зарегистрирован"
        )
    
    # Хешируем пароль, чистый текст уничтожаем в памяти
    hashed_password = pwd_context.hash(user_data.password)
    
    # Сохраняем защищенные данные в Supabase
    new_user = {
        "username": user_data.username,
        "password_hash": hashed_password
    }
    
    try:
        response = supabase.table("users").insert(new_user).execute()
        user_record = response.data[0]
        return {
            "status": "success",
            "message": "Пользователь успешно зарегистрирован в экосистеме ZRQ",
            "user_id": user_record["id"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка БД при создании пользователя: {str(e)}"
        )

# --- ЭНДПОИНТ АВТОРИЗАЦИИ (ЛОГИН) ---
@app.post("/api/auth/login")
async def login_user(user_data: AuthModel):
    # Запрашиваем хеш пароля для введенного username
    user_query = supabase.table("users").select("id", "username", "password_hash").eq("username", user_data.username).execute()
    
    # Защита от тайминг-атак: если пользователь не найден, выполняем "пустой" хеш-чек
    if not user_query.data:
        pwd_context.hash("dummy_password") # Тратит время процессора имитируя проверку
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    db_user = user_query.data[0]
    
    # Верификация хеша из базы с введенным паролем
    if not pwd_context.verify(user_data.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Получаем баланс пользователя из связанной таблицы bank_accounts
    bank_query = supabase.table("bank_accounts").select("balance", "currency").eq("user_id", db_user["id"]).execute()
    balance_info = bank_query.data[0] if bank_query.data else {"balance": 0, "currency": "ZRQ"}

    return {
        "status": "success",
        "message": "Авторизация успешна",
        "session": {
            "user_id": db_user["id"],
            "username": db_user["username"],
            "balance": balance_info["balance"],
            "currency": balance_info["currency"]
        }
    }
