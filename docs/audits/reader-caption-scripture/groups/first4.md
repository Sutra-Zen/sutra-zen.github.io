# 四本繪本口白與經典出處唯讀稽核

基準：a238a0fb549966ac0510b5b89f18b913c8ec40b6。未修改runtime／原稿。
完整4本275頁62幕131組場景與引文配對（含無引文、心經、後記）。
確定問題組4；作者討論17。作者討論不等於放錯經號或必須整改。

## 發現與建議

### F4-C01｜四聖諦｜象跡喻經開示者歸屬需校

分類：confirmed_mismatch；頁碼：[1, 1]；場景：['S01']。

口白（第1頁）：佛陀曾說：就像所有動物的足跡，都能被容納在大象寬廣的腳印裡；
世間所有關於幸福與智慧的秘密，

下方引文：中阿含經第30經：
若有無量善法，彼一切法皆四聖諦所攝，來入四聖諦中，謂：四聖諦於一切法最為第一，所以者何？
攝受一切眾善法故。諸賢！猶如諸畜之跡，象跡為第一，所以者何？彼象跡者最廣大故。

理由：象跡攝善法的內容配對正確，但MA30前文是尊者舍梨子告諸比丘，上方直接說佛陀曾說，與所引經的敘事說話者不同；不是經號錯置。

建議：可改經中舍梨子曾說或經中以象跡比喻，保留四聖諦主旨與佛陀醫師創作角色。

原典對證：爾時，尊者舍梨子告諸比丘：「諸賢！若有無量善法，彼一切法皆四聖諦所攝……猶如諸畜之跡，象跡為第一……彼象跡者最廣大故。」

來源：https://suttacentral.net/ma30/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/ma/ma30.html

檔案位置：[{"file": "four-truths/book/scenes.js", "line": 7, "quote_line": 14, "scene_id": "S01", "in_scene_page": 1}]

### F4-C02｜五陰｜四大造色引文實出SA41卻指SA46

分類：confirmed_mismatch；頁碼：[7, 9]；場景：['S04']。

口白（第7頁）：什麼是「色」？

口白（第8頁）：就是由地、水、火、風，四大與四大所組成的，

下方引文：云何色如實知？

理由：云何色如實知與一切四大及四大造色的完整句逐字出自SA41，SA46沒有此段。三頁source均../#sa46，同庫storyboard.csv第7–9筆亦同。五陰導讀的SA46全文本身正確，並沒有把四大段塞進46經；目前導讀沒有SA41卡。

建議：先在五陰導讀加已核SA41來源卡，再將三頁source改到該卡。保留口白與引文；SA46全文不必改。CSV或獨立公開校訂層同步，避免重建覆回。

原典對證：SA41：云何色如實知？諸所有色，一切四大及四大造色，是名色，如是色如實知。 / SA46：若可閡可分，是名色受陰。

來源：https://suttacentral.net/sa41/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa41.html | https://suttacentral.net/sa46/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa46.html

檔案位置：[{"file": "five-aggregates/book/index.html", "line": 447, "quote_line": 448, "scene_id": "S04", "in_scene_page": 1}, {"file": "five-aggregates/book/index.html", "line": 452, "quote_line": 453, "scene_id": "S04", "in_scene_page": 2}, {"file": "five-aggregates/book/index.html", "line": 457, "quote_line": 453, "scene_id": "S04", "in_scene_page": 3}]

### F4-C03｜五陰｜未來識口白仍配前頁過去識引文

分類：confirmed_mismatch；頁碼：[43, 43]；場景：['S11']。

口白（第43頁）：我現在被識所束縛，如果我繼續貪愛未來的識，
將來也會被識所束縛，就像現在一樣。

下方引文：多聞聖弟子於此受……想……行……識受陰作如是學：『我今現在為現在識所食，
於過去世已曾為識所食，如今現在；

理由：上方已說繼續貪愛未來識，下方卻重複42頁的過去識所食句，未呈現SA46緊接的未來識句。同庫CSV43筆亦同，root原生Next顯示相同資料。

建議：僅第43頁下方改配SA46未來識完整句，source仍SA46；原始交接保留並另記校訂。

原典對證：我今已為現在識所食，若復樂著未來識者，亦當復為彼識所食，如今現在。

來源：https://suttacentral.net/sa46/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa46.html

檔案位置：[{"file": "five-aggregates/book/index.html", "line": 676, "quote_line": 677, "scene_id": "S11", "in_scene_page": 5}]

### F4-D01｜四聖諦｜五盛陰火喻與病癒本淨是敘事延伸

分類：author_discussion；頁碼：[7, 19]；場景：['S03', 'S07']。

口白（第7頁）：你看，有色，受，想，行，識，五條火紅的鎖鏈鎖著你。
佛陀稱之為「五盛陰」。我們的身心就像一團熾盛燃燒的火。

口白（第8頁）：正因為我們把這團火當作是「我」，緊抓不放，
生命才會感到如此灼熱與沉重。這就是苦的真理。

