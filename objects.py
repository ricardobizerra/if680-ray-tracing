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
