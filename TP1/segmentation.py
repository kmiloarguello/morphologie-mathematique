# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 18:20:53 2020

@author: CA
"""

from utils import *


#%% 1. gradient morphologique
im1=skio.imread('Images/bat200.bmp')
se1=strel('disk',1)

dil1=morpho.dilation(im1,se1)
ero1=morpho.erosion(im1,se1)

gm1 = dil1 - ero1

plt.imshow(gm1,cmap="gray")


#%% ligne de partage des eaux
im2=skio.imread('Images/laiton.bmp')
se2=morpho.selem.disk(2)

grad=morpho.dilation(im2,se2) - morpho.erosion(im2,se2)
grad=np.int32(grad > 40) * grad
plt.imshow(grad,cmap="gray")

#local_mini = skf.peak_local_max(255-grad, #il n'y a pas de fonction local_min...
#                            indices=False)
#markers = ndi.label(local_mini)[0]
#plt.imshow(local_mini,cmap="gray")

#%
#local_mini2 = morpho.opening(local_mini,se)
#plt.imshow(local_mini2,cmap="gray")

#%
#labels = morpho.watershed(grad, markers,watershed_line=True)
#plt.imshow(couleurs_alea(labels))
# viewimage_color(couleurs_alea(labels)) - Utilisable si gimp est installé

# visualiation du resultat
#segm=labels.copy()
#for i in range(segm.shape[0]):
#    for j in range(segm.shape[1]):
#        if segm[i,j] == 0: 
#            segm[i,j]=255
#        else:
#            segm[i,j]=0
#superposition des contours de la segmentation a l'image initiale
#contourSup=np.maximum(segm,im)
#plt.imshow(contourSup,cmap="gray") 