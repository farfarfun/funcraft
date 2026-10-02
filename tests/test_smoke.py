"""funcraft.core 的测试：覆盖连接代理和建筑单元的主要契约。"""

import sys
from unittest.mock import MagicMock, patch

import pytest


def test_core_import_does_not_create_connection():
    for name in ("funcraft.core.things", "funcraft.core.core"):
        sys.modules.pop(name, None)

    with patch("mcpi.minecraft.Minecraft.create") as create:
        import funcraft.core.core  # noqa: F401

    create.assert_not_called()


@pytest.fixture
def mock_mc():
    """一个假的 mcpi.minecraft.Minecraft 实例：记录调用但不发起真实网络请求。"""
    return MagicMock(name="Minecraft")


@pytest.fixture
def core(mock_mc):
    """导入模块，并在测试期间阻止实例初始化连接真实服务端。"""
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
    mock_mc.setBlock.assert_called_once_with(1, 2, 3, 4)


def test_mineCraftConn_set_block_with_data_delegates(core, mock_mc):
    core_module, _ = core
    conn = core_module.MineCraftConn(mock_mc)
    conn.set_block(1, 2, 3, 4, 5)
    mock_mc.setBlock.assert_called_once_with(1, 2, 3, 4, 5)


def test_mineCraftConn_set_block_vec_delegates(core, mock_mc):
    from mcpi.vec3 import Vec3

    core_module, _ = core
    conn = core_module.MineCraftConn(mock_mc)
    conn.set_block_vec(Vec3(1, 2, 3), 5)
    mock_mc.setBlock.assert_called_once_with(1, 2, 3, 5)


def test_mineCraftConn_get_player_entity_id(core, mock_mc):
    core_module, _ = core
    mock_mc.getPlayerEntityId.return_value = 42
    conn = core_module.MineCraftConn(mock_mc)
    assert conn.get_player_entity_id("niult") == 42
    mock_mc.getPlayerEntityId.assert_called_once_with("niult")


@pytest.mark.parametrize(
    ("method", "args", "mc_method", "expected"),
    [
        ("get_block", (1, 2, 3), "getBlock", 1),
        ("get_block_with_data", (1, 2, 3), "getBlockWithData", "block"),
        ("set_blocks", (1, 2, 3, 4, 5, 6, 7), "setBlocks", None),
        ("spawn_entity", (1, 2, 3, 4), "spawnEntity", 9),
        ("get_height", (1, 3), "getHeight", 8),
        ("get_player_entity_ids", (), "getPlayerEntityIds", [7, 8]),
        ("save_checkpoint", (), "saveCheckpoint", None),
        ("restore_checkpoint", (), "restoreCheckpoint", None),
        ("post_to_chat", ("hello",), "postToChat", None),
        ("setting", ("world_immutable", True), "setting", None),
        ("get_entity_types", (), "getEntityTypes", ["Player"]),
        ("get_entities", (), "getEntities", []),
        ("remove_entity", (7,), "removeEntity", 1),
        ("remove_entities", (), "removeEntities", 2),
    ],
)
def test_minecraft_conn_delegates(core, mock_mc, method, args, mc_method, expected):
    core_module, _ = core
    delegate = getattr(mock_mc, mc_method)
    delegate.return_value = expected

    result = getattr(core_module.MineCraftConn(mock_mc), method)(*args)

    expected_args = args
    if method in {"get_entities", "remove_entities"}:
        expected_args = (-1,)
    delegate.assert_called_once_with(*expected_args)
    assert result == expected


@pytest.fixture
def real_mc():
    """用假 socket 连接构造真实的 `mcpi.minecraft.Minecraft`。

    和 `mock_mc` 不同，这里走的是 mcpi 真实的参数编排逻辑（`intFloor`、
    `flatten`、告示牌文字的 `str.replace`），所以能发现「传了 `None` 下去
    导致 mcpi 内部抛异常」这类只在真实调用时才暴露的缺陷。
    """
    from mcpi.minecraft import Minecraft

    connection = MagicMock(name="Connection")
    return Minecraft(connection), connection


def test_set_block_without_data_does_not_pass_none_to_mcpi(core, real_mc):
    """`set_block` 不显式给 data 时必须省略该参数（mcpi 会对它做 int(floor())）。"""
    core_module, _ = core
    mc, connection = real_mc

    core_module.MineCraftConn(mc).set_block(0, 1, 2, 5)

    connection.send.assert_called_once_with(b"world.setBlock", [0, 1, 2, 5])


def test_set_block_with_data_passes_data_to_mcpi(core, real_mc):
    core_module, _ = core
    mc, connection = real_mc

    core_module.MineCraftConn(mc).set_block(0, 1, 2, 5, 3)

    connection.send.assert_called_once_with(b"world.setBlock", [0, 1, 2, 5, 3])


def test_set_sign_omits_unfilled_trailing_lines(core, real_mc):
    """只填前两行时，后两行不能以 `None` 形式传进 mcpi。"""
    core_module, _ = core
    mc, connection = real_mc

    core_module.MineCraftConn(mc).set_sign(1, 2, 3, 68, 2, "第一行", "第二行")

    connection.send.assert_called_once_with(
        b"world.setSign", [1, 2, 3, 68, 2, "第一行", "第二行"]
    )


def test_set_sign_keeps_line_positions_when_middle_line_missing(core, real_mc):
    """中间行留空时补成空串，保证后面的文字仍落在原来的行号上。"""
    core_module, _ = core
    mc, connection = real_mc

    core_module.MineCraftConn(mc).set_sign(1, 2, 3, 63, 0, "第一行", None, "第三行")

    connection.send.assert_called_once_with(
        b"world.setSign", [1, 2, 3, 63, 0, "第一行", "", "第三行"]
    )


def test_set_sign_without_any_line(core, real_mc):
    core_module, _ = core
    mc, connection = real_mc

    core_module.MineCraftConn(mc).set_sign(1, 2, 3, 68, 2)

    connection.send.assert_called_once_with(b"world.setSign", [1, 2, 3, 68, 2])


def test_get_block_reads_single_block(core, real_mc):
    """`get_block` 必须走 `world.getBlock`，而不是区域查询 `world.getBlocks`。"""
    core_module, _ = core
    mc, connection = real_mc
    connection.sendReceive.return_value = "7"

    assert core_module.MineCraftConn(mc).get_block(1, 2, 3) == 7
    connection.sendReceive.assert_called_once_with(b"world.getBlock", [1, 2, 3])


def test_get_blocks_returns_reusable_list(core, real_mc):
    """`get_blocks` 返回 list，而不是只能遍历一次的 map 迭代器。"""
    core_module, _ = core
    mc, connection = real_mc
    connection.sendReceive.return_value = "1,2,3"

    blocks = core_module.MineCraftConn(mc).get_blocks(0, 0, 0, 1, 1, 1)

    assert blocks == [1, 2, 3]
    assert list(blocks) == [1, 2, 3]


def test_minecraft_conn_propagates_delegate_errors(core, mock_mc):
    core_module, _ = core
    mock_mc.getHeight.side_effect = ConnectionError("server unavailable")

    with pytest.raises(ConnectionError, match="server unavailable"):
        core_module.MineCraftConn(mock_mc).get_height(1, 2)


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
