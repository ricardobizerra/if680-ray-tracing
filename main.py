from vectors import Ponto, Vector
from objects import Esfera, Plano, Malha
from camera import Camera
import numpy as np

def main():
    # Definição dos valores para a câmera, alvo, up, centro da esfera, ponto do plano e normal ao plano   
    # Criação dos objetos Ponto e Vector com base nos valores fornecidos
    camera_ponto =  np.array([0,1,0])
    alvo_ponto = np.array([2,0,0])
    up_vector = np.array([0,1,0])
   

    # Inicialização dos objetos Camera, Esfera e Plano com base nos dados inseridos
    cam = Camera(camera_ponto, alvo_ponto, up_vector)
    esfera = Esfera(np.array([2,0,0]), 0.25)  # Raio da esfera definido como 1
    esfera2 = Esfera(np.array([2,0,1]), 0.5)  # Raio da esfera definido como 1
    plano = Plano(np.array([0,1,0]), np.array([0,-1,0]))  # Ponto e vetor normal ao plano definidos como 0
    malha = Malha(1, 3, [(1,0,0),(0,1,0),(0,0,0)], [(0,1,2)],[(0,0,1)],[],[1,1,1])
    objects = [plano,esfera,esfera2,malha]
    # Realização do raycasting com os parâmetros fornecidos
    cam.raycasting(1, 500, 500, objects)

if __name__ == "__main__":
    main()
