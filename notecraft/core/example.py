import mcpi.block
import pandas as pd
from mcpi.minecraft import Minecraft
from plyfile import PlyData

BUILDER_NAME = "niult"

MC_SEVER_HOST = "0.0.0.0"
MC_SEVER_PORT = 4711

mc = Minecraft.create(address=MC_SEVER_HOST, port=MC_SEVER_PORT)
p = mc.entity.getTilePos(mc.getPlayerEntityId(BUILDER_NAME))


def t1():
    from notecraft.core.things import River, Wall
    print(p)
    Wall(mc=mc, pos=p).build()

    River(mc=mc, pos=p).build()


def t2():
    file_dir = '/Users/liangtaoniu/workspace/dataset/ply/data_qinghuamenG.ply'  # 文件的路径
    plydata = PlyData.read(file_dir)
    data = plydata.elements[0].data
    data_pd = pd.DataFrame(data)

    data_pd['x'] = round(data_pd['x'] * 30)
    data_pd['y'] = round(data_pd['y'] * 30)
    data_pd['z'] = round(data_pd['z'] * 30)

    data_pd['x'] = p.x + data_pd['x'] - min(data_pd['x'])
    data_pd['y'] = p.y + data_pd['y'] - min(data_pd['y'])
    data_pd['z'] = p.z + data_pd['z'] - min(data_pd['z'])

    data_pd = data_pd.drop_duplicates()
    # mc.setBlocks(p.x, p.y, p.z, max(data_pd['x']), max(data_pd['y']), max(data_pd['z']), mcpi.block.AIR)
    # return
    num = 0
    for line in data_pd.values:

        mc.setBlock(line[0], line[1], line[2], mcpi.block.BRICK_BLOCK.id)
        if num % 1000 == 0:
            print(num, line)
        if num > 1000000:
            break

        num += 1


mc.postToChat('success')

# t1()
t2()
