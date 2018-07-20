# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:52:13 2018

@author: Lynn
"""
import math
from collections import deque
from pyglet import image
import pyglet
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse
from mcworld import World
from mcplayer import Player

TICKS_PER_SEC = 60
TEXTURE_PATH='texture.png'

class Window(pyglet.window.Window):
    worldsize=80
    batch=pyglet.graphics.Batch()
    group=TextureGroup(image.load(TEXTURE_PATH).get_texture())
    world={}
    shown={}
    _shown={}
    sectors={}
    queue=deque()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.exclusive = False
        
        self.strafe = [0, 0]
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))
        self.myworld=World(self.worldsize,
                        self.batch,
                        self.group,
                        self.world,
                        self.shown,
                        self._shown,
                        self.sectors,
                        self.queue)
        self.player=Player()
        self.player.setRotation((0,0))
        self.player.setPosition((0,0,0))
        self.player.setSector(None)
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        
        
    def update(self,dt):
        self.myworld.processQueue()
        sector=self.myworld.sectorize(self.player.position)
        if sector!=self.player.sector:
            self.myworld.changeSectors(self.player.sector,sector)
            if self.player.sector is None:
                self.myworld.processEntireQueue()
            self.player.setSector(sector)
        m=8
        dt=min(dt,0.2)
        for _ in range(m):
            self.player.updatePlayer(dt/m,self.strafe)
            position=self.collide(self.player.position,self.player.PLAYER_HEIGHT)
            self.player.setPosition(position)
            
    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)  #当前位置
        np = self.myworld.normalize(position)    #把位置数据整数化
        for face in self.myworld.FACES:  # check all surrounding blocks
            for i in range(3):  # check each dimension independently
                if not face[i]: #检测到1跳过
                    continue
                # How much overlap you have with this dimension.检测在这个方向上有多少重叠的部分
                d = (p[i] - np[i]) * face[i]    #face控制前后
                
                if d < pad:
                    continue
                for dy in range(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.把速度将为0
                        self.player.setDy(0)
                    break
        return tuple(p)
        
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.exclusive:
#            vector = self.get_sight_vector()
#            block, previous = self.model.hit_test(self.position, vector)    #返回视线矢量方向上的检测到的块
#            if (button == mouse.RIGHT) or \
#                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
#                # ON OSX, control + left click = right click.
#                if previous:
#                    self.model.add_block(previous, self.block)
#            elif button == pyglet.window.mouse.LEFT and block:
#                texture = self.model.world[block]
#                if texture != STONE:
#                    self.model.remove_block(block)
            pass
        else:
            self.set_exclusive_mouse(True)
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            m = 0.15    #鼠标灵敏度
            x, y = self.player.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))    #限制y的范围
            self.player.rotation = (x, y)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.player.dy == 0:
                self.player.setDy(self.player.JUMP_SPEED)
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.player.flying = not self.player.flying
        
    
    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
    
    def on_resize(self, width, height):
        pass
    
    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
#        x, y, z = self.position
        xx,yy=self.player.rotation
        x,y,z=self.player.position
        self.label.text = '%02d  (%.2f, %.2f, %.2f)  %0.2f / %0.2f' % (
            pyglet.clock.get_fps(),x,y,z,xx,yy
            )
        self.label.draw()
    
    def on_draw(self):
        self.clear()
        self.set3d()
        pyglet.gl.glColor3d(1, 1, 1)
        self.batch.draw()
#        self.draw_focused_block()
        self.set2d()
        self.draw_label()
#        self.draw_reticle()
    
    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super().set_exclusive_mouse(exclusive)
        self.exclusive = exclusive
        
    def setupFog(self):
        """ Configure the OpenGL fog properties.
    
        """
        # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
        # post-texturing color."
        pyglet.gl.glEnable(pyglet.gl.GL_FOG)
        # Set the fog color.
        pyglet.gl.glFogfv(pyglet.gl.GL_FOG_COLOR, (pyglet.gl.GLfloat * 4)(0.5, 0.69, 1.0, 1))
        # Say we have no preference between rendering speed and quality.
        pyglet.gl.glHint(pyglet.gl.GL_FOG_HINT, pyglet.gl.GL_DONT_CARE)
        # Specify the equation used to compute the blending factor.
        pyglet.gl.glFogi(pyglet.gl.GL_FOG_MODE, pyglet.gl.GL_LINEAR)
        # How close and far away fog starts and ends. The closer the start and end,
        # the denser the fog in the fog range.
        pyglet.gl.glFogf(pyglet.gl.GL_FOG_START, 20.0)
        pyglet.gl.glFogf(pyglet.gl.GL_FOG_END, 60.0)
    
    def set2d(self):
        """ Configure OpenGL to draw in 2d.

        """
        width, height = self.get_size()
        pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glLoadIdentity()
        
    def set3d(self):
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(65.0, width / height, 0.1, 60.0)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glLoadIdentity()
        x, y = self.player.rotation
#        x, y = 120, -50
        pyglet.gl.glRotatef(x, 0, 1, 0)
        pyglet.gl.glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
#        x, y, z = self.position
        x,y,z= self.player.position
        pyglet.gl.glTranslatef(-x, -y, -z)
        
    def setUp(self):
        """ Basic OpenGL configuration.
    
        """
        # Set the color of "clear", i.e. the sky, in rgba.
        pyglet.gl.glClearColor(0.5, 0.69, 1.0, 1)
        # Enable culling (not rendering) of back-facing facets -- facets that aren't
        # visible to you.
        pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
        # Set the texture minification/magnification function to GL_NEAREST (nearest
        # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
        # "is generally faster than GL_LINEAR, but it can produce textured images
        # with sharper edges because the transition between texture elements is not
        # as smooth."
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
        self.setupFog()
        
        

        
        
def main():
    window = Window(width=800, height=600, caption='Pyglet', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
#    window.set_exclusive_mouse(True)
    window.setUp()
    pyglet.app.run()


if __name__ == '__main__':
    main()