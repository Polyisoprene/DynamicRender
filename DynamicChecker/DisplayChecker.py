from typing import Optional, List, Union

from pydantic import BaseModel, Json, AnyUrl


# 四级
class Check(BaseModel):
    text: Optional[str]
    icon: Optional[str]


class JumpStyle(BaseModel):
    text: str


# 三级

class GoodsDetail(BaseModel):
    adMark: Optional[str]
    appName: Optional[str]
    iconName: Optional[str]
    iconUrl: Union[AnyUrl, str, None]
    img: Union[AnyUrl, str, None]
    jumpLink: Union[AnyUrl, str, None]
    jumpLinkDesc: Optional[str]
    name: Optional[str]
    oriPrice: Optional[str]
    price: Optional[float]
    priceStr: Optional[str]
    schemaPackageName: Optional[str]
    schemaUrl: Union[AnyUrl, str, None]
    shopGoodType: Optional[int]
    sourceDesc: Optional[str]
    wordJumpLinkDesc: Optional[str]


class DescFirst(BaseModel):
    style: Optional[int]
    text: Optional[str]


class ReserveButton(BaseModel):
    status: int
    type: int
    jump_style: Optional[JumpStyle]
    check: Optional[Check]


class AttachCardButton(BaseModel):
    jump_style: Optional[JumpStyle]


class VoteCard(BaseModel):
    choice_cnt: int
    default_share: int
    default_text: Optional[str]
    desc: Optional[str]
    join_num: Optional[int]
    status: Optional[int]
    type: Optional[int]


# 二级
class EmojiDetail(BaseModel):
    emoji_name: Optional[str]
    id: Optional[int]
    url: Union[AnyUrl, str, None]


class RichDetail(BaseModel):
    # 2为专栏，1为视频
    icon_type: Optional[int]
    jump_uri: Union[AnyUrl, str, None]
    orig_text: Optional[str]
    text: Optional[str]


class GoodsDetails(BaseModel):
    list: Optional[List[GoodsDetail]]


class ReserveAttachCard(BaseModel):
    desc_first: Optional[DescFirst]
    desc_second: Optional[str]
    livePlanStartTime: Optional[int]
    reserve_total: Optional[int]
    show_desc_second: Optional[bool]
    state: Optional[int]
    stype: Optional[int]
    title: Optional[str]
    type: Optional[str]
    reserve_button: Optional[ReserveButton]


class NewTopic(BaseModel):
    link: Union[AnyUrl, str, None]
    name: str
    id: int


class TopicDetails(BaseModel):
    is_activity: int
    topic_id: int
    topic_link: Union[AnyUrl, str, None]
    topic_name: str


class AttachCard(BaseModel):
    cover_type: Optional[int]
    cover_url: Union[AnyUrl, str, None]
    desc_first: Optional[str]
    desc_second: Optional[str]
    head_text: Optional[str]
    title: Optional[str]
    type: Optional[str]
    button: Optional[AttachCardButton]


class UgcAttachCard(BaseModel):
    desc_second: Optional[str]
    duration: Optional[str]
    head_text: Optional[str]
    image_url: Optional[str]
    title: Optional[str]
    type: Optional[str]


# 一级
# emoji
class EmojiInfo(BaseModel):
    emoji_details: Optional[List[EmojiDetail]]


# 附加卡片
class AddOnCardDetail(BaseModel):
    # add_on_card_show_type： 6为预约 5为ugc 3为投票 2为游戏或活动或装扮 1为商品
    add_on_card_show_type: Optional[int]
    # 商品橱窗 示例638470480878108680
    goods_card: Optional[Json[GoodsDetails]]
    # 预约 示例动态 597756424231863394
    reserve_attach_card: Optional[ReserveAttachCard]
    # 游戏示例 638931657286484020 type=game
    # 官方活动示例 551289005548902075 type = official_activity
    # 装扮示例 638611334350503973 type = decoration
    # 漫画 示例 637737411561914375 type = manga
    # 动漫 示例 639534382927839233 type = ogv
    attach_card: Optional[AttachCard]
    # ugc_attach_card 示例动态 610622978014393724
    ugc_attach_card: Optional[UgcAttachCard]
    # 投票 示例动态 611702685546788433
    vote_card: Optional[Json[VoteCard]]


# 富文本
class RichDetails(BaseModel):
    rich_details: Optional[List[RichDetail]]


# 话题标签
class TopicInfo(BaseModel):
    # 活动标签
    new_topic: Optional[NewTopic]
    # 讨论话题
    topic_details: Optional[List[TopicDetails]]


class OriginDisplay(BaseModel):
    emoji_info: Optional[EmojiInfo]
    add_on_card_info: Optional[List[AddOnCardDetail]]
    rich_text: Optional[RichDetails]
    topic_info: Optional[TopicInfo]
    usr_action_txt: Optional[str]


class Display(BaseModel):
    emoji_info: Optional[EmojiInfo]
    add_on_card_info: Optional[List[AddOnCardDetail]]
    rich_text: Optional[RichDetails]
    topic_info: Optional[TopicInfo]
    usr_action_txt: Optional[str]
    origin: Optional[OriginDisplay]
    new_topic: Optional[NewTopic]
