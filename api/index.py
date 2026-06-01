import os
import bcrypt
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from supabase import create_client, Client

# Инициализация FastAPI приложения
app = FastAPI(
    title="ZRQ Corp API Gateway",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Настройка CORS, чтобы мобильное приложение Flet (включая веб-версию) могло отправлять запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация клиента Supabase из переменных окружения Vercel
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Критические переменные окружения Supabase (URL или KEY) не настроены в Vercel.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Схемы валидации данных через Pydantic
class AuthRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

# Вспомогательные функции для работы с безопасностью
def hash_password(password: str) -> str:
    """Хеширование пароля с солью с помощью bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка соответствия пароля его сохраненному хешу."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# --- КОРНЕВОЙ ТЕСТОВЫЙ ЭНДПОИНТ ---
@app.get("/api")
async def root_test():
    return {
        "status": "online",
        "system": "ZRQ Corp Ecosystem Gateway",
        "version": "2.0.0"
    }


# --- ЭНДПОИНТ РЕГИСТРАЦИИ ---
@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: AuthRequest):
    # Принудительно приводим логин к нижнему регистру для избежания дубликатов (User и user)
    normalized_username = user_data.username.strip().lower()
    
    # Проверяем наличие пользователя в новой таблице public.users
    existing_user = supabase.table("users").select("username").eq("username", normalized_username).execute()
    
    if existing_user.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже зарегистрирован в системе ZRQ"
        )
    
    # Безопасное хеширование пароля
    hashed_password = hash_password(user_data.password)
    
    # Формируем запись для вставки
    new_user_payload = {
        "username": normalized_username,
        "password_hash": hashed_password
    }
    
    try:
        # Вставка в БД. Наш триггер в Supabase автоматически создаст bank_accounts запись!
        response = supabase.table("users").insert(new_user_payload).execute()
        created_user = response.data[0]
        
        return {
            "status": "success",
            "message": "Регистрация успешно завершена",
            "user_id": created_user["id"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка базы данных: {str(e)}"
        )


# --- ЭНДПОИНТ АВТОРИЗАЦИИ (ВХОД) ---
@app.post("/api/auth/login")
async def login_user(user_data: AuthRequest):
    normalized_username = user_data.username.strip().lower()
    
    # Ищем пользователя по его уникальному username
    user_query = supabase.table("users").select("id", "username", "password_hash").eq("username", normalized_username).execute()
    
    # Если пользователя нет, имитируем проверку хеша, защищаясь от атак по времени (Timing Attacks)
    if not user_query.data:
        fake_salt = bcrypt.gensalt()
        bcrypt.hashpw(b"dummy_password", fake_salt)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    user_record = user_query.data[0]
    
    # Валидация пароля по хешу
    if not verify_password(user_data.password, user_record["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    try:
        # Извлекаем баланс счета, созданного триггером
        bank_query = supabase.table("bank_accounts").select("balance", "currency").eq("user_id", user_record["id"]).execute()
        
        balance_data = bank_query.data[0] if bank_query.data else {"balance": 0.00, "currency": "ZRQ"}
        
        return {
            "status": "success",
            "message": "Вход в систему ZRQ Corp выполнен",
            "session": {
                "user_id": user_record["id"],
                "username": user_record["username"],
                "balance": float(balance_data["balance"]),
                "currency": balance_data["currency"]
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка синхронизации профиля: {str(e)}"
        )
