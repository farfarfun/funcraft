import mcpi.block

from notecraft.core.core import Cell


class Wall(Cell):
    def __init__(self, height=5, length=10, width=1, *args, **kwargs):
        self.height = height
        self.length = length
        self.width = width
        kwargs['block'] = kwargs.get('block', mcpi.block.BRICK_BLOCK)
        super(Wall, self).__init__(*args, **kwargs)

    def _build(self, *args, **kwargs):
        self.conn.set_blocks(self.pos.x, self.pos.y, self.pos.z, self.pos.x + self.length - 1,
                             self.pos.y + self.height - 1, self.pos.z + self.width - 1, self.block.id)


class Line(Wall):
    def __init__(self, *args, **kwargs):
        kwargs['height'] = self.width
        super(Line, self).__init__(*args, **kwargs)


class River(Wall):
    def __init__(self, depth=3, *args, **kwargs):
        kwargs['block'] = kwargs.get('block', mcpi.block.WATER_FLOWING)
        kwargs['height'] = -depth
        super(River, self).__init__(*args, **kwargs)
