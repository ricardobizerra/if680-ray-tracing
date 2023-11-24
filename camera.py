from vectors import Ponto, Vector, produto_escalar, produto_vetorial, multiplica_vetor_por_escalar, norma_vetor, soma_vetores
from objects import Plano, Esfera
import cv2 as cv
import numpy as np

def normalize(vector):
    return vector / np.linalg.norm(vector)

class ObjPointer:
    def __init__(self, ptr_esfera=None, ptr_plano=None, tipo_objeto=None):
        self.ptr_esfera = ptr_esfera
        self.ptr_plano = ptr_plano
        self.tipo = tipo_objeto

class Camera:
    def __init__(self, posicao, target, up_vector):
        self.k = up_vector
        self.posicao = posicao
        self.W = (target - posicao)
        self.W = normalize(self.W)

        self.U = np.cross(self.k, self.W)
        self.U = normalize(self.U)

        self.UP = np.cross(self.W, self.U) * -1
        self.UP = normalize(self.UP)

    def intersect(self, vetor_atual, objects):
        menor_t= 10000000
        cor = [0, 0, 0]
        for obj in objects:
            if obj.tipo == "Esfera":
                inter_esfera = obj.intersecao_esfera_reta(vetor_atual, self.posicao)
                if inter_esfera.intersecao:
                    if inter_esfera.t <= menor_t:
                        cor = [255, 0, 0]
                        menor_t = inter_esfera.t
            elif obj.tipo == "Plano":
                inter_plano = obj.intersecao_plano_reta(vetor_atual, self.posicao)
                if inter_plano:
                    if inter_plano.intersecao:
                        if inter_plano.t <= menor_t:
                            cor = [0, 255, 0]
                            menor_t = inter_plano.t
        return cor
    
    def raycasting(self, distancia, hres, vres, objects):
        deslocamento_vertical = (2*0.5/(hres - 1)*self.U)
        deslocamento_horizontal = (2*0.5/(vres - 1)*self.UP)
        centro_tela = (self.W * distancia)
        pixel_0_0 = centro_tela - (0.5 * self.U) - (0.5 * self.UP)
        imagem = np.zeros((vres, hres, 3), dtype=np.uint8)  # Imagem a ser gerada
        for i in range(vres):
            for j in range(hres):
                vetor_atual = pixel_0_0 + deslocamento_vertical*i + deslocamento_horizontal*j
                imagem[j,i] = self.intersect(vetor_atual, objects)
        cv.imshow("Raycasting", imagem)
        cv.waitKey(0)
        cv.destroyAllWindows('i')

       
