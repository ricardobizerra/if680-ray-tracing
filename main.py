from vectors import Ponto, Vector
from objects import Esfera, Plano, Malha
from camera import Camera
from transform import affine_transform
import numpy as np

def main():
    # Definição dos valores para a câmera, alvo, up, centro da esfera, ponto do plano e normal ao plano   
    # Criação dos objetos Ponto e Vector com base nos valores fornecidos
    camera_ponto =  np.array([-100, 200, 100])
    alvo_ponto = np.array([0, 0, 0])
    up_vector = np.array([0,1,0])
   
    camera_ponto = affine_transform(camera_ponto, [1, 0, 0, 400], [0, 1, 0, 400], [0, 0, 1, 400], [0, 0, 0, 1])
    # Inicialização dos objetos Camera, Esfera e Plano com base nos dados inseridos
    cam = Camera(camera_ponto, alvo_ponto, up_vector)
    esfera = Esfera(np.array([200, 0, 50]), 50)  # Raio da esfera definido como 1
    plano = Plano(np.array([100,0,0]), np.array([0, 0, 1]))  # Ponto e vetor normal ao plano definidos como 0
    p0 = np.array([100, 0, 0])
    p1 = np.array([0, 100, 0])
    p2 = np.array([-100, 0, 0])
    p3 = np.array([0, -100, 0])
    p4 = np.array([0, 0, 100])

    n1 = np.cross(p1 - p0, p4 - p0)
    norma1 = np.linalg.norm(n1)
    n1 = n1 / norma1

    n2 = np.cross(p2 - p1, p4 - p1)
    norma2 = np.linalg.norm(n2)
    n2 = n2 / norma2

    n3 = np.cross(p3 - p2, p4 - p2)
    norma3 = np.linalg.norm(n3)
    n3 = n3 / norma3

    n4 = np.cross(p0 - p3, p4 - p3)
    norma4 = np.linalg.norm(n4)
    n4 = n4 / norma4

    malha = Malha(4, 
                  5, 
                  [p0, p1, p2, p3, p4], 
                  [(0,1,4),(1,2,4),(2,3,4),(0,3,4)],
                  [n1,n2,n3,n4],
                  [],
                  [[255,255,255], [255,0,0], [0,255,0], [0,0,255]])
    objects = [malha]
    # Realização do raycasting com os parâmetros fornecidos
    cam.raycasting(1, 500, 500, objects)

if __name__ == "__main__":
    main()
