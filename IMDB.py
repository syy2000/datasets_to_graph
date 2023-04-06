"""
    电影数据
    title开头的是电影（可能视频更为合适）
    name开头的是人员
    \N 是为空或者缺失

    node:
    label 0->视频 1->人员

    edge:
    label 1e8+->category 2e8+->job 3e8+->characters 4e8->电影内的director和writer信息
    方向：人员->视频
    请注意4e8+和前面事实上是有一定重复的。1e8-3e8部分是由solve_edge处理，4e8部分是由solve_edge2处理，可以自行修改。
"""
"""
    注意：该代码16G内存可能无法运行
"""
"""
    请先按照以下路径建立文件夹
    ./out/IMDB/kv
    请将out_node_and_edge_id.py放在同一目录下
"""
import time
import out_node_and_edge_id as out_trans


def log(s):
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime + "\t" + s)


in_path = "./IMDB/"
in_title_files = [
    "title.akas.tsv",
    "title.basics.tsv",
    "title.episode.tsv",
    "title.ratings.tsv",
]
in_people_file = "name.basics.tsv"
in_edge_file = in_path + "title.principals.tsv"
in_edge_file2 = in_path + "title.crew.tsv",

out_edge_file = "./out/IMDB/edge.txt"
out_node_file = "./out/IMDB/node.txt"
out_kv_dict = "./out/IMDB/kv/"
out_attr_file = "./out/IMDB/attr.txt"

array_keys_without_sorted = [
    "attributes",
    "genres",
    "directors",
    "writers",
    "primaryProfession",
    "knownForTitles"
]

array_keys_split_by_blank_without_sorted = [
    "types",
]


class Node:
    def __init__(self):
        self.id = -1
        # int
        self.label = -1
        # int[]
        self.attr = {}


class Edge:
    def __init__(self):
        self.id = -1
        self.u = -1
        self.v = -1
        self.label = -1


# id:int -> Node
nodes = {}
# id:int -> Edge
edges = {}

# map<label,map<attr,map<attr_val,key>>>
# [label][attr][attr_val]=attr_key
attr_value_vk = {}
all_value_vk = 0
# 这里是事后补救的，将attr->int以便输出，很丑陋建议修改
attr_key_vk = {}
# 现在又补救了一条，更丑了 (int,attr) 记得排序
attr_key_k_list = []

node_val_key = {}

# items: val->key
edges_label_val_key = []
edge_label_bases = [int(1e8), int(2e8), int(3e8), int(4e8)]

now_attr = []
now_len = 0


def split_array(l, attr):
    res = []
    if attr in array_keys_without_sorted:
        res = [i.strip() for i in l.split(',')]
    elif attr in array_keys_split_by_blank_without_sorted:
        res = [i.strip() for i in l.split(' ')]
    else:
        return l
    # res.sort()
    return res


def attr_value_kv_trans(l, label):
    global node_val_key, nodes, attr_value_vk, now_attr, now_len, all_value_vk
    id_v = l[0]
    id = -1
    if id_v not in node_val_key:
        id = len(node_val_key)
        node_val_key[id_v] = id
    else:
        id = node_val_key[id_v]
    assert id == node_val_key[id_v]
    if id not in nodes:
        nodes[id] = Node()
        nodes[id].id = id
        nodes[id].label = label

    for i in range(now_len):
        if i == 0:
            continue
        # attr_value_v = split_array(l[i], now_attr[i])
        attr_value_v = l[i]
        if attr_value_v not in attr_value_vk[label][now_attr[i]]:
            attr_value_vk[label][now_attr[i]][attr_value_v] = all_value_vk
            all_value_vk += 1
        attr_value_k = attr_value_vk[label][now_attr[i]][attr_value_v]
        assert (now_attr[i] not in nodes[id].attr, now_attr[i]) or (nodes[id].attr[now_attr[i]] == attr_value_k)
        nodes[id].attr[now_attr[i]] = attr_value_k


def solve_node(file, label):
    global now_attr, now_len, attr_value_vk, attr_key_vk
    with open(file, "r", encoding="utf-8") as f:
        log("打开 " + file + " 中...")
        cnt = 0
        for line in f.readlines():
            cnt += 1
            l = line.strip().split('\t')
            l = [i.strip() for i in l]
            if cnt == 1:
                now_attr = l
                now_len = len(now_attr)
                for i in range(now_len):
                    if i == 0 and now_attr[i] == "tconst":
                        continue
                    assert now_attr[i] not in attr_value_vk[label]
                    assert now_attr[i] not in attr_key_vk

                    attr_value_vk[label][now_attr[i]] = {}
                    if now_attr[i] not in attr_key_vk:
                        temp = len(attr_key_vk)
                        attr_key_vk[now_attr[i]] = temp
                        attr_key_k_list.append((temp, now_attr[i]))
                continue
            attr_value_kv_trans(l, label)
    log(file + " 处理完毕")


def add_node(id_v, label):
    global node_val_key, nodes
    if id_v not in node_val_key:
        id = len(node_val_key)
        node_val_key[id_v] = id
    else:
        id = node_val_key[id_v]
    assert id == node_val_key[id_v]
    if id not in nodes:
        nodes[id] = Node()
        nodes[id].id = id
        nodes[id].label = label