下方引文：增壹阿含經四諦品第二十五：所謂苦諦者，生苦、老苦、病苦、死苦、憂悲惱苦、怨憎會苦、
恩愛別離苦、所欲不得苦，取要言之，五盛陰苦，是謂名為苦諦。

理由：苦與滅的經號、主題相應，非錯配。五盛陰不是僅因盛字便可作熾盛燃燒的詞源解釋；恢復生命原本清淨健康也不是欲愛盡句逐字定義。作為醫師與火的故事譬喻可以保留。

建議：若作者願意，可用好比引入火與病癒，滅諦承接貪愛止息；不必換經文，非必須整改。

原典對證：取要言之，五盛陰苦，是謂名為苦諦。 / 欲愛永盡無餘，不復更造，是謂名為苦盡諦。

來源：https://suttacentral.net/ea25.1/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/ea/ea25/ea25.1.html | https://suttacentral.net/sa55/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa55.html

檔案位置：[{"file": "four-truths/book/scenes.js", "line": 31, "quote_line": 43, "scene_id": "S03", "in_scene_page": 2}, {"file": "four-truths/book/scenes.js", "line": 31, "quote_line": 43, "scene_id": "S03", "in_scene_page": 3}, {"file": "four-truths/book/scenes.js", "line": 91, "quote_line": 102, "scene_id": "S07", "in_scene_page": 1}, {"file": "four-truths/book/scenes.js", "line": 91, "quote_line": 102, "scene_id": "S07", "in_scene_page": 2}, {"file": "four-truths/book/scenes.js", "line": 100, "quote_line": 102, "scene_id": "S07", "in_scene_page": 3}]

### F4-D02｜五陰｜宿命智三時句被讀成知道未來生命

分類：author_discussion；頁碼：[4, 6]；場景：['S03']。

口白（第4頁）：如果擁有宿命神通的修行人，了解自己過去的種種生命，

口白（第5頁）：那麼他們所知道的過去、現在和未來的生命經歷，
都是在這五受陰中經歷的。

下方引文：若沙門、婆羅門以宿命智自識種種宿命，

理由：SA46語境為宿命智回憶過去世，緊接我過去所經；第5頁卻說知道過去現在未來的生命經歷，易使人把宿命智當預知未來。已識當識今識宜理解不同時候作宿命回憶者仍不離五受陰。平行SN22.79明說回憶種種前世住處。經號未錯，但白話解讀值得優先校訂。

建議：可改不論過去現在未來，修行人以宿命智回憶過去生命時，所回憶的不離五受陰；由作者先核語意。

原典對證：若沙門、婆羅門以宿命智自識種種宿命，已識、當識、今識，皆於此五受陰……我過去所經。 / SN22.79：凡任何沙門或婆羅門回憶種種前世住處之回憶時，都在這五取蘊上回憶，或者其中之一。

來源：https://suttacentral.net/sa46/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa46.html | https://suttacentral.net/sn22.79/zh/zhuang | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/zh/pli/sutta/sn/sn22/sn22.79.html

檔案位置：[{"file": "five-aggregates/book/index.html", "line": 425, "quote_line": 426, "scene_id": "S03", "in_scene_page": 1}, {"file": "five-aggregates/book/index.html", "line": 430, "quote_line": 431, "scene_id": "S03", "in_scene_page": 2}, {"file": "five-aggregates/book/index.html", "line": 435, "quote_line": 436, "scene_id": "S03", "in_scene_page": 3}]

### F4-D03｜五陰｜想、識與判斷好壞的分工可更精確

分類：author_discussion；頁碼：[19, 51]；場景：['S08', 'S10', 'S14']。

口白（第19頁）：各種想法是「想受陰」，無論是少量、多量、無量的想法，
或是認為一切皆無，這些都是「想受陰」的表現。

口白（第20頁）：因此，「想受陰」也是無常、痛苦、會變化的。

下方引文：諸想是想受陰，何所想？少想、多想、無量想，都無所有，作無所有想，是故，名想受陰；

理由：想與識的主經、俱舍與品類足補充都相應，非錯配。各種想法／想太多易泛化成所有思考；35頁把好壞判斷直接交給識，36頁又似識先起想才取相。原引文只說識了別、想取相，未建立單一心理模組或固定先後。

建議：可保留貼標籤與蛋糕譬喻，識寫了別、想寫辨認取相，好壞判斷有多種心理作用參與。非必須整改。

原典對證：別知相是識受陰，何所識？識色，識聲、香、味、觸、法。 / 想謂於境取差別相。 / 想云何？謂取像性。

來源：https://suttacentral.net/sa46/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa46.html | https://cbetaonline.dila.edu.tw/zh/T1558 | https://raw.githubusercontent.com/cbeta-git/xml-p5a/master/T/T29/T29n1558.xml | https://raw.githubusercontent.com/cbeta-git/xml-p5a/6952edb0bca6b86a68c409b36e8be659a8a75e2b/T/T29/T29n1558.xml | https://cbetaonline.dila.edu.tw/zh/T1542 | https://raw.githubusercontent.com/cbeta-git/xml-p5a/master/T/T26/T26n1542.xml | https://raw.githubusercontent.com/cbeta-git/xml-p5a/6952edb0bca6b86a68c409b36e8be659a8a75e2b/T/T26/T26n1542.xml

