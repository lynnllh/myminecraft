# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:21:00 2018

@author: Lynn
"""

from mcenvironment import Environment

from pyglet.gl import GL_QUADS
class Block(Environment):
    '''
    block类是minecraft中最基本的元素，即方块
    '''
    
    
    
    
    def __init__(self,worldsize,batch,group,world,shown,_shown,sectors,queue):
        '''
        '''
        super().__init__()
        self.worldsize=worldsize
        self.batch=batch
        self.group=group
        self.world=world
        self.shown=shown
        self._shown=_shown
        self.sectors=sectors
        self.queue=queue
#    def setTexture(self,texture):
#        if texture=='GRASS':
#            self.texture=self.tex_coords((1, 0), (0, 1), (0, 0))
#        elif texture=='SAND':
#            self.texture=self.tex_coords((1, 1), (1, 1), (1, 1))
#        elif texture=='BRICK':
#            self.texture=self.tex_coords((2, 0), (2, 0), (2, 0))
#        elif texture=='STONE':
#            self.texture=self.tex_coords((2, 1), (2, 1), (2, 1))
#        elif texture=='WATER':
#            pass
#        elif texture=='CLOUD':
#            pass
        
#    def setWorld(self,world):
#        self.world=world
#        
#    def setGroup(self,group):
#        self.group=group
#        
#    def setShown(self,shown):
#        self.shown=shown
#        
#    def set_Shown(self,_shown):
#        self._shown=_shown
#        
#    def setSectors(self,sectors):
#        self.sectors=sectors
#        
#    def setQueue(self,queue):
#        self.queue=queue
#        
#    def setBatch(self,batch):
#        self.batch=batch
        
#    def setGl_quads(self,GL_QUADS):
#        self.GL_QUADS=GL_QUADS
    def isExisted(self,position):
        x,y,z=position
        if x in range(-self.worldsize,self.worldsize+1) and z in range(-self.worldsize,self.worldsize+1):
            return True

        else:
            return False
            
        
    def setDy(self,dy):
        self.dy=dy
        
    def getTextureData(self,texture):
        if texture=='GRASS':
            return list(self.tex_coords((1, 0), (0, 1), (0, 0)))
        elif texture=='SAND':
            return list(self.tex_coords((1, 1), (1, 1), (1, 1)))
        elif texture=='BRICK':
            return list(self.tex_coords((2, 0), (2, 0), (2, 0)))
        elif texture=='STONE':
            return list(self.tex_coords((2, 1), (2, 1), (2, 1)))
        elif texture=='WATER':
            return list(self.tex_coords((3, 0), (3, 0), (3, 0)))
        elif texture=='CLOUD':
            return list(self.tex_coords((3, 1), (3, 1), (3, 1)))
        elif texture=='SOIL':
            return list(self.tex_coords((0, 1), (0, 1), (0, 1)))
        
    def getVertexData(self,position):
        x,y,z = position
        return self.cube_vertices(x,y,z,0.5)
        
    
    
    @staticmethod
    def cube_vertices(x, y, z, n):
        """ Return the vertices of the cube at position x, y, z with size 2*n.
    
        """
        return [
            x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
            x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
            x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
            x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
            x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
            x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
        ]
    
    @staticmethod
    def tex_coord(x, y, n=4):
        """ Return the bounding vertices of the texture square.
    
        """
        m = 1.0 / n
        dx = x * m
        dy = y * m
        return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m
    
    
    def tex_coords(self,top, bottom, side):
        """ Return a list of the texture squares for the top, bottom and side.
    
        """
        top = self.tex_coord(*top)
        bottom = self.tex_coord(*bottom)
        side = self.tex_coord(*side)
        result = []
        result.extend(top)
        result.extend(bottom)
        result.extend(side * 4)
        return result

    def hitTest(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = self.normalize((x, y, z))                      #把position整数化
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m    #在当前位置上加上一个视线矢量的偏移（由近及远）
        return None, None
        
        
    def exposed(self,position):
        x,y,z=position
        for dx,dy,dz in self.FACES:
            if (x+dx,y+dy,z+dz) not in self.world:
                return True
        return False
        
    def checkNeighbors(self, position):
        x,y,z=position
        for dx,dy,dz in self.FACES:
            key=(x+dx,y+dy,z+dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show(key)
            else:
                if key in self.shown:
                    self.hide(key)
                    
    def _enqueue(self,func,*args):
        self.queue.append((func,args))

    def _dequeue(self):
        func, args=self.queue.popleft()
        func(*args)
        
    def add(self,position,texture,immediate=True):
        '''
        '''
        if self.isExisted(position):
            if position in self.world:
                if self.world[position]==texture:
                    return
                else:
                    self.remove(position,immediate)
            self.world[position]=texture
            self.sectors.setdefault(self.sectorize(position),[]).append(position)
            if immediate:
                if self.exposed(position):
                    self.show(position)
                self.checkNeighbors(position)
    
    def remove(self,position,immediate=True):
        '''
        '''
        del self.world[position]
        self.sectors[self.sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide(position)
            self.checkNeighbors(position)
    
    def hide(self,position,immediate=True):
        '''
        '''
        self.shown.pop(position)
        if immediate:
            self._hide(position)
        else:
            self._enqueue(self._hide, position)
     
    def _hide(self,position):
        self._shown.pop(position).delete()
        
    def show(self, position, immediate=True):
        '''
        '''
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show(position, texture)
        else:
            self._enqueue(self._show, position, texture)

    def _show(self, position, texture):
        vertex_data=self.getVertexData(position)
        texture_data=self.getTextureData(texture)
        self._shown[position]=self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))
        
#    def showSector(self,sector):
#        for position in self.sectors.get(sector, []):
#            if position not in self.shown and self.exposed(position):
#                self.show(position, False)
#                
#    def hideSector(self,sector):
#        for position in self.sectors.get(sector, []):
#            if position in self.shown:
#                self.hide(position, False)
#                
#    def changeSectors(self,before,after):
#        before_set = set()
#        after_set = set()
#        pad = 4
#        for dx in range(-pad, pad + 1):
#            for dy in [0]:  # xrange(-pad, pad + 1):
#                for dz in range(-pad, pad + 1):
#                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
#                        continue
#                    if before:
#                        x, y, z = before
#                        before_set.add((x + dx, y + dy, z + dz))
#                    if after:
#                        x, y, z = after
#                        after_set.add((x + dx, y + dy, z + dz))
#        show = after_set - before_set
#        hide = before_set - after_set
#        for sector in show:
#            self.showSector(sector)
#        for sector in hide:
#            self.hideSector(sector)
            
#    def processQueue(self):
#        start=time.clock()
#        while self.queue and time.clock() - start < 1 / 60:
#            self._dequeue()
#            
#    def processEntireQueue(self):
#        while self.queue:
#            self._dequeue()
            
    def drop(self,position,dt):
        x,y,z=position
        self.dy-=dt*self.gravity
        self.dy=max(self.dy,-self.TERMINAL_VELOCITY)
        y+=self.dy*dt
        return self.collide((x,y,z))
        
    def collide(self,position):
        pad = 0.25
        p = list(position)  #当前位置
        np = self.normalize(position)    #把位置数据整数化
        for face in self.FACES:  # check all surrounding blocks
            for i in range(3):  # check each dimension independently
                if not face[i]: #检测到1跳过
                    continue
                # How much overlap you have with this dimension.检测在这个方向上有多少重叠的部分
                d = (p[i] - np[i]) * face[i]    #face控制前后
                
                if d < pad:
                    continue
                
                op = list(np)
                op[i] += face[i]
                if tuple(op) not in self.model.world:
                    continue
                p[i] -= (d - pad) * face[i]
                if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.把速度将为0
                        self.dy = 0
                break
        return tuple(p)