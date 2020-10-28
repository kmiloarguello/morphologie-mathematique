# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:06:54 2020

@author: CA
"""

from utils import *

#%% reconstruction
_im3=skio.imread('Images/retina2.gif')
_se3=strel('diamond',10)
_open3=morpho.opening(_im3,_se3)
_reco3=morpho.reconstruction(_open3,_im3)
plt.imshow(_reco3,cmap="gray")

#%% Point 3.2
im2=skio.imread('Images/retina2.gif')
_imt=im2.copy()
_imt2=im2.copy()
N=5
for k in range(N):
    _se2=strel('diamond',k)
    
    _ouv = morpho.opening(_imt2,_se2)
    _fer = morpho.closing(_ouv,_se2)
    
    f = morpho.reconstruction(morpho.opening(_imt,_se2),_imt,method='dilation')
    fp = morpho.reconstruction(morpho.closing(f,_se2),f,method='erosion')
    
    _imt = fp.copy()
    _imt2 = _fer.copy()

#plt.imshow(_imt2,cmap="gray")
plt.imshow(_imt,cmap="gray")


