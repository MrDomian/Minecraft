from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
wood_texture = load_texture('assets/wood_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
bedrock_texture = load_texture('assets/bedrock_block.png')
leaves_texture = load_texture('assets/leaves_block.png')
sky_texture = load_texture('assets/sky.png')
arm_texture = load_texture('assets/arm_texture.png')
block_build = Audio('assets/block_build.ogg', loop=False, autoplay=False)
block_break = Audio('assets/block_break.ogg', loop=False, autoplay=False)
block_pick = 1

window.fps_counter.enabled = False


def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']: hand.active()
    else: hand.passive()

    if held_keys['escape']: app.quit()
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5
    if held_keys['6']: block_pick = 6


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), textures=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=textures,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.light_gray,
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                block_build.play()
                if block_pick == 1: Voxel(position=self.position + mouse.normal, textures=grass_texture)
                if block_pick == 2: Voxel(position=self.position + mouse.normal, textures=dirt_texture)
                if block_pick == 3: Voxel(position=self.position + mouse.normal, textures=stone_texture)
                if block_pick == 4: Voxel(position=self.position + mouse.normal, textures=wood_texture)
                if block_pick == 5: Voxel(position=self.position + mouse.normal, textures=bedrock_texture)
                if block_pick == 6: Voxel(position=self.position + mouse.normal, textures=leaves_texture)
            elif key == 'right mouse down':
                block_break.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=250,
            double_sided=True,
        )


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.5, -0.5)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


def terrain(num_x=15, num_y=3, num_z=15):
    for x in range(num_x):
        for z in range(num_z):
            Voxel(position=(x, 0, z), textures=grass_texture)
            for y in range(num_y):
                Voxel(position=(x, -y-1, z), textures=stone_texture)
                if y == 0:
                    Voxel(position=(x, y-num_y-1, z), textures=bedrock_texture)


terrain()
player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
