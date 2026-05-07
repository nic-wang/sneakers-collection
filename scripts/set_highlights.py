#!/usr/bin/env python3
"""Step 4: write highlights field per model (4-6 keywords each)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "sneakers.json")

HIGHLIGHTS = {
    "aj1": ["1985 元年", "Peter Moore 设计", "禁穿传奇", "PE 文化起点", "三原色 OG"],
    "aj2": ["1986 意大利制造", "首款无 Swoosh Jordan", "100 美元高端定价", "蜥蜴纹皮革"],
    "aj3": ["Tinker 接棒", "首款可见气垫", "Jumpman Logo 诞生", "1988 罚球线扣篮", "Spike Lee 经典广告"],
    "aj4": ["1989 The Shot", "首款全球发售", "三孔塑料挂带", "电影《Do the Right Thing》同款", "Eminem 联名稀有"],
    "aj5": ["1990 得分王", "P-51 战机鲨鱼齿", "首款 3M 反光", "半透明大底", "PSG 联名"],
    "aj6": ["1991 首冠", "保时捷 911 灵感", "鞋舌双孔进气口", "Infrared 红黑经典", "Travis Scott 联名"],
    "aj7": ["1992 二冠 + 奥运", "Bordeaux 颜值巅峰", "Hatfield 自评最爱", "巴塞罗那梦之队"],
    "aj8": ["1993 三连冠", "双 Cross Strap 绑带", "Bugs Bunny 鞋舌", "Hare Jordan 联名"],
    "aj9": ["1993 退役期产物", "未在 NBA 实战", "10 国语言鞋底", "棒球训练同款"],
    "aj10": ["1994 致敬鞋", "鞋底刻 10 大成就", "1995 复出战靴", "City 系列开端"],
    "aj11": ["1995 漆皮革命", "碳纤维足弓板", "72 胜战靴", "圣诞档周期", "史上最美球鞋公认"],
    "aj12": ["1996 日本武士灵感", "首款 Zoom Air", "1997 流感之战", "10.4 万美元拍卖"],
    "aj13": ["1997 黑豹主题", "鞋底全息猫瞳", "1998 The Last Shot", "He Got Game 同名"],
    "aj14": ["1998 法拉利 F355", "Jumpman 盾牌诞生", "公牛王朝最后一战", "Hatfield 与乔丹合作末作"],
    "kobe1": ["2005 Nike 首签", "81 分之夜", "2018 Protro 启动", "Mamba 起源"],
    "kobe2": ["2006 三版本系统", "Ultimate / Strength / Lite", "未复刻", "OG 高价"],
    "kobe3": ["2007 黑曼巴定型", "MVP 战靴", "华夫饼网格鞋面", "鞋舌 Mamba 标识首现"],
    "kobe4": ["2008 低帮革命", "Flywire 飞线", "OK 分家后首冠", "2018 Protro 爆款"],
    "kobe5": ["2009 巅峰之作", "背靠背连冠", "Chaos 小丑配色", "Bruce Lee Protro 致敬"],
    "kobe6": ["2010 蛇皮鞋面", "颜值天花板", "Grinch 圣诞战靴", "Mambacita 致敬 Gigi"],
    "kobe7": ["2011 System 系统", "可换战术鞋垫", "30000 分里程碑", "Predator 黑金"],
    "kobe8": ["2012 极致轻薄", "Engineered Mesh 网面", "阿基里斯断裂前作", "Venomenon 黑绿"],
    "kobe9": ["2013 高帮 Flyknit", "首款 Flyknit 篮球鞋", "Masterpiece 文艺复兴", "HTM 三巨头联名"],
    "kobe10": ["2014 鲨鱼皮鞋面", "43 年最强抓地力", "Fade to Black 退役预告", "全掌 Lunar"],
    "kobe11": ["2015 退役谢幕", "60 分告别战", "Achilles Heel 致敬伤病", "FTB 880 美元礼盒"],
}

with open(P) as f: d = json.load(f)

count = 0
for s in ("jordan", "kobe"):
    for m in d[s]["models"]:
        if m["id"] in HIGHLIGHTS:
            m["highlights"] = HIGHLIGHTS[m["id"]]
            count += 1

with open(P, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f"Highlights written for {count} models")
