# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 16:59:49 2018

@author: Lynn
"""
from mcblock import Block
import random
import math
class Hill(Block):
    
   
        
    def _generateHill(self,position):
        x,y,z=position
        if x**2 + z**2 < 25**2:
            return
        length=random.randint(6,20)
        width=random.randint(5,15)
        height=random.randint(1,10)
        theta=random.randint(0,180)
        theta=math.radians(theta)
        past=None
        for dy in range(-2,height+1):
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
                        if dz**2/(width-2)**2 + dx**2/(length-2)**2 > 1 or dy==height or (width in (3,4)) or (length in (3,4)):
                            
                            texture='GRASS'
                                                
                        else:
                            texture=random.choice(['SOIL','SOIL','SAND'])
                    

                        self.add(now,texture,False)
                    past=now
                          
            length-=random.randint(0,2)
            width-=random.randint(0,2)
                    
    def generateHill(self,position):
        x,y,z=position
        self._generateHill((x+random.randint(-5,5),y,z+random.randint(-5,5)))
        self._generateHill((x+random.randint(-5,5),y,z+random.randint(-5,5)))
        self._generateHill((x+random.randint(-5,5),y,z+random.randint(-5,5)))


        
                        
                            
                    