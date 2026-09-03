# Changelog

本项目的版本记录按版本倒序排列，每个版本分「新增」「修复」「变更」「废弃」四类。

## [Unreleased]

### 新增

- `funcraft/exceptions.py` 新增 `CellBuildNotImplementedError` 领域异常，替代 `Cell._build()` 中原来的通用 `Exception`。
- `tests/test_smoke.py` 补充 `MineCraftConn`、`Cell`、`Wall`、`Line`、`River` 的正常路径与边界测试（使用打桩的 `mcpi.minecraft.Minecraft.create`，不依赖真实 Minecraft Pi 服务端）。
- 提交 `uv.lock`，保证依赖可复现构建。

### 修复

- `pyproject.toml` 中 `mcpi` 依赖补上版本下限 `>=1.2.0`（此前是裸依赖名）。
- `funcraft/core/core.py`、`funcraft/core/things.py` 公开方法补齐 Python 3.10 类型标注，`set_block_vec`/`set_blocks_vec` 补上缺失的 docstring。

### 变更

- `funcraft/core/core.py`、`funcraft/core/things.py` 的英文 docstring 全部改为中文，覆盖 `Wall`/`Line`/`River` 等此前完全没有 docstring 的公开类。
- `funcraft/core/example.py`、`example/ply_test.py` 移除一次性实验脚本中的 `print()` 诊断输出（这两个脚本本身就是不再维护、硬编码本机路径、无法直接运行的实验代码，故选择直接删除输出而非改用 `farlog`，避免为死代码新增依赖）。
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
