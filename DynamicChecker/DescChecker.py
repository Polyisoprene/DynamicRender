from typing import Optional, Union

from pydantic import BaseModel, AnyUrl


# 三级
class OfficialVerify(BaseModel):
    desc: Optional[str] = None
    type: Optional[int] = None


class Fan(BaseModel):
    color: Optional[str] = None
    is_fan: Optional[int] = None
    num_desc: Optional[str] = None
    number: Optional[int] = None


class Label(BaseModel):
    bg_color: Optional[str] = None
    bg_style: Optional[int] = None
    border_color: Optional[str] = None
    label_theme: Optional[str] = None
    path: Optional[str] = None
    text: Optional[str] = None
    text_color: Optional[str] = None


# 二级
class UserProfileCard(BaseModel):
    official_verify: Optional[OfficialVerify] = None


class UserProfileDecorateCard(BaseModel):
    big_card_url: Optional[str] = None
    card_type: Optional[str] = None
    card_type_name: Optional[str] = None
    card_url: Optional[str] = None
    expire_time: Optional[int] = None
    id: Optional[int] = None
    image_enhance: Optional[str] = None
    item_id: Optional[int] = None
    item_type: Optional[int] = None
    jump_url: Optional[str] = None
    mid: Optional[int] = None
    name: Union[int, str, None] = None
    uid: Optional[int] = None
    fan: Optional[Fan] = None


class UserProfileInfo(BaseModel):
    face: Optional[AnyUrl] = None
    face_nft: Optional[int] = None
    uid: Optional[int] = None
    uname: Optional[str] = None


class UserProfileLevelInfo(BaseModel):
    current_level: Optional[int]


class UserProfilePendant(BaseModel):
    image: Union[AnyUrl, None, str] = None
    image_enhance: Optional[str] = None
    image_enhance_frame: Optional[str] = None
    name: Optional[str] = None
    pid: Optional[int] = None


class UserProfileVip(BaseModel):
    avatar_subscript: Optional[int] = None
    avatar_subscript_url: Optional[str] = None
    label: Optional[Label] = None
    nickname_color: Optional[str] = None
    role: Optional[int] = None
    themeType: Optional[int] = None
    vipDueDate: Optional[int] = None
    vipStatus: Optional[int] = None
    vipType: Optional[int] = None


# 一级
class UserProfile(BaseModel):
    card: Optional[UserProfileCard] = None
    decorate_card: Optional[UserProfileDecorateCard] = None
    info: Optional[UserProfileInfo] = None
    level_info: Optional[UserProfileLevelInfo] = None
    pendant: Optional[UserProfilePendant] = None
    rank: Optional[str] = None
    sign: Optional[str] = None
    vip: Optional[UserProfileVip] = None


class DescOrigin(BaseModel):
    type: int
    view: int
    repost: int


class Desc(BaseModel):
    comment: Optional[int] = None
    dynamic_id: Optional[int] = None
    dynamic_id_str: Optional[str] = None
    is_liked: Optional[int] = None
    like: Optional[int] = None
    orig_dy_id_str: Optional[str] = None
    orig_type: Optional[int] = None
    origin: Optional[DescOrigin]
    pre_dy_id_str: Optional[str] = None
    repost: Optional[int] = None
    rid: Optional[int] = None
    rid_str: Optional[str] = None
    status: Optional[int] = None
    timestamp: Optional[int] = None
    type: Optional[int] = None
    uid: Optional[int] = None
    uid_type: Optional[int] = None
    view: Optional[int] = None
    user_profile: Optional[UserProfile] = None
