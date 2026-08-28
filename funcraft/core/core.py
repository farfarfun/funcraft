import mcpi.block
from mcpi.block import Block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3


class MineCraftConn:
    """The main class to interact with a running instance of Minecraft Pi."""

    def __init__(self, mc: Minecraft = None):
        self.mc = mc or Minecraft.create()

    def get_block(self, x, y, z) -> int:
        """Get block (x,y,z) => id:int"""
        return self.mc.getBlocks(x, y, z)

    def get_block_with_data(self, x, y, z) -> Block:
        """Get block with data (x,y,z) => Block"""
        return self.mc.getBlockWithData(x, y, z)

    def get_blocks(self, x0, y0, z0, x1, y1, z1) -> dict:
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        return self.mc.getBlocks(x0, y0, z0, x1, y1, z1)

    def set_block(self, x, y, z, id, data=None):
        """Set block (x,y,z,id,[data])"""
        return self.mc.setBlock(x, y, z, id, data)

    def set_block_vec(self, pos: Vec3, id):
        return self.set_block(pos.x, pos.y, pos.z, id)

    def set_blocks(self, x0, y0, z0, x1, y1, z1, id):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        return self.mc.setBlocks(x0, y0, z0, x1, y1, z1, id)

    def set_blocks_vec(self, start: Vec3, end: Vec3, id):
        return self.set_blocks(start.x, start.y, start.z, end.x, end.x, end.z, id)

    def set_sign(self, x, y, z, id, data, line1=None, line2=None, line3=None, line4=None):
        """Set a sign (x,y,z,id,data,[line1,line2,line3,line4])

        Wall signs (id=68) require data for facing direction 2=north, 3=south, 4=west, 5=east
        Standing signs (id=63) require data for facing rotation (0-15) 0=south, 4=west, 8=north, 12=east
        @author: Tim Cummings https://www.triptera.com.au/wordpress/"""
        return self.mc.setSign(x, y, z, id, data, [line1, line2, line3, line4])

    def spawn_entity(self, x, y, z, id) -> int:
        """Spawn entity (x,y,z,id)"""
        return self.mc.spawnEntity(x, y, z, id)

    def get_height(self, x, z) -> int:
        """Get the height of the world (x,z) => int"""
        return self.mc.getHeight(x, z)

    def get_player_entity_ids(self) -> list:
        """Get the entity ids of the connected players => [id:int]"""
        return self.mc.getPlayerEntityIds()

    def get_player_entity_id(self, name) -> int:
        """Get the entity id of the named player => [id:int]"""
        return self.mc.getPlayerEntityId(name)

    def save_checkpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        return self.mc.saveCheckpoint()

    def restore_checkpoint(self):
        """Restore the world state to the checkpoint"""
        return self.mc.restoreCheckpoint()

    def post_to_chat(self, msg):
        """Post a message to the game chat"""
        return self.mc.postToChat(msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        return self.mc.setting(setting, status)

    def get_entity_types(self):
        """Return a list of Entity objects representing all the entity types in Minecraft"""
        return self.mc.getEntityTypes()

    def get_entities(self, typeId=-1):
        """Return a list of all currently loaded entities (EntityType:int) => [[entityId:int,entityTypeId:int,entityTypeName:str,posX:float,posY:float,posZ:float]]"""
        return self.mc.getEntities(typeId)

    def remove_entity(self, id):
        """Remove entity by id (entityId:int) => (removedEntitiesCount:int)"""
        return self.mc.removeEntity(id)

    def remove_entities(self, typeId=-1):
        """Remove entities all currently loaded Entities by type (typeId:int) => (removedEntitiesCount:int)"""
        return self.mc.removeEntities(typeId)

    @staticmethod
    def create(address="localhost", port=4711):
        return MineCraftConn(Minecraft.create(address, port))


class Cell:
    conn = MineCraftConn.create()

    def __init__(self, mc: Minecraft = None, pos=None, block=mcpi.block.WOOD, msg='cell'):
        if mc is not None:
            Cell.conn = MineCraftConn(mc) or MineCraftConn.create()

        self._children = []
        self.pos = pos
        self.block = block
        self.msg = msg

    def add_child(self, child):
        self._children.append(child)

    def build(self, *args, **kwargs):
        self._build(*args, **kwargs)
        for node in self._children:
            if isinstance(node, Cell):
                node.build()
        self.conn.post_to_chat("build {} success!".format(self.msg))

    def _build(self, *args, **kwargs):
        raise Exception('Not implement yet!')
