import math
from vectors import Ponto, Vector, produto_escalar
import numpy as np
from bsp import Triangle

class Plano:
    def __init__(self, vetor_normal, Ponto, cor, k_ambiente, k_difuso, k_especular, k_reflexao, k_refracao, ind_refracao, n):
        self.vetor_normal = vetor_normal
        self.ponto = Ponto
        self.tipo = "Plano"
        self.cor = cor
        self.k_ambiente = k_ambiente
        self.k_difuso = k_difuso
        self.k_especular = k_especular
        self.k_reflexao = k_reflexao
        self.k_refracao = k_refracao
        self.IOR = ind_refracao
        self.n = n

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
    def __init__(self, centro, raio, cor, k_ambiente, k_difuso, k_especular, k_reflexao, k_refracao, ind_refracao, n):
        self.centro = centro
        self.raio = raio
        self.tipo = "Esfera"
        self.cor = cor
        self.k_ambiente = k_ambiente
        self.k_difuso = k_difuso
        self.k_especular = k_especular
        self.k_reflexao = k_reflexao
        self.k_refracao = k_refracao
        self.IOR = ind_refracao
        self.n = n

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
            if t<=0.01:
                t = 10000
            if t2<=0.01:
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
    def __init__(self, n_triangulos, n_vertices, lista_vertices, triplas, lista_normais, lista_normais_vertices, lista_cores_normalizadas, cor,
                 k_ambiente, k_difuso, k_especular, n, k_reflexao,k_refracao,ind_refracao ):
        self.n_triangulos = n_triangulos
        self.n_vertices = n_vertices
        self.tipo = "Malha"
        self.lista_vertices = lista_vertices
        self.triangulos = triplas # Organizadas por índice
        self.normais_t = lista_normais
        self.normais_v = lista_normais_vertices
        self.lista_cores_normalizadas = lista_cores_normalizadas
        self.cor = cor
        self.k_ambiente = k_ambiente
        self.k_difuso = k_difuso
        self.k_especular = k_especular
        self.n = n
        self.k_reflexao = k_reflexao
        self.k_refracao = k_refracao
        self.IOR = ind_refracao
        
    def triangularizar(self):
        """ Retorna lista de triângulos dessa malha """
        triangle_list = []
        for i in range(self.n_triangulos):
            tripla = self.triangulos[i]
            triangle = Triangle(self.lista_vertices[tripla[0]], self.lista_vertices[tripla[1]], self.lista_vertices[tripla[2]], self.normais_t[i])
            triangle_list.append(triangle)
        return triangle_list
    
    def intersecao_reta_malha(self, vdiretor, P):
        menor_t = self.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.lista_cores_normalizadas[0], None)
        for idx_triangulo in range(self.n_triangulos):
            intersecao = self.intersecao_triangulo_reta(vdiretor, P, idx_triangulo)
            if intersecao.intersecao and intersecao.t <= menor_t.t:
                menor_t = intersecao
        return menor_t

    class Intersecao_Return:
        def __init__(self, intersecao, t, ponto_intersecao, cor_normalizada, normal_ponto):
            self.intersecao = intersecao
            self.t = t
            self.ponto_intersecao = ponto_intersecao
            self.cor_normalizada = cor_normalizada
            self.normal_ponto = normal_ponto
    
    def calculo_ponto_intersecao(self, vdiretor, P, vetor_normal, ponto_plano):
        temp = np.dot(vetor_normal, vdiretor)
        if temp == 0:
            return Malha.Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.lista_cores_normalizadas[0], None)
        t = (np.dot(vetor_normal, ponto_plano) - np.dot(vetor_normal,P)) / temp
        x = P[0] + vdiretor[0] * t
        y = P[1] + vdiretor[1] * t
        z = P[2] + vdiretor[2] * t
        return Malha.Intersecao_Return(True, t, np.array([x, y, z]), self.lista_cores_normalizadas[0], vetor_normal)

    def intersecao_triangulo_reta(self, vdiretor, P, idx_triangulo):
        tripla_triangulo = self.triangulos[idx_triangulo]
        normal_triangulo = self.normais_t[idx_triangulo]
        cor_normalizada = self.lista_cores_normalizadas[idx_triangulo]

        temp = np.dot(normal_triangulo, vdiretor)
        if temp == 0:
            return Malha.Intersecao_Return(False, 1000000, np.array([0,0,0]), cor_normalizada, None)
        else:
            # Definindo coordenadas baricêntricas
            p1 = self.lista_vertices[tripla_triangulo[0]]
            p2 = self.lista_vertices[tripla_triangulo[1]]
            p3 = self.lista_vertices[tripla_triangulo[2]]

            p1 = np.array(p1)
            p2 = np.array(p2)
            p3 = np.array(p3)

            intersecao_plano = self.calculo_ponto_intersecao(vdiretor, P, normal_triangulo, p1)

            if intersecao_plano.intersecao:
                ponto_intersecao = intersecao_plano.ponto_intersecao
                v0 = p2 - p1
                v1 = p3 - p1
                v2 = ponto_intersecao - p1

                d00 = np.dot(v0, v0)
                d01 = np.dot(v0, v1)
                d11 = np.dot(v1, v1)
                d20 = np.dot(v2, v0)
                d21 = np.dot(v2, v1)

                denom = d00 * d11 - d01 * d01

                v = (d11 * d20 - d01 * d21) / denom
                w = (d00 * d21 - d01 * d20) / denom
                u = 1.0 - v - w

                if v >= 0 and w >= 0 and u >= 0:
                    return Malha.Intersecao_Return(True, intersecao_plano.t, ponto_intersecao, cor_normalizada, normal_triangulo)
                else:
                    return Malha.Intersecao_Return(False, 1000000, np.array([0,0,0]), cor_normalizada, None)
            else:
                return Malha.Intersecao_Return(False, 1000000, np.array([0,0,0]), cor_normalizada, None)
            
