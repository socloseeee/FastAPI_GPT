# schemas.py

from pydantic import BaseModel
from typing import List


class ChatCreate(BaseModel):
    chat_id: int


class SendMessageResponse(BaseModel):
    status: str


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    # user_id: int
    chat_id: int  # Добавляем новое поле chat_id


class Message(MessageBase):
    id: int
    # user_id: int
    role: str
    chat_id: int  # Добавляем новое поле chat_id

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    chat_id: int


# class ChatCreate(ChatBase):
#     user_id: int


class Chat(ChatBase):
    chat_id: int
    # user_id: int
    messages: List[Message] = []

    class Config:
        from_attributes = True


# class UserBase(BaseModel):
#     login: str
#
#
# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     user_id: int
#     chats: List[Chat] = []
#
#     class Config:
#         from_attributes = True
