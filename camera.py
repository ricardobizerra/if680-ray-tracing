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
    
    def phong(self, k_a, I_a, I_l, k_d, O_d, N, L, k_s, R, V, n, lim_r, k_r, vetor_camera, objects, ponto_intersecao, current_obj, contador_r = 0):
        """ Calcula a cor final de um pixel segundo a equação de phong
            Phong:
                componente_ambiente = k_a * I_a
                para cada luz i:
                    componente_difusa = I_l[i] * O_d * k_d * (N * L[i])
                    componente_especular = I_l[i] * k_s * (R[i] * V)^n
                cor_final = componente_ambiente + componente_difusa + componente_especular

        Args:
            k_a (entre 0 e 1) = coeficiente de reflexão do ambiente. O quanto o objeto é afetado pela reflexão da luz ambiente.

            I_a (da forma [255,255,255]) = conjunto RGB que representa a cor da luz ambiente.

            I_l (da forma [[255,255,255], [255,255,0], ...]) = array de componentes RGB, um para cada luz do ambiente.

            k_d (entre 0 e 1)= coeficiente de difusão do objeto

            O_d (da forma [255,255,255]) = conjunto RGB que representa a cor do objeto

            N (vetor_normalizado) = vetor normal do ponto onde ocorreu a interseção

            L (array de vetores normalizados) = array de vetores que vão do ponto para cada luz

            k_s (entre 0 e 1) = coeficiente de especularidade

            R (array de vetores normalizados) = array de vetores refletidos (depende do observador, um para cada objeto de luz)

            V (vetor_normalizado) = Vetor que vai até o observador (câmera)

            n ([0:inf)) = rugosidade

            lim_r (int) = limite de recursão, aumenta em um em cada chamada recursiva de phong.

            k_r (entre 0 e 1) = coeficiente de reflexão do objeto

            vetor_camera (vetor normalizado) = raio que vem do observador (usado para calcular reflexão)

            objects (array de objetos) = lista dos objetos da cena para chamada recursiva de phong

            ponto_intersecao (da forma [1,0,0]) = ponto onde ocorreu a interseção e foi chamado phong

            current_obj (esfera, plano ou triangulo) = diz respeito ao objeto atual resultado da interseção

            contador_r (int) = incrementa em um a cada chamada recursiva de phong

        Returns:
            cor_final (da forma [255, 255, 255]) = conjunto RGB que representa a cor final do pixel em questão. Cada componente de I tem que ser menor ou igual a 255 
        """
        #if contador_r > 0:
            #print('c')
        componente_ambiente = k_a * I_a

        componente_difusa = np.zeros(3)
        componente_especular = np.zeros(3)
        componente_reflexao = np.zeros(3)

        for i in range(len(I_l)):
            componente_difusa += k_d * I_l[i] * np.maximum(0, np.dot(N, L[i]))
            componente_especular += I_l[i] * k_s * np.maximum(0, np.dot(R[i], V) ** n)

        if contador_r <= lim_r:
            vetor_refletido = normalize(2 * np.dot(N, vetor_camera) * N - vetor_camera)
            vetor_refletido = vetor_refletido * -1
            i_r = self.intersect(vetor_atual=vetor_refletido, objects=objects, contador_r=contador_r + 1, posicao=ponto_intersecao, exclude_obj=current_obj)
            #if i_r[0] == 0 and i_r[1] == 0 and i_r[2] == 0:
            #    print('a')
            
            componente_reflexao = k_r * i_r
            #print(i_r)
        # Phong
        cor_final = componente_ambiente + componente_difusa + componente_especular + componente_reflexao
        #if cor_final[0] == cor_final[1] == cor_final[2]:
        #    print('b')
        cor_final = np.clip(cor_final * O_d/255, 0, 255)
        return cor_final

    def intersect(self, vetor_atual, objects, contador_r = 0, posicao = None, exclude_obj = None):
        if posicao is None:
            posicao = self.posicao
        menor_t = 1000000
        cor = np.array([0, 0, 0])
        for obj in objects:
            array_pontos_luz = np.array([np.array([0, 0, 0])])  # Fontes de luz
            # Parâmetros da equação de Phong
            cor_luz_ambiente = np.array([255,255,255])
            I_l = [np.array([255, 255, 255])]
            
            R_array = [] # Inicializando R
            array_vetores_luz = [] # Inicializando array de vetores para luz

            if exclude_obj is not None:
                if obj == exclude_obj:
                    continue


            # Atualizar a cor do pixel se a interseção for menor que a menor encontrada até agora
            if obj.tipo == "Esfera":
                inter_esfera = obj.intersecao_esfera_reta(vetor_atual, posicao)
                if inter_esfera.intersecao:
                    if inter_esfera.t <= menor_t and inter_esfera.t >= 0.01:
                        # Cálculo do vetor normal do ponto:
                        vetor_normal = normalize(inter_esfera.ponto_intersecao - obj.centro)

                        # Definindo e normalizando vetores dos arrays:
                        for i in range(len(array_pontos_luz)):
                            vetor_luz = normalize(array_pontos_luz[i] - inter_esfera.ponto_intersecao)
                            array_vetores_luz.append(vetor_luz)
                            vetor_refletido = normalize(2 * np.dot(vetor_normal, vetor_luz) * vetor_normal - vetor_luz)
                            R_array.append(vetor_refletido)

                        # Calcular a cor do pixel usando a equação de Phong
                        cor_final = self.phong(
                                current_obj=obj,
                                k_a=obj.k_ambiente,
                                I_a=cor_luz_ambiente,
                                I_l=I_l,
                                k_d=obj.k_difuso,
                                O_d=obj.cor,
                                N=vetor_normal,
                                L=array_vetores_luz,
                                k_s=obj.k_especular,
                                R=R_array,
                                V=normalize(posicao - inter_esfera.ponto_intersecao),
                                n=obj.n,
                                lim_r=3,
                                k_r=obj.k_reflexao,
                                vetor_camera=normalize(vetor_atual),
                                objects=objects,
                                ponto_intersecao=inter_esfera.ponto_intersecao,
                                contador_r=contador_r
                                )
                        cor = cor_final
                        menor_t = inter_esfera.t
            elif obj.tipo == "Plano":
                inter_plano = obj.intersecao_plano_reta(vetor_atual, posicao)
                if inter_plano.intersecao:
                    if inter_plano.t <= menor_t and inter_plano.t >= 0.01:
                        # Cálculo do vetor normal do ponto:
                        vetor_normal = obj.vetor_normal

                        # Definindo e normalizando vetores dos arrays:
                        for i in range(len(array_pontos_luz)):
                            vetor_luz = normalize(array_pontos_luz[i] - inter_plano.ponto_intersecao)
                            array_vetores_luz.append(vetor_luz)
                            vetor_refletido = normalize(2 * np.dot(vetor_normal, vetor_luz) * vetor_normal - vetor_luz)
                            R_array.append(vetor_refletido)

                        # Calcular a cor do pixel usando a equação de Phong
                        cor_final = self.phong(
                                current_obj=obj,
                                k_a=obj.k_ambiente,
                                I_a=cor_luz_ambiente,
                                I_l=I_l,
                                k_d=obj.k_difuso,
                                O_d=obj.cor,
                                N=vetor_normal,
                                L=array_vetores_luz,
                                k_s=obj.k_especular,
                                R=R_array,
                                V=normalize(posicao - inter_plano.ponto_intersecao),
                                n=obj.n,
                                lim_r=3,
                                k_r=obj.k_reflexao,
                                vetor_camera=normalize(vetor_atual),
                                objects=objects,
                                ponto_intersecao=inter_plano.ponto_intersecao,
                                contador_r=contador_r
                                )
                        cor = cor_final
                        menor_t = inter_plano.t
            elif obj.tipo == "Malha":
                inter_malha = obj.intersecao_reta_malha(vetor_atual, posicao)
                if inter_malha.intersecao:
                    if inter_malha.t <= menor_t and inter_malha.t >= 0.01:
                        # Cálculo do vetor normal do ponto:
                        vetor_normal = inter_malha.normal_ponto

                        # Definindo e normalizando vetores dos arrays:
                        for i in range(len(array_pontos_luz)):
                            vetor_luz = normalize(array_pontos_luz[i] - inter_malha.ponto_intersecao)
                            array_vetores_luz.append(vetor_luz)
                            vetor_refletido = 2 * np.dot(vetor_normal, vetor_luz) * vetor_normal - vetor_luz
                            R_array.append(vetor_refletido)

                        # Calcular a cor do pixel usando a equação de Phong
                        cor_final = self.phong(
                                current_obj=obj,
                                k_a=obj.k_ambiente,
                                I_a=cor_luz_ambiente,
                                I_l=I_l,
                                k_d=obj.k_difuso,
                                O_d=obj.cor,
                                N=vetor_normal,
                                L=array_vetores_luz,
                                k_s=obj.k_especular,
                                R=R_array,
                                V=normalize(vetor_atual),
                                n=obj.n,
                                lim_r=3,
                                k_r=obj.k_reflexao,
                                vetor_camera=normalize(vetor_atual),
                                objects=objects,
                                ponto_intersecao=inter_malha.ponto_intersecao,
                                )
                        cor = cor_final
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
