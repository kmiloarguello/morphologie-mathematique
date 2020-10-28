# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 16:58:16 2020

@author: Edison
"""

from utils import *

#%%
# Images binaire
im1=skio.imread('Images/cellbin.bmp')
#im1=skio.imread('Images/bat200.bmp')
#im1=skio.imread('Images/cafe.bmp')
#im1=skio.imread('Images/retina2.gif')
#im1=skio.imread('Images/bulles.bmp')
#im1=skio.imread('Images/laiton.bmp')

# Images à niveaux de gris
#im=skio.imread('Images/cailloux1.png')
#im=skio.imread('Images/cailloux2.png')


## np.max (...)

plt.imshow(im1,cmap="gray")

#
# viewimage(im) - Utilisable à la place de plt.imshow si Gimp est installé.

se1=strel('disk',2)

# dilatation
dil=morpho.dilation(im1,se1)
plt.imshow(dil,cmap="gray")

# erosion
ero=morpho.erosion(im1,se1)
plt.imshow(ero,cmap="gray")

#ouverture
_open=morpho.opening(im1,se1)
plt.imshow(_open,cmap="gray")

#fermeture
#_close=morpho.closing(im1,se1)
#plt.imshow(_close,cmap="gray")