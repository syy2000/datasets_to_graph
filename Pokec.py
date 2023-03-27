"""
    该图是facebook的社交网络图
    朋友关系是单向的

    node label 0 -> 社交网络账号
    edge label 0 -> 朋友关系

    null为空或者缺失，这里没有做特殊处理
    \t分隔
"""
"""
    kv文件格式如下
    该属性下的总数量n
    n行，每行为int类型的key值，即存储在node.txt中的值，和str类型的value值，即原本的真实值，使用\t分割
    
    例如
    2
    0 你好
    1 再见
"""
"""
    请先按照以下路径建立文件夹
    ./out/Pokec/kv
"""
import time


def log(s):
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime + "\t" + s)

# 如无特殊说明，以下均是完整路径
in_edge_file = "./Pokec/soc-pokec-relationships.txt"
in_node_file = "./Pokec/soc-pokec-profiles.txt"

out_edge_file = "./out/Pokec/edge.txt"
out_node_file = "./out/Pokec/node.txt"
# 请提供文件夹路径，并最后以/结尾
out_kv_dict = "./out/Pokec/kv/"
out_attr_file = "./out/Pokec/attr.txt"

# 不含user_id
attr_key = ["public",
            "completion_percentage",
            "gender",
            "region",
            "last_login",
            "registration",
            "AGE",
            "body",
            "I_am_working_in_field",
            "spoken_languages",
            "hobbies",
            "I_most_enjoy_good_food",
            "pets",
            "body_type",
            "my_eyesight",
            "eye_color",
            "hair_color",
            "hair_type",
            "completed_level_of_education",
            "favourite_color",
            "relation_to_smoking",
            "relation_to_alcohol",
            "sign_in_zodiac",
            "on_pokec_i_am_looking_for",
            "love_is_for_me",
            "relation_to_casual_sex",
            "my_partner_should_be",
            "marital_status",
            "children",
            "relation_to_children",
            "I_like_movies",
            "I_like_watching_movie",
            "I_like_music",
            "I_mostly_like_listening_to_music",
            "the_idea_of_good_evening",
            "I_like_specialties_from_kitchen",
            "fun",
            "I_am_going_to_concerts",
            "my_active_sports",
            "my_passive_sports",
            "profession",
            "I_like_books",
            "life_style",
            "music",
            "cars",
            "politics",
            "relationships",
            "art_culture",
            "hobbies_interests",
            "science_technologies",
            "computers_internet",
            "education",
            "sport",
            "movies",
            "travelling",
            "health",
            "companies_brands",
            "more",
            ]

# id:int -> attr:int[]
nodes = {}
# (u:int,v:int)
edges = []
attr_len = len(attr_key)

# item: {}，即attr:str -> key:int
attr_value_vk = []


def attr_value_kv_init():
    global attr_value_vk, attr_len
    for i in range(attr_len):
        attr_value_vk.append({})


def attr_value_kv_trans(value_list):
    global attr_value_vk, attr_len
    res_val_k = []
    for i in range(attr_len):
        val_v = value_list[i].strip()
        if val_v in attr_value_vk[i]:
            res_val_k.append(attr_value_vk[i][val_v])
        else:
            val_k = len(attr_value_vk[i])
            attr_value_vk[i][val_v] = val_k
            res_val_k.append(val_k)
    return res_val_k


if __name__ == '__main__':
    attr_value_kv_init()

    log("打开 " + in_node_file + " 中...")
    with open(in_node_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            l = line.strip()
            attr_all = l.split('\t')
            assert len(attr_all) - 1 == attr_len, l + " 实际属性值过少，为" + str(len(attr_all))

            attr_val = attr_all[1:]
            attr_val = attr_value_kv_trans(attr_val)
            nodes[int(attr_all[0])] = attr_val

    log(in_node_file + " 处理完毕！")
    log("打开 " + in_edge_file + " 中...")
    with open(in_edge_file, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            l = line.strip()
            edge = line.split('\t')
            assert len(edge) == 2, l + " 边的顶点不是两个"
            u, v = int(edge[0]), int(edge[1])
            assert u in nodes, l + " " + str(u) + " 不在顶点集合中"
            assert v in nodes, l + " " + str(v) + " 不在顶点集合中"
            edges.append((u, v))

    log(in_edge_file + " 处理完毕！")

    log("数据集合计")
    log("顶点数量 " + str(len(nodes)))
    log("边的数量 " + str(len(edges)))

    log("正在输出...")
    log("输出 " + out_node_file)
    with open(out_node_file, "w+", encoding="utf-8") as f:
        nodes_len = len(nodes)
        f.write(str(nodes_len) + "\n")

        for id, attr_val_k_list in nodes.items():
            f.write(str(id) + "\t" + "0" + "\n")

            # attr
            f.write(str(len(attr_val_k_list)) + "\n")
            for i in range(len(attr_val_k_list)):
                f.write(str(i) + "\t" + str(attr_val_k_list[i]) + "\n")

    log("输出 " + out_edge_file)
    with open(out_edge_file, "w+", encoding="utf-8") as f:
        edges_len = len(edges)
        f.write(str(edges_len) + "\n")

        for i in range(edges_len):
            e = edges[i]
            f.write(str(e[0]) + "\t" + str(e[1]) + "\t" + "0" + "\t" + str(i) + "\n")

    log("输出 " + out_attr_file)
    with open(out_attr_file, "w+", encoding="utf-8") as f:
        attr_len = len(attr_key)
        f.write(str(attr_len) + "\n")

        for i in range(attr_len):
            f.write(str(i) + "\t" + attr_key[i] + "\n")

    log("输出 " + out_kv_dict)
    for i in range(attr_len):
        now_vk = attr_value_vk[i]
        now_attr = attr_key[i]
        now_vk_len = len(now_vk)

        log("输出 " + out_kv_dict + now_attr + ".txt")
        with open(out_kv_dict + now_attr + ".txt", "w+", encoding="utf-8") as f:
            f.write(str(now_vk_len) + "\n")

            for v, k in now_vk.items():
                f.write(str(k) + "\t" + str(v) + "\n")
