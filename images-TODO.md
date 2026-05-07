# 图片替换指南

当前所有款式用**参数化 SVG 占位图**（根据 palette 三色 + 型号名自动生成）渲染。
想换真实图时，走以下流程即可：

## 怎么换

1. 把图片保存到 `assets/img/` 目录，命名建议：`{series}-{modelId}-{colorway-slug}.jpg`
   - 例：`assets/img/aj1-bred.jpg` / `assets/img/aj1-chicago.jpg`
   - 推荐尺寸：正方形 600×600 或更大，JPG / PNG / WebP 均可
2. 在 `data/sneakers.json` 对应条目加一行 `"img"` 字段：
   ```json
   {
     "name": "Bred (Banned)",
     "type": "OG",
     "img": "assets/img/aj1-bred.jpg",
     ...
   }
   ```
3. 刷新页面即可（`img` 优先级 > palette SVG）。

每代鞋的主图用 `hero_img`：
```json
"hero_img": "assets/img/aj1-hero.jpg"
```

## 图源建议

**最干净**（无版权、无防盗链）：
- 自己的收藏照片
- StockX 网页截图（打开商品页，右键图片另存为）
- GOAT 网页截图
- SneakerNews 网页截图

**不推荐**：
- Nike 官方 CDN 直链（路径带 hash，失效快）
- StockX/SneakerNews 图床热链（403 防盗链）

## 已占位的款式（21 条 · Stage 1）

| 款式 ID | 配色 | 文件名建议 |
|---|---|---|
| aj1 | hero | aj1-hero.jpg |
| aj1 | Bred (Banned) | aj1-bred.jpg |
| aj1 | Chicago | aj1-chicago.jpg |
| aj1 | Royal | aj1-royal.jpg |
| aj1 | Shadow | aj1-shadow.jpg |
| aj1 | Black Toe | aj1-black-toe.jpg |
| aj1 | UNC (Powder Blue) | aj1-unc.jpg |
| aj1 | Shattered Backboard | aj1-sbb.jpg |
| aj1 | Off-White × Chicago | aj1-offwhite.jpg |
| aj2 | hero / Chicago | aj2-hero.jpg / aj2-chicago.jpg |
| aj2 | Bred | aj2-bred.jpg |
| aj2 | Off-White × Black | aj2-offwhite.jpg |
| aj3 | hero / White Cement | aj3-hero.jpg / aj3-white-cement.jpg |
| aj3 | Black Cement | aj3-black-cement.jpg |
| aj3 | Fire Red | aj3-fire-red.jpg |
| aj4 | hero / Bred | aj4-hero.jpg / aj4-bred.jpg |
| aj4 | White Cement | aj4-white-cement.jpg |
| aj4 | Military Blue | aj4-military-blue.jpg |
| aj4 | Eminem × Carhartt | aj4-eminem.jpg |
| aj5 | hero / Fire Red | aj5-hero.jpg / aj5-fire-red.jpg |
| aj5 | Metallic Silver | aj5-metallic.jpg |
| aj5 | Grape | aj5-grape.jpg |
| aj5 | PSG | aj5-psg.jpg |

## 批量补图小技巧

如果你想偷懒，只补每代一张 hero 图就够了——列表页和详情页顶部都会用 hero。配色卡继续用 SVG 占位也不违和（不同 palette 生成的 SVG 色块本来就能反映配色差异）。
