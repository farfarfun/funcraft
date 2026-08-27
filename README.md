# funcraft

Minecraft Pi Edition（`mcpi`）的 Python 编程接口封装，用来通过代码远程操控一个正在运行的 Minecraft Pi 服务器：查询/设置方块、生成实体、插旗子、读取玩家位置等。

注意：导入名是 `notecraft`（历史遗留自改名前的 `note*` 系列），不是仓库名 `funcraft`；且截至目前该包**未发布到 PyPI**（`pip install notecraft` 会 404），只能从源码安装。

## 安装

未发布到 PyPI，需要从源码安装：

```bash
git clone https://github.com/farfarfun/funcraft.git
cd funcraft
pip install .
```

## 用法示例

```python
from notecraft.core.core import MineCraftConn, Cell

# 连接本地运行的 Minecraft Pi 服务器（默认 localhost:4711）
conn = MineCraftConn.create()
conn.set_block(0, 0, 0, id=1)       # 放置一个方块
conn.post_to_chat("hello from funcraft")
```

`notecraft/core/things.py` 基于 `Cell` 封装了几个现成的建筑构件：

```python
from notecraft.core.things import Wall, River

Wall(pos=p, length=10, height=5).build()
River(pos=p, length=10, depth=3).build()
```

## 说明

`example/` 目录下的脚本（如 `ply_test.py`、`core/example.py`）是作者本人的一次性实验代码，用于把点云文件（`.ply`）读进来并在 Minecraft 世界里用方块还原出来，代码里硬编码了作者本机的文件路径（如 `/Users/liangtaoniu/...`），不能直接运行，仅作为用法参考，目前也没有在维护。
