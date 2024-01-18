import ezdxf


class Document:
    """基础文档类"""

    @staticmethod
    def initialize(self) -> None:
        """目前仅需要初始化线型（linetypes）即可
        初始化字体样式（styles）会添加 25 个无版权的英文字体样式
        初始化标注类型（dimstyles）会附带初始化字体样式（styles）
        初始化 visualstyles 会导致生成的 DXF 文件无法复制到剪切板
        """
        drawing = ezdxf.new(
            dxfversion="R2018", setup=["linetypes"], units=ezdxf.units.MM
        )
        return drawing
