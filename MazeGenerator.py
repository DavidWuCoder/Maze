import random
from collections import deque
from LinkedStack import Node, LinkedStack

# 边缘类，用于存储两个顶点及其权重
class Edge:
    def __init__(self, u, v, w):
        self.u = u  # 边的第一个顶点
        self.v = v  # 边的第二个顶点
        self.w = w  # 边的中点（是要打通的墙， 也可以没有这个变量）

# 并查集类，用于处理连通性问题
class UnionFind:
    def __init__(self, n):
        self.n = n  # 元素数量
        self.parent = list(range(n))  # 每个元素的父节点，初始化为自己

    def find(self, u):
        # 查找元素u所在的集合的根
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # 路径压缩
        return self.parent[u]

    def union(self, u, v):
        # 将元素u和v所在的集合合并
        pu = self.find(u)
        pv = self.find(v)
        self.parent[pu] = pv  # 将u的根连接到v的根

# 迷宫生成器类
class MazeGenerator:
    def __init__(self, n, m):
        self.n = n  # 迷宫的高度
        self.m = m  # 迷宫的宽度
        self.grid = [[0] * m for _ in range(n)]  # 迷宫网格
        self.edges = []  # 迷宫中的边
        self.uf = UnionFind(n * m)  # 并查集实例

    # 添加一条边到edges列表
    def add_edge(self, u, v, w):
        self.edges.append(Edge(u, v, w))

    # 改变迷宫的大小
    def resize(self, n, m):
        self.n = n
        self.m = m
        self.grid = [[0] * m for _ in range(n)]

    # 生成迷宫
    def generate(self):
        # 初始化迷宫边界
        for i in range(self.n):
            for j in range(self.m):
                if i == 0 or i == self.n - 1 or j == 0 or j == self.m - 1:
                    self.grid[i][j] = 2  # 设置边界墙
                else:
                    if i % 2 == 0:
                        self.grid[i][j] = 1  # 设置内部墙
                    else:
                        if j % 2 == 0:
                            self.grid[i][j] = 1  # 设置内部墙
        self.edges = []  # 清空之前的边
        # 创建迷宫内部的所有可能的边
        for i in range(self.n):
            for j in range(self.m):
                if i == 0 or i == self.n - 1 or j == 0 or j == self.m - 1:
                    continue  # 忽略边界
                if i % 2 == 0 and j % 2 == 1:
                    self.add_edge((i - 1) * self.m + j, (i + 1) * self.m + j, i * self.m + j)
                if i % 2 == 1 and j % 2 == 0:
                    self.add_edge(i * self.m + j - 1, i * self.m + j + 1, i * self.m + j)
        # 打乱边的顺序
        r = random.Random()
        r.shuffle(self.edges)
        uf = UnionFind(self.n * self.m)
        # 对每条边进行处理，如果它们不在同一个集合，则合并
        for e in self.edges:
            if self.grid[e.u // self.m][e.u % self.m] == 0:
                if uf.find(e.u) != uf.find(e.v):
                    uf.union(e.u, e.v)
                    uf.union(e.u, e.w)
                    self.grid[e.w // self.m][e.w % self.m] = 0

    # 输出路径
    def PathPrint(self, st, canvas, cell_size=10, ex=0, ey=0, ans=""):
        head = st.top
        my_stack = LinkedStack()
        cnt = 0
        while head is not None:
            my_stack.push(Node(head.x, head.y))
            head = head.next
        while not my_stack.is_empty():
            node = my_stack.pop()
            canvas.create_rectangle(node.y * cell_size, node.x * cell_size,
                                    (node.y + 1) * cell_size, (node.x + 1) * cell_size,
                                    fill='yellow', outline='black')
            ans += f"-> ({node.x}, {node.y})"
            cnt += 1
            if cnt == 10:
                ans += "\n"
                cnt = 0
        canvas.create_rectangle(ey * cell_size, ex * cell_size,
                                (ey + 1) * cell_size, (ex + 1) * cell_size,
                                fill='yellow', outline='black')
        return ans

    # 非递归实现的深度优先搜索
    def dfs(self, x, y, ex, ey, canvas, cell_size=10):
        ans = ""
        stack = LinkedStack()
        stack.push(Node(x, y))
        visited = [[False] * self.m for _ in range(self.n)]
        dx = [0, 0, -1, 1]
        dy = [-1, 1, 0, 0]
        flag = 0
        count = 1
        visited[x][y] = True
        while not stack.is_empty():
            node = stack.top
            if node.x == ex and node.y == ey:
                flag = 1
                node.direction = 4
                ans += f"第{count}条路径如下：\n"
                ans = self.PathPrint(stack, canvas, cell_size, ex, ey, ans)
                count += 1
            find = False
            while node.direction < 4:
                node.direction += 1
                nx = node.x + dx[node.direction - 1]
                ny = node.y + dy[node.direction - 1]
                if 0 <= nx < self.n and 0 <= ny < self.m and not visited[nx][ny] and self.grid[nx][ny] == 0:
                    stack.push(Node(nx, ny))
                    visited[nx][ny] = True
                    find = True
                    break
            if not find:
                visited[node.x][node.y] = False
                stack.pop()
        return ans

    # 广度优先搜索
    def bfs(self, x, y, ex, ey, canvas, cell_size=10):
        ans = ""
        queue = deque([(x, y)])
        visited = [[False] * self.m for _ in range(self.n)]
        prev = [[None] * self.m for _ in range(self.n)]
        dx = [0, 0, -1, 1]
        dy = [-1, 1, 0, 0]
        while queue:
            x, y = queue.popleft()
            if x == ex and y == ey:
                break
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 <= nx < self.n and 0 <= ny < self.m and not visited[nx][ny] and self.grid[nx][ny] == 0:
                    queue.append((nx, ny))
                    prev[nx][ny] = (x, y)
                    visited[nx][ny] = True
        ans += "最短路径如下：\n"
        x, y = ex, ey
        path = []
        while x != 1 or y != 1:
            path.append((x, y))
            x, y = prev[x][y]
        path.reverse()
        cnt = 0
        for i in path:
            ans += f"-> ({i[0]}, {i[1]})"
            cnt += 1
            if cnt == 10:
                ans += "\n"
                cnt = 0
            canvas.create_rectangle(i[1] * cell_size + 4, i[0] * cell_size + 4,
                                    (i[1] + 1) * cell_size - 4, (i[0] + 1) * cell_size - 4,
                                    fill='purple', outline='black')
        return ans

if __name__ == '__main__':
    n = 11
    m = 11
    mg = MazeGenerator(n, m)
    mg.grid = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2],
        [2, 1, 1, 0, 1, 1, 1, 0, 1, 0, 2],
        [2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2],
        [2, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2],
        [2, 0, 1, 0, 0, 0, 0, 0, 1, 0, 2],
        [2, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2],
        [2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2],
        [2, 1, 1, 0, 1, 0, 1, 0, 1, 0, 2],
        [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ]
    # 调用dfs和bfs方法并打印结果
    mg.dfs(1, 1, n-2, m-2, None)
    mg.bfs(1, 1, n-2, m-2, None)
    # 打印迷宫
    for i in range(0, n):
        for j in range(m):
            print(mg.grid[i][j], end=' ')
        print()