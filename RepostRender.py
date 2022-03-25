from .TextRender import MainTextRender
from .DynamicChecker import Dynamic
from PIL import Image
from .ExtraCard import ExtraCardRender
from .addOnCardRender import AddOnCardRender
import asyncio


class RepostProcess:
    def __init__(self, card: Dynamic):
        self.__card = card
        self.__all_render = {
            "2": self.pic_dynamic_render,
            "4": self.plain_text_dynamic_render,
            "8": self.video_dynamic_render,
            "64": self.article_dynamic_render,
            "256": self.music_dynamic_render,
            "512": self.movie_render,
            "2048": self.decorate_dynamic_render,
            "2049": self.comic_dynamic_render,
            "4098": self.movie_render,
            "4099": self.movie_render,
            "4101": self.movie_render,
            "4302": self.course_render,
            "4308": self.live_dynamic_render,
            "4200": self.repost_live_render
        }

    async def render(self):
        return await self.__all_render[str(self.__card.desc.orig_type)]()

    async def pic_dynamic_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        pics = await ExtraCardRender(self.__card, isOrigin=True).picture_render()
        content_list.append(pics)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def plain_text_dynamic_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def video_dynamic_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        pics = await ExtraCardRender(self.__card, isOrigin=True).video_card_render()
        content_list.append(pics)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def article_dynamic_render(self):
        content_list = []
        pics = await ExtraCardRender(self.__card, isOrigin=True).extra_article()
        content_list.append(pics)

        img = await self.assemble_card(content_list)
        return img

    async def music_dynamic_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        t = await ExtraCardRender(self.__card, isOrigin=True).extra_music()
        content_list.append(t)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def decorate_dynamic_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        t = await ExtraCardRender(self.__card, isOrigin=True).multi_bize_type()
        content_list.append(t)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def comic_dynamic_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        t = await ExtraCardRender(self.__card, isOrigin=True).multi_bize_type()
        content_list.append(t)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def live_dynamic_render(self):
        content_list = []
        pics = await ExtraCardRender(self.__card).extra_repost_live(flag=True)
        content_list.append(pics)
        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def movie_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        pics = await ExtraCardRender(self.__card).extra_movie()
        content_list.append(pics)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def anime_render(self):
        content_list = []
        text_pic = await MainTextRender(self.__card).origin_content_render()
        if text_pic:
            content_list.append(text_pic)

        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def assemble_card(self, result):
        y = 0
        for i in result:
            y += i.size[1]
        container = Image.new("RGBA", (1080, y))
        position_y = 0
        for z in range(len(result)):
            if z != 0:
                position_y += result[z - 1].size[1]
            container.paste(result[z], (0, position_y))
        return container

    async def repost_live_render(self):
        content_list = []
        pics = await ExtraCardRender(self.__card, isOrigin=True).extra_repost_live()
        content_list.append(pics)
        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img

    async def course_render(self):
        content_list = []
        pics = await ExtraCardRender(self.__card).extra_course()
        content_list.append(pics)
        if self.__card.display and self.__card.display.origin and self.__card.display.origin.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.origin.add_on_card_info, isOrigin=True).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        img = await self.assemble_card(content_list)
        return img