檔案位置：[{"file": "five-aggregates/book/index.html", "line": 535, "quote_line": 536, "scene_id": "S08", "in_scene_page": 1}, {"file": "five-aggregates/book/index.html", "line": 540, "quote_line": 541, "scene_id": "S08", "in_scene_page": 2}, {"file": "five-aggregates/book/index.html", "line": 545, "quote_line": 546, "scene_id": "S08", "in_scene_page": 3}, {"file": "five-aggregates/book/index.html", "line": 550, "quote_line": 532, "scene_id": "S08", "in_scene_page": 4}, {"file": "five-aggregates/book/index.html", "line": 555, "quote_line": 532, "scene_id": "S08", "in_scene_page": 5}, {"file": "five-aggregates/book/index.html", "line": 560, "quote_line": 532, "scene_id": "S08", "in_scene_page": 6}, {"file": "five-aggregates/book/index.html", "line": 565, "quote_line": 532, "scene_id": "S08", "in_scene_page": 7}, {"file": "five-aggregates/book/index.html", "line": 570, "quote_line": 532, "scene_id": "S08", "in_scene_page": 8}, {"file": "five-aggregates/book/index.html", "line": 624, "quote_line": 611, "scene_id": "S10", "in_scene_page": 3}, {"file": "five-aggregates/book/index.html", "line": 629, "quote_line": 611, "scene_id": "S10", "in_scene_page": 4}, {"file": "five-aggregates/book/index.html", "line": 634, "quote_line": 611, "scene_id": "S10", "in_scene_page": 5}, {"file": "five-aggregates/book/index.html", "line": 639, "quote_line": 611, "scene_id": "S10", "in_scene_page": 6}, {"file": "five-aggregates/book/index.html", "line": 644, "quote_line": 611, "scene_id": "S10", "in_scene_page": 7}, {"file": "five-aggregates/book/index.html", "line": 734, "quote_line": 734, "scene_id": "S14", "in_scene_page": 1}]

### F4-D04｜五陰｜五陰與五受陰差別在總結易淡化

分類：author_discussion；頁碼：[13, 52]；場景：['S06', 'S14', 'S15']。

口白（第13頁）：我們的身體，會被蚊子咬、被雨淋濕，會冷、會熱，也會生病。

口白（第14頁）：甚至連你喜歡的東西，也會被風吹走、摔壞、融化...

下方引文：觀自在菩薩。行深般若波羅蜜多時。
照見五蘊皆空。度一切苦厄。
舍利子。色不異空。空不異色。色即是空。空即是色。受想行識。亦復如是。
舍利子。是諸法空相。不生不滅。不垢不淨。不增不減。
是故空中無色。無受想行識。無眼耳鼻舌身意。無色聲香味觸法。無眼界。乃至無意識界。無無明。亦無無明盡。乃至無老死。亦無老死盡。無苦集滅道。無智亦無得。以無所得故。
菩提薩埵。依般若波羅蜜多故。心無罣礙。無罣礙故。無有恐怖。遠離顛倒夢想。究竟涅槃。
三世諸佛。依般若波羅蜜多故。得阿耨多羅三藐三菩提。
故知般若波羅蜜多。是大神咒。是大明咒。是無上咒。是無等等咒。能除一切苦。真實不虛。
故說般若波羅蜜多咒。即說咒曰。揭諦揭諦。波羅揭諦。波羅僧揭諦。菩提薩婆訶。

理由：把所有會變壞的東西直接稱色受陰、把一般物質與認知等同各受陰，可能淡化陰與有漏／被執取受陰的差別。現guide的SA55、58已分清。此為簡化精度，不把刻意心經五蘊對照判錯配。

建議：可在總結短句連接對身心現象的執取與束縛；保留五蘊／心經對讀，非必須整改。

原典對證：SA55：我今當說陰及受陰……若色是有漏、是取……受、想、行、識亦復如是，是名受陰。 / SA58：非五陰即受，亦非五陰異受；能於彼有欲貪者，是五受陰。

來源：https://suttacentral.net/sa55/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa55.html | https://suttacentral.net/sa58/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa58.html

檔案位置：[{"file": "five-aggregates/book/index.html", "line": 491, "quote_line": 488, "scene_id": "S06", "in_scene_page": 1}, {"file": "five-aggregates/book/index.html", "line": 496, "quote_line": 488, "scene_id": "S06", "in_scene_page": 2}, {"file": "five-aggregates/book/index.html", "line": 501, "quote_line": 488, "scene_id": "S06", "in_scene_page": 3}, {"file": "five-aggregates/book/index.html", "line": 506, "quote_line": 488, "scene_id": "S06", "in_scene_page": 4}, {"file": "five-aggregates/book/index.html", "line": 734, "quote_line": 734, "scene_id": "S14", "in_scene_page": 1}, {"file": "five-aggregates/book/index.html", "line": 753, "quote_line": 750, "scene_id": "S15", "in_scene_page": 1}]

