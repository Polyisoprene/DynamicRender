import os

import qrcode
from PIL import Image, ImageDraw, ImageFont


class FooterRender:
    def __init__(self, dynamic_id):
        self.__dynamic_id = dynamic_id
        self.__base_path = os.path.dirname(os.path.abspath(__file__))

    async def foot_render(self):
        container = Image.new("RGBA", (1080, 300), (68, 68, 68, 255))
        qr_code = await self.__make_qrcode()
        girl = Image.open(os.path.join(self.__base_path, "Static", "Picture", "ffn.png")).convert("RGBA").resize(
            (300, 300))
        bili_pic = Image.open(os.path.join(self.__base_path, "Static", "Picture", "bilibili.png")).convert("RGBA")
        bili_pic = bili_pic.resize((int(bili_pic.size[0] / 4), int(bili_pic.size[1] / 4)))
        # 贴上看板娘
        container.paste(girl, (840, -5), girl)
        # 贴上二维码
        container.paste(qr_code, (915, 155), qr_code)
        # 贴上bili图标
        container.paste(bili_pic, (50, 100), bili_pic)
        # 写入提示扫码语句
        draw = ImageDraw.Draw(container, "RGBA")
        font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 20, encoding='utf-8')
        draw.text((50, 180), "扫描二维码查看动态", font=font, fill=(251, 114, 153))

        return container

    async def __make_qrcode(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=3, border=1)
        qr.add_data("https://t.bilibili.com/" + self.__dynamic_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="white", back_color=(34, 34, 34, 255)).convert("RGBA").rotate(-8, expand=True)
        return img
