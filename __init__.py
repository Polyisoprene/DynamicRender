from .DynamicChecker import Dynamic
from .HeadRender import HeadPicRender
from .FootRender import FooterRender
from .addOnCardRender import AddOnCardRender
from .ExtraCard import ExtraCardRender
import asyncio
import time
from PIL import Image
from .TextRender import MainTextRender
from .RepostRender import RepostProcess


class Render:
    def __init__(self, card: Dynamic):
        # 256 类型动态 611350614197990095
        # 2049 的不同biz_type 对应的动态如下
        # 3 装扮 551309621391003098
        # 131 歌单 639296660796604438
        # 141 频道 631743110398869511
        # 201 漫画 639302493349609508
        # 231 挂件 639301892067819543
        self.__card = card
        self.__all_render = {"1": self.repost_dynamic_render,
                             "2": self.pic_dynamic_render,
                             "4": self.plain_text_dynamic_render,
                             "8": self.video_dynamic_render,
                             "64": self.article_dynamic_render,
                             "256": self.music_dynamic_render,
                             "2048": self.decorate_dynamic_render,
                             "2049": self.comic_dynamic_render,
                             "4308": self.live_dynamic_render}

    async def render(self):
        return await self.__all_render[str(self.__card.desc.type)]()

    async def plain_text_dynamic_render(self):
        content_list = []

        header = await HeadPicRender(self.__card.desc.timestamp,
                                     self.__card.desc.user_profile.info.face,
                                     self.__card.desc.user_profile.pendant.image,
                                     self.__card.desc.user_profile.info.uname,
                                     self.__card.desc.user_profile.card.official_verify.type).render_main_card_header()

        content_list.append(header)
        text_pic = await MainTextRender(self.__card).text_content_render()
        if text_pic:
            content_list.append(text_pic)
        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list = await AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render()
            for i in add_on_card_list:
                content_list.append(i)

        footer = await FooterRender(self.__card.desc.dynamic_id_str).foot_render()
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def repost_dynamic_render(self):
        content_list = []

        header = await HeadPicRender(self.__card.desc.timestamp,
                                     self.__card.desc.user_profile.info.face,
                                     self.__card.desc.user_profile.pendant.image,
                                     self.__card.desc.user_profile.info.uname,
                                     self.__card.desc.user_profile.card.official_verify.type).render_main_card_header()

        content_list.append(header)

        text_pic = await MainTextRender(self.__card).text_content_render()
        content_list.append(text_pic)
        # 4101纪录片 4098 电影 512 番剧 4099电视剧 4302付费课程
        if self.__card.desc.orig_type in [4101, 4098, 4099, 512]:
            repost_header = await HeadPicRender(
                face=self.__card.card.origin.apiSeasonInfo.cover,
                uname=self.__card.card.origin.apiSeasonInfo.title,
            ).render_origin_card_header()
            content_list.append(repost_header)
        elif self.__card.desc.orig_type == 4302:
            repost_header = await HeadPicRender(
                face=self.__card.card.origin.up_info.avatar,
                uname=self.__card.card.origin.up_info.name,
            ).render_origin_card_header()
            content_list.append(repost_header)
        else:
            repost_header = await HeadPicRender(
                face=self.__card.card.origin_user.info.face,
                uname=self.__card.card.origin_user.info.uname,
            ).render_origin_card_header()
            content_list.append(repost_header)

        repost_content = await RepostProcess(self.__card).render()
        if repost_content:
            content_list.append(repost_content)

        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list = await AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render()
            for i in add_on_card_list:
                content_list.append(i)

        footer = await FooterRender(self.__card.desc.dynamic_id_str).foot_render()
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def pic_dynamic_render(self):
        content_list = []

        header_task = asyncio.create_task(HeadPicRender(self.__card.desc.timestamp,
                                                        self.__card.desc.user_profile.info.face,
                                                        self.__card.desc.user_profile.pendant.image,
                                                        self.__card.desc.user_profile.info.uname,
                                                        self.__card.desc.user_profile.card.official_verify.type).render_main_card_header())

        pics_task = asyncio.create_task(ExtraCardRender(self.__card).picture_render())

        text_pic_tak = asyncio.create_task(MainTextRender(self.__card).text_content_render())

        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)

        footer_task = asyncio.create_task(FooterRender(self.__card.desc.dynamic_id_str).foot_render())
        header = await header_task
        pics = await pics_task
        footer = await footer_task
        text_pic = await text_pic_tak
        content_list.insert(0, header)
        if not text_pic:
            content_list.insert(1, pics)
        else:
            content_list.insert(1, text_pic)
            content_list.insert(2, pics)
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def video_dynamic_render(self):
        content_list = []

        header_task = asyncio.create_task(HeadPicRender(self.__card.desc.timestamp,
                                                        self.__card.desc.user_profile.info.face,
                                                        self.__card.desc.user_profile.pendant.image,
                                                        self.__card.desc.user_profile.info.uname,
                                                        self.__card.desc.user_profile.card.official_verify.type).render_main_card_header())

        video_card_task = asyncio.create_task(ExtraCardRender(self.__card).video_card_render())
        text_pic_tak = asyncio.create_task(MainTextRender(self.__card).text_content_render())

        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list_task = asyncio.create_task(
                AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render())
            add_on_card_list = await add_on_card_list_task
            for i in add_on_card_list:
                content_list.append(i)
        footer_task = asyncio.create_task(FooterRender(self.__card.desc.dynamic_id_str).foot_render())
        header = await header_task
        video_card = await video_card_task
        footer = await footer_task
        text_pic = await text_pic_tak
        content_list.insert(0, header)
        if not text_pic:
            content_list.insert(1, video_card)
        else:
            content_list.insert(1, text_pic)
            content_list.insert(2, video_card)
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def article_dynamic_render(self):
        content_list = []

        header = await HeadPicRender(self.__card.desc.timestamp,
                                     self.__card.desc.user_profile.info.face,
                                     self.__card.desc.user_profile.pendant.image,
                                     self.__card.desc.user_profile.info.uname,
                                     self.__card.desc.user_profile.card.official_verify.type).render_main_card_header()

        content_list.append(header)

        t = await ExtraCardRender(self.__card).extra_article()
        content_list.append(t)

        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list = await AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render()
            for i in add_on_card_list:
                content_list.append(i)

        footer = await FooterRender(self.__card.desc.dynamic_id_str).foot_render()
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def music_dynamic_render(self):
        content_list = []

        header = await HeadPicRender(self.__card.desc.timestamp,
                                     self.__card.desc.user_profile.info.face,
                                     self.__card.desc.user_profile.pendant.image,
                                     self.__card.desc.user_profile.info.uname,
                                     self.__card.desc.user_profile.card.official_verify.type).render_main_card_header()

        content_list.append(header)

        text_pic = await MainTextRender(self.__card).text_content_render()
        content_list.append(text_pic)

        t = await ExtraCardRender(self.__card).extra_music()
        content_list.append(t)

        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list = await AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render()
            for i in add_on_card_list:
                content_list.append(i)

        footer = await FooterRender(self.__card.desc.dynamic_id_str).foot_render()
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def decorate_dynamic_render(self):
        content_list = []

        header = await HeadPicRender(self.__card.desc.timestamp,
                                     self.__card.desc.user_profile.info.face,
                                     self.__card.desc.user_profile.pendant.image,
                                     self.__card.desc.user_profile.info.uname,
                                     self.__card.desc.user_profile.card.official_verify.type).render_main_card_header()

        content_list.append(header)

        text_pic = await MainTextRender(self.__card).text_content_render()
        content_list.append(text_pic)

        t = await ExtraCardRender(self.__card).multi_bize_type()
        if t:
            content_list.append(t)

        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list = await AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render()
            for i in add_on_card_list:
                content_list.append(i)

        footer = await FooterRender(self.__card.desc.dynamic_id_str).foot_render()
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def comic_dynamic_render(self):
        content_list = []

        header = await HeadPicRender(self.__card.desc.timestamp,
                                     self.__card.desc.user_profile.info.face,
                                     self.__card.desc.user_profile.pendant.image,
                                     self.__card.desc.user_profile.info.uname,
                                     self.__card.desc.user_profile.card.official_verify.type).render_main_card_header()

        content_list.append(header)

        text_pic = await MainTextRender(self.__card).text_content_render()
        content_list.append(text_pic)

        t = await ExtraCardRender(self.__card).multi_bize_type()
        content_list.append(t)

        if self.__card.display and self.__card.display.add_on_card_info:
            add_on_card_list = await AddOnCardRender(self.__card.display.add_on_card_info).addon_card_render()
            for i in add_on_card_list:
                content_list.append(i)

        footer = await FooterRender(self.__card.desc.dynamic_id_str).foot_render()
        content_list.append(footer)

        img = await self.assemble_card(content_list)
        return img

    async def live_dynamic_render(self):
        content_list = []

        header = await HeadPicRender(self.__card.desc.timestamp,
                                     self.__card.desc.user_profile.info.face,
                                     self.__card.desc.user_profile.pendant.image,
                                     self.__card.desc.user_profile.info.uname,
                                     self.__card.desc.user_profile.card.official_verify.type).render_main_card_header()

        content_list.append(header)

        # t = await ExtraCardRender(self.__card).multi_bize_type()
        # content_list.append(t)

        footer = await FooterRender(self.__card.desc.dynamic_id_str).foot_render()
        content_list.append(footer)

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
