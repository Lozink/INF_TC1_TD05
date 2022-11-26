# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 08:16:18 2022

@author: loisb
"""
from PIL import Image
import math

im=Image.open("Image10.bmp")
px=im.load()
W,H=im.size
#%% ex 1
def compteur_couleur(W,H,px):
    # Compte les couleurs présentes sur une image donnée
    liste_couleur=[]
    nombre_couleur=0
    for x in range (0,W):
        for y in range (0,H):
            if px[x,y] not in liste_couleur:
                liste_couleur.append(px[x,y])
                nombre_couleur+=1
    return(nombre_couleur)

#%% ex 2
def palette_couleur_naive(W,H,px,k):
    # Prend une image et retourne une image d'une palette de k couleurs
    # Cette palette est déterminée en comptant le nombre de fois qu'apparaisse chaque couleur et en prenant celles qui apparaissent le plus
    liste_couleur=[]
    liste_couleur_passe=[]
    for x in range (0,W):
        for y in range (0,H):
            if px[x,y] not in liste_couleur_passe:
                liste_couleur.append([px[x,y],1])
                liste_couleur_passe.append(px[x,y])
            else:
                for i in range (0,len(liste_couleur)):
                    if liste_couleur[i][0]==px[x,y]:
                        liste_couleur[i][1]+=1
    palette_k_couleur=[]
    while len(palette_k_couleur)<k:
        i_max=0
        couleur=liste_couleur[0][0]
        for i in range (1,len(liste_couleur)):péa
            if liste_couleur[i][1]>i_max and liste_couleur[i][0] not in palette_k_couleur:
                i_max=liste_couleur[i][1]
                couleur=liste_couleur[i][0]
        palette_k_couleur.append(couleur)
    im2=Image.new('RGB',(50,50*k))
    px2=im2.load()
    indice_coloriage=0
    while indice_coloriage<k:
        r,g,b=palette_k_couleur[indice_coloriage]
        for y in range(indice_coloriage*50,(indice_coloriage+1)*50):
            for x in range (0,50):
                px2[x,y]=r,g,b
        indice_coloriage+=1
    return(im2)

#%% Fonction distance euclidienne
def distance(c1, c2):
    # Distance euclidienne entre deux couleurs (r, g, b)
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

#%% ex 3
def recoloriage_distance_euclidienne(W,H,px,k,fonction_palette):
    # On se sert de la palette créée par la méthode désirée pour re-colorier l'image, en comparant chaque pixel et en utilisant la distance euclidienne de celui-ci avec chaque pixel de la palette
    im2=fonction_palette(W,H,px,k)
    px2=im2.load()
    W2,H2=im2.size
    palette_k_couleur=[]
    for i in range(0,k):
        palette_k_couleur.append(px2[0,i*H2/k])
    im3=Image.new('RGB',(W,H))
    px3=im3.load()
    for x in range (0,W):
        for y in range (0,H):
            distance_euclidienne=distance(palette_k_couleur[0],px[x,y])
            couleur=palette_k_couleur[0]
            for i in range (1,k):
                if distance(palette_k_couleur[i],px[x,y])<distance_euclidienne:
                    distance_euclidienne=distance(palette_k_couleur[i],px[x,y])
                    couleur=palette_k_couleur[i]
            px3[x,y]=couleur
    return(im3)
            
#%% ex 4
def comparaison_entre_image(W,H,px,px2):
    # Comparaison de la différence entre chaque couleur de chaque image et calcul d'un score en faisant la moyenne des erreus
    total_distance=0
    for x in range(0,W):
        for y in range(0,H):
            total_distance+=distance(px[x,y],px2[x,y])
    return(total_distance/(W*H))

#%% ex 5
def palette_couleur_frequence_puis_proche(W,H,px,k):
    # Amélioration du choix des couleurs dans la palette en déterminant pour chaque couleur les plus présentes, les 200 plus proches, les triant, en prenant le mileur de chaque
    liste_couleur=[]
    liste_couleur_passe=[]
    for x in range (0,W):
        for y in range (0,H):
            if px[x,y] not in liste_couleur_passe:
                liste_couleur.append([px[x,y],1])
                liste_couleur_passe.append(px[x,y])
            else:
                for i in range (0,len(liste_couleur)):
                    if liste_couleur[i][0]==px[x,y]:
                        liste_couleur[i][1]+=1
    palette_k_couleur=[]
    while len(palette_k_couleur)<k:
        couleur=liste_couleur[0][0]
        indice_max=liste_couleur[0][1]
        for cl in liste_couleur:
            if cl[1]>indice_max:
                indice_max=cl[1]
                couleur=cl[0]
        liste_couleur.remove([couleur,indice_max])
        liste_couleur_triee=[[couleur,0]]
        while len(liste_couleur_triee)<200: #on prend un nombre de couleur proche arbitraire pour limiter la complexite
            dist=distance(couleur,liste_couleur[0][0])
            couleur_ajout=liste_couleur[0]
            for cl in liste_couleur:
                if distance(couleur,cl[0])<dist:
                    dist=distance(couleur,cl[0])
                    couleur_ajout=cl
            liste_couleur.remove(couleur_ajout)
            liste_couleur_triee.append([couleur_ajout[0],dist])
        palette_k_couleur.append(liste_couleur_triee[len(liste_couleur_triee)//2][0])
    im2=Image.new('RGB',(50,50*k))
    px2=im2.load()
    indice_coloriage=0
    while indice_coloriage<k:
        r,g,b=palette_k_couleur[indice_coloriage]
        for y in range(indice_coloriage*50,(indice_coloriage+1)*50):
            for x in range (0,50):
                px2[x,y]=r,g,b
        indice_coloriage+=1
    return(im2)

#%%
def palette_couleur_triee_par_bleu(W,H,px,k):
    liste_couleur=[]
    for x in range (0,W):
        for y in range (0,H):
            liste_couleur.append(px[x,y])
    liste_couleur.sort(key=lambda x : x[2])
    palette_k_couleur=[]
    pas=len(liste_couleur)//k
    for i in range (0,k):
        palette_k_couleur.append(liste_couleur[(i*pas+(i+1)*pas)//2])
    im2=Image.new('RGB',(50,50*k))
    px2=im2.load()
    indice_coloriage=0
    while indice_coloriage<k:
        r,g,b=palette_k_couleur[indice_coloriage]
        for y in range(indice_coloriage*50,(indice_coloriage+1)*50):
            for x in range (0,50):
                px2[x,y]=r,g,b
        indice_coloriage+=1
    return(im2)
#%% ex 6
im2=recoloriage_distance_euclidienne(W, H, px, 10,palette_couleur_triee_par_bleu)
im2.show()
px2=im2.load()
#%%
im3=im.quantize(10)
im3.show()
px3=im3.load()
#%%
score1=comparaison_entre_image(W, H, px, px2)
score2=comparaison_entre_image(W, H, px, px3)
print(score1,score2)
#%% test im.quantize
im1=im.quantize(256)
im1.show()
#%%