### F4-D05｜六處｜六故事談五種患卻只節錄色患

分類：author_discussion；頁碼：[29, 91]；場景：['S03', 'S04', 'S05', 'S06', 'S07', 'S08']。

口白（第29頁）：但如果不能一直看下去，心就會開始煩躁，產生了「過患」。

口白（第30頁）：因為五受陰的色、受、想、行、識，都是無常、苦、變易。

下方引文：《雜阿含經》第 41 經
云何色患如實知？若色無常、苦、變易法，是名色患，如是色患如實知。

理由：六組經號皆SA41正確，非串頁。上方說色受想行識皆無常苦變易，下方卻只有色患，尤其回憶悲傷等心理經驗不如受想行識患直接。SA41五項均齊，後S10也已用完整五項。列作節錄範圍偏窄，非確定錯經號。

建議：可重用S10五項患，或心理經驗配相應受想行識患；由作者判斷是否保留代表性節錄。

原典對證：若色無常、苦、變易法，是名色患。 / 若受無常、苦、變易法，是名受患。 / 謂想無常、苦、變易法，是名想患。 / 若行無常、苦、變易法，是名行患。 / 若識無常、苦、變易法，是名識患。

來源：https://suttacentral.net/sa41/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa41.html

檔案位置：[{"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S03", "in_scene_page": 9}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S03", "in_scene_page": 10}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S03", "in_scene_page": 11}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S04", "in_scene_page": 11}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S04", "in_scene_page": 12}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S04", "in_scene_page": 13}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S04", "in_scene_page": 14}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S05", "in_scene_page": 8}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S05", "in_scene_page": 9}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S05", "in_scene_page": 10}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S05", "in_scene_page": 11}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S06", "in_scene_page": 8}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S06", "in_scene_page": 9}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S06", "in_scene_page": 10}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S06", "in_scene_page": 11}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S07", "in_scene_page": 10}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S07", "in_scene_page": 11}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S07", "in_scene_page": 12}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S07", "in_scene_page": 13}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S08", "in_scene_page": 9}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S08", "in_scene_page": 10}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S08", "in_scene_page": 11}]

### F4-D06｜六處｜不加喜歡討厭標籤的說明可澄清

分類：author_discussion；頁碼：[106, 110]；場景：['S14']。

口白（第106頁）：如果守護好我們的根門，

口白（第107頁）：遇到可愛的六境，不貪。遇到不可愛的六境，不瞋。

下方引文：《雜阿含經》第 245 經
有眼識色可愛、可念、可樂、可著，比丘見已，知喜不讚歎、不樂著堅實。
有眼識色不可愛、念、樂著，比丘見已，不瞋恚、嫌薄。

理由：SA245與護根完全相應，非錯配。原文知喜不讚歎仍知歡喜，重點是不隨貪著或瞋恚。沿前文想=貼標籤的教學，108頁可能被讀為停止辨認或消除樂受。

建議：可寫知道喜歡或不喜歡，但不跟著貪著或排斥；經文不必換，非必須整改。

原典對證：比丘見已，知喜不讚歎、不樂著堅實……比丘見已，不瞋恚、嫌薄。

來源：https://suttacentral.net/sa245/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa201-300/sa245.html

檔案位置：[{"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S14", "in_scene_page": 1}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S14", "in_scene_page": 2}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S14", "in_scene_page": 3}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S14", "in_scene_page": 4}, {"file": "six-senses/book/index.html", "line": 593, "quote_line": 593, "scene_id": "S14", "in_scene_page": 5}]

### TL-C01｜十二因緣｜滑手機例子的識、名色與所緣色境標名錯置

分類：confirmed_mismatch；頁碼：[44, 45]；場景：[11]。

口白（第44頁）：這就像你在滑手機：眼睛看到一張圖片（名色），心裡覺得「真有趣」（識）
前一刻的名色行為產生了前一刻的識。

口白（第45頁）：這個念頭推動手指往下滑（新的名色），又讓你看到了下一則內容（新的識）
我們的心就是這樣，抓著一個體驗，搖過下一個體驗。

下方引文：彼心、意、識日夜時刻，須臾轉變，異生、異滅。猶如獼猴遊林樹間，須臾處處，攀捉枝條，放一取一。彼心、意、識亦復如是，異生、異滅。

理由：「覺得真有趣」至少涉及樂受、想與意行，不能用括號直接等同識；一張圖片只是所緣色境，不是完整名色。289經只說心意識須臾轉變，並未建立前一刻名色行為產生前一刻識的機制。 「下一則內容」是新色境，並非新的識本身；指滑手機是身行的一個事例，也不等同整體新的名色。此例把所緣內容、名色與識交替標名，289經獼猴譬喻不能支持這個名相對照。

