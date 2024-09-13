# 定义一个节点类Node，用于链式结构中的每个元素
class Node:
    def __init__(self, x, y, d=0):
        # 初始化节点的数据成员
        self.x = x  # 节点的x坐标
        self.y = y  # 节点的y坐标
        self.direction = d  # 节点的方向信息，默认为0
        self.next = None  # 指向下一个节点的引用，初始化为None

# 定义一个基于链表实现的栈类LinkedStack
class LinkedStack:
    def __init__(self):
        # 初始化栈顶指针为None，栈为空
        self.top = None
        # 初始化栈的大小为0
        self.size = 0

    def push(self, node):
        # 向栈中添加新节点
        new_node = node  # 将传入的节点赋值给new_node
        # 新节点的next指向当前栈顶
        new_node.next = self.top
        # 更新栈顶指针为新的节点
        self.top = new_node
        # 栈的大小加1
        self.size += 1

    def pop(self):
        # 从栈顶移除一个节点并返回其值
        if self.is_empty():  # 如果栈为空，则抛出异常
            raise Exception("Stack is empty")
        # 创建一个新的Node对象，将栈顶节点的值复制给它
        popped_value = Node(self.top.x, self.top.y)
        # 移动栈顶指针到下一个节点
        self.top = self.top.next
        # 栈的大小减1
        self.size -= 1
        # 返回移除的节点的值
        return popped_value


    def is_empty(self):
        # 判断栈是否为空
        return self.size == 0  # 如果size为0，则栈为空

    def __len__(self):
        # 返回栈的大小
        return self.size  # 直接返回size属性