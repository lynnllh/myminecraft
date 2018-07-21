# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:32:32 2018

@author: Lynn
"""

class Environment:
    '''
    设置整个世界的物理参数
    '''
    def __init__(self):
        self.gravity=9.8
        self.SECTOR_SIZE=16
        self.FACES = [
                        ( 0, 1, 0),
                        ( 0,-1, 0),
                        (-1, 0, 0),
                        ( 1, 0, 0),
                        ( 0, 0, 1),
                        ( 0, 0,-1),
                        ]
        self.TERMINAL_VELOCITY = 50
                        
        
    @staticmethod
    def normalize(position):
        #把位置变成整数
        """ Accepts `position` of arbitrary precision and returns the block
        containing that position.
    
        Parameters
        ----------
        position : tuple of len 3
    
        Returns
        -------
        block_position : tuple of ints of len 3
    
        """
        x, y, z = position
        x, y, z = (round(x), round(y), round(z))
        return (x, y, z)
    
    
   
    def sectorize(self,position):
        #区域化，把世界划分为一个个的小区域，默认区域大小为16*16，只划分平面
        """ Returns a tuple representing the sector for the given `position`.
    
        Parameters
        ----------
        position : tuple of len 3
    
        Returns
        -------
        sector : tuple of len 3
    
        """
        x, y, z = self.normalize(position)
        x, y, z = x // self.SECTOR_SIZE, y // self.SECTOR_SIZE, z // self.SECTOR_SIZE
        return (x, 0, z)
        
        
        