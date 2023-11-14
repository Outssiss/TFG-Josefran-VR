import pygame as pg

# Load the image
img = pg.image.load("./cameraImages/ambasNoDistortV1.png")
img_data = pg.image.tostring(img,'RGBA')
res_first, res_second = img_data[:len(img_data)//2], img_data[len(img_data)//2:]
primera_mitad = pg.image.frombytes(res_first, [1224, 920], 'RGBA')
segunda_mitad = pg.image.frombytes(res_second, [1224, 920], 'RGBA')

pg.image.save(primera_mitad, "aweno.png")
pg.image.save(segunda_mitad, "aweno2.png")
