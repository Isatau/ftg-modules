import random
from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message


@loader.tds
class FarmhoneygameMod(loader.Module):
    """Для Жабабота by isa"""

    strings = {
        "name": "frogFarm",
        "fron": "<i>Автоматическая слежка за жабой запустится через 20 сек...</i>",
        "fron_already": "<i>Уже запущено</i>",
        "froff": "<i>❌\Слежка за жабой остановлена.</i> ",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.myid = (await client.get_me()).id
        self.honeygame = 1276392130

    async def froncmd(self, message):
        """Запустить слежку"""
        status = self.db.get(self.name, "status", False)
        if status:
            return await message.edit(self.strings["fron_already"])
        self.db.set(self.name, "status", True)
        await self.client.send_message(
            self.honeygame, "покормить жабу", schedule=timedelta(seconds=20)
        )
        await message.edit(self.strings["fron"])

    async def froffcmd(self, message):
        """Остановить слежку"""
        self.db.set(self.name, "status", False)

   
    async def watcher(self, event):
        if not isinstance(event, Message):
            return
        chat = utils.get_chat_id(event)
        if chat != self.honeygame:
            return
        status = self.db.get(self.name, "status", False)
        if not status:
            return
        if event.raw_text == "покормить жабу":
            return await self.client.send_message(
                self.honeygame, "покормить жабу", schedule=timedelta(minutes=random.randint(1, 20))
            )
        if event.sender_id != self.honeygame:
            return
        if "Дружище, у тебя премиум-жаба, но 6 часов с момента кормежки не прошло!" in event.raw_text:
            args = [int(x) for x in event.raw_text.split() if x.isnumeric()]
            randelta = random.randint(20, 60)
            if len(args) == 7:
                delta = timedelta(
                    hours=args[4], minutes=args[5], seconds=args[6] + randelta
                )
            elif len(args) == 6:
                delta = timedelta(minutes=args[4], seconds=args[5] + randelta)
            elif len(args) == 5:
                delta = timedelta(seconds=args[4] + randelta)
            else:
                return
            sch = (
                await self.client(
                    functions.messages.GetScheduledHistoryRequest(self.honeygame, 1488)
                )
            ).messages
            await self.client(
                functions.messages.DeleteScheduledMessagesRequest(
                    self.honeygame, id=[x.id for x in sch]
                )
            )
            return await self.client.send_message(self.iris, "покормить жабу", schedule=delta)