建議：修正名相括號，不必換掉289經。可改為看到圖片時生眼識；有趣屬感受、認想與意行；滑到的新圖片成為新的色境。

原典對證：彼心、意、識日夜時刻，須臾轉變，異生、異滅。猶如獼猴遊林樹間，須臾處處，攀捉枝條，放一取一。彼心、意、識亦復如是，異生、異滅。

來源：https://suttacentral.net/sa289/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa289.html | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa273.html | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa298.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 2134, "narration_line": 2147, "quote_line": 2152}, {"file": "twelve-links/book/book-data.js", "object_line": 2156, "narration_line": 2169, "quote_line": 2174}]

### TL-D01｜十二因緣｜有被寫成已定、不可逆轉的命運

分類：author_discussion；頁碼：[7, 12]；場景：[3, 4]。

口白（第7頁）：為什麼會有「生」呢？
原來，在出生之前，我們已經「懷」著一股強大的業力慣性，這就是「有」。

口白（第8頁）：就像種子已經熟透，只要因緣成熟，它必然會破土而出，變成一個新的生命。

下方引文：「何法有故生有？何法緣故生有？」即正思惟，起無間等，知：「有有故生有，有緣故生有。」

理由：「有緣生」經號正確；把有完全等同出生前已攜帶的強大業力慣性，是選擇性的三世譬喻。 種熟必生是有緣生的譬喻，但應保留條件可變、緣滅則滅的脈絡。 配三有定義正確；「寫好的生命預約單」及「想要擁有形體」易使三有成為預定命運與單純願望。 「不可逆轉」並非298經的三有定義，且285經另明說有滅故生滅；建議由作者改為因緣具足時的推動。 取緣有配對正確；「未來必須承受的命運」將條件性的緣起寫成必然宿命，宜與作者討論。

建議：保留三世譬喻，但將已寫好／不可逆轉／必須承受改成因緣具足時帶來後續生；補285經有滅故生滅。

原典對證：「何法有故生有？何法緣故生有？」即正思惟，起無間等，知：「有有故生有，有緣故生有。」 / 云何為有？三有－欲有、色有、無色有。 / 「何法有故有有？何法緣故有有？」即正思惟，如實無間等起，知：「取有故有有，取緣故有有。」

來源：https://suttacentral.net/sa285/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa285.html | https://suttacentral.net/sa298/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa298.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 1327, "narration_line": 1340, "quote_line": 1345}, {"file": "twelve-links/book/book-data.js", "object_line": 1349, "narration_line": 1362, "quote_line": 1366}, {"file": "twelve-links/book/book-data.js", "object_line": 1370, "narration_line": 1383, "quote_line": 1388}, {"file": "twelve-links/book/book-data.js", "object_line": 1392, "narration_line": 1405, "quote_line": 1410}, {"file": "twelve-links/book/book-data.js", "object_line": 1436, "narration_line": 1449, "quote_line": 1454}]

### TL-D02｜十二因緣｜戒取被縮成僵化習慣

分類：author_discussion；頁碼：[14, 14]；場景：[5]。

口白（第14頁）：抓取「我是對的」那份固執、抓取僵化的習慣，
還有「抓取」最難放下的那個「我」。

下方引文：云何為取？四取：欲取、見取、戒取、我取。

理由：欲取、見取、我取的白話相應；把戒取只說成僵化習慣，易漏掉執持戒禁儀式為清淨道的重點。

建議：可改成抓住某些規矩或儀式，認為只靠它們就能清淨解脫；避免把所有生活習慣一概當戒取。

原典對證：云何為取？四取：欲取、見取、戒取、我取。

來源：https://suttacentral.net/sa298/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa298.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 1480, "narration_line": 1493, "quote_line": 1498}]

### TL-D03｜十二因緣｜三愛的三項白話例子不能逐項對應所引三愛

分類：author_discussion；頁碼：[19, 19]；場景：[6]。

口白（第19頁）：我們渴求感官的快樂、渴求完美的自我，甚至渴求永恆的存在。
這種「想要更多」的衝動，讓我們上癮，不停地追逐下一杯。

下方引文：彼云何為愛？謂三愛。欲愛、色愛、無色愛。

理由：感官樂與欲愛相應，但「完美自我、永恆存在」不能逐項替代此引文的色愛、無色愛。

建議：若要教298經三愛，說明欲界、色界、無色界的貪著；若保留完美自我與永恆存在，標為渴愛的生活例子。

原典對證：彼云何為愛？謂三愛。欲愛、色愛、無色愛。

來源：https://suttacentral.net/sa298/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa298.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 1589, "narration_line": 1602, "quote_line": 1607}]

### TL-D04｜十二因緣｜受被一概寫成擾亂平靜

分類：author_discussion；頁碼：[24, 24]；場景：[7]。

口白（第24頁）：感受就像「射入眼睛的一隻箭」，是如此直接且無法迴避。
無論是快樂還是痛苦，都會驚擾我們內心的平靜。

下方引文：云何為受？謂三受。苦受、樂受、不苦不樂受。

