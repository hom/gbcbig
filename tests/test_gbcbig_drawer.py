import os
from pathlib import Path
from datetime import datetime
from gbcbig.drawer import Drawer
from ezdxf import bbox

dist = Path.joinpath(Path(__file__).parent, "dist")
if not dist.exists():
    os.mkdir(dist)


def test_1():
    drawer = Drawer()
    shape = {
        "shape": "7,4,9,3,102,2,14,8,(-34,-80),2,8,(0,-5),0,5,2,8,(39,63),1,8,(6,25),2,8,(-16,-1),1,8,(0,-25),2,8,(-17,9),1,8,(48,6),2,8,(-38,-11),1,8,(0,-28),2,8,(0,22),1,8,(26,3),2,8,(1,4),1,8,(-1,-22),2,8,(2,0),1,8,(-28,-3),2,8,(4,10),1,8,(16,2),2,8,(-16,-15),1,8,(-8,-13),8,(-14,-11),2,8,(20,16),1,8,(31,3),2,8,(1,6),1,8,(-9,-42),8,(-5,7),2,8,(-22,21),1,8,(0,-18),2,8,(-2,-1),1,8,(26,4),2,8,(-9,20),1,8,(-2,-9),2,8,(1,0),1,8,(9,-5),2,8,(-18,-4),1,8,(8,9),7,6,2,14,8,(-32,-32),2,8,(66,5),4,102,3,9,0,0",
        "gb2312": "B8F0",
        "unicode": "0x845b",
        "length": "140",
        "character": "葛",
    }
    drawer.draw(shape.get("shape"))
    # 添加图形的轮廓
    (x1, y1, z1), (x2, y2, z2) = bbox.extents(drawer.modelspace, cache=bbox.Cache())

    drawer.modelspace.add_lwpolyline(
        points=[
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
        ],
        close=True,
    )
    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    drawer.drawing.saveas(dist / f"{shape.get('character')}_{created_at}.dxf")

def test_2():
    drawer = Drawer()
    shape = {
        "shape": "7,4,9,3,102,2,14,8,(-34,-80),2,8,(0,-5),0,5,2,8,(39,78),1,8,(0,-64),2,8,(18,74),1,8,(0,-89),2,8,(-28,57),1,8,(7,-13),2,8,(9,14),1,8,(7,-14),2,8,(-27,40),1,8,(-2,-51),8,(-4,-11),8,(-12,-22),2,8,(8,63),1,8,(-1,-17),8,(-2,-9),7,6,2,14,8,(-32,-32),2,8,(66,5),4,102,3,9,0,0",
        "gb2312": "B8F0",
        "unicode": "0x845b",
        "length": "140",
        "character": "州",
    }
    drawer.draw(shape.get("shape"))
    # 添加图形的轮廓
    (x1, y1, z1), (x2, y2, z2) = bbox.extents(drawer.modelspace, cache=bbox.Cache())

    drawer.modelspace.add_lwpolyline(
        points=[
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
        ],
        close=True,
    )
    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    drawer.drawing.saveas(dist / f"{shape.get('character')}_{created_at}.dxf")

def test_3():
    drawer = Drawer()
    shape = {
        "shape": "7,4,9,3,102,2,14,8,(-34,-80),2,8,(0,-5),0,5,2,8,(5,38),1,8,(56,4),7,6,2,14,8,(-32,-32),2,8,(66,5),4,102,3,9,0,0",
        "gb2312": "B8F0",
        "unicode": "0x845b",
        "length": "140",
        "character": "一",
    }
    drawer.draw(shape.get("shape"))
    # 添加图形的轮廓
    (x1, y1, z1), (x2, y2, z2) = bbox.extents(drawer.modelspace, cache=bbox.Cache())

    drawer.modelspace.add_lwpolyline(
        points=[
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
        ],
        close=True,
    )
    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    drawer.drawing.saveas(dist / f"{shape.get('character')}_{created_at}.dxf")
