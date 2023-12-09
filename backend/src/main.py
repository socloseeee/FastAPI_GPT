import asyncio
from typing import List

import fastapi
import g4f
from fastapi import FastAPI, HTTPException, Depends
from fastapi import WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from operations import models, schemas
import database

from utilities.GptRequest import GptThread

_providers = [
    g4f.Provider.Aichat,
    g4f.Provider.ChatBase,
    g4f.Provider.Bing,
    g4f.Provider.GptGo,
    g4f.Provider.You,
    g4f.Provider.Yqcloud,
    g4f.Provider.GeekGpt,
    g4f.Provider.Acytoo,
    g4f.Provider.AiAsk,
    g4f.Provider.AItianhu,
    g4f.Provider.Bard,
    g4f.Provider.ChatAnywhere,
    g4f.Provider.ChatForAi,
    g4f.Provider.Phind,
    # langchain.chat_models.gigachat.GigaChat
]

app = FastAPI(
    title="GPT_API"
)

# Настройки CORS, позволяющие запросы с любых доменов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1:8000"],  # Замените "*" на URL вашего фронтенда, если это возможно
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get an async database session
async def get_db():
    async with database.async_session_maker() as db:
        yield db


@app.post("/send_message", response_model=schemas.SendMessageResponse)
async def send_message(
        message: schemas.MessageCreate,
        session: database.AsyncSession = Depends(get_db),
):
    try:
        # Вставить в таблицу message(сообщения)
        query = insert(models.Message).values(
            # user_id=message.user_id,
            chat_id=message.chat_id,
            role="user",
            content=message.content
        )
        await session.execute(query)
        await session.commit()

        result = await session.execute(query.returning(models.Message.c.id))
        message_id = result.fetchone()[0]

        # Вставить в таблицу chat_message(чат с сообщениями)
        query = insert(models.ChatMessage).values(chat_id=message.chat_id, message_id=message_id)
        await session.execute(query)
        await session.commit()

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_chat", response_model=schemas.ChatBase)
async def create_chat(session: database.AsyncSession = Depends(get_db)):
    try:
        # Создаем новый чат
        query = insert(models.Chat)
        result = await session.execute(query)
        await session.commit()

        # Возвращаем созданный чат в качестве ответа
        return {"chat_id": result.inserted_primary_key[0]}
    except IntegrityError as e:
        # Обработка ошибки уникальности (если такая обработка необходима)
        await session.rollback()
        return fastapi.responses.JSONResponse(
            status_code=400,
            content={"detail": "Chat creation failed"},
        )
    except Exception as e:
        # Обработка других ошибок
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_GPT_response", response_model=schemas.MessageBase)
async def get_GPT_response(
        chat_id: int,
        content: str,
        session: database.AsyncSession = Depends(get_db),
):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        query = select(models.Message).where(
            # (models.Message.c.user_id == user_id)
            # &
            models.Message.c.chat_id == chat_id
        ).limit(5)
        result = await session.execute(query)
        result = result.fetchall()
        selected_messages = [{"role": message.role, "content": message.content} for message in result]
        messages.extend(selected_messages)
        messages.append(
            {"role": "assistant", "content": content}
        )

        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=messages,
            provider=g4f.Provider.GeekGpt,
            stream=False
        )
        print(response)

        # Вставить в таблицу message(сообщения)
        query = insert(models.Message).values(
            # user_id=message.user_id,
            chat_id=chat_id,
            role="assistant",
            content=response
        )
        await session.execute(query)
        await session.commit()

        result = await session.execute(query.returning(models.Message.c.id))
        message_id = result.fetchone()[0]

        # Вставить в таблицу chat_message(чат с сообщениями)
        query = insert(models.ChatMessage).values(chat_id=chat_id, message_id=message_id)
        await session.execute(query)
        await session.commit()

        return {"content": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_messages/{chat_id}", response_model=List[schemas.Message])
async def get_messages(chat_id: int, session: database.AsyncSession = Depends(get_db)):
    query = select(models.Message).where(
        # (models.Message.c.user_id == user_id)
        # &
        (models.Message.c.chat_id == chat_id)
    )
    result = await session.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Сообщения не найдены")
    return result.all()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
