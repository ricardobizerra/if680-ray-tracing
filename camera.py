from vectors import Ponto, Vector, produto_escalar, produto_vetorial, multiplica_vetor_por_escalar, norma_vetor, soma_vetores
from objects import Plano, Esfera, Malha
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
    
    def phong(self, k_a, I_a, I_l, k_d, O_d, N, L, k_s, R, V, n):
        first = k_a * I_a

        second = np.zeros(3)
        for i in range(min(len(I_l), len(R))):
            second += (k_d * np.array(O_d) * np.array(I_l[i]) * np.maximum(0, np.dot(N, L[i]))) + (np.array(I_l[i]) * k_s * np.maximum(0, np.dot(R[i], V)) ** n)
        
        return first + second

    def intersect(self, vetor_atual, objects):
        menor_t = 1000000
        cor = [0, 0, 0]
        for obj in objects:
            # pegue o vetor normal no ponto de interseção
            vetor_normal = self.k
            vetor_luz = np.array([0, 1, 1])  # Vetor de luz direcional
            # Parâmetros da equação de Phong
            cor_luz_ambiente = np.array([0.1, 0.1, 0.1])
            I_l = np.array([np.array([255, 245, 0])])
            k_ambiente = 0.2
            k_difuso = 0.5
            k_especular = 0.5
            n = 32

            # Calcular a cor do pixel usando a equação de Phong
            cor_final = self.phong(
                k_a=k_ambiente,
                I_a=cor_luz_ambiente,
                I_l=I_l,
                k_d=k_difuso,
                O_d=obj.cor,
                N=vetor_normal,
                L=vetor_luz,
                k_s=k_especular,
                R=np.dot(2*vetor_normal, np.dot(vetor_normal, vetor_luz)) - vetor_luz,
                V=vetor_atual,
                n=n
            )

            # Atualizar a cor do pixel se a interseção for menor que a menor encontrada até agora
            if obj.tipo == "Esfera":
                inter_esfera = obj.intersecao_esfera_reta(vetor_atual, self.posicao)
                if inter_esfera.intersecao:
                    if inter_esfera.t <= menor_t and inter_esfera.t >= 0.01:
                        cor += cor_final
                        menor_t = inter_esfera.t
            elif obj.tipo == "Plano":
                inter_plano = obj.intersecao_plano_reta(vetor_atual, self.posicao)
                if inter_plano.intersecao:
                    if inter_plano.t <= menor_t and inter_plano.t >= 0.01:
                        cor += cor_final
                        menor_t = inter_plano.t
            elif obj.tipo == "Malha":
                inter_malha = obj.intersecao_reta_malha(vetor_atual, self.posicao)
                if inter_malha.intersecao:
                    if inter_malha.t <= menor_t and inter_malha.t >= 0.01:
                        cor += cor_final
                        menor_t = inter_malha.t

        return cor

    def raycasting(self, distancia, hres, vres, objects):
        deslocamento_vertical = (2 * 0.5 / (hres - 1) * self.U)
        deslocamento_horizontal = (2 * 0.5 / (vres - 1) * self.UP)
        centro_tela = (self.W * distancia)
        pixel_0_0 = centro_tela - (0.5 * self.U) - (0.5 * self.UP)
        imagem = np.zeros((vres, hres, 3), dtype=np.uint8)  # Imagem a ser gerada
        for i in range(vres):
            for j in range(hres):
                vetor_atual = pixel_0_0 + deslocamento_vertical * i + deslocamento_horizontal * j
                cor = self.intersect(vetor_atual, objects)
                imagem[i, j] = cor
        cv.imshow("Raycasting", imagem)
        cv.waitKey(0)
        cv.destroyAllWindows('i')
