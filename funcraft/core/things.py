import mcpi.block

from funcraft.core.core import Cell


class Wall(Cell):
    """一面长方体墙，默认使用砖块，从 `pos` 起沿 x/y/z 三个方向铺开。"""

    def __init__(self, height=5, length=10, width=1, *args, **kwargs):
        """初始化墙体尺寸。

        Args:
            height: 高度（y 方向格数）。
            length: 长度（x 方向格数）。
            width: 厚度（z 方向格数）。
        """
        self.height = height
        self.length = length
        self.width = width
        kwargs['block'] = kwargs.get('block', mcpi.block.BRICK_BLOCK)
        super().__init__(*args, **kwargs)

    def _build(self, *args, **kwargs) -> None:
        """按 `pos`/`height`/`length`/`width` 计算出的立方体区域批量放置方块。"""
        self.conn.set_blocks(self.pos.x, self.pos.y, self.pos.z, self.pos.x + self.length - 1,
                             self.pos.y + self.height - 1, self.pos.z + self.width - 1, self.block.id)


class Line(Wall):
    """一条“线”，本质是高度等于厚度（`width`）的最薄墙体。"""

    def __init__(self, *args, **kwargs):
        """初始化时强制 `height = width`，其余参数与 `Wall` 相同。"""
        kwargs['height'] = self.width
        super().__init__(*args, **kwargs)


class River(Wall):
    """一条河流，使用流动水方块，并向下（负高度）挖出 `depth` 层深度。"""

    def __init__(self, depth=3, *args, **kwargs):
        """初始化河流。

        Args:
            depth: 河床深度（向下的格数），内部转换为负的 `height` 传给 `Wall`。
        """
        kwargs['block'] = kwargs.get('block', mcpi.block.WATER_FLOWING)
        kwargs['height'] = -depth
        super().__init__(*args, **kwargs)
