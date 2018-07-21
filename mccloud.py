# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 21:52:02 2018

@author: Lynn
"""
from mcblock import Block
import math
import random
class Cloud(Block):
    
    
    def _generateCloud(self,position):
        x,y,z=position
        length=random.randint(2,10)
        width=random.randint(2,8)
        height=random.randint(1,6)
        theta=random.randint(60,120)
        theta=math.radians(theta)
        past=None
        for dy in range(height,-3,-1):
            for dx in range(-round(1.4*length),round(1.4*length)+1):
                dx=dx/1.4
                for dz in range(-round(1.4*width),round(1.4*width)+1):
                    dz=dz/1.4
                    if width in (1,2) or length in (1,2):
                        return
                    nx=math.cos(theta)*(dx)-math.sin(theta)*(dz)+x
                    ny=y+dy
                    nz=math.sin(theta)*(dx)+math.cos(theta)*(dz)+z
                    now=self.normalize((nx,ny,nz))
                    if now==past:
                        continue
                    if dz**2/width**2 + dx**2/length**2 < 1 :
                                      
                        self.add(now,'CLOUD',False)
                    past=now
                          
            length-=random.randint(0,2)
            width-=random.randint(0,2)
            
    def generateCloud(self,position):
        x,y,z=position
        self._generateCloud((x+random.randint(-2,2),y,z+random.randint(-2,2)))
        self._generateCloud((x+random.randint(-2,2),y,z+random.randint(-2,2)))
        self._generateCloud((x+random.randint(-2,2),y,z+random.randint(-2,2)))
        
    def generateClouds(self):
        r=self.worldsize
        num=random.randint(round(r**2/200),round(r**2/50))
        for _ in range(num):
            x=random.randint(-r,r+1)
            y=random.randint(20,30)
            z=random.randint(-r,r+1)
            self.generateCloud((x,y,z))
        