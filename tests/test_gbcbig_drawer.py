import os
import sys
from pathlib import Path
from datetime import datetime
from gbcbig.drawer import Drawer
from ezdxf import bbox

dist = Path.joinpath(Path(__file__).parent, "dist")
print(dist)
if not dist.exists():
    os.mkdir(dist)


def test_gbcbig():
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

    bounding_box_block = drawer.drawing.blocks.new_anonymous_block(
        base_point=(x1, y1 + 2 * drawer.scale)
    )
    bounding_box_block.add_lwpolyline(
        points=[
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
        ],
        close=True,
    )
    drawer.modelspace.add_blockref(
        name=bounding_box_block.name,
        insert=(x1, y1),
    )
    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    drawer.drawing.saveas(dist / f"{sys._getframe().f_code.co_name}_{created_at}.dxf")
