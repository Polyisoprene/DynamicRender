# DynamicRender

#### 介绍
将B站动态渲染为图片

#### 依赖

___1.pydantic___  
___2.asyncio___  
___3.pillow___  
___4.httpx___  
___5.qrcode___  
___6.emoji___  
___7.fontTools___  


#### 使用说明

> 假设我们有以下一个card

<details>
  <summary>展开查看</summary>
  <pre><code> 
```json
card = {
  "desc": {
    "uid": 37815472,
    "type": 1,
    "rid": 641447168023423400,
    "view": 5,
    "repost": 1,
    "comment": 0,
    "like": 0,
    "is_liked": 0,
    "dynamic_id": 641447168104726500,
    "timestamp": 1648186957,
    "pre_dy_id": 641446072875483100,
    "orig_dy_id": 641298076909174800,
    "orig_type": 8,
    "user_profile": {
      "info": {
        "uid": 37815472,
        "uname": "_DMC_",
        "face": "https://i1.hdslb.com/bfs/face/b796fc234e84db55d37f48562004a070705c2258.jpg",
        "face_nft": 0
      },
      "card": {
        "official_verify": {
          "type": -1,
          "desc": ""
        }
      },
      "vip": {
        "vipType": 1,
        "vipDueDate": 1647446400000,
        "vipStatus": 0,
        "themeType": 0,
        "label": {
          "path": "",
          "text": "",
          "label_theme": "",
          "text_color": "",
          "bg_style": 0,
          "bg_color": "",
          "border_color": ""
        },
        "avatar_subscript": 0,
        "nickname_color": "",
        "role": 0,
        "avatar_subscript_url": ""
      },
      "pendant": {
        "pid": 1010,
        "name": "大航海_舰长",
        "image": "https://i1.hdslb.com/bfs/garb/item/1b7684c1de7dfc5aa0c43c55edb247432b0cbe64.png",
        "expire": 0,
        "image_enhance": "https://i1.hdslb.com/bfs/garb/item/1b7684c1de7dfc5aa0c43c55edb247432b0cbe64.png",
        "image_enhance_frame": ""
      },
      "decorate_card": {
        "mid": 37815472,
        "id": 5021,
        "card_url": "https://i0.hdslb.com/bfs/garb/item/bef87ecfbdbf46020f1800d8c098771b1f7c56b7.png",
        "card_type": 2,
        "name": "舰长",
        "expire_time": 0,
        "card_type_name": "免费",
        "uid": 37815472,
        "item_id": 5021,
        "item_type": 1,
        "big_card_url": "https://i0.hdslb.com/bfs/garb/item/bef87ecfbdbf46020f1800d8c098771b1f7c56b7.png",
        "jump_url": "https://live.bilibili.com/blackboard/activity-lVEr9rQGw2.html",
        "fan": {
          "is_fan": 0,
          "number": 0,
          "color": "",
          "num_desc": ""
        },
        "image_enhance": "https://i0.hdslb.com/bfs/garb/item/bef87ecfbdbf46020f1800d8c098771b1f7c56b7.png"
      },
      "rank": "10000",
      "sign": "",
      "level_info": {
        "current_level": 6
      }
    },
    "uid_type": 1,
    "status": 1,
    "dynamic_id_str": "641447168104726550",
    "pre_dy_id_str": "641446072875483139",
    "orig_dy_id_str": "641298076909174785",
    "rid_str": "641447168023423305",
    "origin": {
      "uid": 11041571,
      "type": 8,
      "rid": 937506207,
      "acl": 0,
      "view": 38,
      "repost": 3,
      "like": 0,
      "dynamic_id": 641298076909174800,
      "timestamp": 1648152244,
      "pre_dy_id": 0,
      "orig_dy_id": 0,
      "uid_type": 1,
      "stype": 0,
      "r_type": 0,
      "inner_id": 0,
      "status": 1,
      "dynamic_id_str": "641298076909174785",
      "pre_dy_id_str": "0",
      "orig_dy_id_str": "0",
      "rid_str": "937506207",
      "bvid": "BV1GT4y1i7kw"
    },
    "previous": {
      "uid": 1383815813,
      "type": 1,
      "rid": 641446072803611400,
      "acl": 0,
      "view": 5186,
      "repost": 1,
      "like": 0,
      "dynamic_id": 641446072875483100,
      "timestamp": 1648186702,
      "pre_dy_id": 641298076909174800,
      "orig_dy_id": 641298076909174800,
      "uid_type": 1,
      "stype": 0,
      "r_type": 0,
      "inner_id": 0,
      "status": 1,
      "dynamic_id_str": "641446072875483139",
      "pre_dy_id_str": "641298076909174785",
      "orig_dy_id_str": "641298076909174785",
      "rid_str": "641446072803611335"
    }
  },
  "card": "{ \"user\": { \"uid\": 37815472, \"uname\": \"_DMC_\", \"face\": \"https:\\/\\/i1.hdslb.com\\/bfs\\/face\\/b796fc234e84db55d37f48562004a070705c2258.jpg\" }, \"item\": { \"rp_id\": 641447168023423305, \"uid\": 37815472, \"content\": \"\\/\\/@吉诺儿kino:玩上瘾了\", \"ctrl\": \"[{\\\"data\\\":\\\"1383815813\\\",\\\"location\\\":2,\\\"length\\\":8,\\\"type\\\":1}]\", \"orig_dy_id\": 641298076909174785, \"pre_dy_id\": 641446072875483139, \"timestamp\": 1648186957, \"at_uids\": [ 1383815813 ], \"reply\": 0, \"orig_type\": 8 }, \"origin\": \"{\\\"aid\\\":937506207,\\\"attribute\\\":0,\\\"cid\\\":558086422,\\\"copyright\\\":1,\\\"ctime\\\":1648152243,\\\"desc\\\":\\\"看到有夏韭菜整了合成大九夏的活，波波派也不甘示弱，试着整了这个小活\\\\n喜欢的话，请多多关注kino这位小可爱哦\\\\n\\\\n吉诺儿kino：https:\\\\\\/\\\\\\/b23.tv\\\\\\/regaBYH\\\\n\\\\n唐九夏还想再躺一下：https:\\\\\\/\\\\\\/b23.tv\\\\\\/C0oz3AW \\\\n\\\\n游戏链接：https:\\\\\\/\\\\\\/bigkino-6g924lmf533f5715-1310510710.tcloudbaseapp.com\\\\\\/\\\\n\\\\n目前手机打开链接，应该就能直接玩\\\\n（电脑端打开有显示bug，不会整，摆了）\\\\n灵感来源：BV1oU4y1d7hQ\\\",\\\"dimension\\\":{\\\"height\\\":2340,\\\"rotate\\\":0,\\\"width\\\":1080},\\\"duration\\\":51,\\\"dynamic\\\":\\\"\\\",\\\"first_frame\\\":\\\"https:\\\\\\/\\\\\\/i0.hdslb.com\\\\\\/bfs\\\\\\/storyff\\\\\\/n220325a28q4l1c4978u93a4krqs0j9v_firsti.jpg\\\",\\\"jump_url\\\":\\\"bilibili:\\\\\\/\\\\\\/video\\\\\\/937506207\\\\\\/?page=1&player_preload=null&player_width=1080&player_height=2340&player_rotate=0\\\",\\\"owner\\\":{\\\"face\\\":\\\"https:\\\\\\/\\\\\\/i2.hdslb.com\\\\\\/bfs\\\\\\/face\\\\\\/9b43b627f62087f3898ab9d2e24967e080946862.jpg\\\",\\\"mid\\\":11041571,\\\"name\\\":\\\"Mrboo萝卜\\\"},\\\"pic\\\":\\\"https:\\\\\\/\\\\\\/i0.hdslb.com\\\\\\/bfs\\\\\\/archive\\\\\\/b4ebd5ffa42dcee444b89bed3a6c352d78547729.jpg\\\",\\\"player_info\\\":null,\\\"pubdate\\\":1648152243,\\\"rights\\\":{\\\"autoplay\\\":1,\\\"bp\\\":0,\\\"download\\\":0,\\\"elec\\\":0,\\\"hd5\\\":0,\\\"is_cooperation\\\":0,\\\"movie\\\":0,\\\"no_background\\\":0,\\\"no_reprint\\\":1,\\\"pay\\\":0,\\\"ugc_pay\\\":0,\\\"ugc_pay_preview\\\":0},\\\"short_link\\\":\\\"https:\\\\\\/\\\\\\/b23.tv\\\\\\/BV1GT4y1i7kw\\\",\\\"short_link_v2\\\":\\\"https:\\\\\\/\\\\\\/b23.tv\\\\\\/BV1GT4y1i7kw\\\",\\\"stat\\\":{\\\"aid\\\":937506207,\\\"coin\\\":0,\\\"danmaku\\\":1,\\\"dislike\\\":0,\\\"favorite\\\":2,\\\"his_rank\\\":0,\\\"like\\\":25,\\\"now_rank\\\":0,\\\"reply\\\":6,\\\"share\\\":3,\\\"view\\\":648},\\\"state\\\":0,\\\"tid\\\":27,\\\"title\\\":\\\"合 成 大 kino\\\",\\\"tname\\\":\\\"综合\\\",\\\"videos\\\":1}\", \"origin_extend_json\": \"{\\\"like_icon\\\":{\\\"action\\\":\\\"\\\",\\\"action_url\\\":\\\"https:\\\\\\/\\\\\\/i0.hdslb.com\\\\\\/bfs\\\\\\/garb\\\\\\/item\\\\\\/9b45433f7b334e7b0ed2c0e8e264a8dcfdb4f3dc.bin\\\",\\\"end\\\":\\\"\\\",\\\"end_url\\\":\\\"\\\",\\\"like_icon_id\\\":5022,\\\"start\\\":\\\"\\\",\\\"start_url\\\":\\\"\\\"},\\\"topic\\\":{\\\"is_attach_topic\\\":1}}\", \"origin_user\": { \"info\": { \"uid\": 11041571, \"uname\": \"Mrboo萝卜\", \"face\": \"https:\\/\\/i2.hdslb.com\\/bfs\\/face\\/9b43b627f62087f3898ab9d2e24967e080946862.jpg\", \"face_nft\": 0 }, \"card\": { \"official_verify\": { \"type\": -1, \"desc\": \"\" } }, \"vip\": { \"vipType\": 2, \"vipDueDate\": 1695830400000, \"vipStatus\": 1, \"themeType\": 0, \"label\": { \"path\": \"\", \"text\": \"年度大会员\", \"label_theme\": \"annual_vip\", \"text_color\": \"#FFFFFF\", \"bg_style\": 1, \"bg_color\": \"#FB7299\", \"border_color\": \"\" }, \"avatar_subscript\": 1, \"nickname_color\": \"#FB7299\", \"role\": 3, \"avatar_subscript_url\": \"https:\\/\\/i0.hdslb.com\\/bfs\\/vip\\/icon_Certification_big_member_22_3x.png\" }, \"pendant\": { \"pid\": 0, \"name\": \"\", \"image\": \"\", \"expire\": 0, \"image_enhance\": \"\", \"image_enhance_frame\": \"\" }, \"rank\": \"10000\", \"sign\": \"(╯‵□′)╯︵┻━┻\", \"level_info\": { \"current_level\": 6 } } }",
  "extend_json": "{\"\":{\"at_mids\":[{\"at_type\":2,\"mid_list\":[1383815813]}],\"content\":\"\\/\\/@吉诺儿kino:玩上瘾了\",\"data_type\":2,\"ext_info\":\"\",\"need_send_msg\":true,\"publisher\":37815472},\"ctrl\":[{\"data\":\"1383815813\",\"length\":8,\"location\":2,\"type\":1}],\"from\":{\"emoji_type\":1,\"up_close_comment\":0},\"like_icon\":{\"action\":\"\",\"action_url\":\"https:\\/\\/i0.hdslb.com\\/bfs\\/garb\\/item\\/9b45433f7b334e7b0ed2c0e8e264a8dcfdb4f3dc.bin\",\"end\":\"\",\"end_url\":\"\",\"like_icon_id\":5022,\"start\":\"\",\"start_url\":\"\"}}",
  "display": {
    "origin": {
      "topic_info": {
        "topic_details": [
          {
            "topic_id": 24438355,
            "topic_name": "NB二创",
            "is_activity": 0,
            "topic_link": "https://search.bilibili.com/all?keyword=NB%E4%BA%8C%E5%88%9B"
          },
          {
            "topic_id": 2423,
            "topic_name": "可爱",
            "is_activity": 0,
            "topic_link": "https://search.bilibili.com/all?keyword=%E5%8F%AF%E7%88%B1"
          },
          {
            "topic_id": 1833,
            "topic_name": "搞笑",
            "is_activity": 0,
            "topic_link": "https://search.bilibili.com/all?keyword=%E6%90%9E%E7%AC%91"
          },
          {
            "topic_id": 1217,
            "topic_name": "自制",
            "is_activity": 0,
            "topic_link": "https://search.bilibili.com/all?keyword=%E8%87%AA%E5%88%B6"
          },
          {
            "topic_id": 20660912,
            "topic_name": "吉诺儿kino",
            "is_activity": 0,
            "topic_link": "https://search.bilibili.com/all?keyword=%E5%90%89%E8%AF%BA%E5%84%BFkino"
          },
          {
            "topic_id": 18231081,
            "topic_name": "合成大西瓜",
            "is_activity": 0,
            "topic_link": "https://search.bilibili.com/all?keyword=%E5%90%88%E6%88%90%E5%A4%A7%E8%A5%BF%E7%93%9C"
          }
        ],
        "new_topic": {
          "id": 10739,
          "name": "NB二创",
          "link": "https://m.bilibili.com/topic-detail?topic_id=10739&topic_name=NB%E4%BA%8C%E5%88%9B"
        }
      },
      "usr_action_txt": "投稿了视频",
      "relation": {
        "status": 1,
        "is_follow": 0,
        "is_followed": 0
      },
      "show_tip": {
        "del_tip": "要删除动态吗？"
      },
      "cover_play_icon_url": "https://i0.hdslb.com/bfs/album/2269afa7897830b397797ebe5f032b899b405c67.png"
    }
  }
}
```
  </code></pre>
</details>


1. 导入DynamicRender及card校验文件
```python
from DynamicRender.DynamicChecker import Dynamic
from DynamicRender import Render
import asyncio
```

2. 格式化card并且渲染图片

```python

async def main():
    card = Dynamic(**card)
    dynamic_img = await Render(card).render()
    dynamic_img.show()
    
asyncio.run(main())
 ```

3. 完整代码

```python
from DynamicRender.DynamicChecker import Dynamic
from DynamicRender import Render
import asyncio

async def main():
    card = Dynamic(**card)
    dynamic_img = await Render(card).render()
    dynamic_img.show()
    
asyncio.run(main())

```
#### 注意

如果使用过程中报错字体缺失，请自行下载对应字体放在DynamicRender->Static->Font目录下




#### 效果预览

![这是图片](http://i0.hdslb.com/bfs/album/96fa55d0947ed244be58e925257af66e815e6e7d.png)
![这是图片](http://i0.hdslb.com/bfs/album/f90a5f75d4785462a7be26afa580236c47592996.png)

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request



