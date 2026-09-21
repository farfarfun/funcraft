"""funcraft.core 的测试：覆盖 MineCraftConn、Cell、Wall、Line、River 的正常路径与边界。

背景说明：`funcraft.core.core` 在类体中执行
`Cell.conn = MineCraftConn.create()`，首次 import 该模块就会尝试用真实
socket 连接 `localhost:4711` 上的 Minecraft Pi 服务端；测试环境没有真实
服务端。因此下面用 `unittest.mock.patch` 在 import 之前把
`mcpi.minecraft.Minecraft.create` 换成返回 `MagicMock()` 的桩，避免真实
网络连接，同时每次都重新 import 相关模块以保证桩生效。
"""

import sys
from unittest.mock import MagicMock, patch

import pytest


def test_import():
    import funcraft  # noqa: F401


@pytest.fixture
def mock_mc():
    """一个假的 mcpi.minecraft.Minecraft 实例：记录调用但不发起真实网络请求。"""
    return MagicMock(name="Minecraft")


@pytest.fixture
def core(mock_mc):
    """在 `Minecraft.create` 被打桩的前提下（重新）导入 core/things 子模块。

    打桩需要在整个测试用例执行期间保持生效（不只是 import 那一刻），
    因为部分用例会在测试体内再次显式调用 `MineCraftConn.create()`。
    """
    for name in ("funcraft.core.things", "funcraft.core.core"):
        sys.modules.pop(name, None)
    with patch("mcpi.minecraft.Minecraft.create", return_value=mock_mc):
        import funcraft.core.core as core_module
        import funcraft.core.things as things_module

        yield core_module, things_module
    for name in ("funcraft.core.things", "funcraft.core.core"):
        sys.modules.pop(name, None)


def test_mineCraftConn_wraps_provided_mc(core, mock_mc):
    core_module, _ = core
    conn = core_module.MineCraftConn(mock_mc)
    assert conn.mc is mock_mc


def test_mineCraftConn_create_default_uses_minecraft_create(core, mock_mc):
    core_module, _ = core
    conn = core_module.MineCraftConn.create()
    assert conn.mc is mock_mc


def test_mineCraftConn_set_block_delegates(core, mock_mc):
    core_module, _ = core
    conn = core_module.MineCraftConn(mock_mc)
    conn.set_block(1, 2, 3, 4)
    mock_mc.setBlock.assert_called_once_with(1, 2, 3, 4, None)


def test_mineCraftConn_set_block_vec_delegates(core, mock_mc):
    from mcpi.vec3 import Vec3

    core_module, _ = core
    conn = core_module.MineCraftConn(mock_mc)
    conn.set_block_vec(Vec3(1, 2, 3), 5)
    mock_mc.setBlock.assert_called_once_with(1, 2, 3, 5, None)


def test_mineCraftConn_get_player_entity_id(core, mock_mc):
    core_module, _ = core
    mock_mc.getPlayerEntityId.return_value = 42
    conn = core_module.MineCraftConn(mock_mc)
    assert conn.get_player_entity_id("niult") == 42
    mock_mc.getPlayerEntityId.assert_called_once_with("niult")


def test_cell_build_without_subclass_raises_domain_exception(core):
    from funcraft.exceptions import CellBuildNotImplementedError

    core_module, _ = core
    cell = core_module.Cell(pos=None)
    with pytest.raises(CellBuildNotImplementedError):
        cell.build()


def test_cell_build_posts_success_message_and_builds_children(core, mock_mc):
    from mcpi.vec3 import Vec3

    _, things_module = core
    Wall = things_module.Wall

    pos = Vec3(0, 0, 0)
    parent = Wall(pos=pos, height=2, length=3, width=1, msg="parent")
    child = Wall(pos=pos, height=1, length=1, width=1, msg="child")
    parent.add_child(child)

    parent.build()

    assert mock_mc.setBlocks.call_count == 2
    mock_mc.postToChat.assert_any_call("build parent success!")
    mock_mc.postToChat.assert_any_call("build child success!")


def test_wall_build_sets_expected_cuboid(core, mock_mc):
    from mcpi.vec3 import Vec3

    _, things_module = core
    Wall = things_module.Wall

    pos = Vec3(1, 2, 3)
    wall = Wall(pos=pos, height=2, length=3, width=1)
    wall.build()

    mock_mc.setBlocks.assert_called_once_with(
        1, 2, 3, 1 + 3 - 1, 2 + 2 - 1, 3 + 1 - 1, wall.block.id
    )


def test_line_constructs_and_builds(core, mock_mc):
    """Line 应按厚度设置高度，并能正常建造。"""
    from mcpi.vec3 import Vec3

    _, things_module = core
    Line = things_module.Line
    line = Line(pos=Vec3(0, 0, 0), length=5, width=2)
    assert line.height == 2
    line.build()
    mock_mc.setBlocks.assert_called_once_with(0, 0, 0, 4, 1, 1, line.block.id)


def test_set_blocks_vec_preserves_end_y(core, mock_mc):
    from mcpi.vec3 import Vec3

    core_module, _ = core
    core_module.MineCraftConn(mock_mc).set_blocks_vec(Vec3(1, 2, 3), Vec3(4, 5, 6), 7)
    mock_mc.setBlocks.assert_called_once_with(1, 2, 3, 4, 5, 6, 7)


def test_river_uses_negative_depth_and_water_block(core):
    import mcpi.block
    from mcpi.vec3 import Vec3

    _, things_module = core
    River = things_module.River

    river = River(pos=Vec3(0, 0, 0), length=4, width=1, depth=3)
    assert river.height == -3
    assert river.block == mcpi.block.WATER_FLOWING
