# 四念處與四顛倒：逐幕畫面核對

原始素材與分鏡保持不變。artOverlay座標是未裁切圖片左上角百分比，不是視窗座標，也不是舊繪本的標籤中心點。除下列作者核可調整外，各標籤沿用原x、y、width、color、fontSizeCqw與align；手機同比縮小，另提供文字閱讀與圖片放大。bakedText僅由原圖呈現。

2026-11-28：S10第31–38頁「觀身不淨」的y由13%上移至6%，避開圖內「氣流（風）」，其餘位置與字級保持。現行展示值由reader-edits.json覆寫，原storyboard／README與91檔hash保留；一般圖框與放大圖框共用同一座標。

同日：S12三格漫畫第44–49頁沿藤蔓分隔遮黑，以原段落選格：第1段／44–45頁亮左格，第2、3段／46–47頁亮中格，第4段／48–49頁亮右格，其餘兩格沿用共用76%暗色。展示映射單獨維護於mindfulness/book/panel-focus-data.js；本書CSS的三個polygon共用相同曲邊，正常／放大圖皆沿用原picture-panel-focus圖框定位。原圖、口白／經文、分頁與91檔原稿不改；前後幕不留遮罩。

已將各幕原圖與references影格並列檢視；章名與五蓋標籤依交接表定位。此核對不宣稱字幕影片影格與原始插畫逐像素相同。自動量測標籤左上角、寬度及cqw字級對實際圖片框的誤差小於1px。

