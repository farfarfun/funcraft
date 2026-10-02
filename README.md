# funcraft

Minecraft Pi Edition（`mcpi`）的 Python 编程接口封装，用来通过代码远程操控一个正在运行的 Minecraft Pi 服务器：查询/设置方块、生成实体、插旗子、读取玩家位置等。

注意：截至目前该包**未发布到 PyPI**（`pip install funcraft` 会 404），只能从源码安装。

## 安装

未发布到 PyPI，需要从源码安装：

```bash
git clone https://github.com/farfarfun/funcraft.git
cd funcraft
uv sync
```

## 用法示例

```python
from funcraft.core.core import MineCraftConn, Cell

# 连接本地运行的 Minecraft Pi 服务器（默认 localhost:4711）
conn = MineCraftConn.create()
conn.set_block(0, 0, 0, id=1)  # 放置一个方块
conn.post_to_chat("hello from funcraft")
```

`funcraft/core/things.py` 基于 `Cell` 封装了几个现成的建筑构件：

```python
from mcpi.vec3 import Vec3
from funcraft.core.things import Wall, River

p = Vec3(0, 0, 0)
Wall(pos=p, length=10, height=5).build()
River(pos=p, length=10, depth=3).build()
```

使用 `uv run` 执行脚本或测试，例如 `uv run pytest`。

## 说明

`example/` 目录下的 `ply_test.py` 是作者本人的一次性点云数据处理实验，未包含在发行包中，目前也没有维护。

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
