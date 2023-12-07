import math
from vectors import Ponto, Vector, produto_escalar
import numpy as np


class Plano:
    def __init__(self, v, P):
        self.vetor_normal = v
        self.ponto = P
        self.tipo = "Plano"

    def intersecao_plano_reta(self, vdiretor, P):
        calculo_ponto_intersecao = self.calculo_ponto_intersecao(vdiretor, P)
        return calculo_ponto_intersecao

    class Intersecao_Return:
        def __init__(self, intersecao, t, ponto_intersecao):
            self.intersecao = intersecao
            self.t = t
            self.ponto_intersecao = ponto_intersecao

    def calculo_ponto_intersecao(self, vdiretor, P):
        temp = np.dot(self.vetor_normal, vdiretor)
        if temp == 0:
            return Plano.Intersecao_Return(False, 1000000, np.array([0, 0, 0]))
        t = (np.dot(self.vetor_normal,self.ponto) - np.dot(self.vetor_normal,P)) / temp
        x = P[0] + vdiretor[0] * t
        y = P[1] + vdiretor[1] * t
        z = P[2] + vdiretor[2] * t
        return Plano.Intersecao_Return(True, t, np.array([x, y, z]))

class Esfera:
    def __init__(self, P, r):
        self.centro = P
        self.raio = r
        self.tipo = "Esfera"

    class Intersecao_Return:
        def __init__(self, intersecao, t, ponto_intersecao):
            self.intersecao = intersecao
            self.t = t
            self.ponto_intersecao = ponto_intersecao

    def intersecao_esfera_reta(self, vdiretor, P):
        CP = P - self.centro
        a = np.dot(vdiretor, vdiretor)
        b = 2 * np.dot(vdiretor, CP)
        c = np.dot(CP, CP) - self.raio * self.raio
        delta = b * b - 4 * a * c

        if delta >= 0:
            bhaskara_upper = -b + math.sqrt(delta)
            bhaskara_upper2 = -b - math.sqrt(delta)
            bhaskara_lower = 2 * a
            t = bhaskara_upper / bhaskara_lower
            t2 = bhaskara_upper2 / bhaskara_lower
            if t<=0:
                t = 10000
            if t2<=0:
                t2 = 10000
            if t==10000 and t2==10000:
                return Esfera.Intersecao_Return(False, 1000000, np.array([0, 0, 0]))
            teste = min(t,t2)
            x = P[0] + vdiretor[0] * teste
            y = P[1] + vdiretor[1] * teste
            z = P[2] + vdiretor[2] * teste
            return Esfera.Intersecao_Return(True, min(t,t2), np.array([x, y, z]))
        
        return Esfera.Intersecao_Return(False, 1000000, np.array([0, 0, 0]))

class Malha:
    def __init__(self, n_triangulos, n_vertices, lista_vertices, triplas, lista_normais, lista_normais_vertices, cor_normalizada):
        self.n_triangulos = n_triangulos
        self.n_vertices = n_vertices
        self.tipo = "Malha"
        self.lista_vertices = lista_vertices
        self.triangulos = triplas
        self.normais_t = lista_normais
        self.normais_v = lista_normais_vertices
        self.cor_normalizada = cor_normalizada

    def intersecao_reta_malha(self, vdiretor, P):
        menor_t = self.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.cor_normalizada)
        for idx_triangulo in range(self.n_triangulos):
            intersecao = self.intersecao_triangulo_reta(vdiretor, P, idx_triangulo)
            if intersecao.intersecao and intersecao.t <= menor_t.t:
                menor_t = intersecao
        return menor_t

    class Intersecao_Return:
        def __init__(self, intersecao, t, ponto_intersecao, cor_normalizada):
            self.intersecao = intersecao
            self.t = t
            self.ponto_intersecao = ponto_intersecao
            self.cor_normalizada = cor_normalizada
    
    def calculo_ponto_intersecao(self, vdiretor, P, vetor_normal, ponto_plano):
        temp = np.dot(vetor_normal, vdiretor)
        if temp == 0:
            return Malha.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.cor_normalizada)
        t = (np.dot(vetor_normal, ponto_plano) - np.dot(vetor_normal,P)) / temp
        x = P[0] + vdiretor[0] * t
        y = P[1] + vdiretor[1] * t
        z = P[2] + vdiretor[2] * t
        return Malha.Intersecao_Return(True, t, np.array([x, y, z]), self.cor_normalizada)

    def intersecao_triangulo_reta(self, vdiretor, P, idx_triangulo):
        tripla_triangulo = self.triangulos[idx_triangulo]
        normal_triangulo = self.normais_t[idx_triangulo]

        temp = np.dot(normal_triangulo, vdiretor)
        if temp == 0:
            return False
        else:
            # Definindo coordenadas baricêntricas
            p1 = self.lista_vertices[tripla_triangulo[0]]
            p2 = self.lista_vertices[tripla_triangulo[1]]
            p3 = self.lista_vertices[tripla_triangulo[2]]

            p1 = np.array(p1)
            p2 = np.array(p2)
            p3 = np.array(p3)

            intersecao_plano = self.calculo_ponto_intersecao(vdiretor, P, normal_triangulo, p1)

            # c1 + c2 + c3 = 1
            # Px = c1 * p1x + c2 * p2x + c3 * p3x
            # Py = c1 * p1y + c2 * p2y + c3 * p3y
            # Pz = c1 * p1z + c2 * p2z + c3 * p3z

            # Para não ter que calcular a solução desse sistema linear, podemos usar uma fórmula para o cálculo dos coeficientes de forma mais direta
            # Podemos dizer que a área que o ponto em questão com cada dupla de pontos do triângulo pode nos dar os coeficientes
            # [t1]/[p1p2p3] + [t2]/[p1p2p3] + [t3]/[p1p2p3] = 1
            # c1 = [t1]/[p1p2p3]
            # c2 = [t2]/[p1p2p3]
            # c3 = [t3]/[p1p2p3]

            area_total = np.linalg.norm(np.cross((p2-p1), (p3-p1))) / 2

            # Check for division by zero or invalid values
            if np.any(area_total == 0):
                return Malha.Intersecao_Return(False, 100000, np.array([0,0,0]), self.cor_normalizada)

            t1 = np.linalg.norm(np.cross((p1 - intersecao_plano.ponto_intersecao), (p2 - intersecao_plano.ponto_intersecao))) / 2
            t2 = np.linalg.norm(np.cross((p1 - intersecao_plano.ponto_intersecao), (p3 - intersecao_plano.ponto_intersecao))) / 2
            t3 = np.linalg.norm(np.cross((p2 - intersecao_plano.ponto_intersecao), (p3 - intersecao_plano.ponto_intersecao))) / 2

            c1 = t1 / area_total
            c2 = t2 / area_total
            c3 = t3 / area_total
            
            if c1 >= 0 and c2 >= 0 and c3 >= 0:
                return Malha.Intersecao_Return(True, intersecao_plano.t, intersecao_plano.ponto_intersecao, self.cor_normalizada)
            else:
                return Malha.Intersecao_Return(False, 100000, np.array([0,0,0]), self.cor_normalizada)