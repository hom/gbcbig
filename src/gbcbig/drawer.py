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

    def handler(self, code, paths: list):
        """处理代码"""
        # 读取 code，根据 code 的值来判断下一步的操作
        # https://help.autodesk.com/view/ACD/2022/CHS/?guid=GUID-06832147-16BE-4A66-A6D0-3ADF98DC8228
        if code == "0":
            return
        if code == "1":
            print("PEN_DOWN")
            self.mode = True
            return self.handler(paths.pop(0), paths)
        if code == "2":
            print("PEN_UP")
            self.mode = False
            dx, dy = 0, 0
            code = self.paths[i]
            if code in special_codes and code != "8":
                return i, x, y
            if code == "8":
                dx = (
                    int(self.paths[i + 1][1:])
                    if self.paths[i + 1][0] == "("
                    else int(self.paths[i + 1])
                )
                dy = (
                    int(self.paths[i + 2][:-1])
                    if self.paths[i + 2][-1] == ")"
                    else int(self.paths[i + 2])
                )
                x += dx
                y += dy
                return self.pen_up(i=i + 3, x=x, y=y)
            print(f"code: {code}")
            length = int(code[1], 16)
            direction = int(code[2], 16)
            # 计算 dx 的值
            dx, dy = delta_x_y(length, direction)
            x += dx
            y += dy
            return
        if code == "3":
            print("矢量除以比例因子")
            scale = scale / int(self.paths[i + 1], 16)
            i += 3
            return
        if code == "4":
            print("矢量乘以比例因子")
            scale = scale * int(self.paths[i + 1], 16)
            i += 1
            return
        if code == "5":
            print("MOVE_REL")
            self.stack.append((x, y))
            i += 2
            return
        if code == "6":
            print("LINE_ABS")
            x, y = self.stack.pop()
            i += 1
            return
        if code == "7":
            print("LINE_REL")
            i += 3
            return
        if code == "8":
            dx, dy = paths.pop(0), paths.pop(0)
            dx = int(dx[1:]) if "(" in dx else int(dx)
            dx = int(dy[:-1]) if ")" in dy else int(dy)
            dy = (
                int(self.paths[i + 2][:-1])
                if self.paths[i + 2][-1] == ")"
                else int(self.paths[i + 2])
            )
            length = int(code[1], 16)
            direction = int(code[2], 16)
            # 计算 dx 的值
            dx, dy = delta_x_y(length, direction)
            self.modelspace.add_line(
                start=(x, y),
                end=(x + dx, y + dy),
            )
            x += dx
            y += dy
            self.modelspace.add_line(start=(x, y), end=(x + dx, y + dy))
            print("XY_DISPLACEMENT")
            i += 3
            return
        if code == "10" or code == "0a":
            print("OCTANT_ARC")
            i += 4
            return
        if code == "11" or code == "0b":
            print("FRACTIONAL_ARC")
            i += 6
            return
        if code == "12" or code == "0c":
            print("BULGE_ARC")
            i += 4
            return
        if code == "13" or code == "0d":
            print("POLY_BULGE_ARC")
            i += 9
            return
        if code == "14" or code == "0e":
            print("COND_MODE_2")
            i, x, y = self.only_verticle_line(i + 1, x, y)
        else:
            print("END_OF_SHAPE")
            return

    def draw(self, path: str):
        """绘制图形"""
        paths = path.split(",")
        while len(paths) > 0:
            self.handler(paths.pop(0), paths)
        print("绘制完成")

    def saveas(self):
        """保存绘图"""
        self.drawing.saveas("test.dxf")
