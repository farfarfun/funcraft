from typing import Any

import mcpi.block
from mcpi.block import Block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

from funcraft.exceptions import CellBuildNotImplementedError


class MineCraftConn:
    """封装一个正在运行的 Minecraft Pi 服务器连接，提供中文语义的方法名。"""

    def __init__(self, mc: Minecraft | None = None) -> None:
        """初始化连接。

        Args:
            mc: 已建立的 `mcpi.minecraft.Minecraft` 实例；为空时调用
                `Minecraft.create()` 使用默认地址/端口新建一个。
        """
        self.mc = mc or Minecraft.create()

    def get_block(self, x: int, y: int, z: int) -> int:
        """读取指定坐标处的方块 id。

        Args:
            x: 方块的 x 坐标。
            y: 方块的 y 坐标。
            z: 方块的 z 坐标。
        Returns:
            方块 id。
        """
        return self.mc.getBlocks(x, y, z)

    def get_block_with_data(self, x: int, y: int, z: int) -> Block:
        """读取指定坐标处的方块及其附加数据。

        Args:
            x: 方块的 x 坐标。
            y: 方块的 y 坐标。
            z: 方块的 z 坐标。
        Returns:
            包含方块 id 和 data 的 `Block`。
        """
        return self.mc.getBlockWithData(x, y, z)

    def get_blocks(
        self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int
    ) -> list[int]:
        """读取一个立方体区域内的方块 id 列表。

        Args:
            x0, y0, z0: 区域起点坐标。
            x1, y1, z1: 区域终点坐标。
        Returns:
            按 Minecraft 协议顺序排列的方块 id 列表。
        """
        return self.mc.getBlocks(x0, y0, z0, x1, y1, z1)

    def set_block(
        self, x: int, y: int, z: int, id: int, data: int | None = None
    ) -> None:
        """在指定坐标放置一个方块。

        Args:
            x, y, z: 方块坐标。
            id: 方块 id。
            data: 可选的方块附加数据。
        Returns:
            无返回值。
        """
        return self.mc.setBlock(x, y, z, id, data)

    def set_block_vec(self, pos: Vec3, id: int) -> None:
        """按 `Vec3` 坐标放置一个方块。

        Args:
            pos: 方块坐标。
            id: 方块 id。
        Returns:
            无返回值。
        """
        return self.set_block(pos.x, pos.y, pos.z, id)

    def set_blocks(
        self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, id: int
    ) -> None:
        """将一个立方体区域内的方块全部设置为同一 id。

        Args:
            x0, y0, z0: 区域起点坐标。
            x1, y1, z1: 区域终点坐标。
            id: 要设置的方块 id。
        Returns:
            无返回值。
        """
        return self.mc.setBlocks(x0, y0, z0, x1, y1, z1, id)

    def set_blocks_vec(self, start: Vec3, end: Vec3, id: int) -> None:
        """按两个 `Vec3` 坐标构成的立方体区域批量设置方块。

        Args:
            start: 区域起点坐标。
            end: 区域终点坐标。
            id: 要设置的方块 id。
        Returns:
            无返回值。
        """
        return self.set_blocks(start.x, start.y, start.z, end.x, end.y, end.z, id)

    def set_sign(
        self,
        x: int,
        y: int,
        z: int,
        id: int,
        data: int,
        line1: str | None = None,
        line2: str | None = None,
        line3: str | None = None,
        line4: str | None = None,
    ) -> None:
        """放置一个告示牌（最多 4 行文字）。

        挂墙告示牌（id=68）的 data 表示朝向：2=北，3=南，4=西，5=东；
        立式告示牌（id=63）的 data 表示旋转角度（0-15）：0=南，4=西，8=北，12=东。

        Args:
            x, y, z: 告示牌坐标。
            id: 告示牌方块 id。
            data: 朝向或旋转角度。
            line1, line2, line3, line4: 最多四行文字。
        Returns:
            无返回值。

        致谢：Tim Cummings <https://www.triptera.com.au/wordpress/>
        """
        return self.mc.setSign(x, y, z, id, data, [line1, line2, line3, line4])

    def spawn_entity(self, x: int, y: int, z: int, id: int) -> int:
        """在指定坐标生成一个实体。

        Args:
            x, y, z: 生成位置。
            id: 实体类型 id。
        Returns:
            新实体 id。
        """
        return self.mc.spawnEntity(x, y, z, id)

    def get_height(self, x: int, z: int) -> int:
        """获取 `(x, z)` 处地形的高度。

        Args:
            x: x 坐标。
            z: z 坐标。
        Returns:
            地形高度。
        """
        return self.mc.getHeight(x, z)

    def get_player_entity_ids(self) -> list[int]:
        """获取所有已连接玩家的实体 id 列表。

        Returns:
            玩家实体 id 列表。
        """
        return self.mc.getPlayerEntityIds()

    def get_player_entity_id(self, name: str) -> int:
        """根据玩家名获取其实体 id。

        Args:
            name: 玩家名称。
        Returns:
            玩家实体 id。
        """
        return self.mc.getPlayerEntityId(name)

    def save_checkpoint(self) -> None:
        """保存一个检查点，供后续 `restore_checkpoint()` 恢复世界状态。

        Returns:
            无返回值。
        """
        return self.mc.saveCheckpoint()

    def restore_checkpoint(self) -> None:
        """将世界状态恢复到上一次 `save_checkpoint()` 保存的检查点。

        Returns:
            无返回值。
        """
        return self.mc.restoreCheckpoint()

    def post_to_chat(self, msg: str) -> None:
        """向游戏聊天频道发送一条消息。

        Args:
            msg: 要发送的消息。
        Returns:
            无返回值。
        """
        return self.mc.postToChat(msg)

    def setting(self, setting: str, status: bool) -> None:
        """设置世界参数，例如 `world_immutable`、`nametags_visible`。

        Args:
            setting: 参数名称。
            status: 是否启用参数。
        Returns:
            无返回值。
        """
        return self.mc.setting(setting, status)

    def get_entity_types(self) -> list[str]:
        """获取 Minecraft 中所有实体类型的列表。

        Returns:
            实体类型名称列表。
        """
        return self.mc.getEntityTypes()

    def get_entities(self, typeId: int = -1) -> list[list[int | str]]:
        """获取当前已加载的实体列表，可按 `typeId` 过滤。

        Args:
            typeId: 实体类型 id，默认 `-1` 表示全部类型。
        Returns:
            形如
        `[[entityId, entityTypeId, entityTypeName, posX, posY, posZ], ...]`。
        """
        return self.mc.getEntities(typeId)

    def remove_entity(self, id: int) -> int:
        """按实体 id 移除单个实体。

        Args:
            id: 要移除的实体 id。
        Returns:
            被移除的实体数量。
        """
        return self.mc.removeEntity(id)

    def remove_entities(self, typeId: int = -1) -> int:
        """按类型批量移除已加载的实体。

        Args:
            typeId: 实体类型 id，默认 `-1` 表示全部类型。
        Returns:
            被移除的实体数量。
        """
        return self.mc.removeEntities(typeId)

    @staticmethod
    def create(address: str = "localhost", port: int = 4711) -> "MineCraftConn":
        """按地址、端口新建一个连接。

        Args:
            address: Minecraft Pi 服务端地址。
            port: Minecraft Pi 服务端端口。
        Returns:
            新建的连接对象。
        """
        return MineCraftConn(Minecraft.create(address, port))