def solve_edge(file):
    with open(file, "r", encoding="utf-8") as f:
        log("打开 " + file + " 中...")
        cnt = 0
        for line in f.readlines():
            cnt += 1
            l = line.strip().split('\t')
            l = [i.strip() for i in l]
            if cnt == 1:
                continue
            u_v = l[2]
            v_v = l[0]
            if u_v not in node_val_key:
                add_node(u_v, 1)
            if v_v not in node_val_key:
                add_node(v_v, 0)
            # assert u_v in node_val_key
            # assert v_v in node_val_key
            u = node_val_key[u_v]
            v = node_val_key[v_v]
            for i in range(3):
                if l[3 + i] == "\\N":
                    continue
                label_v = l[3 + i]
                if label_v not in edges_label_val_key[i]:
                    temp = len(edges_label_val_key[i])
                    edges_label_val_key[i][label_v] = temp + edge_label_bases[i]
                label_k = edges_label_val_key[i][label_v]
                edge_id = len(edges)
                edges[edge_id] = Edge()
                edges[edge_id].id = edges[edge_id]
                edges[edge_id].u = u
                edges[edge_id].v = v
                edges[edge_id].label = label_k
            if cnt % 10000 == 0:
                log(str(cnt) + " 行处理完毕")
    log(file + " 处理完毕")


def solve_edge2(file):
    with open(file, "r", encoding="utf-8") as f:
        log("打开 " + file + " 中...")
        cnt = 0
        for line in f.readlines():
            cnt += 1
            l = line.strip().split('\t')
            l = [i.strip() for i in l]
            if cnt == 1:
                continue
            for j in range(2):
                s = l[j + 1].split(",")
                for u_v in s:
                    v_v = l[0]
                    if u_v == "\\N":
                        continue
                    if u_v not in node_val_key:
                        add_node(u_v, 1)
                    if v_v not in node_val_key:
                        add_node(v_v, 0)
                    # assert u_v in node_val_key
                    # assert v_v in node_val_key
                    u = node_val_key[u_v]
                    v = node_val_key[v_v]
                    i = 3
                    label_v = "director"
                    if j == 0:
                        label_v = "director"
                    else:
                        label_v = "writer"
                    if label_v not in edges_label_val_key[i]:
                        temp = len(edges_label_val_key[i])
                        edges_label_val_key[i][label_v] = temp + edge_label_bases[i]
                    label_k = edges_label_val_key[i][label_v]
                    edge_id = len(edges)
                    edges[edge_id] = Edge()
                    edges[edge_id].id = edges[edge_id]
                    edges[edge_id].u = u
                    edges[edge_id].v = v
                    edges[edge_id].label = label_k
    log(file + " 处理完毕")


if __name__ == '__main__':
    attr_value_vk[0] = {}
    attr_value_vk[1] = {}
    edges_label_val_key.append({})
    edges_label_val_key.append({})
    edges_label_val_key.append({})
    edges_label_val_key.append({})
    for file in in_title_files:
        solve_node(in_path + file, 0)
    solve_node(in_path + in_people_file, 1)

    solve_edge(in_edge_file)
    solve_edge2(in_edge_file2)

    log("数据集合计")
    log("顶点数量 " + str(len(nodes)))
    log("边的数量 " + str(len(edges)))
    log("属性数量 " + str(len(attr_key_vk)))

    attr_key_k_list.sort()
    log("输出 " + out_node_file + " 中...")
    with open(out_node_file, "w+", encoding="utf-8") as f:
        nodes_len = len(nodes)
        f.write(str(nodes_len) + "\n")

        for id, node in nodes.items():
            f.write(out_trans.insert_get_str_id_node(node.id) + "\t" + str(node.label) + "\n")

            # attr
            f.write(str(len(node.attr)) + "\n")
            assert len(node.attr) == len(attr_key_k_list)
            # for k, v in node.attr.items():
            #     f.write(str(attr_key_vk[k]) + "\t" + str(v) + "\n")
            for k_id, k in attr_key_k_list:
                f.write(str(k_id) + "\t" + str(node.attr[k]) + "\n")
    log("输出 " + out_node_file + " 完成")

    log("输出 " + out_edge_file + " 中...")
    with open(out_edge_file, "w+", encoding="utf-8") as f:
        edges_len = len(edges)
        f.write(str(edges_len) + "\n")

        for i, e in edges.items():
            f.write(out_trans.insert_get_str_id_node(e.u) + "\t" +
                    out_trans.insert_get_str_id_node(e.v) + "\t" +
                    str(e.label) + "\t" +
                    out_trans.insert_get_str_id_edge(i) + "\n")
    log("输出 " + out_edge_file + " 完成")

    log("输出 " + out_attr_file + " 中...")
    with open(out_attr_file, "w+", encoding="utf-8") as f:
        f.write(str(len(attr_key_vk)) + "\n")
        for v, k in attr_key_vk.items():
            f.write(str(k) + "\t" + str(v) + "\n")
    log("输出 " + out_attr_file + " 完成")

    log("输出 " + out_kv_dict + " 中...")
    for label, attr_all in attr_value_vk.items():
        for attr_key, attr_val_all in attr_all.items():
            with open(out_kv_dict + attr_key + ".txt", "w+", encoding="utf-8") as f:
                log("输出 " + out_kv_dict + attr_key + " 中...")
                f.write(str(len(attr_val_all)) + "\n")
                for v, k in attr_val_all.items():
                    f.write(str(k) + "\t" + str(v) + "\n")
            log("输出 " + out_kv_dict + attr_key + " 完成")

    log("输出 " + out_kv_dict + " 完成")
