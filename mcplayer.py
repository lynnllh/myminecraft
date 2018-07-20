# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 20:51:13 2018

@author: Lynn
"""
import math
from mcenvironment import Environment
class Player(Environment):
    
    def __init__(self):
        super().__init__()
        self.rotation=(0,0)
        self.position = (0, 0, 0)
        self.sector=None
        self.WALKING_SPEED = 5
        self.FLYING_SPEED = 15
        self.MAX_JUMP_HEIGHT = 1.0
        self.JUMP_SPEED = math.sqrt(2 * self.gravity * self.MAX_JUMP_HEIGHT)
        self.PLAYER_HEIGHT = 2
        self.flying = False
        self.dy = 0
    
    def setDy(self,dy):
        self.dy=dy
        
    def setSector(self,sector):
        self.sector=sector
        
    def setRotation(self,rotation):
        self.rotation=rotation
    
    def setPosition(self,position):
        self.position=position
        
    def getSightVector(self):
        x,y=self.rotation
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x-90)) * m
        dz = math.sin(math.radians(x-90)) * m
        return (dx, dy, dz)
        
    def getMotionVector(self,strafe):
        if any(strafe):
            x, y = self.rotation
            thisStrafe = math.degrees(math.atan2(*strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + thisStrafe)

            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)
        
    def updatePlayer(self,dt,strafe):
        speed = self.FLYING_SPEED if self.flying else self.WALKING_SPEED
        d = dt * speed # distance covered this tick.
        dx, dy, dz = self.getMotionVector(strafe)
        dx, dy, dz = dx * d, dy * d, dz * d
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * self.gravity
            self.dy = max(self.dy, -self.TERMINAL_VELOCITY)
            dy += self.dy * dt
        x, y, z = self.position
        self.position = (x+dx, y+dy, z+dz)
        

        