import pysolr, os, sys

solr = pysolr.Solr("http://localhost:8983/solr/daizhige/", timeout=10)
root_dir ="../daizhige-data/艺藏"
current_count = 0
current_id = 0
maps_to_post = []

for root, subdirs, files in os.walk(os.path.abspath(root_dir)):
    for file in files:
        print(os.path.relpath(os.path.join(root, file), root_dir))
        abs_path = os.path.join(root, file)
        rel_path = os.path.relpath(abs_path, root_dir)
        categories = rel_path.split("/")[0:-1]
        with open(os.path.join(root, file), "r") as data:
            article = data.readlines()

        if current_count == 100:
            solr.add(maps_to_post)
            maps_to_post = []
            current_count = 0
        else:
            maps_to_post.append(
                {
                    "id": str(current_id),
                    "name": file.split(".")[0],
                    "article": article,
                    "chapter": 1,
                    "categories": categories
                }
            )
            current_count += 1
            current_id += 1


# solr.add([
#     {
#         "id": "1",
#         "name": "菩萨五法忏悔文",
#         "article": """
#         菩萨五法忏悔文一卷
#
#
# 大乘律
# 菩萨五法忏悔文一卷
# 失译师名开元附梁录
#
#
# 　　
#
# 菩萨五法忏悔文
# 　　十方三世佛。五眼照世间。三大无不知。明见罪福相。弟子某甲等。从无数劫来。不遇善知识。造作一切罪。破戒犯四重。六重及八重。谤法断善根。具足一阐提。幸遇诸如来。经法贤圣众。能除众罪者。弟子头面礼。愿诸恶云消。令发无上慧>。忏悔竟五体作礼。
# 　　十方诸佛始登道场。观树经行未转法轮。无明老死长衰可悲。愿设法药救诸疾苦。法雨流布枯槁众生。得道明了。十方现在佛。已度有缘者。众生多懈怠。方便现泥洹。弟子诚心礼。请佛令久住。一切诸菩萨。已发无上意。愿勤加精进。于无佛>世界。现成等正觉。普度诸群生。慈哀无过佛。是故至心请。请佛已竟头面作礼。
# 　　历世怀妒嫉。我慢及恚痴。见人得利如箭射心。闻人得乐如钉入眼。坐此诸罪障。堕落三恶道。常不遇诸佛。今日一心悟。发大随喜心。十方三世佛。及彼弟子众。其数无有量。从初发一念。乃至坐道场。四等大布施。清净持禁戒。定慧及解脱>。无量诸知见。弟子悉随喜。慧心朗然明。愚痴暗障灭。一念发随喜。功德满十方。智慧如诸佛。随喜已竟五体作礼。
# 　　往返生死中。从生故至死。从贵故还贱。惟未得泥洹。法身常清净。波若妙解脱。今当求此利。所可有福业。一切皆和合。回以施众生。共成无上道。广大如虚空。无相如真智。究竟尽法界。金刚空慧常现在前。无行神通有感必应。回向已竟头>面作礼。
# 　　诚心发大愿。行道如誓愿。慧心如猛风。定力如金刚。于此回向后。念念转慈悲。舍离爱着想。欢喜度一切。舍去身命时。佛放光明灭除一切难障。化生兜率天。面睹慈氏尊。修相尽具足。六根普聪彻。闻佛说妙法。即悟无生忍。皆住不退地。>乘大神通力周游十方国。供养一切佛。无量妙音声。赞叹佛功德。二十五有中。无时不现身。如日照世界。光明朗十方。一切幽闇处。皆为作灯明。虽得佛道转法轮现泥洹。众生不尽成佛不舍。普贤文殊愿。发愿已竟洗心作礼。
#
# """,
#         "chapter": 1,
#         "categories": ["佛藏", "乾隆藏", "大乘律"]
#     }
# ])