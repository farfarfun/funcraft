# Changelog

本项目的版本记录按版本倒序排列，每个版本分「新增」「修复」「变更」「废弃」四类。

## [0.0.3]

### 新增

- `funcraft/exceptions.py` 新增 `CellBuildNotImplementedError` 领域异常，替代 `Cell._build()` 中原来的通用 `Exception`。
- `tests/test_smoke.py` 补充 `MineCraftConn`、`Cell`、`Wall`、`Line`、`River` 的正常路径与边界测试（使用打桩的 `mcpi.minecraft.Minecraft.create`，不依赖真实 Minecraft Pi 服务端）。
- `tests/test_smoke.py` 另补一组「真实 `Minecraft` 对象 + 假 socket 连接」的回归测试，走 mcpi 真实的参数编排逻辑（`intFloor`/`flatten`/告示牌文字处理），覆盖只在真实调用时才暴露的传参缺陷。
- 不提交 `uv.lock`；库项目由 `uv` 根据 `pyproject.toml` 解析依赖。

### 修复

- `MineCraftConn.set_block()` 不显式传 `data` 时不再把 `None` 透传给 mcpi。mcpi 会对全部位置参数做 `int(math.floor(...))`，此前 `set_block(x, y, z, id)`（即 README 示例里的用法）和 `set_block_vec()` 一调用就抛 `TypeError: must be real number, not NoneType`。
- `MineCraftConn.set_sign()` 不再把未填写的行以 `None` 传给 mcpi。mcpi 对每行文字调用 `str.replace`，此前只填部分行就抛 `AttributeError: 'NoneType' object has no attribute 'replace'`；现在去掉末尾未填写的行，中间空缺的行补成空串以保留行号位置。
- `MineCraftConn.get_block()` 改为调用 `Minecraft.getBlock()`。此前误调区域查询 `getBlocks()`，发出的是 `world.getBlocks` 命令，返回的也不是方块 id。
- `MineCraftConn.get_blocks()` 把 mcpi 返回的一次性 `map` 迭代器固化成 `list`，与 `list[int]` 返回标注一致，调用方二次遍历不再拿到空结果。
- `Cell` 去掉类体里的 `conn: MineCraftConn = MineCraftConn.create()`，连接改为实例属性在 `__init__` 中创建：此前仅 `import funcraft.core.core` 就会尝试连接 `localhost:4711`，且类级连接会被后创建的实例互相覆盖。
- `pyproject.toml` 中 `mcpi` 依赖补上版本下限 `>=1.2.0`（此前是裸依赖名）。
- `funcraft/core/core.py`、`funcraft/core/things.py` 公开方法补齐 Python 3.10 类型标注，`set_block_vec`/`set_blocks_vec` 补上缺失的 docstring。

### 变更

- `funcraft/core/core.py`、`funcraft/core/things.py` 的英文 docstring 全部改为中文，覆盖 `Wall`/`Line`/`River` 等此前完全没有 docstring 的公开类。
- `pyproject.toml` 的 `description` 由占位文案 `funcraft` 改为实际功能描述。
- 删除 `src/funcraft/core/example.py`：一次性实验脚本，导入未声明的 `pandas`/`plyfile`，并在模块导入时就连接 Minecraft、读取玩家位置、发送聊天消息并执行点云建造。
- 删除 `example/ply_test.py`：同类一次性点云实验脚本，依赖未声明的 `numpy`/`pandas`/`plyfile`、硬编码作者本机路径、在模块导入时就执行，且用了 numpy 已移除的 `np.float`，本身无法运行。
- 删除 `script/build.sh`、`script/__version__.md`：前者手写 `setup.py`/`twine` 构建发布流程且存在恒真条件导致的无条件 `git push`，后者是配套的遗留版本文件；构建发布统一改为使用组织的 `funbuild` 工具，不在仓库内保留自定义构建脚本（对齐 `fundata`/`funaction`/`fundaily` 等仓库的现状）。

### 废弃

- 无

### 说明：关于 `notecraft` 旧包转发（对应 codex 审计 finding #13）

`notecraft -> funcraft` 是一次仓库改名，但截至本次修复，`notecraft` 和 `funcraft`
均**从未发布到 PyPI**（`README.md` 中已注明，`pip install funcraft` 会 404）。
SPEC §15.2「整个包改名时提供旧包最终转发版本」这条规则的前提是旧包已经在
PyPI 上被外部使用者依赖；本仓库不存在这个前提，没有任何外部用户在用
`pip install notecraft`，因此不存在需要保留兼容、发出 `DeprecationWarning`
或发布转发版本的旧包可言。这里判定该发现为不适用（false positive），保留
本条说明作为审计留痕，不做代码改动。

## [0.0.2]

### 新增

- 初始可用版本：基于 `mcpi` 封装 `MineCraftConn`/`Cell`/`Wall`/`Line`/`River`，用于远程操控 Minecraft Pi 服务器。

### 修复

- 无

### 变更

- 由 `notecraft` 改名为 `funcraft`（导入名与仓库名保持一致）。
- 迁移到 `pyproject.toml`，移除 `setup.py`。
- 补充 PEP 561 `py.typed` 标记。

### 废弃

- 无
