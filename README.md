# Sneakers Collection

> AJ 1-14 + Kobe 1-11 双系列整合展示站 · SNKRS 风 · 纯静态

一个收藏级球鞋展示站，每代 OG + 代表性复刻都附出处、图片、故事与价格。

## 范围（MVP）

- **Air Jordan**: 1 – 14（1985 – 1998）
- **Nike Kobe**: 1 – 11（2005 – 2016），含 Protro 复刻版

## 技术栈

- 纯静态 HTML / CSS / Vanilla JS
- 单一数据源：`data/sneakers.json`
- GitHub Pages 部署

## 本地预览

```bash
# 任选其一
python3 -m http.server 8000
# 然后浏览器访问 http://localhost:8000
```

## 目录结构

```
sneakers-collection/
├── index.html         首页：两系列入口 + 统计
├── jordan.html        AJ 1-14 列表
├── kobe.html          Kobe 1-11 列表
├── detail.html        详情页（?series=&id= 路由）
├── data/
│   └── sneakers.json  全站数据
├── assets/
│   ├── style.css      SNKRS 风样式
│   └── app.js         渲染逻辑
└── README.md
```

## 数据字段

见 `data/sneakers.json` 的 schema：

**代系级**：`id, name, subtitle, year, designer, style_code, original_price, market_price, icon_moment, hero_image, story[], colorways[]`

**款式级**：`name, type(OG/Retro/Collab/PE), year, release_date, retail, market_price, image, story, sources[]`

## 数据源优先级

1. Nike.com 官方归档页（最权威）
2. SneakerNews 复刻历史（字段齐全）
3. StockX / GOAT（市价区间参考）
4. Wikipedia 交叉校验

## 图片策略

所有图片优先使用外部 CDN 直链：
- Nike 官方 CDN（`static.nike.com`）
- StockX（`images.stockx.com`）
- 页面 `<meta name="referrer" content="no-referrer">` 规避 Referer 防盗链

图失效时集中在 `data/sneakers.json` 内更新。

## 开发进度

- [x] Stage 0 · 骨架
- [x] Stage 1 · AJ 1-5 样板
- [x] Stage 2 · AJ 6-14
- [x] Stage 3 · Kobe 1-11（含 Protro）
- [x] Stage 3.5 · 浅色主题翻新
- [x] Stage 3.6 · 经典款 hero 对齐 + 配色补全到 146 条
- [x] Stage 3.7 · 详情页区块化（事实矩阵 + 关键词胶囊 + 段落锚点 + 配色筛选）
- [ ] Stage 4 · GitHub Pages 上线

## 当前数据量

- 25 代签名鞋（14 AJ + 11 Kobe）
- **146 条配色记录**（每代 4-9 款，覆盖 OG / Retro / Collab / PE）
- **146 张真实产品图 · 100% 覆盖**
- 浅色 SNKRS 风

## 免责声明

本站仅用于资料归档与学习交流。所有品牌、图片版权归 Nike, Inc. 及原始作者所有。价格数据仅供参考。

---

© 2026 · Curated with 🦜
