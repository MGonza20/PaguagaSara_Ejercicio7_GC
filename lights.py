
from mathLib import *


DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

def reflectVector(normal, direction):
    reflect = 2 * dotProduct(normal, direction)
    reflect = [reflect * normal[0], reflect * normal[1], reflect * normal[2]]
    reflect = subtractVList(reflect, direction)
    reflect = normV(reflect)
    return reflect

# ior (Indice de refraccion)
def refractVector(normal, direction, ior): 
    # Snell's law
    cosi = max(-1, min(1, dotProduct(direction, normal)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        normal = [normal[0] * -1,
                  normal[1] * -1,
                  normal[2] * -1]

    eta = etai / etat
    k = 1 - (eta**2) * (1 - (cosi**2)) 

    if k < 0: # Total internal Reflection
        return None

    normalStr = [(eta * cosi - k**0.5) * normal[0], 
                 (eta * cosi - k**0.5) * normal[1],
                 (eta * cosi - k**0.5) * normal[2]]

    dirStrange = [eta * direction[0],
                  eta * direction[1],
                  eta * direction[2]]
    R = addVectors(dirStrange, normalStr)
    return R


def fresnel(normal, direction, ior):
    # Fresnel Equation
    cosi = max(-1, min(1, dotProduct(direction, normal)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint  = etai / etat * (max(0, 1 - cosi**2) ** 0.5)

    if sint >= 1:
        return 1

    cost = max(0, 1 - sint**2) ** 0.5
    cosi = abs(cosi)

    Rs = ((etat * cosi) - (etai * cosi)) / ((etat * cosi) + (etai * cosi))
    Rp = ((etai * cosi) - (etat * cosi)) / ((etai * cosi) + (etat * cosi))

    return (Rs**2 + Rp**2) /2
     


class DirectionalLight(object):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = normV(direction)
        self.intensity = intensity
        self.color = color
        self.lightType = DIR_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = [self.direction[0] * -1, self.direction[2] * -1, self.direction[2] * -1]
        intensity = dotProduct(intersect.normal, light_dir) * self.intensity
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = [self.direction[0] * -1, self.direction[1] * -1, self.direction[2] * -1]
        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = subtractVList( raytracer.camPosition, intersect.point) #Check later
        view_dir = normV(view_dir)

        spec_intensity = self.intensity * max(0, dotProduct(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * self.color[0],
                     spec_intensity * self.color[1],
                     spec_intensity * self.color[2]]

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = [self.direction[0] * -1, self.direction[1] * -1, self.direction[2] * -1]

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class PointLight(object):
    def __init__(self, point, constant = 1.0, linear = 0.1, quad = 0.05, color = (1,1,1)):
        self.point = point
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = subtractVList(self.point, intersect.point)
        light_dir = normV(light_dir)

        attenuation = 1.0
        intensity = dotProduct(intersect.normal, light_dir) * attenuation
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = subtractVList(self.point, intersect.point)
        light_dir = normV(light_dir)

        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = subtractVList( raytracer.camPosition, intersect.point)
        view_dir = normV(view_dir)

        attenuation = 1.0

        spec_intensity = attenuation * max(0, dotProduct(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * self.color[0],
                     spec_intensity * self.color[1],
                     spec_intensity * self.color[2]]

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = subtractVList(self.point, intersect.point)
        light_dir = normV(light_dir)

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class AmbientLight(object):
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        return [list(self.color)[0] * self.intensity, list(self.color)[1] * self.intensity, list(self.color)[2] * self.intensity]

    def getSpecColor(self, intersect, raytracer):
        return [0,0,0]

    def getShadowIntensity(self, intersect, raytracer):
        return 0
