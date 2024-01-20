import math
from ezdxf.document import Drawing
from ezdxf.layouts.layout import Modelspace
from .document import Document

special_codes = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "10",
    "0a",
    "11",
    "0b",
    "12",
    "0c",
    "13",
    "0d",
    "14",
    "0e",
]


def delta_x_y(length, direction):
    """根据 length 和 direction 计算 dx 和 dy 的值"""
    dx, dy = 0, 0
    # 计算 dx 的值
    if direction in [0, 1, 2, 14, 15]:
        dx = length
    elif direction in [3, 13]:
        dx = length / 2
    elif direction in [4, 12]:
        dx = 0
    elif direction in [5, 11]:
        dx = -length / 2
    elif direction in [6, 7, 8, 9, 10]:
        dx = -length
    # 计算 dy 的值
    if direction in [1, 7]:
        dy = length / 2
    elif direction in [2, 3, 4, 5, 6]:
        dy = length
    elif direction in [0, 8]:
        dy = 0
    elif direction in [9, 15]:
        dy = -length / 2
    elif direction in [10, 11, 12, 13, 14]:
        dy = -length
    return dx, dy


class Drawer:
    def __init__(self):
        self.drawing: Drawing = Document.initialize()
        self.modelspace: Modelspace = self.drawing.modelspace()
        self.scale = 1
        self.mode = False
        self.stack = []
        self.pen = (0, 0)

    def handler(self, code, paths: list):
        """处理代码"""
        # 读取 code，根据 code 的值来判断下一步的操作
        # https://help.autodesk.com/view/ACD/2022/CHS/?guid=GUID-06832147-16BE-4A66-A6D0-3ADF98DC8228
        if code == "0":
            return
        if code == "1":
            print("PEN_DOWN")
            if self.direction:
                return
            self.mode = True
            return
        if code == "2":
            if self.direction:
                return
            print("PEN_UP")
            self.mode = False
            return
        if code == "3":
            if self.direction:
                paths.pop(0)
                return
            print("矢量除以比例因子")
            self.scale /= int(paths.pop(0), 16)
            return
        if code == "4":
            if self.direction:
                paths.pop(0)
                return
            print("矢量乘以比例因子")
            self.scale *= int(paths.pop(0), 16)
            return
        if code == "5":
            if self.direction:
                return
            print("将当前位置压入堆栈")
            self.stack.append(self.pen)
            return
        if code == "6":
            if self.direction:
                return
            print("将当前位置从堆栈弹出")
            self.pen = self.stack.pop()
            return
        if code == "7":
            print("绘制子形")
            return
        if code == "8":
            print("绘制位移")
            if self.direction:
                paths.pop(0)
                paths.pop(0)
                return
            dx, dy = paths.pop(0), paths.pop(0)
            dx = int(dx[1:]) if "(" in dx else int(dx)
            dy = int(dy[:-1]) if ")" in dy else int(dy)

            # length = int(code[1], 16)
            # direction = int(code[2], 16)
            # # 计算 dx 的值
            # dx, dy = delta_x_y(length, direction)
            # self.modelspace.add_line(
            #     start=(x, y),
            #     end=(x + dx, y + dy),
            # )
            if self.mode:
                self.modelspace.add_line(
                    start=self.pen,
                    end=(self.pen[0] + dx, self.pen[1] + dy),
                )
            self.pen = (self.pen[0] + dx, self.pen[1] + dy)
            return
        if code == "10" or code == "0a":
            if self.direction:
                for _ in range(2):
                    paths.pop(0)
                return
            print("绘制圆弧")
            radius = int(paths.pop(0), 16)
            print(radius)
            start_and_end = paths.pop(0)
            print(start_and_end)
            return
        if code == "11" or code == "0b":
            if self.direction:
                for _ in range(5):
                    paths.pop(0)
                return
            print("由下两个字节指定的圆弧")
            start_offset = int(paths.pop(0), 16)
            end_offset = int(paths.pop(0), 16)
            print(start_offset, end_offset)
            high_radius = int(paths.pop(0), 16)
            low_radius = int(paths.pop(0), 16)
            print(high_radius, low_radius)
            start_and_end = paths.pop(0)
            print(start_and_end)
            return
        if code == "12" or code == "0c":
            if self.direction:
                for _ in range(3):
                    paths.pop(0)
                return
            print("由x,y位移和凸度指定的圆弧")
            x_displacement = int(paths.pop(0), 16)
            y_displacement = int(paths.pop(0), 16)
            bulge = int(paths.pop(0), 16)
            print(x_displacement, y_displacement, bulge)
            return
        if code == "13" or code == "0d":
            while paths.pop(0) != "0" and paths.pop(0) != "0":
                x_displacement = int(paths.pop(0), 16)
                y_displacement = int(paths.pop(0), 16)
                bulge = int(paths.pop(0), 16)
                print(x_displacement, y_displacement, bulge)
            return
        if code == "14" or code == "0e":
            print("仅当垂直方向处理")
            return
        print("未知代码：".format(code))

    def draw(self, path: str, direction: int = 0):
        """绘制图形"""
        self.direction = direction
        paths = path.split(",")
        while len(paths) > 0:
            self.handler(paths.pop(0), paths)
        print("绘制完成")
