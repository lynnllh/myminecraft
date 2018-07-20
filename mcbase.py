# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:57:04 2018

@author: Lynn
"""
from mcblock import Block
import random
import math
class Base(Block):
    
    
        
#        self.generateBase()
        
    def generateBase(self):
        r=self.worldsize
        c=math.sqrt(2)/2
        for x in range(-r,r+1):
            for z in range(-r,r+1):
                self.add((x,-6,z),'STONE',immediate=False)
                for y in range(-5,-1):
                    if (c*(z-x)+1.2*r)**2/(3/2*r)**2 + y**2/3**2 + (c*(z+x))**2/(0.8*r)**2 <1:
#                    if (x-10)**2/(3/2*r)**2 + y**2/4**2 + (z-10)**2/(r/2)**2 <1:
                        self.add((x,y,z),'WATER',immediate=False)
                    else:
                        if y==-2:
                            self.add((x,y,z),'GRASS',immediate=False)
                        else:
                            self.add((x,y,z),random.choice(['SOIL','SAND','SOIL']),immediate=False)
                    
                        
                        
        
                 