| 幕 | 原圖 | 原口白段落 | 經文對應 | 圖內標籤（x / y / width%，字級cqw） |
| --- | --- | ---: | --- | --- |
| S01 研究引子 | [76AE6FE5-595C-4432-8012-5F6F3C5F23F2.png](assets/76AE6FE5-595C-4432-8012-5F6F3C5F23F2.png) | 4 | 無；不自行配經 | 無；不自行加字 |
| S02 想快轉的爸爸 | [E91F2803-66D8-4CEE-A752-EB17F52DDBA9.png](assets/E91F2803-66D8-4CEE-A752-EB17F52DDBA9.png) | 3 | 無；不自行配經 | 放逸：掉舉追悔蓋：3 / 57 / 48，4.5，white，left |
| S03 想倒退的爸爸 | [BD74B990-D46B-4DB8-9D64-049D9A0B2118.png](assets/BD74B990-D46B-4DB8-9D64-049D9A0B2118.png) | 3 | 無；不自行配經 | 放逸：掉舉追悔蓋：50 / 65 / 47，4.5，white，left |
| S04 人在餐桌，心不在 | [00250A9F-F6B8-41BB-AE01-FB2A85DCE5AD.jpeg](assets/00250A9F-F6B8-41BB-AE01-FB2A85DCE5AD.jpeg) | 3 | 無；不自行配經 | 放逸：惛沉睡眠蓋：26 / 59 / 49，4.5，white，left |
| S05 回到當下 | [8ACD7BAD-64C1-476B-A4AD-7A63F5A2048E.png](assets/8ACD7BAD-64C1-476B-A4AD-7A63F5A2048E.png) | 3 | Q01：第1、2、3段 | 不放逸：39 / 68 / 23，5，white，left |
| S06 身念處：日常姿勢 | [IMG_0527.jpeg](assets/IMG_0527.jpeg) | 1 | Q02：第1段 | 無；不自行加字 |
| S07 身念處：呼吸 | [IMG_0528.jpeg](assets/IMG_0528.jpeg) | 2 | Q03：第1、2段 | 無；不自行加字 |
| S08 四顛倒總覽 | [C2350C0A-3A01-42DD-95F1-346029469087.png](assets/C2350C0A-3A01-42DD-95F1-346029469087.png) | 3 | Q04：第3段 | 四顛倒：43 / 42 / 22，5，black，left |
| S09 淨顛倒 | [IMG_0532.jpeg](assets/IMG_0532.jpeg) | 5 | Q04：第1、2、3、4、5段 | 淨顛倒：59 / 13 / 22，5，black，left |
| S10 觀身不淨：四界 | [A6D74077-1A27-421A-AACD-F417404038BE.png](assets/A6D74077-1A27-421A-AACD-F417404038BE.png) | 4 | Q05：第1、2段<br>Q06：第3、4段 | 觀身不淨：54 / 6 / 30，5，black，left |
| S11 觀身不淨：變壞譬喻 | [IMG_0541.jpeg](assets/IMG_0541.jpeg) | 4 | Q07：第1、2、3、4段 | 無；不自行加字 |
| S12 觀受是苦 | [IMG_0589.jpeg](assets/IMG_0589.jpeg) | 4 | Q04：第1、2、3、4段 | 無；不自行加字 |
| S13 便知樂受 | [B403B03F-8A20-4FBA-AB70-792401ED5DFA.jpeg](assets/B403B03F-8A20-4FBA-AB70-792401ED5DFA.jpeg) | 5 | Q08：第1、2、3、4、5段 | 無；不自行加字 |
| S14 便知苦受 | [662A414E-1B2E-4B67-B848-DD8528F029CB.jpeg](assets/662A414E-1B2E-4B67-B848-DD8528F029CB.jpeg) | 5 | Q08：第1、2、3、4、5段 | 無；不自行加字 |
| S15 感受圖鑑 | [D86791B4-6640-4FD4-BA5D-EF3E04B87F97.png](assets/D86791B4-6640-4FD4-BA5D-EF3E04B87F97.png) | 5 | Q09：第1、2段<br>Q09：第3段<br>Q09：第4、5段 | 無；不自行加字 |
| S16 內外觀受 | [236DF7C4-998F-425E-8C89-C3AE82F54330.png](assets/236DF7C4-998F-425E-8C89-C3AE82F54330.png) | 5 | Q10：第1段<br>Q10：第2、3段<br>Q10：第4、5段 | 無；不自行加字 |
| S17 心念處觀測站 | [7DB731F6-CA65-4F5F-A665-5221D2194981.png](assets/7DB731F6-CA65-4F5F-A665-5221D2194981.png) | 2 | Q11：第1、2段 | 無；不自行加字 |
| S18 觀心無常 | [B8B53DDC-3F80-45AF-A76C-09EBC836A630.jpeg](assets/B8B53DDC-3F80-45AF-A76C-09EBC836A630.jpeg) | 6 | Q12：第1、2、3、4、5、6段<br>Q15：第2、3、4段 | 觀心無常：39 / 40 / 25，5，white，left |
| S19 法念處：辨認五蓋 | [95D90BB7-2405-4DCC-BAA1-20C484761D9E.png](assets/95D90BB7-2405-4DCC-BAA1-20C484761D9E.png) | 5 | Q13：第1、2、3、4、5段 | 貪欲：13 / 51 / 13，5，black，left<br>瞋恚：28 / 38 / 13，5，black，left<br>惛沉：46 / 25 / 13，5，black，left<br>掉悔：63 / 38 / 13，5，black，left<br>疑：83 / 51 / 8，5，black，left |
| S20 法念處：七覺支 | [9BFFC0D8-7F5B-4FDB-AA41-0022B5F476DB.jpeg](assets/9BFFC0D8-7F5B-4FDB-AA41-0022B5F476DB.jpeg) | 5 | Q13：第1、2段<br>Q14：第3、4、5段 | 無；不自行加字 |
| S21 放下刺藤 | [3DF2D5E4-25B8-47F8-B159-56DD4189763D.jpeg](assets/3DF2D5E4-25B8-47F8-B159-56DD4189763D.jpeg) | 3 | Q15：第1、2、3段 | 無；不自行加字 |
| S22 觀法無我 | [45459DE4-E662-49FB-81B6-B914997A03C9.png](assets/45459DE4-E662-49FB-81B6-B914997A03C9.png) | 5 | Q16：第1、2、3、4、5段 | 觀法無我：47 / 39 / 25，5，white，left |
| S23 牧牛守田 | [CED3CE88-8343-4D7A-870F-4B2FAD34E1CA.png](assets/CED3CE88-8343-4D7A-870F-4B2FAD34E1CA.png) | 2 | Q17：第1、2段 | 無；不自行加字 |
| S24 收成後安住 | [D36D3E3A-5B66-4701-B27C-42DF12C06155.png](assets/D36D3E3A-5B66-4701-B27C-42DF12C06155.png) | 5 | Q18：第1、2、3、4、5段 | 無；不自行加字 |
| S25 四念處總結 | [D36D3E3A-5B66-4701-B27C-42DF12C06155.png](assets/D36D3E3A-5B66-4701-B27C-42DF12C06155.png) | 0（四行既定總結） | 無；不自行配經 | 無；不自行加字 |

## 需特別保留的差異

- S03使用分鏡指定車站，不用備用圖另加一幕。S18刺藤／水果與S21刺藤／蓮花沒有交換。
- S10第1、2段後顯示Q05，第3、4段後顯示Q06；六界引文的空界、識界保留。
- S15與S16同一引文各合併顯示一次，但三組段落範圍與focus分開列出，沒有遺失對應。
- S18的Q15為跨幕補充對照，S20的Q13為承接上一幕，依原relation標示。
- S23／S24保留「因品念經」。S25不採原稿中的實作提示當作口白；四行summaryRows原文完整呈現。圖片寬度不足900px時改用圖外可讀文字卡。
- reviewNote／note與所有經義待校差異另列[REVIEW_TODO.md](REVIEW_TODO.md)，不混入經文引號。

[橫直式截圖與驗證](../previews/mindfulness/README.md)。