理由：箭為生命之輪的圖像譬喻，無引錯經；但「無論快樂痛苦都會驚擾平靜」將受與煩惱混同，宜限定未受訓練的心。

建議：將無論快樂或痛苦都會驚擾，限定為心跟著感受抓取抗拒時；可參289經如實知受、292經明生後仍知身壽分齊受。

原典對證：云何為受？謂三受。苦受、樂受、不苦不樂受。

來源：https://suttacentral.net/sa298/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa298.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 1698, "narration_line": 1711, "quote_line": 1716}]

### TL-D05｜十二因緣｜觸的握手譬喻漏掉相應識

分類：author_discussion；頁碼：[27, 29]；場景：[8]。

口白（第27頁）：什麼是「觸」呢？它是生命與世界在握手。
當眼睛對上色彩、耳朵對上聲音、

口白（第28頁）：我們的手輕輕牽在一起，覺知的火花就在那一瞬間點燃了。
我們透過六種方式觸摸這個世界，就像兩隻手掌相擊，

下方引文：云何為觸？謂六觸身。眼觸身、耳觸身、鼻觸身、舌觸身、身觸身、意觸身。

理由：298經是六觸身，圖像握手譬喻可用；文字目前只有根境兩項，宜交代相應識參與。 「碰到世界才點燃覺知」易讓讀者以為觸先於識；此處所引298經只列六觸身，宜補根境識和合。 「存在的響聲」為觸的詩性譬喻，需接前頁根境識說明才不把觸說成生出存在。

建議：可加「感官、對象和相應的識相遇」；目前298經六觸身的節錄正確，不需改經號。

原典對證：云何為觸？謂六觸身。眼觸身、耳觸身、鼻觸身、舌觸身、身觸身、意觸身。

來源：https://suttacentral.net/sa298/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa298.html | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa273.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 1764, "narration_line": 1777, "quote_line": 1782}, {"file": "twelve-links/book/book-data.js", "object_line": 1786, "narration_line": 1799, "quote_line": 1804}, {"file": "twelve-links/book/book-data.js", "object_line": 1808, "narration_line": 1821, "quote_line": 1825}]

### TL-D06｜十二因緣｜識的能量譬喻與名色相依引文範圍

分類：author_discussion；頁碼：[40, 41]；場景：[10]。

口白（第40頁）：佛陀思考：是誰讓這場航行開始的？原來，是那股被稱為「識」的覺知能量。

口白（第41頁）：「識」與「名色」輾轉相依，就像「旋轉動力」和「水流」形成的漩渦。
當「識」不再執著這場航行，名色的沉重負擔，也就能在寧靜中放下了。

下方引文：思量名色何因、何集、何生、何觸？知彼名色識因、識集、識生、識觸。

理由：名色以識為因與292經相應；「覺知能量」易把識實體化為先在啟動者，宜改為依因緣生起的識。 識與名色相依有288經三蘆譬喻可證，但現配292經這一節僅明識緣名色；建議補288經，並避免識成為主動放下的實體。

建議：把覺知能量改成依條件生起的識；相依句可補288經三蘆展轉相依，避免誤稱292單節已明說雙向。

原典對證：思量名色何因、何集、何生、何觸？知彼名色識因、識集、識生、識觸。

來源：https://suttacentral.net/sa292/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa292.html | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa288.html | https://suttacentral.net/sa288/lzh/taisho

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 2047, "narration_line": 2060, "quote_line": 2064}, {"file": "twelve-links/book/book-data.js", "object_line": 2068, "narration_line": 2081, "quote_line": 2086}]

### TL-D07｜十二因緣｜識被稱為住在心裡的觀察者

分類：author_discussion；頁碼：[42, 42]；場景：[11]。

口白（第42頁）：什麼是「識」呢？它是住在我們心裡的觀察者。
透過眼睛、耳朵和身體，它讓我們知道世界是什麼樣子。

下方引文：云何為識？謂六識身——眼識身、耳識身、鼻識身、舌識身、身識身、意識身。

理由：298經定義為六識身；「住在心裡的觀察者」易指向內住不變主體，與後頁289經不可於識繫我我的語境有張力。

建議：改為「依眼耳等因緣而生、隨時變化的認識作用」；配合下一頁289經不可於識繫我我所。

原典對證：云何為識？謂六識身——眼識身、耳識身、鼻識身、舌識身、身識身、意識身。

來源：https://suttacentral.net/sa298/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa298.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 2090, "narration_line": 2103, "quote_line": 2108}]

### TL-D08｜十二因緣｜無所有行被泛化為追求平靜

分類：author_discussion；頁碼：[52, 52]；場景：[12]。

口白（第52頁）：甚至當我們追求平靜，捏塑出空靈的陶罐，也會生起相應的覺知。

下方引文：作諸福行，善識生；作諸不福不善行，不善識生；作無所有行，無所有識生

理由：292經無所有行、無所有識不是所有一般追求平靜的總稱；空靈陶罐可保留，但需作者交代此處與福行、不福行並列的專門用語，避免直接等同一般平靜。

