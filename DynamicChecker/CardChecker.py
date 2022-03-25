from typing import Optional, Union, List

from pydantic import BaseModel, AnyUrl, Json


# 二级
class AtControl(BaseModel):
    data: Optional[str]
    length: Optional[int]
    location: Optional[int]
    type: Optional[int]
    type_id: Optional[str]


class Pictures(BaseModel):
    img_height: Union[int, float, None]
    img_size: Union[int, float, None]
    img_src: Optional[AnyUrl]
    img_width: Union[int, float, None]


class ApiSeasonInfo(BaseModel):
    bgm_type: Optional[int]
    cover: Optional[AnyUrl]
    title: Optional[str]
    type_name: Optional[str]


class At(BaseModel):
    location: Optional[int] = None
    length: Optional[int] = None
    data: Union[int, None] = None
    type: Optional[int] = None


# 一级
class Item(BaseModel):
    ctrl: Optional[Union[Json[List[At]], str]] = None
    at_control: Optional[Union[Json[List[At]], str]] = None
    category: Optional[str] = None
    id: Optional[int] = None
    pictures: Optional[List[Pictures]] = None
    description: Union[str, int, None] = None
    content: Union[str, int, None] = None
    pictures_count: Optional[int]


class CardUser(BaseModel):
    head_url: Optional[AnyUrl]
    face: Optional[AnyUrl]
    uid: Optional[int]
    name: Optional[str]
    uname: Optional[str]


class Stat(BaseModel):
    coin: Optional[int]
    danmaku: Optional[int]
    like: Optional[int]
    reply: Optional[int]
    share: Optional[int]
    view: Optional[int]


class OriginUser(BaseModel):
    info: Optional[CardUser]


class Sketch(BaseModel):
    # - 3 装扮 551309621391003098
    # - 131 歌单 639296660796604438
    # - 141 频道 631743110398869511
    # - 201 漫画 639302493349609508
    # - 231 挂件 639301892067819543
    biz_type: Optional[int]
    cover_url: Optional[AnyUrl]
    desc_text: Optional[str]
    title: Optional[str]
    text: Optional[str]


class Vest(BaseModel):
    content: Optional[str] = None
    ctrl: Optional[str] = None


class Author(BaseModel):
    face: AnyUrl
    name: str


class LivePlayInfo(BaseModel):
    cover: Optional[AnyUrl]
    title: Optional[str]
    area_name: Optional[str]
    watched_show: Optional[str]


class Budge(BaseModel):
    bg_color: Optional[str]
    bg_dark_color: Optional[str]
    text: Optional[str]
    text_color: Optional[str]
    text_dark_color: Optional[str]


class UpInfo(BaseModel):
    avatar: Optional[AnyUrl]
    name: Optional[str]


class CardOrigin(BaseModel):
    # 共享的
    item: Optional[Item]
    title: Optional[str]
    user: Optional[CardUser]
    author: Union[str, Author, None]
    # 投稿视频
    desc: Optional[str]
    duration: Optional[int]
    dynamic: Optional[str]
    first_frame: Optional[AnyUrl]
    jump_url: Optional[AnyUrl]
    pic: Optional[AnyUrl]
    short_link: Optional[AnyUrl]
    short_link_v2: Optional[AnyUrl]
    stat: Optional[Stat]
    title: Optional[str]
    tname: Optional[str]
    # 投稿音频
    cover: Optional[AnyUrl]
    intro: Optional[str]
    playCnt: Optional[int]
    replyCnt: Optional[int]
    typeInfo: Optional[str]
    # 挂件装扮
    sketch: Optional[Sketch]
    vest: Optional[Vest]
    # 专栏
    image_urls: Optional[List[AnyUrl]]
    origin_image_urls: Optional[List[AnyUrl]]
    stats: Optional[Stat]
    summary: Optional[str]
    # 番剧/电影/纪录片
    apiSeasonInfo: Optional[ApiSeasonInfo]
    bullet_count: Optional[int]
    cover: Optional[AnyUrl]
    index_title: Optional[str]
    new_desc: Optional[str]
    play_count: Optional[int]
    reply_count: Optional[int]
    # 直播
    title: Optional[str]
    area_v2_name: Optional[str]
    watched_show: Optional[str]
    live_play_info: Optional[LivePlayInfo]
    # 付费课程
    badge: Optional[Budge]
    subtitle: Optional[str]
    up_info: Optional[UpInfo]
    update_info: Optional[str]
    url: Optional[AnyUrl]


class Card(BaseModel):
    # 共享的
    item: Optional[Item]
    title: Optional[str]
    user: Optional[CardUser]
    author: Union[str, Author, None]
    # 投稿视频
    desc: Optional[str]
    duration: Optional[int]
    dynamic: Optional[str]
    first_frame: Optional[AnyUrl]
    jump_url: Optional[AnyUrl]
    pic: Optional[AnyUrl]
    short_link: Optional[AnyUrl]
    short_link_v2: Optional[AnyUrl]
    stat: Optional[Stat]
    title: Optional[str]
    tname: Optional[str]
    # 转发
    origin_user: Optional[OriginUser]
    origin: Optional[Json[CardOrigin]]
    # 挂件装扮
    sketch: Optional[Sketch]
    vest: Optional[Vest]
    # 投稿音频
    cover: Optional[AnyUrl]
    intro: Optional[str]
    playCnt: Optional[int]
    replyCnt: Optional[int]
    typeInfo: Optional[str]
    # 专栏
    image_urls: Optional[List[AnyUrl]]
    origin_image_urls: Optional[List[AnyUrl]]
    stats: Optional[Stat]
    summary: Optional[str]
    # 番剧
    apiSeasonInfo: Optional[ApiSeasonInfo]
    bullet_count: Optional[int]
    cover: Optional[AnyUrl]
    index_title: Optional[str]
    new_desc: Optional[str]
    play_count: Optional[int]
    reply_count: Optional[int]
    #
