from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from src.database.models import get_db
from src.servises import UserServ
from src.entities.user import UserCreate, UserUpdate

router = APIRouter(tags=['chats'], prefix='/chats')

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()

    # Получаем список всех клиентов
    clients = await redis_pool.smembers("clients")

    try:
        while True:
            message = await websocket.receive_text()
            await broadcast_message(message, client_id)
    except Exception as e:
        print(f"Ошибка при обработке WebSocket: {e}")
    finally:
        await websocket.close()

@router.get("/messages/{recipient}")
async def get_messages(recipient: str, skip: int = 0, limit: int = 100):
    messages = await redis_pool.lrange(f"{request.current_app.state.redis_client}:{recipient}", skip, skip + limit - 1)
    return {"messages": messages}


@router.post("/send")
async def send_message(message: dict):
    recipient = message["recipient"]
    sender = message["sender"]

    # Сохраняем сообщение в Redis
    await redis_pool.rpush(f"{sender}:{recipient}", message["content"])

    # Рассылаем сообщение всем клиентам
    await broadcast_message(message["content"], sender)

    return {"message": "Сообщение успешно отправлено"}
