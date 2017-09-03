# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 00:40:50 2017

@author: asus1
"""

import numpy as np
import matplotlib.pyplot as plt
#
#plt.axis([0, 100, 0, 1])
#plt.ion()
#
#for i in range(100):
#    y = np.random.random()
#    plt.scatter(i, y)
#    plt.pause(0.1)
    
fig,ax=plt.figure()
fig2,ax2=plt.subplots()


y1=[]
y2=[]

for i in range(50):
    y1.append(np.sin(i))
    y2.append(np.cos(i))
    ax.cla()
    ax.set_title("Loss")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Loss")
    ax.set_xlim(0,55)
    ax.set_ylim(-1,1)
    ax.grid()
    ax.plot(y1,label='train')
    ax.plot(y2,label='test')
    ax.legend(loc='best')
    ax2.cla()
    ax2.set_title("Loss")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Loss")
    ax2.set_xlim(0,55)
    ax2.set_ylim(-1,1)
    ax2.grid()
    ax2.plot(y1,label='train')
    ax2.plot(y2,label='test')
    ax2.legend(loc='best')
    plt.pause(0.1)