建議：保留陶罐譬喻，交代此處與福行、不福行並列的專門用語；不把所有安靜或平靜都等同無所有行。平行SN12.51的āneñja（不動）可供作者另行比對，不直接限縮為無所有處定。

原典對證：作諸福行，善識生；作諸不福不善行，不善識生；作無所有行，無所有識生

來源：https://suttacentral.net/sa292/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa292.html | https://raw.githubusercontent.com/suttacentral/bilara-data/published/root/pli/ms/sutta/sn/sn12/sn12.51_root-pli-ms.json

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 2309, "narration_line": 2322, "quote_line": 2326}]

### TL-D09｜十二因緣｜不思量被讀成停念即可終結生死

分類：author_discussion；頁碼：[60, 64]；場景：[15]。

口白（第60頁）：由無明進入到明，我們已經看清了，接下來該怎麼做呢？
佛陀教我們一個最簡單也最難的秘訣：就是「別再加戲」了。

口白（第61頁）：我們的心很愛「加戲」，不停地回想過去、不停地幻想未來。
這些念頭就像是一個個黏人的鉤子，讓覺知緊緊地「住」在裡面。

下方引文：若思量、若妄想者，則有使攀緣識住；有攀緣識住故，入於名色；入名色故，有未來世生、老、病、死、憂、悲、惱、苦，如是純大苦聚集。

理由：360經談思量妄想、使攀緣識住；「別加戲」為可用譬喻，但必須保留煩惱使與攀緣條件。 回憶或計畫本身不必然等於360經導致未來苦聚的煩惱攀緣；宜限定被貪愛與我執取牽引的反覆想像。 名色與未來苦聚是360經原脈絡；「機器轉動」應避免使一切當下身心活動都成為應消除對象。 原經同時說無使、無攀緣識住，不能把不思量理解為單純停止思考即可解脫。 360經說無使無攀緣而苦聚滅；口白宜保留條件，避免一時寧靜等同生死永盡。

建議：將不思量限定為不再受煩惱使、貪愛執取驅動的攀緣；保留原經無使、無攀緣識住的條件，避免以壓抑思想為目標。

原典對證：若思量、若妄想者，則有使攀緣識住；有攀緣識住故，入於名色；入名色故，有未來世生、老、病、死、憂、悲、惱、苦，如是純大苦聚集。 / 若不思量、無妄想，無使、無攀緣識住；無攀緣識住故，不入名色，不入名色故，生、老、病、死、憂、悲、惱、苦滅，如是純大苦聚滅。

來源：https://suttacentral.net/sa360/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa301-400/sa360.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 2482, "narration_line": 2495, "quote_line": 2500}, {"file": "twelve-links/book/book-data.js", "object_line": 2504, "narration_line": 2517, "quote_line": 2522}, {"file": "twelve-links/book/book-data.js", "object_line": 2526, "narration_line": 2539, "quote_line": 2543}, {"file": "twelve-links/book/book-data.js", "object_line": 2547, "narration_line": 2560, "quote_line": 2565}, {"file": "twelve-links/book/book-data.js", "object_line": 2569, "narration_line": 2582, "quote_line": 2586}]

### TL-D10｜十二因緣｜明觸的條件被縮成喜惡或換語法

分類：author_discussion；頁碼：[66, 69]；場景：[16]。

口白（第66頁）：這就是「無明觸」，我們總是加上了「我喜歡」或「我討厭」的濾鏡，
結果把單純的感受，變成了心裡的熱惱與大火。

口白（第67頁）：現在，試著用「明觸」來面對吧！就像右邊這隻清涼的手。
當感受來臨時，只是輕輕地知道，

下方引文：多聞聖弟子於此六觸入處，捨離無明而生明，不生有覺、無覺、有無覺、勝覺、等覺、卑覺、我知我見覺。如是知、如是見已，先所起無明觸滅，後明觸覺起。

理由：45經的無明觸還包括五陰我見與有無勝等覺；「我喜歡討厭」只能作例子，不能作完整定義。 45經明觸以捨離無明、不起諸我見覺為條件；只輕輕知道是練習說明，宜交代無我正見。 將我感覺改成有感覺能提示去我執取，但單換用語不是45經捨離無明、不生我知我見覺的完整條件。

建議：加入不把五陰當我我所、捨離無明的正見條件；生活練習可與468經不貪樂不瞋苦並列。

原典對證：多聞聖弟子於此六觸入處，捨離無明而生明，不生有覺、無覺、有無覺、勝覺、等覺、卑覺、我知我見覺。如是知、如是見已，先所起無明觸滅，後明觸覺起。

來源：https://suttacentral.net/sa45/lzh/taisho | https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa1-100/sa45.html

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 2618, "narration_line": 2637, "quote_line": 2642}, {"file": "twelve-links/book/book-data.js", "object_line": 2646, "narration_line": 2665, "quote_line": 2670}, {"file": "twelve-links/book/book-data.js", "object_line": 2702, "narration_line": 2721, "quote_line": 2725}]

