from PIL import Image, ImageChops, ImageFilter, ImageFont, ImageDraw
from math import sqrt

gauss3 = [[1,2,1],
        [2,4,2],
        [1,2,1]]

gauss7 = [[1,1,2,2,2,1,1],
        [1,2,2,4,2,2,1],
        [2,2,4,8,4,2,2],
        [2,4,8,16,8,4,2],
        [2,2,4,8,4,2,2],
        [1,2,2,4,2,2,1],
        [1,1,2,2,2,1,1]]

im = Image.open("Image10.bmp")
im2 = im.copy()
px = im.load()
px2 = im2.load()
W, H = im.size

def somme_matrice(m: list = []) -> list:
    s = 0
    for row in m:
        s += sum(row)
    return s

def conversion_gris(px, W: int, H: int) -> None:
    for x in range(0, W):
        for y in range(0, H):
            m = int(0.30*px[x, y][0] + 0.59*px[x, y][1] + 0.11*px[x, y][2])
            px[x, y] = (m, m, m)

def convolution(px, W: int, H: int, m: list) -> None:
    w = len(m)
    h = len(m[0])
    wp = int((w-1)/2)
    hp = int((h-1)/2)
    for x in range(w, W - w): # a améliorer pour gérer les bords
        for y in range(h, H - w):
            sum = 0
            for a in range(-wp, wp+1):
                for b in range(-hp, hp+1):
                    sum += px[x+a, y+b][0] * m[a+wp][b+hp]
            v = int(sum / somme_matrice(m))
            px[x, y] = v, v, v

def distance(c1 -> tuple, c2 -> tuple) -> float: 
    """Distance entre deux couleurs (r, g, b)"""
    return sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

if __name__ == "__main__":
    
    conversion_gris(px2, W, H)
    convolution(px2, W, H, gauss7)
    #im2.show()

    # exemple de flou guassien avec PIL
    _im = im2.filter(ImageFilter.GaussianBlur)
    #_im.show()

    # résultats
    dst = Image.new('RGB', (im.width + im2.width, im.height))
    dst.paste(im, (0, 0))
    dst.paste(im2, (im.width, 0))
    font = ImageFont.truetype("Keyboard.ttf",16)
    draw = ImageDraw.Draw(dst)    
    draw.text((0, 0), "image originale", (255,255,255), font=font)
    draw.text((im.width, 0), "filtre gaussien", (255,255,255), font=font)    
    dst.show()

    # différence entre deux images
    diff = Image.new('RGB', (im.width, im.height))
    px_diff = diff.load()
    for x in range(0, W):
        for y in range(0, H):
            d = int(distance(px[x, y], px2[x, y]) )
            px_diff[x, y] = (d, d, d)

    diff.show()

    # exemple de différence d'image avec PIL
    # diff = ImageChops.difference(im, im2)
    # diff.show()
