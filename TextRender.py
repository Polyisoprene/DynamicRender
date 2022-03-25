import os
import re
import time

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import httpx
import emoji
from concurrent.futures import ThreadPoolExecutor
from fontTools.ttLib.ttFont import TTFont
from multiprocessing.pool import ThreadPool


class MainTextRender:
    def __init__(self, dynamic):
        self.content_inside = None
        self.dynamic = dynamic
        self.content_img = None
        self.draw = None
        self.__base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Static")
        self.emoji_list = []
        # 0 视频 1超链接 2抽奖  3专栏 4恰饭文本
        self.rich_text_Instead = ["㉠", "㉡", "㉣", "㉢", "㉤", "㉥", "㉦"]
        self.emoji_pic_tag_instead = ["㉧", "㉨", "㉩", "㉪", "㉫", "㉬", "㉭", "㉮", "㉯", '㉰', "㉱", "㉲", "㉳", "㉴", "㉵", "㉶",
                                      "㉷", "㉸", "㉹", "㉺", "㉻", "㉿", "㋐", "㋑", "㋒", "㋓", "㋔", "㋕", "㋖", "㋗", "㋘", "㋙",
                                      "㋚", "㋛", "㋜", "㋝", "㋞", "㋟", "㋠", "㋡", "㋢", "㋣", "㋤", "㋥", "㋦", "㋧", "㋨", "㋩"]

    async def text_content_render(self):
        dynamic_type = self.dynamic.desc.type
        if dynamic_type in [1, 4]:
            description = self.dynamic.card.item.content
        elif dynamic_type in [2048, 2049]:
            description = self.dynamic.card.vest.content
        elif dynamic_type == 2:
            description = self.dynamic.card.item.description
        elif dynamic_type == 8:
            description = self.dynamic.card.dynamic
        elif dynamic_type == 256:
            description = self.dynamic.card.intro
        else:
            description = None
        if description:
            if dynamic_type in [1, 4]:
                ctrl = self.dynamic.card.item.ctrl
            elif dynamic_type in [2]:
                ctrl = self.dynamic.card.item.at_control
            else:
                ctrl = None
            result = await self.get_particular_text(description=description, at_control=ctrl)
            description = result["content"]
            all_emoji = emoji.emoji_lis(description)
            if all_emoji:
                for i in all_emoji:
                    self.emoji_list.append(i["emoji"])
            heterochrosis_info_list = result["heterochrosis_info_list"]
            emoji_list = result["emoji_img_list"]
            particular_text_index_set = await self.calculate_particular_text_index(heterochrosis_info_list, description)
            position_info = await self.calculate_position(start_x=10, start_y=10, x_restrain=875, content=description,
                                                          line_height=35, font_size=25,
                                                          particular_text_index_set=particular_text_index_set,
                                                          img_list=emoji_list)

            content_y = position_info[-1]["position"][1] + 50
            self.content_img = Image.new("RGBA", (900, content_y), color=(68, 68, 68, 255))
            self.draw = ImageDraw.Draw(self.content_img)
            for i in position_info:
                await self.draw_pic(i, self.content_img)
            container = Image.new("RGBA", (1080, self.content_img.size[1]), (68, 68, 68, 255))
            container.paste(self.content_img, (int((container.size[0] - self.content_img.size[0]) / 2), 0))

            return container
        else:
            if self.dynamic.display and self.dynamic.display.topic_info.new_topic:
                description = ""
                result = await self.get_particular_text(description=description)
                description = result["content"]
                heterochrosis_info_list = result["heterochrosis_info_list"]
                emoji_list = result["emoji_img_list"]
                particular_text_index_set = await self.calculate_particular_text_index(heterochrosis_info_list,
                                                                                       description)
                position_info = await self.calculate_position(start_x=10, start_y=10, x_restrain=875,
                                                              content=description,
                                                              line_height=35, font_size=25,
                                                              particular_text_index_set=particular_text_index_set,
                                                              img_list=emoji_list)
                content_y = position_info[-1]["position"][1] + 50
                self.content_img = Image.new("RGBA", (900, content_y), color=(68, 68, 68, 255))
                self.draw = ImageDraw.Draw(self.content_img)
                for i in position_info:
                    await self.draw_pic(i, self.content_img)
                container = Image.new("RGBA", (1080, self.content_img.size[1]), (68, 68, 68, 255))
                container.paste(self.content_img, (int((container.size[0] - self.content_img.size[0]) / 2), 0))
                return container
            else:
                return

    async def origin_content_render(self):
        dynamic_type = self.dynamic.desc.orig_type
        if dynamic_type in [1, 4]:
            description = self.dynamic.card.origin.item.content
        elif dynamic_type in [2048, 2049]:
            description = self.dynamic.card.origin.vest.content
        elif dynamic_type == 2:
            description = self.dynamic.card.origin.item.description
        elif dynamic_type == 8:
            description = self.dynamic.card.origin.dynamic
        elif dynamic_type == 256:
            description = self.dynamic.card.origin.intro
        else:
            description = None
        if description:
            if dynamic_type in [1, 4]:
                ctrl = self.dynamic.card.origin.item.ctrl
            elif dynamic_type in [2]:
                ctrl = self.dynamic.card.origin.item.at_control
            else:
                ctrl = None
            result = await self.get_origin_particular_text(description=description, at_control=ctrl)
            description = result["content"]
            all_emoji = emoji.emoji_lis(description)
            if all_emoji:
                for i in all_emoji:
                    self.emoji_list.append(i["emoji"])
            heterochrosis_info_list = result["heterochrosis_info_list"]
            emoji_list = result["emoji_img_list"]
            particular_text_index_set = await self.calculate_particular_text_index(heterochrosis_info_list, description)
            position_info = await self.calculate_position(start_x=10, start_y=10, x_restrain=875, content=description,
                                                          line_height=35, font_size=25,
                                                          particular_text_index_set=particular_text_index_set,
                                                          img_list=emoji_list)

            content_y = position_info[-1]["position"][1] + 50

            self.content_img = Image.new("RGBA", (1000, content_y), color="#222")

            self.content_inside = Image.new("RGBA", (900, content_y), color="#222")
            self.draw = ImageDraw.Draw(self.content_inside)
            for i in position_info:
                await self.draw_pic(i, self.content_inside)
            self.content_img.paste(self.content_inside,
                                   (int((self.content_img.size[0] - self.content_inside.size[0]) / 2), 0))
            container = Image.new("RGBA", (1080, self.content_img.size[1]), (68, 68, 68, 255))
            container.paste(self.content_img, (int((container.size[0] - self.content_img.size[0]) / 2), 0))
            return container
        else:
            if self.dynamic.display and self.dynamic.display.origin and self.dynamic.display.origin.topic_info.new_topic:
                description = ""
                result = await self.get_origin_particular_text(description=description)
                description = result["content"]
                heterochrosis_info_list = result["heterochrosis_info_list"]
                emoji_list = result["emoji_img_list"]
                particular_text_index_set = await self.calculate_particular_text_index(heterochrosis_info_list,
                                                                                       description)
                position_info = await self.calculate_position(start_x=10, start_y=10, x_restrain=875,
                                                              content=description,
                                                              line_height=35, font_size=25,
                                                              particular_text_index_set=particular_text_index_set,
                                                              img_list=emoji_list)

                content_y = position_info[-1]["position"][1] + 50

                self.content_img = Image.new("RGBA", (1000, content_y), color="#222")

                self.content_inside = Image.new("RGBA", (900, content_y), color="#222")
                self.draw = ImageDraw.Draw(self.content_inside)
                for i in position_info:
                    await self.draw_pic(i, self.content_inside)
                self.content_img.paste(self.content_inside,
                                       (int((self.content_img.size[0] - self.content_inside.size[0]) / 2), 0))
                container = Image.new("RGBA", (1080, self.content_img.size[1]), (68, 68, 68, 255))
                container.paste(self.content_img, (int((container.size[0] - self.content_img.size[0]) / 2), 0))
                return container
            else:
                return

    async def get_origin_particular_text(self, description=None, at_control=None):
        """
               获取所有蓝色的文本
               :param description: 文本主体
               :param at_control: ctrl列表
               :return:
               """
        info_list = []
        emoji_list = []
        # 取出所有的ctrl字符
        if at_control:
            # 过滤掉所有的emoji以防止其造成ctrl错位
            content = await self.filter_emoji(description)
            for at_detail in at_control:
                at_location = at_detail.location
                at_length = at_detail.length
                at_type = at_detail.type
                if at_type == 1:
                    at_start = at_location
                    at_end = at_start + at_length
                    at_content = content[at_start:at_end]
                    info_list.append({"origin_text": at_content, "at_type": 1, "text_type": "at"})
                elif at_type == 3:
                    at_start = at_detail.location
                    at_end = at_start + int(at_detail.data)
                    at_content = content[at_start:at_end]
                    info_list.append(
                        {"origin_text": at_content, "new_content": self.rich_text_Instead[5] + at_content,
                         "at_type": at_type,
                         "text_type": "at"})

                else:
                    at_start = at_detail.location
                    at_end = at_start + int(at_detail.data)
                    at_content = content[at_start:at_end]
                    info_list.append(
                        {"origin_text": at_content, "new_content": self.rich_text_Instead[at_type] + at_content,
                         "at_type": at_type,
                         "text_type": "at"})

            for info in info_list:
                if info["at_type"] != 1:
                    description = description.replace(info["origin_text"], info["new_content"])

        # 取出所有富文本字符并且把原字符换成富文本字符
        if self.dynamic.display and self.dynamic.display.origin and self.dynamic.display.origin.rich_text:
            for rich_detail in self.dynamic.display.origin.rich_text.rich_details:
                if rich_detail.icon_type == 1:
                    description = description.replace(rich_detail.orig_text,
                                                      self.rich_text_Instead[0] + rich_detail.text)
                    info_list.append({"origin_text": rich_detail.text, "text_type": "rich_text"})
                else:
                    description = description.replace(rich_detail.orig_text,
                                                      self.rich_text_Instead[3] + rich_detail.text)
                    info_list.append({"origin_text": rich_detail.text, "text_type": "rich_text"})
        # 把所有的bili_emoji换成特殊字符，并且获取所有的bili_emoji图片
        if self.dynamic.display and self.dynamic.display.origin and self.dynamic.display.origin.emoji_info:
            emoji_url_list = []
            for i in range(len(self.dynamic.display.origin.emoji_info.emoji_details)):
                emoji_details = self.dynamic.display.origin.emoji_info.emoji_details
                description = description.replace(emoji_details[i].emoji_name, self.emoji_pic_tag_instead[i])
                info_list.append(
                    {self.emoji_pic_tag_instead[i]: emoji_details[i].emoji_name, "text_type": "bili_emoji"})
                emoji_url_list.append(emoji_details[i].url)
            with ThreadPoolExecutor(max_workers=5) as pool:
                results = pool.map(self.get_emoji, emoji_url_list)
                for i in results:
                    emoji_list.append(i)
        # 获取所有的话题标签
        if self.dynamic.display and self.dynamic.display.origin and self.dynamic.display.origin.topic_info:
            if self.dynamic.display.origin.topic_info.topic_details:
                for topic_detail in self.dynamic.display.origin.topic_info.topic_details:
                    info_list.append({"origin_text": f"#{topic_detail.topic_name}#", "text_type": "topic"})
            if self.dynamic.display.origin.topic_info.new_topic:
                topic_name = self.dynamic.display.origin.topic_info.new_topic.name
                description = self.rich_text_Instead[6] + topic_name + "\n" + description
                info_list.append({"origin_text": self.rich_text_Instead[6] + topic_name, "text_type": "new_topic"})

        # 去除文本主体中的特殊符号
        description = description.replace("\r", "")
        # region
        # 获取文本中所有的url
        reg = r'https?:[0-9a-zA-Z.?#&=_@(-/\d]+'
        urls = re.findall(reg, description)
        for url in urls:
            reg_1 = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', flags=re.M)
            hosts = re.match(reg_1, url).group()
            # 如果链接的host是B站的就换成  “㉡网页链接”
            if hosts in ["https://t.bilibili.com", "https://live.bilibili.com",
                         "https://www.bilibili.com", "https://space.bilibili.com",
                         "https://m.bilibili.com", "https://mall.bilibili.com",
                         "https://b23.tv", "https://manga.bilibili.com"]:
                description = description.replace(url, self.rich_text_Instead[1] + "网页链接")
        info_list.append({"text_type": "link", "origin_text": self.rich_text_Instead[1] + "网页链接"})
        # endregion
        return {"content": description, "heterochrosis_info_list": info_list, "emoji_img_list": emoji_list}

    async def get_particular_text(self, description=None, at_control=None):
        """
        获取所有蓝色的文本
        :param description: 文本主体
        :param at_control: ctrl列表
        :return:
        """
        info_list = []
        emoji_list = []
        # 取出所有的ctrl字符
        if at_control:
            # 过滤掉所有的emoji以防止其造成ctrl错位
            content = await self.filter_emoji(description)
            for at_detail in at_control:
                at_location = at_detail.location
                at_length = at_detail.length
                at_type = at_detail.type
                if at_type == 1:
                    at_start = at_location
                    at_end = at_start + at_length
                    at_content = content[at_start:at_end]
                    info_list.append({"origin_text": at_content, "at_type": 1, "text_type": "at"})
                elif at_type == 3:
                    at_start = at_detail.location
                    at_end = at_start + int(at_detail.data)
                    at_content = content[at_start:at_end]
                    info_list.append(
                        {"origin_text": at_content, "new_content": self.rich_text_Instead[5] + at_content,
                         "at_type": at_type,
                         "text_type": "at"})

                else:
                    at_start = at_detail.location
                    at_end = at_start + int(at_detail.data)
                    at_content = content[at_start:at_end]
                    info_list.append(
                        {"origin_text": at_content, "new_content": self.rich_text_Instead[at_type] + at_content,
                         "at_type": at_type,
                         "text_type": "at"})

            for info in info_list:
                if info["at_type"] != 1:
                    description = description.replace(info["origin_text"], info["new_content"])

        # 取出所有富文本字符并且把原字符换成富文本字符
        if self.dynamic.display and self.dynamic.display.rich_text:
            for rich_detail in self.dynamic.display.rich_text.rich_details:
                if rich_detail.icon_type == 1:
                    description = description.replace(rich_detail.orig_text,
                                                      self.rich_text_Instead[0] + rich_detail.text)
                    info_list.append({"origin_text": rich_detail.text, "text_type": "rich_text"})
                else:
                    description = description.replace(rich_detail.orig_text,
                                                      self.rich_text_Instead[3] + rich_detail.text)
                    info_list.append({"origin_text": rich_detail.text, "text_type": "rich_text"})
        # 把所有的bili_emoji换成特殊字符，并且获取所有的bili_emoji图片
        if self.dynamic.display and self.dynamic.display.emoji_info:
            emoji_url_list = []
            for i in range(len(self.dynamic.display.emoji_info.emoji_details)):
                emoji_details = self.dynamic.display.emoji_info.emoji_details
                description = description.replace(emoji_details[i].emoji_name, self.emoji_pic_tag_instead[i])
                info_list.append(
                    {self.emoji_pic_tag_instead[i]: emoji_details[i].emoji_name, "text_type": "bili_emoji"})
                emoji_url_list.append(emoji_details[i].url)
            with ThreadPoolExecutor(max_workers=5) as pool:
                results = pool.map(self.get_emoji, emoji_url_list)
                for i in results:
                    emoji_list.append(i)
        # 获取所有的话题标签
        if self.dynamic.display and self.dynamic.display.topic_info:
            if self.dynamic.display.topic_info.topic_details:
                for topic_detail in self.dynamic.display.topic_info.topic_details:
                    info_list.append({"origin_text": f"#{topic_detail.topic_name}#", "text_type": "topic"})
            if self.dynamic.display.topic_info.new_topic:
                topic_name = self.dynamic.display.topic_info.new_topic.name
                description = self.rich_text_Instead[6] + topic_name + "\n" + description
                info_list.append({"origin_text": self.rich_text_Instead[6] + topic_name, "text_type": "new_topic"})

        # if self.dynamic.display and self.dynamic.display.new_topic:

        # 去除文本主体中的特殊符号
        description = description.replace("\r", "")
        # region
        # 获取文本中所有的url
        reg = r'https?:[0-9a-zA-Z.?#&=_@(-/\d]+'
        urls = re.findall(reg, description)
        for url in urls:
            reg_1 = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', flags=re.M)
            hosts = re.match(reg_1, url).group()
            # 如果链接的host是B站的就换成  “㉡网页链接”
            if hosts in ["https://t.bilibili.com", "https://live.bilibili.com",
                         "https://www.bilibili.com", "https://space.bilibili.com",
                         "https://m.bilibili.com", "https://mall.bilibili.com",
                         "https://b23.tv", "https://manga.bilibili.com"]:
                description = description.replace(url, self.rich_text_Instead[1] + "网页链接")
        info_list.append({"text_type": "link", "origin_text": self.rich_text_Instead[1] + "网页链接"})
        # endregion
        return {"content": description, "heterochrosis_info_list": info_list, "emoji_img_list": emoji_list}

    async def calculate_particular_text_index(self, particular_text_info, description):
        """
        计算所有的蓝色文字的索引
        :param particular_text_info_dict: 蓝色字体的具体信息字典
        :param description: 主体文本
        :return:
        """
        # 先使用元组，后面方便合并，在最后会转成集合
        particular_text_index_set = ()
        # 如果特殊文本是at别人
        for particular_text_info_dict in particular_text_info:
            if particular_text_info_dict["text_type"] == "at":
                for t in re.finditer(particular_text_info_dict["origin_text"], description):
                    particular_text_index_set = particular_text_index_set + tuple(x for x in range(t.start(), t.end()))
            elif particular_text_info_dict["text_type"] == "rich_text" or particular_text_info_dict[
                "text_type"] == "topic":
                # 加号和左括号会影响正则，把它们换成转义字符
                origin_text = particular_text_info_dict["origin_text"].replace("+", "\+").replace("(", "\(")
                for t in re.finditer(origin_text, description):
                    particular_text_index_set = particular_text_index_set + tuple(x for x in range(t.start(), t.end()))
            elif particular_text_info_dict["text_type"] == "link":
                for t in re.finditer(particular_text_info_dict["origin_text"], description):
                    particular_text_index_set = particular_text_index_set + tuple(
                        x for x in range(t.start() + 1, t.end()))
            elif particular_text_info_dict["text_type"] == "new_topic":
                for t in re.finditer(particular_text_info_dict["origin_text"], description):
                    particular_text_index_set = particular_text_index_set + tuple(x for x in range(t.start(), t.end()))

        return set(particular_text_index_set)

    async def calculate_position(self, start_x: int, start_y: int, x_restrain: int, content: str, line_height: int,
                                 font_size: int, particular_text_index_set=None, img_list=None):
        tag_pic_list = {"0": "play.png", "1": "link.png", "2": "lottery.png", "3": "article.png", "4": "taobao.png",
                        "5": "icon_vote.png", "6": "new_topic.png"}
        position_list = []
        x, y = start_x, start_y

        for i in range(len(content)):
            while 1:
                # 如果是图标
                if content[i] in self.rich_text_Instead:
                    # 打开图标图片
                    t_content = Image.open(os.path.join(self.__base_path, "Picture", tag_pic_list[
                        str(self.rich_text_Instead.index(content[i]))])).convert(
                        "RGBA").resize((font_size, font_size), Image.ANTIALIAS)
                    position_list.append({"info_type": "img", "content": t_content, "position": (x, y + 3)})
                    x += font_size + 2
                    if x > x_restrain:
                        x = start_x
                        y += line_height
                    break
                # 如果是bili_emoji
                if content[i] in self.emoji_pic_tag_instead:
                    t_content = img_list[self.emoji_pic_tag_instead.index(content[i])].resize((font_size, font_size),
                                                                                              Image.ANTIALIAS)
                    position_list.append({"info_type": "img", "content": t_content, "position": (x, y + 5)})
                    x += font_size
                    if x > x_restrain:
                        x = start_x
                        y += line_height
                    break
                # 如果是emoji
                if await self.isEmoji(content[i]):
                    font = ImageFont.truetype(os.path.join(self.__base_path, "Font", "nte.ttf"), 109)
                    size = font.getsize(content[i])
                    img = Image.new("RGBA", size)
                    draw = ImageDraw.Draw(img)
                    draw.text(xy=(0, 0), text=content[i], font=font, embedded_color=True)
                    img = img.resize((font_size, font_size), Image.ANTIALIAS)
                    position_list.append({"info_type": "img", "content": img, "position": (x, y)})
                    x += font_size
                    if x > x_restrain:
                        x = start_x
                        y += line_height
                    break
                # 如果是换行
                if content[i] == "\n":
                    x = start_x
                    y += line_height
                    break
                # 如果是文字
                font = ImageFont.truetype(os.path.join(self.__base_path, "Font", "msyh.ttc"), font_size)
                size = font.getsize(content[i])
                # 如果是蓝色字体
                if i in particular_text_index_set:

                    position_list.append(
                        {"info_type": "text", "content": content[i], "position": (x, y), "font_color": "#00A0D8",
                         "font_size": font_size})
                else:
                    position_list.append(
                        {"info_type": "text", "content": content[i], "position": (x, y), "font_color": "white",
                         "font_size": font_size})
                x += size[0]
                if x > x_restrain:
                    x = start_x
                    y += line_height
                break
        return position_list

    async def filter_emoji(self, content):
        """
        将文本主体的emoji过滤掉
        :param content: 文本主体
        :return:
        """
        try:
            cont = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            cont = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return cont.sub(u'32', content)

    def get_emoji(self, url):
        response = httpx.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        return img

    async def draw_pic(self, info, img):

        if info["info_type"] == "text":
            font = ImageFont.truetype(os.path.join(self.__base_path, "Font", "msyh.ttc"),
                                      info["font_size"])
            self.draw.text(info["position"], info["content"], fill=info["font_color"], font=font)
        elif info["info_type"] == "emoji":
            font = ImageFont.truetype(os.path.join(self.__base_path, "Font", "seo.ttf"), info["font_size"])
            self.draw.text(xy=info["position"], text=info["content"], font=font, embedded_color=True)
        else:
            img.paste(info["content"], info["position"], info["content"])

    async def isEmoji(self, content):
        if not content:
            return False
        if content in self.emoji_list:
            return True
        else:
            return False
