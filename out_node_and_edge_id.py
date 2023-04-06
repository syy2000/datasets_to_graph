# 修改node和edge的id从0还是从1开始再这里改
offset = 0

# int -> int
node_id_trans_inorder = {}
# int -> int
edge_id_trans_inorder = {}


# int -> str
# 多次插入不会影响
def insert_get_str_id_node(id):
    global node_id_trans_inorder, edge_id_trans_inorder, offset
    id = int(id)
    if id in node_id_trans_inorder:
        return str(node_id_trans_inorder[id])
    l = len(node_id_trans_inorder)
    node_id_trans_inorder[id] = l + offset
    return str(node_id_trans_inorder[id])


def insert_get_str_id_edge(id):
    global node_id_trans_inorder, edge_id_trans_inorder, offset
    id = int(id)
    if id in edge_id_trans_inorder:
        return str(edge_id_trans_inorder[id])
    l = len(edge_id_trans_inorder)
    edge_id_trans_inorder[id] = l + offset
    return str(edge_id_trans_inorder[id])
