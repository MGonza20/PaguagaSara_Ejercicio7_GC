from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 1024
height = 1024

# Materiales

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)

earth = Material(texture = Texture("earthDay.bmp"))
marble = Material( diffuse = (0.8, 0.8, 0.8), texture = Texture("marbleTex2.bmp"), spec = 32, matType = REFLECTIVE)
marble2 = Material( diffuse = (0.2, 0.2, 0.8), texture = Texture("marbleTex3.bmp"), spec = 32, matType = TRANSPARENT)

marble3 = Material( diffuse = (0.8, 0.8, 0.8), texture = Texture("colored-tex.bmp"), spec = 32, matType = REFLECTIVE) # yes
marble4 = Material( diffuse = (0.8, 0.8, 0.8), texture = Texture("colored-tex-2.bmp"), spec = 32, matType = REFLECTIVE) # yes
marble5 = Material( diffuse = (0.8, 0.8, 0.8), texture = Texture("colored-tex-3.bmp"), spec = 32, matType = OPAQUE) # yes
marble7 = Material( diffuse = (0.8, 0.8, 0.8), texture = Texture("colored-tex-6.bmp"), spec = 32, matType = OPAQUE) # yes
marble9 = Material( diffuse = (171/255, 240/255, 1), texture = Texture("colored-tex-8.bmp"), spec = 32, matType = TRANSPARENT) # yes
marble10 = Material( diffuse = (247/255, 95/255, 20/255), texture = Texture("colored-tex-8.bmp"), spec = 32, matType = TRANSPARENT) # yes

mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)

glass = Material(diffuse = (0.8, 0.8, 0.8), spec = 64, ior = 1.5, matType = TRANSPARENT)
diamond = Material(diffuse = (0.8, 0.8, 0.8), spec = 64, ior = 2.417, matType = TRANSPARENT)

# blueMirror = Material(diffuse = (0.2, 0.2, 0.9), spec = 64, matType = REFLECTIVE)
# yellowMirror = Material(diffuse = (0.9, 0.9, 0.2), spec = 64, matType = REFLECTIVE)

rtx = Raytracer(width, height)

rtx.envMap = Texture("parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
#rtx.lights.append( PointLight(point = (0,0,0)))

rtx.scene.append( Sphere(V3(-3,1.5,-10), 1, marble3))
rtx.scene.append( Sphere(V3(0,1.5,-10), 1, marble5))
rtx.scene.append( Sphere(V3(3,1.5,-10), 1, marble9))

rtx.scene.append( Sphere(V3(-3,-1.5,-10), 1, marble4))
rtx.scene.append( Sphere(V3(0,-1.5,-10), 1, marble7))
rtx.scene.append( Sphere(V3(3,-1.5,-10), 1, marble10))

# rtx.scene.append( Sphere(V3(3,1,-13), 1, stone))

# rtx.scene.append( Sphere(V3(-3,0,-10), 1, brick))
# rtx.scene.append( Sphere(V3(0,0,-10), 1, mirror))
# rtx.scene.append( Sphere(V3(3,0,-10), 1, glass))
# rtx.scene.append( Sphere(V3(3,1,-13), 1, stone))

# rtx.scene.append( Sphere(V3(3,0,-10), 1, brick)  )
# rtx.scene.append( Sphere(V3(0,3,-10), 1, stone)  )

# rtx.scene.append( Sphere(V3(-3,0,-10),1, blueMirror)  )
# rtx.scene.append( Sphere(V3(0,-3,-10), 1, yellowMirror)  )


rtx.glRender()

rtx.glFinish("output.bmp")