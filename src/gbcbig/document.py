import ezdxf


class Document:
    """基础文档类"""

    def __init__(self) -> None:
        """目前仅需要初始化线型（linetypes）即可
        初始化字体样式（styles）会添加 25 个无版权的英文字体样式
        初始化标注类型（dimstyles）会附带初始化字体样式（styles）
        初始化 visualstyles 会导致生成的 DXF 文件无法复制到剪切板
        """
        doc = ezdxf.new(dxfversion="R2018", setup=["linetypes"], units=ezdxf.units.MM)
        # doc.styles.new(
        #     name="Albedo", dxfattribs={"font": "gbenor", "bigfont": "gbcbig"}
        # )
        # doc.styles.new("宋体", dxfattribs={"font": "simsun.ttf"})
        # doc.styles.new(name="Romantic", dxfattribs={"font": "romantic.ttf"})
        # doc.styles.new(name="Times", dxfattribs={"font": "times.ttf"})
        # doc.styles.new(name="Romans", dxfattribs={"font": "romans"})
        self.doc = doc
        self.msp = doc.modelspace()