### TL-D11｜十二因緣｜心經明暗譬喻須區分無自性與未曾發生

分類：author_discussion；頁碼：[76, 76]；場景：[18]。

口白（第76頁）：當我們點亮了智慧的燈，「黑暗」就不曾真的存在過。
既然黑暗本來就不是實體，當然也就沒有所謂的「消滅黑暗」這回事。

下方引文：觀自在菩薩。行深般若波羅蜜多時。照見五蘊皆空。度一切苦厄。
舍利子。色不異空。空不異色。色即是空。空即是色。受想行識。亦復如是。
舍利子。是諸法空相。不生不滅。不垢不淨。不增不減。是故空中無色。無受想行識。無眼耳鼻舌身意。無色聲香味觸法。無眼界。乃至無意識界。無無明。亦無無明盡。乃至無老死。亦無老死盡。
無苦集滅道。無智亦無得。以無所得故。
菩提薩埵。依般若波羅蜜多故。心無罣礙。無罣礙故。無有恐怖。遠離顛倒夢想。究竟涅槃。
三世諸佛。依般若波羅蜜多故。得阿耨多羅三藐三菩提。
故知般若波羅蜜多。是大神咒。是大明咒。是無上咒。是無等等咒。能除一切苦。真實不虛。故說般若波羅蜜多咒。即說咒曰。
揭諦揭諦。波羅揭諦。波羅僧揭諦。菩提薩婆訶。

理由：心經空性可用明暗譬喻；「黑暗不曾真的存在」需區分無自性與緣起層面的無明仍待斷，屬作者詮釋討論，非跨經收尾錯誤。

建議：保留作者刻意的心經收尾；可把黑暗不曾真的存在改為黑暗不是不變實體，不把空性讀成從來沒有緣起無明或無須修道。

原典對證：無無明亦無無明盡，乃至無老死亦無老死盡；無苦、集、滅、道；無智，亦無得。

來源：https://cbetaonline.dila.edu.tw/zh/T0251 | https://raw.githubusercontent.com/cbeta-org/xml-p5/8ebac86d00719479db5777dc6cd77ba111c3067a/T/T08/T08n0251.xml

檔案位置：[{"file": "twelve-links/book/book-data.js", "object_line": 2883, "narration_line": 2889, "quote_line": 2894}]

## 完整覆蓋

前三本：四聖諦29頁11幕11配對；五陰54頁16幕39配對；六處115頁16幕46配對。十二因緣77頁19幕35配對。
每一頁原口白、引文、分類、理由、位置在JSON的books[].page_assessments；每一場景／引文組在books[].scene_quote_pairs。同一書內並非只抽關鍵字。

## 小異文與刻意對讀（不算錯配）

- four-truths：EA25.1所核大正藏與guide用正治，reader用正志；義同八道用字差異，不當錯經號。若逐字出版需另按底本校訂。
- four-truths：具壽憍陳如／有集法者悉皆有此滅法與莊譯凡任何集法都是滅法同段同義；reader未冒署莊譯，但中文原版尚未獨立辨認。
- five-aggregates：SA46部分節錄有不願／不顧、增是／法、虫蟲及標點展開等小異文，不混同43頁重複句的實質錯配。CSV54筆引文與runtime同字；口白僅54頁溫柔起點已依作者修訂刪溫柔。
- six-senses：273耳鼻舌身意句均明標依經意展開，原經末段也許六處類推，故不算錯配。
- six-senses：Ud1.10:8.2巴利四句與影片譯句相應，未冒署莊譯；SC固定中文小部目錄沒有Ud，404不是無此經，已核官方bilara正確vagga1路徑巴利／英譯。中文原譯者及音軌未核。
- first3：完整T251心經刻意對照五蘊／十二處／四諦；不因非主體阿含判錯。正文已核官方CBETA，咒語異體只作底本校勘。

## 官方來源與限制

前三本下載receipt：/tmp/sutra-audit-sources-first4/receipt.json；固定版本SC c7bba0f184e66904949d4918587975fb7fd7ec69、CBETA 6952edb0bca6b86a68c409b36e8be659a8a75e2b、bilara baa73bb5dae8a99d71073a3f7370bfd22de633e2。十二因緣獨立固定版與10份receipt見/tmp/sutra-twelve-source-info.json及合併JSON。

- 未另找到四聖諦／六處獨立原始作者分鏡包，以現有資料、guide與原典全文審查；五陰CSV是同庫證據，不假稱獨立手稿。
- 未逐字精聽影片與校時間碼。本次內容語意與資料配對稽核。
- Buddhaspace／莊站直連CONNECT403，以官方固定commit正文替代；SC網站200可僅SPA殼，不冒稱已驗正文呈現。
- 小異文、漢譯標點、不同譯本用語另記，不自動判錯經號；影片中文獨立譯者部分未辨明。
- 只寫/tmp，未改runtime、原稿、圖片、資料，未提交或發布。
