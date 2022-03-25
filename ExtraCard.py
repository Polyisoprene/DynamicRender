from .DynamicChecker import Dynamic
import httpx
import math
import os
from io import BytesIO
import time
from PIL import Image, ImageDraw, ImageFont

from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor


class ExtraCardRender:
    def __init__(self, dynamic: Dynamic, isOrigin=False):
        self.dynamic = dynamic
        self.__base_path = os.path.dirname(os.path.abspath(__file__))
        self.content = None
        self.container = None
        self.draw = None
        self.isOrigin = isOrigin

    async def extra_article(self):
        if self.isOrigin:
            cover_url = self.dynamic.card.origin.image_urls[0]
            title = self.dynamic.card.origin.title
            summary = self.dynamic.card.origin.summary
            # self.content = Image.new("RGBA", (1000, 400), (68, 68, 68, 255))
        else:
            cover_url = self.dynamic.card.image_urls[0]
            title = self.dynamic.card.title
            summary = self.dynamic.card.summary
        self.content = Image.new("RGBA", (1000, 400), "#222")
        response = httpx.get(cover_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA").resize((1000, 265))
        # 容器和主体
        self.container = Image.new("RGBA", (1080, 400), (68, 68, 68, 255))
        # 贴上封面
        self.content.paste(cover)
        # 准备写入
        self.draw = ImageDraw.Draw(self.content, "RGBA")
        # 得到标题的所有字的坐标
        position_list = await self.calculate_text_position(10, 275, 30, 25, 980, 380, title)
        # 写入标题
        pool = ThreadPool(5)
        pool.map_async(self.write_pic, position_list)
        pool.close()
        pool.join()
        position_list = await self.calculate_text_position(10, 320, 25, 20, 980, 350, summary, True)
        # 写入内容
        pool = ThreadPool(5)
        pool.map_async(self.write_pic, position_list)
        pool.close()
        pool.join()

        if not self.isOrigin:
            self.container.paste(self.content, (
                int((self.container.size[0] - self.content.size[0]) / 2),
                int((self.container.size[1] - self.content.size[1]) / 2)))
        else:
            content_outer = Image.new("RGBA", (1000, self.container.size[1]), "#222")
            content_outer.paste(self.content, (int((content_outer.size[0] - self.content.size[0]) / 2), 0))
            self.container.paste(content_outer, (int((self.container.size[0] - content_outer.size[0]) / 2),
                                                 int((self.container.size[1] - content_outer.size[1]) / 2)))

        # self.container.paste(self.content, (
        #     int((self.container.size[0] - self.content.size[0]) / 2),
        #     int((self.container.size[1] - self.content.size[1]) / 2)))
        return self.container

    async def calculate_text_position(self, start_x, start_y, y_interval, test_size, x_constraint, y_constrain, text,
                                      interrupt=False, ignor_n=False):
        if interrupt:
            x, y = start_x, start_y
            position_list = []
            break_outer = False
            for i in text:
                if not break_outer:
                    while 1:
                        if i == "\n":
                            if not ignor_n:
                                x = start_x
                                y += y_interval
                                if y > y_constrain:
                                    break_outer = True
                            break
                        else:
                            font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), test_size, encoding='utf-8')
                            font_size = font.getsize(i)
                            position_list.append(
                                {"content": i, "x": x, "y": y, "font": "HanaMinA.ttf",
                                 "text_size": test_size})
                            x += font_size[0]
                            if x > x_constraint:
                                x = start_x
                                y += y_interval
                                if y > y_constrain:
                                    break_outer = True
                            break
                else:
                    position_list[-1]["content"] = ""
                    position_list[-2]["content"] = "..."
                    break
        else:
            x, y = start_x, start_y
            position_list = []
            break_outer = False
            for i in text:
                if not break_outer:
                    while 1:
                        if i == "\n":
                            break_outer = True
                            break
                        else:
                            font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), test_size, encoding='utf-8')
                            font_size = font.getsize(i)
                            position_list.append(
                                {"content": i, "x": x, "y": y, "font": "HanaMinA.ttf",
                                 "text_size": test_size})
                            x += font_size[0]
                            if x > x_constraint:
                                break_outer = True
                            break
                else:
                    position_list[-1]["content"] = ""
                    position_list[-2]["content"] = "..."
                    break

        return position_list

    async def picture_render(self):
        pic_list = []
        if self.isOrigin:
            pictures = self.dynamic.card.origin.item.pictures
            pictures_count = self.dynamic.card.origin.item.pictures_count
        else:
            pictures = self.dynamic.card.item.pictures
            pictures_count = self.dynamic.card.item.pictures_count
        if pictures_count == 1:
            img_height = pictures[0].img_height
            img_width = pictures[0].img_width
            if img_height / img_width >= 3:
                img_url = pictures[0].img_src + f"@240w_320h_!header.webp"
                response = httpx.get(img_url)
            else:
                img_url = pictures[0].img_src + f"@400w_{int(400 * img_height / img_width)}h.webp"
                response = httpx.get(img_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((800, int(img.size[1] * 800 / img.size[0])), Image.ANTIALIAS)
            if self.isOrigin:
                content = Image.new("RGBA", (1000, img.size[1] + 20), "#222")
                self.container = Image.new("RGBA", (1080, img.size[1] + 20), (68, 68, 68, 255))
                content.paste(img, (int((content.size[0] - img.size[0]) / 2), 0))
                self.container.paste(content, (int((self.container.size[0] - content.size[0]) / 2), 0))
            else:
                self.container = Image.new("RGBA", (1080, img.size[1]), (68, 68, 68, 255))
                self.container.paste(img, (int((self.container.size[0] - img.size[0]) / 2), 0))
            return self.container
        elif pictures_count in [2, 4]:
            for i in pictures:
                if i.img_height / i.img_width >= 3:
                    img_url = i.img_src + '@250w_250h_!header.webp'
                    pic_list.append(img_url)
                    continue
                img_url = i.img_src + '@250w_250h_1e_1c.webp'
                pic_list.append(img_url)
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = pool.map(self.get_pic, pic_list)
            num = math.ceil(pictures_count / 2)
            if self.isOrigin:
                content = Image.new("RGBA", (1000, 420 * num + 20), "#222")
                x, y = 90, 10
                for i in results:
                    i = i.resize((400, 400), Image.ANTIALIAS)
                    content.paste(i, (x, y))
                    x += 420
                    if x > 560:
                        x = 90
                        y += 420
                self.container = Image.new("RGBA", (1080, content.size[1]), (68, 68, 68, 255))
                self.container.paste(content, (int((self.container.size[0] - content.size[0]) / 2), 0))
            else:
                self.container = Image.new("RGBA", (1080, 420 * num), (68, 68, 68, 255))
                x, y = 130, 10
                for i in results:
                    i = i.resize((400, 400), Image.ANTIALIAS)
                    self.container.paste(i, (x, y))
                    x += 420
                    if x > 560:
                        x = 130
                        y += 420
            return self.container
        else:
            for i in pictures:
                if i.img_height / i.img_width >= 3:
                    img_url = i.img_src + '@250w_250h_!header.webp'
                    pic_list.append(img_url)
                    continue
                img_url = i.img_src + '@250w_250h_1e_1c.webp'
                pic_list.append(img_url)
            with ThreadPoolExecutor(max_workers=9) as pool:
                results = pool.map(self.get_pic, pic_list)
            num = math.ceil(pictures_count / 3)
            if self.isOrigin:
                content = Image.new("RGBA", (1000, 260 * num + 20), "#222")
                self.container = Image.new("RGBA", (1080, content.size[1]), (68, 68, 68, 255))
                x, y = 100, 5
                for i in results:
                    i = i.resize((250, 250), Image.ANTIALIAS)
                    content.paste(i, (x, y))
                    x += 260
                    if x > 800:
                        x = 100
                        y += 260
                self.container.paste(content, (int((self.container.size[0] - content.size[0]) / 2), 0))
            else:
                self.container = Image.new("RGBA", (1080, 260 * num), (68, 68, 68, 255))
                x, y = 155, 5
                for i in results:
                    i = i.resize((250, 250), Image.ANTIALIAS)
                    self.container.paste(i, (x, y))
                    x += 260
                    if x > 800:
                        x = 155
                        y += 260
            return self.container

    async def extra_music(self):
        if self.isOrigin:
            title = self.dynamic.card.origin.title
            typeInfo = self.dynamic.card.origin.typeInfo
            cover = self.dynamic.card.origin.cover
            content = Image.new("RGBA", (950, 200), (68, 68, 68, 255))
        else:
            title = self.dynamic.card.title
            typeInfo = self.dynamic.card.typeInfo
            cover = self.dynamic.card.cover
            content = Image.new("RGBA", (950, 200), "#222")
        response = httpx.get(cover)
        cover = Image.open(BytesIO(response.content)).convert("RGBA").resize((200, 200))
        # 容器
        container = Image.new("RGBA", (1080, 240), (68, 68, 68, 255))
        draw = ImageDraw.Draw(content)
        # 播放图标
        play = Image.open(os.path.join(self.__base_path, "Static", "Picture", "play2.png")).convert("RGBA")
        draw.text((230, 40), title, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 30), fill=(255, 255, 255))
        draw.text((230, 100), typeInfo, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20), fill="#AAAAAA")
        content.paste(cover)
        content.paste(play, (60, 60), play)
        if self.isOrigin:
            content_outer = Image.new("RGBA", (1000, container.size[1]), "#222")
            content_outer.paste(content, (int((content_outer.size[0] - content.size[0]) / 2), 0))
            container.paste(content_outer, (int((container.size[0] - content_outer.size[0]) / 2),
                                            int((container.size[1] - content_outer.size[1]) / 2)))
        else:
            container.paste(content, (
                int((container.size[0] - content.size[0]) / 2),
                int((container.size[1] - content.size[1]) / 2)))
        return container

    async def multi_bize_type(self):
        if self.isOrigin:
            if self.dynamic.card.origin.sketch.biz_type:
                process_func = {"3": self.extra_decoration, "131": self.extra_song_list, "141": self.extra_guild,
                                "201": self.extra_manga, "231": self.extra_pendant}[str(self.dynamic.card.origin.sketch.biz_type)]
            else:
                process_func = self.extra_decoration
        else:
            if self.dynamic.card.sketch.biz_type:
                process_func = {"3": self.extra_decoration, "131": self.extra_song_list, "141": self.extra_guild,
                                "201": self.extra_manga, "231": self.extra_pendant}[str(self.dynamic.card.sketch.biz_type)]
            else:
                process_func = self.extra_decoration
        img = await process_func()
        return img

    async def extra_decoration(self):
        if not self.isOrigin:
            content = Image.new("RGBA", (950, 200), "#222")
            title = self.dynamic.card.sketch.title
            desc_text = self.dynamic.card.sketch.desc_text
            cover_url = self.dynamic.card.sketch.cover_url
        else:
            content = Image.new("RGBA", (950, 200), (68, 68, 68, 255))
            title = self.dynamic.card.origin.sketch.title
            desc_text = self.dynamic.card.origin.sketch.desc_text
            cover_url = self.dynamic.card.origin.sketch.cover_url
        response = httpx.get(cover_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA").resize((200, 200))
        # 容器
        container = Image.new("RGBA", (1080, 240), (68, 68, 68, 255))
        draw = ImageDraw.Draw(content)
        draw.text((230, 40), title, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20), fill=(255, 255, 255))
        draw.text((230, 100), desc_text, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 15), fill="#AAAAAA")
        content.paste(cover)
        if self.isOrigin:
            content_outer = Image.new("RGBA", (1000, container.size[1]), "#222")
            content_outer.paste(content, (int((content_outer.size[0] - content.size[0]) / 2), 0))
            container.paste(content_outer, (int((container.size[0] - content_outer.size[0]) / 2),
                                            int((container.size[1] - content_outer.size[1]) / 2)))
        else:
            container.paste(content, (
                int((container.size[0] - content.size[0]) / 2),
                int((container.size[1] - content.size[1]) / 2)))
        return container

    async def extra_song_list(self):
        """
        处理type 2049
        biz_type 131
        :return:
        """
        if self.isOrigin:
            title = self.dynamic.card.origin.sketch.title
            cover_url = self.dynamic.card.origin.sketch.cover_url
            content = Image.new("RGBA", (950, 200), (68, 68, 68, 255))
        else:
            title = self.dynamic.card.sketch.title
            content = Image.new("RGBA", (950, 200), "#222")
            cover_url = self.dynamic.card.sketch.cover_url
        response = httpx.get(cover_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA").resize((200, 200))
        # 容器
        container = Image.new("RGBA", (1080, 240), (68, 68, 68, 255))
        position = await self.calculate_text_position(start_x=239, start_y=60, y_interval=30, test_size=30,
                                                      x_constraint=800, y_constrain=90, text=title, ignor_n=True)
        btn = Image.open(os.path.join(self.__base_path, "Static", "Picture", "gd.png")).convert("RGBA")
        btn = btn.resize((int(btn.size[0] / 2.7), int(btn.size[1] / 2.7)))
        draw = ImageDraw.Draw(content)
        for i in position:
            draw.text((i["x"], i["y"]), i["content"],
                      font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), i["text_size"]), fill=(255, 255, 255))
        content.paste(cover)
        content.paste(btn, (800, 70), btn)
        if self.isOrigin:
            content_outer = Image.new("RGBA", (1000, container.size[1]), "#222")
            content_outer.paste(content, (int((content_outer.size[0] - content.size[0]) / 2), 0))
            container.paste(content_outer, (int((container.size[0] - content_outer.size[0]) / 2),
                                            (int((container.size[1] - content_outer.size[1]) / 2))))
        else:
            container.paste(content, (
                int((container.size[0] - content.size[0]) / 2),
                int((container.size[1] - content.size[1]) / 2)))
        return container

    async def extra_guild(self):
        """
        处理type 2049
        biz_type 141
        :return:
        """
        if self.isOrigin:
            title = self.dynamic.card.origin.sketch.title
            desc_text = self.dynamic.card.origin.sketch.desc_text
            cover_url = self.dynamic.card.origin.sketch.cover_url
            content = Image.new("RGBA", (950, 200), (68, 68, 68, 255))
        else:
            title = self.dynamic.card.sketch.title
            desc_text = self.dynamic.card.sketch.desc_text
            cover_url = self.dynamic.card.sketch.cover_url
            content = Image.new("RGBA", (950, 200), "#222")

        response = httpx.get(cover_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA").resize((200, 200))
        # 容器
        container = Image.new("RGBA", (1080, 240), (68, 68, 68, 255))
        btn = Image.open(os.path.join(self.__base_path, "Static", "Picture", "guild.png")).convert("RGBA")
        btn = btn.resize((int(btn.size[0] / 2.7), int(btn.size[1] / 2.7)))
        position = await self.calculate_text_position(start_x=239, start_y=60, y_interval=30, test_size=30,
                                                      x_constraint=800, y_constrain=90, text=title, ignor_n=True)
        draw = ImageDraw.Draw(content)
        for i in position:
            draw.text((i["x"], i["y"]), i["content"],
                      font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), i["text_size"]), fill=(255, 255, 255))
        draw.text((239, 120), desc_text, fill=(255, 255, 255), font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20))
        content.paste(cover, (0, 0), cover)
        content.paste(btn, (800, 70), btn)
        if self.isOrigin:
            content_outer = Image.new("RGBA", (1000, container.size[1]), "#222")
            content_outer.paste(content, (int((content_outer.size[0] - content.size[0]) / 2), 0))
            container.paste(content_outer, (int((container.size[0] - content_outer.size[0]) / 2),
                                            (int((container.size[1] - content_outer.size[1]) / 2))))
        else:
            container.paste(content, (
                int((container.size[0] - content.size[0]) / 2),
                int((container.size[1] - content.size[1]) / 2)))
        return container

    async def extra_pendant(self):
        if not self.isOrigin:
            title = self.dynamic.card.sketch.title
            desc_text = self.dynamic.card.sketch.desc_text
            cover_url = self.dynamic.card.sketch.cover_url
            content = Image.new("RGBA", (950, 200), "#222")
        else:
            title = self.dynamic.card.origin.sketch.title
            desc_text = self.dynamic.card.origin.sketch.desc_text
            cover_url = self.dynamic.card.origin.sketch.cover_url
            content = Image.new("RGBA", (950, 200), (68, 68, 68, 255))
        response = httpx.get(cover_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA").resize((200, 200))
        # 容器
        container = Image.new("RGBA", (1080, 240), (68, 68, 68, 255))
        draw = ImageDraw.Draw(content)
        # 播放图标
        btn = Image.open(os.path.join(self.__base_path, "Static", "Picture", "zb.png")).convert("RGBA")
        btn = btn.resize((int(btn.size[0] * 0.7), int(btn.size[1] * 0.7)))
        draw.text((230, 40), title, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 30), fill=(255, 255, 255))
        draw.text((230, 100), desc_text, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20), fill="#AAAAAA")
        content.paste(cover)
        content.paste(btn, (800, 60), btn)
        if self.isOrigin:
            content_outer = Image.new("RGBA", (1000, container.size[1]), "#222")
            content_outer.paste(content, (int((content_outer.size[0] - content.size[0]) / 2), 0))
            container.paste(content_outer, (int((container.size[0] - content_outer.size[0]) / 2),
                                            (int((container.size[1] - content_outer.size[1]) / 2))))
        else:
            container.paste(content, (
                int((container.size[0] - content.size[0]) / 2),
                int((container.size[1] - content.size[1]) / 2)))
        return container

    async def extra_manga(self):
        """
        处理type 2049
        biz_type 201
        :return:
        """
        if not self.isOrigin:
            title = self.dynamic.card.sketch.title
            desc_text = self.dynamic.card.sketch.desc_text
            text = self.dynamic.card.sketch.text
            cover_url = self.dynamic.card.sketch.cover_url
            content = Image.new("RGBA", (950, 292), "#222")
        else:
            title = self.dynamic.card.origin.sketch.title
            desc_text = self.dynamic.card.origin.sketch.desc_text
            text = self.dynamic.card.origin.sketch.text
            cover_url = self.dynamic.card.origin.sketch.cover_url
            content = Image.new("RGBA", (950, 292), (68, 68, 68, 255))
        response = httpx.get(cover_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA").resize((219, 292))
        # 容器
        container = Image.new("RGBA", (1080, 302), (68, 68, 68, 255))
        content.paste(cover)
        draw = ImageDraw.Draw(content)
        draw.text((260, 40), title, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 30), fill=(255, 255, 255))
        draw.text((260, 100), desc_text, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20), fill="#AAAAAA")
        draw.text((260, 150), text, font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20), fill="#AAAAAA")

        if self.isOrigin:
            content_outer = Image.new("RGBA", (1000, container.size[1] + 10), "#222")
            content_outer.paste(content, (int((content_outer.size[0] - content.size[0]) / 2), 0))
            container.paste(content_outer, (int((container.size[0] - content_outer.size[0]) / 2),
                                            (int((container.size[1] - content_outer.size[1]) / 2))))
        else:
            container.paste(content, (
                int((container.size[0] - content.size[0]) / 2),
                int((container.size[1] - content.size[1]) / 2)))
        return container

    async def extra_repost_live(self, flag=False):
        if not flag:
            cover = self.dynamic.card.origin.cover
            title = self.dynamic.card.origin.title
            desc = self.dynamic.card.origin.area_v2_name + " • " + self.dynamic.card.origin.watched_show
        else:
            cover = self.dynamic.card.origin.live_play_info.cover
            title = self.dynamic.card.origin.live_play_info.title
            desc = self.dynamic.card.origin.live_play_info.area_name + " • " + self.dynamic.card.origin.live_play_info.watched_show
        self.content = Image.new("RGBA", (950, 230), (68, 68, 68, 255))
        self.container = Image.new("RGBA", (1080, 250), (68, 68, 68, 255))
        response = httpx.get(cover)
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
        cover = cover.resize((int(230 * cover.size[0] / cover.size[1]), 230))
        self.content.paste(cover)
        self.draw = ImageDraw.Draw(self.content, "RGBA")
        position_list = await self.calculate_text_position(cover.size[0] + 20, 20, 30, 25, 920, 50, title,
                                                           interrupt=False)
        pool = ThreadPool(5)
        pool.map(self.write_pic, position_list)
        pool.close()
        pool.join()
        self.draw.text((cover.size[0] + 20, 150), desc, fill=(255, 255, 255),
                       font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20))
        self.content.paste(cover)
        tg = Image.open(os.path.join(self.__base_path, "Static", "Picture", "live.png")).convert("RGBA")
        tg = tg.resize((int(tg.size[0] / 2.4), int(tg.size[1] / 2.4)))
        self.content.paste(tg, (250, 20), tg)

        content_outer = Image.new("RGBA", (1000, self.container.size[1]), "#222")
        content_outer.paste(self.content, (int((content_outer.size[0] - self.content.size[0]) / 2), 0))
        self.container.paste(content_outer, (int((self.container.size[0] - content_outer.size[0]) / 2),
                                             int((self.container.size[1] - content_outer.size[1]) / 2)))

        return self.container

    async def video_card_render(self):
        if not self.isOrigin:
            title = self.dynamic.card.title
            desc = self.dynamic.card.desc
            pic = self.dynamic.card.pic
            self.content = Image.new("RGBA", (950, 230), "#222")
        else:
            title = self.dynamic.card.origin.title
            desc = self.dynamic.card.origin.desc
            pic = self.dynamic.card.origin.pic
            self.content = Image.new("RGBA", (950, 230), (68, 68, 68, 255))
        # 容器
        self.container = Image.new("RGBA", (1080, 250), (68, 68, 68, 255))
        response = httpx.get(pic)
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
        cover = cover.resize((int(230 * cover.size[0] / cover.size[1]), 230))
        self.content.paste(cover)
        tg = Image.open(os.path.join(self.__base_path, "Static", "Picture", "tg.png")).convert("RGBA")
        tg = tg.resize((int(tg.size[0] / 2), int(tg.size[1] / 2)))
        self.content.paste(tg, (250, 20), tg)
        self.draw = ImageDraw.Draw(self.content, "RGBA")
        # 标题的所有字的坐标

        position_list = await self.calculate_text_position(cover.size[0] + 20, 20, 30, 25, 920, 50, title,
                                                           interrupt=True)
        pool = ThreadPool(5)
        pool.map(self.write_pic, position_list)
        pool.close()
        pool.join()
        position_list_2 = await self.calculate_text_position(cover.size[0] + 20, 100, 30, 20, 920, 150, desc,
                                                             interrupt=True, ignor_n=True)
        # 写入内容
        pool = ThreadPool(5)
        pool.map(self.write_pic, position_list_2)
        pool.close()
        pool.join()
        if not self.isOrigin:
            self.container.paste(self.content, (
                int((self.container.size[0] - self.content.size[0]) / 2),
                int((self.container.size[1] - self.content.size[1]) / 2)))
        else:
            content_outer = Image.new("RGBA", (1000, self.container.size[1]), "#222")
            content_outer.paste(self.content, (int((content_outer.size[0] - self.content.size[0]) / 2), 0))
            self.container.paste(content_outer, (int((self.container.size[0] - content_outer.size[0]) / 2),
                                                 int((self.container.size[1] - content_outer.size[1]) / 2)))
        return self.container

    async def extra_movie(self):
        new_desc = self.dynamic.card.origin.new_desc
        if not new_desc:
            new_desc = self.dynamic.card.origin.apiSeasonInfo.title
        index_title = self.dynamic.card.origin.index_title
        cover = self.dynamic.card.origin.cover
        self.content = Image.new("RGBA", (950, 230), "#222")
        self.container = Image.new("RGBA", (1080, 250), (68, 68, 68, 255))
        response = httpx.get(cover)
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
        cover = cover.resize((int(230 * cover.size[0] / cover.size[1]), 230))
        self.content.paste(cover)
        self.draw = ImageDraw.Draw(self.content, "RGBA")
        self.draw.text((cover.size[0] + 40, 10), new_desc, fill=(255, 255, 255),
                       font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 25))
        self.draw.text((cover.size[0] + 40, 150), index_title, fill="#AAAAAA",
                       font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20))
        tg_name = {"1": "fj.png", "5": "dsj.png", "3": "jlp.png", "2": "dy.png"}[
            str(self.dynamic.card.origin.apiSeasonInfo.bgm_type)]
        tg = Image.open(os.path.join(self.__base_path, "Static", "Picture", tg_name)).convert("RGBA")
        tg = tg.resize((int(tg.size[0] / 2.3), int(tg.size[1] / 2.3)))
        self.content.paste(tg, (250, 15), tg)
        content_outer = Image.new("RGBA", (1000, self.container.size[1]), "#222")
        content_outer.paste(self.content, (int((content_outer.size[0] - self.content.size[0]) / 2), 0))
        self.container.paste(content_outer, (int((self.container.size[0] - content_outer.size[0]) / 2),
                                             int((self.container.size[1] - content_outer.size[1]) / 2)))

        return self.container

    async def extra_course(self):
        cover = self.dynamic.card.origin.cover
        title = self.dynamic.card.origin.title
        subtitle = self.dynamic.card.origin.subtitle
        update_info = self.dynamic.card.origin.update_info
        self.content = Image.new("RGBA", (950, 230), (68, 68, 68, 255))
        self.container = Image.new("RGBA", (1080, 250), (68, 68, 68, 255))
        response = httpx.get(cover)
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
        cover = cover.resize((int(230 * cover.size[0] / cover.size[1]), 230))
        self.content.paste(cover)
        self.draw = ImageDraw.Draw(self.content, "RGBA")
        subtitle_position = await self.calculate_text_position(cover.size[0] + 20, 180, 20, 15, 940, 230, subtitle,interrupt=True,ignor_n=True)
        pool = ThreadPool(5)
        pool.map(self.write_pic, subtitle_position)
        pool.close()
        pool.join()
        tg = Image.open(os.path.join(self.__base_path, "Static", "Picture", "course.png")).convert("RGBA")
        tg = tg.resize((int(tg.size[0] / 2.8), int(tg.size[1] / 2.8)))
        self.content.paste(tg, (250, 15), tg)
        self.draw.text((cover.size[0] + 20, 10), title, fill=(255, 255, 255),font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 25))
        self.draw.text((cover.size[0] + 20, 80), update_info, fill=(255, 255, 255),font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20))
        content_outer = Image.new("RGBA", (1000, self.container.size[1]), "#222")
        content_outer.paste(self.content, (int((content_outer.size[0] - self.content.size[0]) / 2), 0))
        self.container.paste(content_outer, (int((self.container.size[0] - content_outer.size[0]) / 2),
                                             int((self.container.size[1] - content_outer.size[1]) / 2)))

        return self.container

    def write_pic(self, info_dic):
        font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", info_dic["font"]), info_dic["text_size"], encoding='utf-8')
        self.draw.text((info_dic["x"], info_dic["y"]), info_dic["content"], font=font, fill=(255, 255, 255))

    def get_pic(self, url):
        response = httpx.get(url)
        img = Image.open(BytesIO(response.content))
        return img

    async def isEmoji(self, content):

        if not content:
            return False
        if u"\U0001F600" <= content and content <= u"\U0001F64F":
            return True
        elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
            return True
        elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
            return True
        elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
            return True
        else:
            return False
