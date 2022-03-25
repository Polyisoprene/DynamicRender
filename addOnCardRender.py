import os
import httpx
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor


class AddOnCardRender:
    def __init__(self, add_on_card_info, isOrigin=False):
        self.__base_path = os.path.dirname(os.path.abspath(__file__))
        self.__add_on_card_info = add_on_card_info
        self.__isOrigin = isOrigin
        self.__addon_card_handle_func = {"1": self.goods_card_handle,
                                         "2": self.attach_card_handle,
                                         "3": self.vote_card_handle,
                                         "5": self.ugc_attach_card,
                                         "6": self.reserve_attach_card}

    async def addon_card_render(self):
        add_on_card_img_list = []
        for add_on_card_detail in self.__add_on_card_info:
            add_on_card_img_list.append(
                await self.__addon_card_handle_func[str(add_on_card_detail.add_on_card_show_type)](add_on_card_detail))

        return add_on_card_img_list

    async def goods_card_handle(self, add_on_card_detail):
        """
        示例动态为 638839435764432901
        处理商品类型的附加卡片
        :return:
        """
        goods_card = add_on_card_detail.goods_card
        adMark = goods_card.list[0].adMark
        img = goods_card.list[0].img + "@120w_120h.webp"
        name = goods_card.list[0].name[0:21] + "..."
        priceStr = goods_card.list[0].priceStr + "起"
        response = httpx.get(img)
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
        # 容器和主体
        goods_container = Image.new("RGBA", (1080, 200), (68, 68, 68, 255))
        if self.__isOrigin:
            goods_content = Image.new("RGBA", (864, 150), (68, 68, 68, 255))
        else:
            goods_content = Image.new("RGBA", (864, 150), '#222')
        # 圆角处理
        goods_content = await self.circle_corner(goods_content, 15)
        # 按钮
        btn = Image.open(os.path.join(self.__base_path, "Static", "Picture", "look.png")).convert("RGBA")
        btn = btn.resize((int(btn.size[0] / 2), int(btn.size[1] / 2)))
        draw_container = ImageDraw.Draw(goods_container, "RGBA")
        draw_content = ImageDraw.Draw(goods_content, "RGBA")
        # 写入来源
        draw_container.text((120, 10), adMark,
                            font=ImageFont.truetype(
                                os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 15,
                                encoding='utf-8'), fill='#AAAAAA')
        # 写入商品名
        draw_content.text((150, 30), name,
                          font=ImageFont.truetype(
                              os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 15,
                              encoding='utf-8'), fill=(255, 255, 255))
        # 写入价格
        draw_content.text((160, 80), priceStr,
                          font=ImageFont.truetype(
                              os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 15,
                              encoding='utf-8'), fill="#00A0D8")
        # 贴上商品封面
        goods_content.paste(cover, (20, int((goods_content.size[1] - cover.size[1]) / 2)), cover)
        # 贴上按钮
        goods_content.paste(btn, (700, int((goods_content.size[1] - btn.size[1]) / 2)), btn)
        if self.__isOrigin:
            goods_content_outer = Image.new("RGBA", (1000, goods_container.size[1]), '#222')
            goods_content_outer.paste(goods_content,
                                      (int((goods_content_outer.size[0] - goods_content.size[0]) / 2), 0),
                                      goods_content)
            # 贴上content
            goods_container.paste(goods_content_outer,
                                  (int((goods_container.size[0] - goods_content_outer.size[0]) / 2), 0))
        else:
            goods_container.paste(goods_content,
                                  (int((goods_container.size[0] - goods_content.size[0]) / 2),
                                   int((goods_container.size[1] - goods_content.size[1]) / 2) + 10), goods_content)

        return goods_container

    async def attach_card_handle(self, add_on_card_detail):
        """
        处理游戏或活动或装扮类型的附加卡片
        :return:
        """
        attach_card = add_on_card_detail.attach_card

        btn_name_dict = {"game": "enter.png", "official_activity": "check.png", "decoration": "look.png",
                         "manga": "zm.png", "ogv": "zf.png"}
        try:
            btn_name = btn_name_dict[attach_card.type]
        except:
            btn_name = "look.png"
        attach_card = add_on_card_detail.attach_card
        head_text = attach_card.head_text
        title = attach_card.title
        desc_first = attach_card.desc_first
        desc_second = attach_card.desc_second
        cover_url = attach_card.cover_url + "@128w_128h.webp"
        response = httpx.get(cover_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
        # 容器和主体
        attach_container = Image.new("RGBA", (1080, 200), (68, 68, 68, 255))
        if self.__isOrigin:
            attach_content = Image.new("RGBA", (864, 150), (68, 68, 68, 255))
        else:
            attach_content = Image.new("RGBA", (864, 150), "#222")
        # 按钮
        btn = Image.open(os.path.join(self.__base_path, "Static", "Picture", btn_name)).convert("RGBA")
        btn = btn.resize((127, 61))
        # 贴上封面
        attach_content.paste(cover, (15, int((attach_content.size[1] - cover.size[1]) / 2)), cover)
        # 贴上按钮
        attach_content.paste(btn, (710, int((attach_content.size[1] - btn.size[1]) / 2)), btn)
        # 准备写入内容
        draw_container = ImageDraw.Draw(attach_container, "RGBA")
        draw_content = ImageDraw.Draw(attach_content, "RGBA")
        # 写入来源
        draw_container.text((120, 10), head_text,
                            font=ImageFont.truetype(
                                os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 15,
                                encoding='utf-8'), fill='#AAAAAA')
        # 写入标题
        draw_content.text((180, 10), title,
                          font=ImageFont.truetype(
                              os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 25,
                              encoding='utf-8'), fill=(255, 255, 255))
        # 写入分类
        draw_content.text((180, 60), desc_first,
                          font=ImageFont.truetype(
                              os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 20,
                              encoding='utf-8'), fill="#AAAAAA")
        # 写入其他信息
        draw_content.text((180, 100), desc_second,
                          font=ImageFont.truetype(
                              os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"), 20,
                              encoding='utf-8'), fill="#AAAAAA")
        if self.__isOrigin:
            attach_content_outer = Image.new("RGBA", (1000, attach_container.size[1]), '#222')
            attach_content_outer.paste(attach_content,
                                       (int((attach_content_outer.size[0] - attach_content.size[0]) / 2), 0),
                                       attach_content)
            # 贴上content
            attach_container.paste(attach_content_outer,
                                   (int((attach_container.size[0] - attach_content_outer.size[0]) / 2), 0))
        else:
            # 贴上主体
            attach_container.paste(attach_content, (int((attach_container.size[0] - attach_content.size[0]) / 2),
                                                    int((attach_container.size[1] - attach_content.size[1]) / 2) + 10))
        return attach_container

    async def vote_card_handle(self, add_on_card_detail):
        """
        处理投票类型的附加卡片
        :add_on_card_detail: add_on_card_detail
        :return: Img
        """
        vote_card = add_on_card_detail.vote_card
        desc = vote_card.desc
        join_num_info = str(vote_card.join_num) + "人参与"

        # 容器
        vote_container = Image.new("RGBA", (1080, 180), (68, 68, 68, 255))
        if self.__isOrigin:
            vote_content = Image.new("RGBA", (864, 150), (68, 68, 68, 255))
        else:
            vote_content = Image.new("RGBA", (864, 150), '#222')
        # 投票图标
        vote_icon = Image.open(os.path.join(self.__base_path, "Static", "Picture", "vote_icon.png")).convert(
            "RGBA").resize((150, 150))
        # 投票按钮
        vote_btn = Image.open(os.path.join(self.__base_path, "Static", "Picture", "vote_btn.png")).convert(
            "RGBA")
        vote_btn = vote_btn.resize((int(vote_btn.size[0] / 2), int(vote_btn.size[1] / 2)))
        # 粘贴上投票图标
        vote_content.paste(vote_icon, (0, 0), vote_icon)
        # 粘贴上投票按钮
        vote_content.paste(vote_btn, (700, int((150 - vote_btn.size[1]) / 2)), vote_btn)

        draw = ImageDraw.Draw(vote_content, "RGBA")
        # 写入投票标题
        title_position = await self.calculate_text_position(start_x=200, start_y=30, y_interval=30, test_size=20,
                                                            x_constraint=650, y_constrain=30, text=desc,
                                                            interrupt=False, ignor_n=True)
        for i in title_position:
            draw.text((i["x"], i["y"]), i["content"],
                      font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "HanaMinA.ttf"), 20,
                                              encoding='utf-8'), fill=(255, 255, 255))
        # 写入参与投票人数
        draw.text((200, 80), join_num_info,
                  font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"),
                                          20,
                                          encoding='utf-8'), fill='#AAAAAA')

        # 给vote_content加一点圆角
        vote_content = await self.circle_corner(vote_content, 15)

        if self.__isOrigin:
            content_outer = Image.new("RGBA", (1000, vote_container.size[1]), '#222')
            content_outer.paste(vote_content, (int((content_outer.size[0] - vote_content.size[0]) / 2), 0),
                                vote_content)
            # 贴上content
            vote_container.paste(content_outer,
                                 (int((vote_container.size[0] - content_outer.size[0]) / 2), 0))
        else:
            vote_container.paste(vote_content, (int((vote_container.size[0] - vote_content.size[0]) / 2),
                                                int((vote_container.size[1] - vote_content.size[1]) / 2)), vote_content)

        return vote_container

    async def ugc_attach_card(self, add_on_card_detail):
        """
        处理ugc类型的附加卡片
        :return:
        """
        ugc_attach_card = add_on_card_detail.ugc_attach_card
        # 标题
        title = ugc_attach_card.title if len(ugc_attach_card.title) < 30 else ugc_attach_card.title[0:30] + "..."
        # 观看与弹幕数量
        desc_second = ugc_attach_card.desc_second
        # 封面的链接
        image_url = ugc_attach_card.image_url + "@190w_120h.webp"
        # 时长
        duration = ugc_attach_card.duration
        # 容器
        ugc_container = Image.new("RGBA", (1080, 180), (68, 68, 68, 255))
        if self.__isOrigin:
            ugc_content = Image.new("RGBA", (864, 150), (68, 68, 68, 255))
        else:
            ugc_content = Image.new("RGBA", (864, 150), '#222')
        # 获取封面
        response = httpx.get(image_url)
        cover = Image.open(BytesIO(response.content)).convert("RGBA")
        # 贴上封面
        ugc_content.paste(cover, (20, (int((ugc_content.size[1] - cover.size[1]) / 2))))
        # 时长的容器
        duration_container = Image.new("RGBA", (50, 25), (0, 0, 0, 180))
        # 贴上时长的容器
        ugc_content.paste(duration_container, (150, 100), duration_container)
        draw = ImageDraw.Draw(ugc_content, "RGBA")
        # 写入时长
        draw.text((155, 100), duration,
                  font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"),
                                          15,
                                          encoding='utf-8'), fill=(255, 255, 255))
        # 写入标题
        draw.text((230, 20), title,
                  font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"),
                                          20,
                                          encoding='utf-8'), fill=(255, 255, 255))
        # 写入观看人数及弹幕
        draw.text((240, 80), desc_second,
                  font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"),
                                          15,
                                          encoding='utf-8'),
                  fill="#AAAAAA")

        if self.__isOrigin:
            content_outer = Image.new("RGBA", (1000, ugc_container.size[1]), '#222')
            content_outer.paste(ugc_content, (int((content_outer.size[0] - ugc_content.size[0]) / 2), 0),
                                ugc_content)
            # 贴上content
            ugc_container.paste(content_outer,
                                (int((ugc_container.size[0] - content_outer.size[0]) / 2), 0))
        else:
            ugc_container.paste(ugc_content, (int((ugc_container.size[0] - ugc_content.size[0]) / 2),
                                              int((ugc_container.size[1] - ugc_content.size[1]) / 2)))

        # 贴上主体

        return ugc_container

    async def reserve_attach_card(self, add_on_card_detail):
        """
        处理预约类型的卡片
        :add_on_card_detail: add_on_card_detail
        :return:
        """
        reserve_attach_card = add_on_card_detail.reserve_attach_card
        title = reserve_attach_card.title
        desc = reserve_attach_card.desc_first.text + "    " + reserve_attach_card.desc_second
        # 容器
        reserve_container = Image.new("RGBA", (1080, 180), (68, 68, 68, 255))
        # 主体
        if self.__isOrigin:
            reserve_content = Image.new("RGBA", (864, 150), (68, 68, 68, 255))
        else:
            reserve_content = Image.new("RGBA", (864, 150), '#222')
        # 预约按钮
        reserve_btn = Image.open(os.path.join(self.__base_path, "Static", "Picture", "yy.png")).convert("RGBA")
        # 重设按钮的尺寸
        reserve_btn = reserve_btn.resize((int(reserve_btn.size[0] / 2), int(reserve_btn.size[1] / 2)))
        draw = ImageDraw.Draw(reserve_content, "RGBA")
        # 写入标题
        draw.text((50, 30), title,
                  font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"),
                                          20,
                                          encoding='utf-8'), fill=(255, 255, 255))
        # 写入预约
        draw.text((50, 80), desc,
                  font=ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", "NotoSansCJKsc-Regular.otf"),
                                          15,
                                          encoding='utf-8'), fill='#AAAAAA')
        # 给reserve_content加一点圆角
        reserve_content = await self.circle_corner(reserve_content, 15)
        # 贴上按钮
        reserve_content.paste(reserve_btn, (700, int((150 - reserve_btn.size[1]) / 2)), reserve_btn)
        # 贴上content

        if self.__isOrigin:
            content_outer = Image.new("RGBA", (1000, reserve_container.size[1]), '#222')
            content_outer.paste(reserve_content, (int((content_outer.size[0] - reserve_content.size[0]) / 2), 0),
                                reserve_content)
            # 贴上content
            reserve_container.paste(content_outer,
                                    (int((reserve_container.size[0] - content_outer.size[0]) / 2), 0))
        else:
            reserve_container.paste(content, (int((reserve_container.size[0] - reserve_content.size[0]) / 2),
                                              int((reserve_container.size[1] - reserve_content.size[1]) / 2) + 10),
                                    reserve_content)
        return reserve_container

    async def circle_corner(self, img, border):
        """
        将头像变成圆角图片
        :param img: 图片
        :param border: 圆角大小
        :return: img 将处理好的头像返回
        """
        # 画圆（用于分离4个角）
        circle = Image.new('L', (border * 2, border * 2), 0)  # 创建一个黑色背景的画布
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, border * 2, border * 2), fill=255)  # 画白色圆形
        # 原图
        w, h = img.size
        # 画4个角（将整圆分离为4个部分）
        alpha = Image.new('L', img.size, 255)
        alpha.paste(circle.crop((0, 0, border, border)), (0, 0))  # 左上角
        alpha.paste(circle.crop((border, 0, border * 2, border)), (w - border, 0))  # 右上角
        alpha.paste(circle.crop((border, border, border * 2, border * 2)), (w - border, h - border))  # 右下角
        alpha.paste(circle.crop((0, border, border, border * 2)), (0, h - border))  # 左下角
        img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
        return img

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
                            font = ImageFont.truetype("HanaMinA.ttf", test_size, encoding='utf-8')
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
                            font = ImageFont.truetype("HanaMinA.ttf", test_size, encoding='utf-8')
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
