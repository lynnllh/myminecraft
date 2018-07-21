# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 17:13:18 2018

@author: Lynn
"""

from mcblock import Block
import random
import math
class Landscape(Block):
    
   
        
    def _generateLandscape(self,position):
        x,y,z=position
        if x**2 + z**2 < 18**2:
            return
        length=random.randint(15,20)
        width=random.randint(10,15)
        height=random.randint(-1,0)
        theta=random.randint(0,180)
        theta=math.radians(theta)
        past=None
        for dy in range(-2,height+1):
            for dx in range(-round(1.4*length),round(1.4*length)+1):
                dx=dx/1.4
                for dz in range(-round(1.4*width),round(1.4*width)+1):
                    dz=dz/1.4
                    
                    nx=math.cos(theta)*(dx)-math.sin(theta)*(dz)+x
                    ny=y+dy
                    nz=math.sin(theta)*(dx)+math.cos(theta)*(dz)+z
                    now=self.normalize((nx,ny,nz))
                    if now==past:
                        continue
                    if dz**2/width**2 + dx**2/length**2 < 1 :
                        if dz**2/(width-3)**2 + dx**2/(length-3)**2 > 1 or dy==height:
                            
                            texture='GRASS'
                                                
                        else:
                            texture=random.choice(['SOIL','SOIL','SAND'])
                    

                        self.add(now,texture,False)
                    past=now
                          
            length-=random.randint(1,3)
            width-=random.randint(1,3)
                    
    def generateLandscape(self,position):
        x,y,z=position
        self._generateLandscape((x+random.randint(-5,5),y,z+random.randint(-5,5)))
        self._generateLandscape((x+random.randint(-5,5),y,z+random.randint(-5,5)))
        self._generateLandscape((x+random.randint(-5,5),y,z+random.randint(-5,5)))


        
                        
                            
                    