class Cell:
    """一个可建造的最小单元，支持嵌套子节点并统一触发建造。

    子类需要实现 `_build()` 完成实际的建造逻辑；`build()` 会先调用
    `_build()`，再递归建造所有子节点，最后向聊天频道播报建造成功。
    """

    conn: MineCraftConn = MineCraftConn.create()

    def __init__(
        self,
        mc: Minecraft | None = None,
        pos: Vec3 | None = None,
        block: Block = mcpi.block.WOOD,
        msg: str = "cell",
    ):
        """初始化建造单元。

        Args:
            mc: 已建立的 `Minecraft` 连接；提供时会覆盖类级别共用的 `conn`。
            pos: 建造起始坐标。
            block: 使用的方块类型，默认木头。
            msg: 建造完成后播报到聊天频道的消息内容。
        """
        if mc is not None:
            Cell.conn = MineCraftConn(mc) or MineCraftConn.create()

        self._children: list[Cell] = []
        self.pos = pos
        self.block = block
        self.msg = msg

    def add_child(self, child: "Cell") -> None:
        """添加一个子建造单元，会在 `build()` 时一并建造。

        Args:
            child: 要添加的子建造单元。
        Returns:
            无返回值。
        """
        self._children.append(child)

    def build(self, *args: Any, **kwargs: Any) -> None:
        """建造当前单元及其所有子节点，完成后播报成功消息。

        Args:
            *args, **kwargs: 传递给子类建造逻辑的额外参数。
        Returns:
            无返回值。
        """
        self._build(*args, **kwargs)
        for node in self._children:
            if isinstance(node, Cell):
                node.build()
        self.conn.post_to_chat(f"build {self.msg} success!")

    def _build(self, *args: Any, **kwargs: Any) -> None:
        """实际建造逻辑，需由子类实现。"""
        raise CellBuildNotImplementedError(self)
