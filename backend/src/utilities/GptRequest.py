"""gpt"""
import g4f
import threading
import asyncio
# import configparser
# from PyQt5.QtCore import pyqtSignal, QThread
# from langchain.schema import HumanMessage, SystemMessage
# from langchain.chat_models.gigachat import GigaChat
# from langchain_core.callbacks import BaseCallbackHandler


# config = configparser.ConfigParser()
# config.read('credentials.ini')
# value1 = config.get('Section1', 'variable1')

# class StreamHandler(BaseCallbackHandler):
#     def __init__(self, signal):
#         self.signal = signal
#
#     def on_llm_new_token(self, token: str, **kwargs) -> None:
#         print(f"{token}", end="", flush=True)
#         self.signal.emit(token, 0)


class GptThread:
    def __init__(self, text, extension, model, is_summarization):
        self.model = model
        self.text = text
        self.extension = extension
        self.is_summarization = is_summarization

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.start()

    async def _run_async(self):
        try:
            if self.text:
                text = self.text if not self.is_summarization else \
                    f"Суммаризируй содержимое {self.extension}-файла на русском:\n" + self.text
                text = text[:10000]
                if self.model == "GigaChat":
                    pass
                    # await self._gigachat_run_async(text)
                else:
                    await self._other_model_run_async(text)
                print("\n\n", 0)  # Замените этот вывод на отправку результата в WebSocket
                print("Update DB")  # Замените этот вывод на отправку сигнала об обновлении в WebSocket
        except Exception as e:
            print(str(e), 1)  # Замените этот вывод на отправку сообщения об ошибке в WebSocket

    def _run(self):
        asyncio.run(self._run_async())

    async def _other_model_run_async(self, text):
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": text}],
            provider=g4f.Provider.GeekGpt,
            stream=True,
            timeout=3,
        )
        print(f"\nБот: ")
        for message in response:
            print(f"{message}")