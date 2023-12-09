from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Table, Sequence
from sqlalchemy.orm import relationship

metadata = MetaData()


# User = Table(
#     "user",
#     metadata,
#     Column("user_id", Integer, primary_key=True, index=True),
#     Column("login", String),
#     Column("password", String),
#
#     # Определите отношение между пользователем и чатами
#     # chats = relationship("Chat", back_populates="user")
# )


Chat = Table(
    "chat",
    metadata,
    Column("chat_id", Integer, primary_key=True, autoincrement=True),
    # Column("user_id", Integer, ForeignKey("user.user_id")), # Внешний ключ на пользователя
    # Column("chat_story", String),
    # Определите отношение между чатом и пользователями
    #user = relationship("User", back_populates="chats"),
    # Определите отношение между чатом и сообщениями
    #messages = relationship("Message", back_populates="chat")
)

Message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("role", String),
    # Column("user_id", Integer, ForeignKey("user.user_id")),  # Внешний ключ на пользователя
    Column("chat_id", Integer, ForeignKey("chat.chat_id")),  # Внешний ключ на чат
    Column("content", String),
    # Определите отношение между сообщением и чатом
    #chat = relationship("Chat", back_populates="messages")
)


ChatMessage = Table(
    "chat_message",
    metadata,
    Column("chat_id", Integer, ForeignKey("chat.chat_id"), primary_key=True),
    Column("message_id", Integer, ForeignKey("message.id"), primary_key=True)
)


# UserChat = Table(
#     "user_chat",
#     metadata,
#     Column("user_id", Integer, ForeignKey("user.user_id"), primary_key=True),
#     Column("chat_id", Integer, ForeignKey("chat.chat_id"), primary_key=True)
# )
