import tkinter as tk
from MazeGenerator import MazeGenerator

def draw_rotated_text(canvas, text, x, y, angle, font):
    """在给定的位置以指定的角度绘制旋转文本"""
    # 创建一个文本项
    text_id = canvas.create_text(x, y, text=text, font=font)
    # 获取文本项的边界框
    bbox = canvas.bbox(text_id)
    # 计算文本中心点
    center_x = (bbox[0] + bbox[2]) / 2
    center_y = (bbox[1] + bbox[3]) / 2
    # 删除原来的文本项
    canvas.delete(text_id)
    # 重新创建文本项，并应用旋转
    text_id = canvas.create_text(center_x, center_y, text=text, font=font, angle=angle)
    # 调整位置以确保文本在指定的(x, y)处
    bbox = canvas.bbox(text_id)
    canvas.move(text_id, x - bbox[0], y - bbox[1])

def draw_maze(canvas, maze, cell_size):
    n = len(maze)
    m = len(maze[0])

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1 or cell == 2:
                canvas.create_rectangle(x * cell_size, y * cell_size,
                                        (x + 1) * cell_size, (y + 1) * cell_size,
                                        fill='gray', outline='black')
            if cell == 3:
                canvas.create_rectangle(x * cell_size, y * cell_size,
                                        (x + 1) * cell_size, (y + 1) * cell_size,
                                        fill='yellow', outline='black')
    if (n % 2 == 0 and m % 2 == 0):
        canvas.create_rectangle(cell_size, 0, 2 * cell_size, cell_size, fill='red', outline='black')
        canvas.create_rectangle((n - 3) * cell_size, (m) * cell_size, (n - 2) * cell_size, (m - 1) * cell_size,
                                fill='red', outline='black')
    elif (n % 2 == 0 and m % 2 == 1):
        canvas.create_rectangle(cell_size, 0, 2 * cell_size, cell_size, fill='red', outline='black')
        canvas.create_rectangle((m) * cell_size, (n - 2) * cell_size, (m - 1) * cell_size, (n - 1) * cell_size,
                                fill='red', outline='black')
    else:
        canvas.create_rectangle(cell_size, 0, 2 * cell_size, cell_size, fill='red', outline='black')
        canvas.create_rectangle((n - 1) * cell_size, (m - 1) * cell_size, (n) * cell_size, (m - 2) * cell_size,
                                fill='red', outline='black')
    # 绘制底部的横坐标
    # 增加额外的空间以防止文本重叠
    extra_space = cell_size  # 可以根据实际效果调整这个值
    for x in range(m):
        # 调整文本位置以确保它们不会重叠
        draw_rotated_text(canvas, str(x), (x-0.8) * cell_size + extra_space, (n + 1) * cell_size, 270, font=('Arial', 8))

    # 绘制右侧的纵坐标
    for y in range(n):
        canvas.create_text(m * cell_size + cell_size / 2, (y + 0.5) * cell_size,
                           text=str(y), anchor=tk.W)

def regenerate_maze(canvas, mz, cell_size):\
    # 清楚之前的内容
    canvas.delete("all")
    # 生成新的迷宫
    mz.generate()
    # 绘制新的迷宫
    draw_maze(canvas, mz.grid, cell_size)

def show_ans(canvas, n, m, mz, cell_size):
    ans1 = ""
    ans2 = ""
    if (n % 2 == 0 and m % 2 == 0):
        ans1 = mz.dfs(1, 1, n - 3, m - 3, canvas, cell_size)
        ans2 = mz.bfs(1, 1, n - 3, m - 3, canvas, cell_size)
    else:
        ans1 = mz.dfs(1, 1, n - 2, m - 2, canvas, cell_size)
        ans2 = mz.bfs(1, 1, n - 2, m - 2, canvas, cell_size)
    canvas.create_text(cell_size * (m + m / 2 + m / 4)  + cell_size / 2, cell_size * (n / 2 ) +  cell_size + cell_size / 2, text="BFS: " + ans2, anchor=tk.CENTER)


