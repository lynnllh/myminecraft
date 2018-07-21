# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:44:49 2018

@author: Lynn
"""
from mcenvironment import Environment
from mcbase import Base
from mchill import Hill
from mcblock import Block
from mccloud import Cloud
from mclandscape import Landscape
import random
import time
import math

class World(Environment):
    
    def __init__(self,worldsize,batch,group,world,shown,_shown,sectors,queue):
        super().__init__()
        self.worldsize=worldsize
        self.queue=queue
        self.world=world
        self.shown=shown
        self._shown=_shown
        self.sectors=sectors
        self.block=Block(worldsize,batch,group,world,shown,_shown,sectors,queue)
        self.base=Base(worldsize,batch,group,world,shown,_shown,sectors,queue)
        self.hill=Hill(worldsize,batch,group,world,shown,_shown,sectors,queue)
        self.landscape=Landscape(worldsize,batch,group,world,shown,_shown,sectors,queue)
        self.cloud=Cloud(worldsize,batch,group,world,shown,_shown,sectors,queue)
        self.base.generateBase()
        self.generateLandscapes()
        self.generateHills()
        self.cloud.generateClouds()
        
#        self.hill.generateHill((40,0,40))
        
    
    def generateLandscapes(self):
        r=self.worldsize
        c=math.sqrt(2)/2
        num=random.randint(round(r**2/750),round(r**2/300))
        for _ in range(num):
            x=random.randint(-r,r+1)
            y=0
            z=random.randint(-r,r+1)
            if (c*(z-x)+1.2*r)**2/(3/2*r-6)**2 +  (c*(z+x))**2/(0.8*r-6)**2 >1:
           
                self.landscape.generateLandscape((x,y,z))
                
                
                
    def generateHills(self):
        count=1
        r=self.worldsize
        c=math.sqrt(2)/2
        num=random.randint(round(r**2/350),round(r**2/100))
        print(num)
        for _ in range(num):
            x=random.randint(-r,r+1)
            y=0
            z=random.randint(-r,r+1)
            if (c*(z-x)+1.2*r)**2/(3/2*r-25)**2 +  (c*(z+x))**2/(0.8*r-25)**2 <1:
                if count<2:
                    self.hill.generateHill((x,y,z))
                    count+=1
                    print(1)
            else:
                self.hill.generateHill((x,y,z))
                print(1)
            
        
    def _enqueue(self,func,*args):
        self.queue.append((func,args))

    def _dequeue(self):
        func, args=self.queue.popleft()
        func(*args)
    
    def processQueue(self):
        start=time.clock()
        while self.queue and time.clock() - start < 1 / 60:
            self._dequeue()
            
    def processEntireQueue(self):
        while self.queue:
            self._dequeue()
    
    def showSector(self,sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.block.exposed(position):
                self.block.show(position, False)
                
    def hideSector(self,sector):
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.block.hide(position, False)
            
    def changeSectors(self,before,after):
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:  # xrange(-pad, pad + 1):
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.showSector(sector)
        for sector in hide:
            self.hideSector(sector)
    