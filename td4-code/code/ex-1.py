from PIL import Image 
from math import sqrt
from random import randint

def GetPixel(x, y, px) -> tuple:
    """ Retourne les valeurs r,v,b du pixel de coordonnées x et y
        paramètres :
        x, y : les coordonnées du pixel
        Retourne : px[x,y], les valeurs r,v,b du pixel"""
    return px[x,y]
    
def PutPixel(x,y,r,g,b, px) -> None:
    """ Affecte les valeurs r,v,b au pixel de coordonnées x et y
    paramètres :
    x, y : les coordonnées du pixel
    r,v,b : les valeurs r,v,b à affecter au pixel"""
    px[x,y]=int(r),int(g),int(b)
    
def PutRegion(x,y,w,h,color, px) -> None:
    """Affecte la couleur, color, aux pixels de la région rectangulaire
    definie par les coordonnées x et y du point en haut à gauche et de largeur
    w et hauteur h    
    paramètres :
        x, y : les coordonnées du pixel
        w,h : la largeur et la hauteur de la région    
        color : les valeurs r,v,b à affceter au pixel """
    for i in range(int(x), int(x+w)):
        for j in range(int(y), int(y+h)):
            PutPixel(i,j,color[0],color[1],color[2], px)


def Average(corner_x,corner_y,region_w,region_h,px) -> tuple: 
    """ Elle calcule la moyenne pour chacune des trois couleurs primaires dans
        la région rectangulaire définie par le point en haut à gauche de
        coordonnées corner_x et corner_y et la largeur, region_w, et la
        hauteur, region_h
        paramètres :
             corner_x, corner_y : les coordonnées du point en haut à gauche
             region_w,region_h : la largeur et la hauteur de la région
        Retourne : Sum_red, sum_green, sum_blue : l'intensité moyenne en rouge, vert et bleu
        de la région         """
    #Initialisation des compteurs
    sum_red, sum_green, sum_blue = 0,0,0
    #Calcul de la superficie de la région
    area = region_w*region_h    
    
    for i in range(int(corner_x), int(corner_x+region_w)): 
        for j in range(int(corner_y),int(corner_y+region_h)):
            r,g,b=GetPixel(i,j,px)#Nous lisons les données r,v,b d'un pixel
            #Nous procédons à la sommation des r,v,b de la région
            sum_red += r
            sum_green += g
            sum_blue += b 
    #Normalisation            
    sum_red/=area
    sum_green/=area
    sum_blue/=area

    return (sum_red,sum_green,sum_blue)

def RegionMeasure(corner_x,corner_y,region_w,region_h,px) -> float: 
    """ Fonction RegionMeasure(corner_x,corner_y,region_w,region_h)
        Elle calcule la std2 des pixels dans la région rectangulaire définie 
        par le point en haut à gauche de coordonnées corner_x et corner_y et 
        la largeur, region_w, et la hauteur, region_h
        paramètres :
             corner_x, corner_y : les coordonnées du point en haut à gauche
             region_w,region_h : la largeur et la hauteur de la région
        Retourne : la veleur std2 dans la région      """

    #calcul de la moyenne des couleurs primaires
    av_red, av_blue, av_green = Average(corner_x,corner_y,region_w,region_h,px)  
    #Initialisation des compteurs
    sum_red,sum_green,sum_blue=0,0,0
    #Nous visitions chaque pixel de la région
    for i in range(int(corner_x), int(corner_x+region_w)):
        for j in range(int(corner_y),int(corner_y+region_h)):
            #nous lisons les valuers r,v,b du pixel en cours
            red,green,blue = GetPixel(i,j,px)
            sum_red  += (red   - av_red)   * (red   - av_red)
            sum_green+= (green - av_green) * (green - av_green)
            sum_blue += (blue  - av_blue)  * (blue  - av_blue)
    #Normalisation            
    #std2=(sqrt(sum_red)+sqrt(sum_green)+sqrt(sum_blue))/(3*region_w*region_h)
    std2=(sqrt(sum_red/(region_w*region_h))+sqrt(sum_green/(region_w*region_h))+sqrt(sum_blue/(region_w*region_h)))/3

    return(std2)

def distance(c1, c2) -> float: 
    """Distance euclidienne entre deux couleurs (r, g, b)"""
    return sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

def floodFill(w, h, start_x: int, start_y: int, c: tuple, s, px, px2):
    """ Algorithme de flood filling
        - vérifie que l'on est dans l'image
        - vérifie que les voisins sont homogènes
        - vérifie qu'ils n'ont pas été visités
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    q = [(start_x, start_y)]
    visited = {(start_x, start_y)}
    while q:
        x, y = q.pop()
        px2[x, y] = c # on colorie l'image ici
        for dirx, diry in directions:
            tx, ty = x + dirx, y + diry
            if 0 <= tx < w and 0 <= ty < h and distance(px[tx, ty], c) < s and (tx, ty) not in visited:
                q.append((tx, ty))
                visited.add((tx, ty))
    return visited

if __name__ == "__main__":

    im = Image.open("Image10.bmp")
    im2 = Image.new('RGB', (im.width, im.height))
    px = im.load()
    px2 = im2.load()
    W, H = im.size

    print("nombre de pixels dans l'image:", W * H)

    c =  px[0, 0]
    seuil = 200
    visited = floodFill(W, H, 0, 0, c, seuil, px, px2)
    print("nombre de noeuds coloriés", len(visited))

    im2.show()