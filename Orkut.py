"""
    该数据集合提供了社区、top5000社区、全部关系的无向图
    这里仅仅使用了全部关系的无向图
    有需求可自行选择社区进行生成

    数据使用\t分割，社区的每一行都是一个社区，每一个都是一个数据
"""
"""
    node label:
        0 -> 社交账户
    edge label:
        0 -> 社交关系
"""
"""
    请先按照以下路径建立文件夹
    ./out/Orkut
"""
import time

in_edge_file = "./Orkut/com-orkut.ungraph.txt"

out_node_file = "./out/Orkut/node.txt"
out_edge_file = "./out/Orkut/edge.txt"


def log(s):
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime + "\t" + s)


nodes = {}
edges = {}


def find_and_insert(u):
    if u not in nodes:
        temp = len(nodes)
        nodes[u] = temp
    return nodes[u]


def solve(file):
    cnt = 0
    with open(file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            cnt += 1
            if cnt <= 4:
                # 前4行是说明，跳过
                log("跳过 " + line)
                continue
            l = line.strip()
            l = [i.strip() for i in l.split()]
            u = int(l[0])
            v = int(l[1])
            u = find_and_insert(u)
            v = find_and_insert(v)
            edge_len = len(edges)
            edges[edge_len] = (u, v, 0)
            edges[edge_len + 1] = (v, u, 0)
            if cnt % 10000 == 0:
                log(str(cnt/10000) + " 万行处理完毕")


if __name__ == '__main__':
    log("打开 " + in_edge_file + " 中...")
    solve(in_edge_file)
    log(in_edge_file + " 处理完毕")

    log("数据集合计")
    log("顶点数量 " + str(len(nodes)))
    log("边的数量 " + str(len(edges)))

    log("输出 " + out_node_file + "中...")
    with open(out_node_file, "w+", encoding="utf-8") as f:
        nodes_len = len(nodes)
        f.write(str(nodes_len) + "\n")

        for v, id in nodes.items():
            f.write(str(id) + "\t" + "0" + "\n")
            f.write("0" + "\n")
    log("输出 " + out_node_file + "完成")

    log("输出 " + out_edge_file + "中...")
    with open(out_edge_file, "w+", encoding="utf-8") as f:
        edges_len = len(edges)
        f.write(str(edges_len) + "\n")

        for id, e in edges.items():
            f.write(str(e[0]) + "\t" + str(e[1]) + "\t" + str(e[2]) + "\t" + str(id) + "\n")
    log("输出 " + out_edge_file + "完成")
