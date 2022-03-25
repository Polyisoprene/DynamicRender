import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import Optional, Union

import httpx
from PIL import Image, ImageDraw, ImageFont
from pydantic import AnyUrl


class HeadPicRender:
    def __init__(self,
                 timestamp: Optional[int] = None,
                 face: Optional[AnyUrl] = None,
                 pendant: Union[AnyUrl, str, None] = None,
                 uname: Optional[str] = None,
                 official_verify: Optional[int] = None):
        self.__official_verify_path = None
        self.__timestamp = timestamp
        self.__face = face + "@240w_240h_1c_1s.webp"
        self.__pendant = pendant
        self.__uname = uname
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.__official_varify = official_verify

    async def render_main_card_header(self):
        """
        渲染发送主动态的图片头
        :return:
        """
        time_format = await self.__format_time(self.__timestamp)
        if self.__pendant:

            url_list = [self.__face, self.__pendant + "@150w_150h.webp"]
            img_list = []
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = pool.map(self.__get_pic_thread, url_list)
            for i in results:
                img_list.append(i)
            face_img = img_list[0]
            pendant_img = img_list[1]
            head = await self.assembly_header(time_format, face_img, pendant_img)
        else:
            url_list = [self.__face]
            img_list = []
            with ThreadPoolExecutor(max_workers=1) as pool:
                results = pool.map(self.__get_pic_thread, url_list)
            for i in results:
                img_list.append(i)
            face_img = img_list[0]
            head = await self.assembly_header(time_format, face_img)
        return head

    async def render_origin_card_header(self):
        """
        渲染源动态头
        :return:
        """
        url_list = [self.__face]
        img_list = []
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = pool.map(self.__get_pic_thread, url_list)
        for i in results:
            img_list.append(i)
        face_img = img_list[0]
        face_img = face_img.resize((240, 240))
        face_img = await self.__make_face_circle(face_img)
        face_img = face_img.resize((48, 48))
        container = Image.new("RGBA", (1080, 70), (68, 68, 68, 255))
        content = Image.new("RGBA", (1000, 70), "#222")
        content.paste(face_img, (10, 5), face_img)
        draw = ImageDraw.Draw(content)
        draw.text((70, 10), text=self.__uname, fill="#00A1D6",
                  font=ImageFont.truetype(os.path.join(self.base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"),
                                          25,encoding='utf-8'))

        container.paste(content, (
            int((container.size[0] - content.size[0]) / 2),
            int((container.size[1] - content.size[1]) / 2)))
        return container

    async def __format_time(self, timestamp: int) -> str:
        """
        格式化时间
        :param timestamp:int
        :return: str
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    def __get_pic_thread(self, url: Optional[str] = None):
        """
        多张图片通过线程池来发请求比较快
        :param url:
        :return:
        """
        response = httpx.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        return img

    async def __get_pic(self, url: Optional[str] = None):
        """
        请求图片
        :param url:图片url
        :return: Union[Image, None]
        """
        async with httpx.AsyncClient() as session:
            response = await session.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        return img

    async def assembly_header(self, time_format: Optional[str] = None, face_img=None, pendant=None):
        """
        组装动态图片头
        :param time_format: 格式化后的时间戳
        :param face_img:头像
        :param pendant:装饰
        :return:
        """
        # 制作图片主体
        container = Image.new("RGBA", (1080, 260), (68, 68, 68, 255))
        # 将头像裁剪为圆形
        round_face = await self.__make_face_circle(face_img)
        # 打开bilibili图标并缩放至合适大小
        bili_img = Image.open(os.path.join(self.base_path, "Static", "Picture", "bilibili.png")).convert("RGBA")
        bili_img = bili_img.resize((int(bili_img.size[0] / 3), int(bili_img.size[1] / 3)), Image.ANTIALIAS)
        # 粘贴头像
        container.paste(round_face, (50, 150), round_face)

        # 粘贴bili图标
        container.paste(bili_img, (int((container.size[0] - bili_img.size[0]) / 2), 30), bili_img)

        # 写入昵称和时间
        draw = ImageDraw.Draw(container, "RGBA")
        name_font = ImageFont.truetype(os.path.join(self.base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 25,
                                       encoding='utf-8')
        time_font = ImageFont.truetype(os.path.join(self.base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 15,
                                       encoding='utf-8')
        draw.text((175, 160), self.__uname, font=name_font, fill=(251, 114, 153))
        draw.text((175, 210), time_format, font=time_font, fill="#AAAAAA")
        if pendant:
            pendant = pendant
            container.paste(pendant, (22, 125), pendant)
        # 如果存在官方认证
        if self.__official_varify:
            self.__official_verify_path = [os.path.join(self.base_path, "Static", "Picture", "official_yellow.png"),
                                           os.path.join(self.base_path, "Static", "Picture", "official_blue.png"),
                                           None][self.__official_varify]
            if self.__official_verify_path:
                official_pic = Image.open(self.__official_verify_path).convert("RGBA").resize((24, 24))
                container.paste(official_pic, (120, 220), official_pic)
        return container

    async def __make_face_circle(self, avatar):
        """
        将头像裁剪成圆形
        :param avatar: 头像
        :return:处理好的头像
        """
        # 背景尺寸
        bg_size = (240, 240)
        bg = Image.new('RGBA', bg_size, color=(255, 255, 255, 0))
        # 头像尺寸
        avatar_size = avatar.size
        # 头像路径
        # 新建一个蒙板图
        mask = Image.new('RGBA', avatar_size, color=(0, 0, 0, 0))
        # 画一个圆
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=(0, 0, 0, 255))
        box = (0, 0, 240, 240)
        # 以下使用到paste(img, box=None, mask=None)方法
        #   img 为要粘贴的图片对你
        #   box 为图片 头像在 bg 中的位置
        #   mask 为蒙板，原理同 ps， 只显示 mask 中 Alpha 通道值大于等于1的部分
        bg.paste(avatar, box, mask)
        bg = bg.resize((96, 96), Image.ANTIALIAS)
        return bg


if __name__ == '__main__':
    print()