def menu_click(canvas, start_button, e1, e2, cell_size, text1, text2, regenerate_button, show_ans_button,):
    canvas.delete("all")
    canvas.config(width=50, height=100)
    e1.grid()
    e2.grid()
    text1.grid(row=1, column=0)
    text2.grid(row=1, column=0)
    start_button.grid(row=2, column=0)
    regenerate_button.grid(row=2, column=0)
    show_ans_button.grid(row=2, column=0)

def on_start_button_click(canvas, start_button, regenerate_button, mz, cell_size, e1, e2, root, text1, text2, return_button, show_ans_button):
    global n, m
    n = -1
    m = -1
    try:
        a = e1.get()
        b = e2.get()
        if (a == "" or b == ""):
            return
        else:
            # 获取输入框的值
            n = int(a)
            m = int(b)


        # 确保输入的是有效的整数
        if n <= 0 or m <= 0:
            raise ValueError("长度和宽度必须大于0")

        # 创建画布
        canvas.config(width=(2 * m + 6 )  * cell_size, height=(n + 5) * cell_size)
        canvas.grid(row=2, columnspan=3)  # 使用grid布局
        mz.resize(n, m)
        mz.generate()

        # 清除之前的内容
        canvas.delete("all")
        # 绘制迷宫
        draw_maze(canvas, mz.grid, cell_size)
        # 显示输入框

        # 隐藏开始按钮
        start_button.grid_forget()

        # 显示重新生成按钮
        regenerate_button.grid(row=1, column=1)
        show_ans_button = tk.Button(root, text="查看答案", command=lambda: show_ans(canvas, n, m, mz, cell_size))
        show_ans_button.grid(row=1, column=2)

        return_button.grid_forget()
        return_button.grid(row=1, column=3)
    except ValueError as ve:
        # 处理无效输入的情况
        print(f"输入错误: {ve}")

    # 隐藏输入框
    e1.grid_remove()
    e2.grid_remove()
    text1.grid_remove()
    text2.grid_remove()

def main():
    global canvas
    root = tk.Tk()
    root.title("Maze")

    # 如果不需要输入框，可以注释掉下面这两行
    text1 = tk.Label(root, text="请输入宽度")
    text2 = tk.Label(root, text="请输入长度")
    text1.grid(row=0, column=0)
    text2.grid(row=1, column=0)
    e1 = tk.Entry(root)
    e2 = tk.Entry(root)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    length = 51
    width = 51

    mz = MazeGenerator(length, width)
    cell_size = 10


    # 创建重新生成按钮
    regenerate_button = tk.Button(root, text="重新生成",
                                  command=lambda: regenerate_maze(canvas, mz, cell_size))

    regenerate_button.grid(row=1, column=2)

    # 创建查看答案按钮
    show_ans_button = tk.Button(root, text="查看答案", command=lambda: show_ans(canvas, n, m, mz, cell_size))

    canvas = tk.Canvas(root, width=50, height=100)
    canvas.grid(row=2, columnspan=3)  # 使用grid布局

    return_button = tk.Button(root, text="返回菜单",
                              command=lambda: menu_click(canvas, start_button, e1, e2, cell_size, text1, text2, regenerate_button, show_ans_button))
    return_button.grid(row=3, column=3)

    # 创建开始按钮
    start_button = tk.Button(root, text="生成迷宫",
                             command=lambda: on_start_button_click(canvas, start_button, regenerate_button, mz,
                                                                   cell_size, e1, e2, root, text1, text2,
                                                                   return_button, show_ans_button))
    start_button.grid(row=2, column=0)

    # 初始时不显示重新生成按钮
    regenerate_button.grid_remove()
    return_button.grid_remove()
    root.mainloop()

if __name__ == "__main__":
    main()