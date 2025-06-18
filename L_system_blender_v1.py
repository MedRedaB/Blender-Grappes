import bpy
import numpy as np
import math
import mathutils
import random
#import pandas as pd
#import matplotlib.pyplot as plt

def clear_scene():
    """
    fonction qui vide la scene
    """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def norm(nu, sigma):
    """
    nu, sigma : float
    retourne une valeur approchee de nu selon une distribution normale d'ecart type sigma
    """
    return np.random.normal(nu, sigma)

def rotation(curseur, axe, alpha):
    """
    vecteur : numpy array 
    axe : str
    alpha : float (en degrès)
    Renvoie le vecteur après rotation d'angle alpha en degrès autour de l'axe choisi
    """
    
    posi_curseur, direc_curseur = curseur[0, :], curseur[1, :]
    a = alpha*math.pi/180 #conversion de degres en radian
    rot_x = np.array([[1, 0, 0],
                     [0, math.cos(a), -math.sin(a)],
                     [a, math.sin(a), math.cos(a)]])
    rot_y = np.array([[math.cos(a), 0, -math.sin(a)],
                     [0, 1, 0],
                     [math.sin(a), 0, math.cos(a)]])
    rot_z = np.array([[math.cos(a), math.sin(a), 0],
                     [-math.sin(a), math.cos(a), 0],
                     [0, 0, 1]])
    if axe == 'x' :
        direc_curseur = np.round(np.matmul(direc_curseur, rot_x), 4)
    elif axe == 'y' :
        direc_curseur =  np.round(np.matmul(direc_curseur, rot_y), 4)
    else :
        direc_curseur =  np.round(np.matmul(direc_curseur, rot_z), 4)
    curseur = np.array([posi_curseur, direc_curseur])
    return curseur 

def convert_vect(vecteur):
    if isinstance(vecteur,tuple) or isinstance(vecteur,np.ndarray):
        return mathutils.Vector((vecteur[0], vecteur[1], vecteur[2])) 

def vect_a_rota(vecteur):
    """
    prend en entrée un vecteur direction et renvoie les rotations correspondantes 
    """

    default_dir = mathutils.Vector((0, 0, 1))
    vecteur = convert_vect(vecteur)
    rotation = default_dir.rotation_difference(vecteur).to_euler()
    return rotation

def dessine_cylindre(curseur, rayon = 0.5, hauteur = 3):
    """
    Dessine un cylindre partant de depart dans la direction direction.
    - depart : mathutils.Vector
    - direction : mathutils.Vector
    - rayon : float
    - hauteur : float
    problems : quand direction = (0,0,0)
    """
    posi_curseur, direc_curseur = curseur[0, :], curseur[1, :]
    direc_curseur = direc_curseur/np.linalg.norm(direc_curseur)
    rotation = vect_a_rota(direc_curseur)
    midpoint = posi_curseur + (direc_curseur * (hauteur / 2))
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=rayon,
        depth=hauteur,
        enter_editmode=False,
        align='WORLD',
        location=midpoint,
        rotation=rotation)
        
    posi_curseur = posi_curseur + direc_curseur*hauteur
    curseur = np.array([posi_curseur, direc_curseur])
    return curseur 
    

def dessine_sphere(curseur, rayon = 1):
    """
    Dessine une sphere partant de depart dans la direction direction.
    - depart : mathutils.Vector
    - direction : mathutils.Vector
    - rayon : float
    problems : quand direction = (0,0,0)
    """
    posi_curseur, direc_curseur = curseur[0, :], curseur[1, :]
    direc_curseur = direc_curseur/np.linalg.norm(direc_curseur)
    midpoint = posi_curseur + direc_curseur*rayon

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=rayon,
        enter_editmode=False,
        align='WORLD',
        location=midpoint)
        
    posi_curseur = posi_curseur + direc_curseur*rayon
    curseur = np.array([posi_curseur, direc_curseur])
    return curseur 
      

def actions(L_systeme, stade = None):
    posi_curseur, direc_curseur = np.array((0, 0, 10)), np.array((0, 0, -1))
    curseur = np.array([posi_curseur, direc_curseur])
    sauv = [curseur]
    for alphabet in L_systeme:
        alpha = norm(30, 10) #en degrès
        if alphabet == "F":
            curseur = dessine_cylindre(curseur)
        elif alphabet == "H":
            dessine_sphere(curseur)
        elif alphabet == "+":
            curseur = rotation(curseur, 'x', alpha)
        elif alphabet == "-":
            curseur = rotation(curseur, 'x', -alpha)
        elif alphabet == "∼":
            curseur = rotation(curseur, 'y', alpha)
        elif alphabet == "?":
            curseur = rotation(curseur, 'y', -alpha)
        elif alphabet == "&":
            curseur = rotation(curseur, 'z', alpha)
        elif alphabet == "^":
            curseur = rotation(curseur, 'z', -alpha)
        elif alphabet == "[":
            sauv.append(curseur)
        elif alphabet == "]":
            curseur = sauv[-1]
            sauv.pop(-1) 
    return None


def regles_de_prod(alphabet):
    """
    Règles de production de notre L-système.
    ici l'ajoue de stochasticité viendra 
    """
    if alphabet == 'A':
        return 'F[-FAH][+FAH][∼FAH][?FAH]' #comme sur mon rapport mais version 3D que je propose moi meme pour avoir 4 embranchements 
    else :
        return alphabet 

def systeme(n):
    """
    renvoie le L-systeme après n intérations
    """
    L_systeme = ['A']  #axiome
    for i in range(n+1):
        chaine_precedente = L_systeme[-1]
        nouvelle_chaine = ''
        for c in chaine_precedente:
            nouvelle_chaine += regles_de_prod(c)
        L_systeme.append(nouvelle_chaine)
    return L_systeme


def principale(n):
    clear_scene()
    L_systeme = systeme(n)[-1]
    actions(L_systeme)
    return None

#compteur de baies

#print(systeme(1))
principale(3)