#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 10:23:50 2018
Modified Oct 2020

@author: Said,Isabelle
"""


#%% SECTION 1 inclusion de packages externes 

import numpy as np
import platform
import tempfile
import os
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
# necessite scikit-image 
from skimage import io as skio


# POUR LA MORPHO
import skimage.morphology as morpho  
import skimage.feature as skf
from scipy import ndimage as ndi

#%% SECTION 2 fonctions utiles pour le TP

def viewimage(im,normalise=True,MINI=0.0, MAXI=255.0):
    """ Cette fonction fait afficher l'image EN NIVEAUX DE GRIS 
        dans gimp. Si un gimp est deja ouvert il est utilise.
        Par defaut normalise=True. Et dans ce cas l'image est normalisee 
        entre 0 et 255 avant d'être sauvegardee.
        Si normalise=False MINI et MAXI seront mis a 0 et 255 dans l'image resultat
        
    """
    imt=np.float32(im.copy())
    if platform.system()=='Darwin': #on est sous mac
        prephrase='open -a GIMP '
        endphrase=' ' 
    else: #SINON ON SUPPOSE LINUX (si vous avez un windows je ne sais comment faire. Si vous savez dites-moi.)
        prephrase='gimp '
        endphrase= ' &'
    
    if normalise:
        m=imt.min()
        imt=imt-m
        M=imt.max()
        if M>0:
            imt=imt/M

    else:
        imt=(imt-MINI)/(MAXI-MINI)
        imt[imt<0]=0
        imt[imt>1]=1
    
    nomfichier=tempfile.mktemp('TPIMA.png')
    commande=prephrase +nomfichier+endphrase
    skio.imsave(nomfichier,imt)
    os.system(commande)

def viewimage_color(im,normalise=True,MINI=0.0, MAXI=255.0):
    """ Cette fonction fait afficher l'image EN NIVEAUX DE GRIS 
        dans gimp. Si un gimp est deja ouvert il est utilise.
        Par defaut normalise=True. Et dans ce cas l'image est normalisee 
        entre 0 et 255 avant d'être sauvegardee.
        Si normalise=False MINI(defaut 0) et MAXI (defaut 255) seront mis a 0 et 255 dans l'image resultat
        
    """
    imt=np.float32(im.copy())
    if platform.system()=='Darwin': #on est sous mac
        prephrase='open -a GIMP '
        endphrase= ' '
    else: #SINON ON SUPPOSE LINUX (si vous avez un windows je ne sais comment faire. Si vous savez dites-moi.)
        prephrase='gimp '
        endphrase=' &'
    
    if normalise:
        m=imt.min()
        imt=imt-m
        M=imt.max()
        if M>0:
            imt=imt/M
    else:
        imt=(imt-MINI)/(MAXI-MINI)
        imt[imt<0]=0
        imt[imt>1]=1
    
    nomfichier=tempfile.mktemp('TPIMA.pgm')
    commande=prephrase +nomfichier+endphrase
    skio.imsave(nomfichier,imt)
    os.system(commande)


def strel(forme,taille,angle=45):
    """renvoie un element structurant de forme  
     'diamond'  boule de la norme 1 fermee de rayon taille
     'disk'     boule de la norme 2 fermee de rayon taille
     'square'   carre de cote taille (il vaut mieux utiliser taille=impair)
     'line'     segment de langueur taille et d'orientation angle (entre 0 et 180 en degres)
      (Cette fonction n'est pas standard dans python)
    """

    if forme == 'diamond':
        return morpho.selem.diamond(taille)
    if forme == 'disk':
        return morpho.selem.disk(taille)
    if forme == 'square':
        return morpho.selem.square(taille)
    if forme == 'line':
        angle=int(-np.round(angle))
        angle=angle%180
        angle=np.float32(angle)/180.0*np.pi
        x=int(np.round(np.cos(angle)*taille))
        y=int(np.round(np.sin(angle)*taille))
        if x**2+y**2 == 0:
            if abs(np.cos(angle))>abs(np.sin(angle)):
                x=int(np.sign(np.cos(angle)))
                y=0
            else:
                y=int(np.sign(np.sin(angle)))
                x=0
        rr,cc=morpho.selem.draw.line(0,0,y,x)
        rr=rr-rr.min()
        cc=cc-cc.min()
        img=np.zeros((rr.max()+1,cc.max()+1) )
        img[rr,cc]=1
        return img
    raise RuntimeError('Erreur dans fonction strel: forme incomprise')

            

def couleurs_alea(im):
    """ 
    Donne des couleurs aleatoires a une image en niveau de gris.
    Cette fonction est utile lorsque le niveua de gris d'interprete comme un numero
      de region. Ou encore pour voir les leger degrades d'une teinte de gris.
      """
    sh=im.shape
    out=np.zeros((sh[0],sh[1],3),dtype=np.uint8)
    nbcoul=np.int32(im.max())
    tabcoul=np.random.randint(0,256,size=(nbcoul+1,3))
    tabcoul[0,:]=0
    for k in range(sh[0]):
        for l in range(sh[1]):
            out[k,l,:]=tabcoul[im[k,l]]
    return out
    
#%% SECTION 3 exemples de commandes pour effectuer ce qui est demande pendant le TP

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

#plt.imshow(im,cmap="gray")

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
_close=morpho.closing(im1,se1)
plt.imshow(_close,cmap="gray")

#%% CA - tp

# EX1 - 3
_im = skio.imread('Images/bat200.bmp')
#plt.imshow(_im,cmap="gray")
_se3x3 =strel('square',3)
_se5x5 =strel('square',5)
_se7x7 =strel('square',7)

#Avec dilatation
_dil1 = morpho.opening(_im,_se3x3)
plt.imshow(_dil1,cmap="gray")
_dil2 = morpho.opening(_dil1,_se5x5)
plt.imshow(_dil2,cmap="gray",vmin=0, vmax=255)

# Avec ouverture
_ouvert1 = morpho.opening(_im,_se3x3)
plt.imshow(_ouvert1,cmap="gray")
_ouvert2 = morpho.opening(_ouvert1,_se5x5)
plt.imshow(_ouvert2,cmap="gray",vmin=0, vmax=255)
_ouvert3 = morpho.opening(_ouvert2,_se5x5)
plt.imshow(_ouvert3,cmap="gray",vmin=0, vmax=255)


#%% Chapeau haut-de-forme
#im=skio.imread('Images/retina2.gif')
#plt.imshow(im,cmap="gray")
#t=2
#se=strel('disk',t,-45)
#ch=im-morpho.opening(im,se)
#plt.imshow(ch,cmap="gray")

#%% Chapeau haut-de-forme pour deuxieme exemple
#im3=skio.imread('Images/laiton.bmp')
#plt.imshow(im3,cmap="gray")
#t=10
#se3=strel('square',t,-45)
#ch3=morpho.closing(im3,se3) - im3
#plt.imshow(ch3,cmap="gray")

#%%  Filtre alterne sequentiel

_im2=skio.imread('Images/bat200.bmp')
_imt=im.copy()
N=3
for k in range(N):
    _se2=strel('disk',k)
    imt=morpho.closing(morpho.opening(_imt,_se2),_se2)
plt.imshow(_imt,cmap="gray")


#%% ligne de partage des eaux
#im=skio.imread('Images/laiton.bmp')
#se=morpho.selem.disk(2)

#grad=morpho.dilation(im,se) - morpho.erosion(im,se)
#grad=np.int32(grad > 40) * grad
#plt.imshow(grad,cmap="gray")

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


#%% reconstruction
_im3=skio.imread('Images/retina2.gif')
_se3=strel('diamond',10)
_open3=morpho.opening(_im3,_se3)
_reco3=morpho.reconstruction(_open3,_im3)
plt.imshow(_reco3,cmap="gray")
#%% FIN exemples TP MORPHO
