import math

import cv2 as cv
import numpy as np
from scipy.optimize import fsolve

from objects import Esfera, Malha, Plano
from vectors import (Ponto, Vector, multiplica_vetor_por_escalar, norma_vetor,
                     produto_escalar, produto_vetorial, soma_vetores)

# class Toro:
#     def _init_(self, centro_y, centro_z, R, theta, alfa):
#       self.centro_y = centro_y
#       self.centro_z = centro_z
#       self.R = R
#       self.theta = theta
#       self.alfa = alfa
#       self.control_points = self._generate_control_points()

#     def _generate_control_points(self):
#       control_points = []
#       theta_values = np.linspace(0, 2 * math.pi, num=100)
#       alfa_values = np.linspace(0, 2 * math.pi, num=100)

#       for theta in theta_values:
#         for alfa in alfa_values:
#           x = (self.centro_y + self.R * math.cos(theta)) * math.sin(alfa)
#           y = (self.centro_y + self.R * math.cos(theta)) * math.cos(alfa)
#           z = self.centro_z + self.R * math.sin(theta)
#           control_points.append([x, y, z])

#       return np.array(control_points)
    
#     def point_on_surface(self, u, w):
#       u_pts, w_pts, _ = self.control_points.shape
#       point = np.zeros(3)

#       for i in range(u_pts):
#         for j in range(w_pts):
#           bu = self._bernstein_polynomial(u_pts - 1, i, u)
#           bw = self._bernstein_polynomial(w_pts - 1, j, w)
#           point += bu * bw * self.control_points[i, j, :]

#       return point
    
#     def bezier_surface(self, u_cells=10, w_cells=10):
#       u_pts, w_pts, _ = self.control_points.shape
#       u = np.linspace(0, 1, u_cells)
#       w = np.linspace(0, 1, w_cells)

#       surface = np.zeros((u_cells, w_cells, 3))

#       for i in range(u_pts):
#         for j in range(w_pts):
#           b_i = np.array([self._bernstein_polynomial(u_pts - 1, i, u_val) for u_val in u])
#           b_j = np.array([self._bernstein_polynomial(w_pts - 1, j, w_val) for w_val in w])

#           for k in range(3):
#             surface[:, :, k] += np.outer(b_i, b_j) * self.control_points[i, j, k]

#       return surface
    
#     @staticmethod
#     def _binomial_coefficient(n, k):
#       return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))
    
#     @staticmethod
#     def _bernstein_polynomial(n, i, t):
#       return Toro._binomial_coefficient(n, i) * (t ** i) * ((1 - t) ** (n - i))

def ajustar_valores(espacamento):
    """ Ajusta os valores de t e s para a triangularização

    Args:
        espacamento (float): Espaçamento entre os valores

    Returns:
        np.array: Array com os valores ajustados

    """
    valores = np.arange(0, 2 * math.pi + espacamento, espacamento)
    if valores[-1] > 2 * math.pi:
        # Remove the last value if it is greater than 2*pi
        valores = valores[:-1]
    # Make sure that 2*pi is included
    if valores[-1] < 2 * math.pi:
        valores = np.append(valores, 2 * math.pi)
    return valores
class Toro:
    def __init__(self, control_points, cor):
       
        self.control_points = control_points
        self.cor = cor

    @staticmethod
    def _binomial_coefficient(n, k):
        
        return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))

    @staticmethod
    def _bernstein_polynomial(n, i, t):
        
        return Toro._binomial_coefficient(n, i) * (t ** i) * ((1 - t) ** (n - i))
    def point_on_surface(self, u, w):
        
        u_pts, w_pts, _ = self.control_points.shape
        point = np.zeros(3)  # Initialize the point

        for i in range(u_pts):
            for j in range(w_pts):
                bu = self._bernstein_polynomial(u_pts - 1, i, u)
                bw = self._bernstein_polynomial(w_pts - 1, j, w)
                point += bu * bw * self.control_points[i, j, :]

        return point
    
    def bezier_surface(self, u_cells=10, w_cells=10):
      
        u_pts, w_pts, _ = self.control_points.shape
        u = np.linspace(0, 1, u_cells)
        w = np.linspace(0, 1, w_cells)

        # Initialize the surface
        surface = np.zeros((u_cells, w_cells, 3))

        for i in range(u_pts):
            for j in range(w_pts):
                b_i = np.array([self._bernstein_polynomial(u_pts - 1, i, u_val) for u_val in u])
                b_j = np.array([self._bernstein_polynomial(w_pts - 1, j, w_val) for w_val in w])
                
                # Update the surface points
                for k in range(u_cells):
                    for l in range(w_cells):
                        surface[k, l, :] += b_i[k] * b_j[l] * self.control_points[i, j, :]

        return surface
    

    def triangularizar(self,espaçamento):
        """ Recebe um espaçamento e triangulariza o objeto

        Args:
            espaçamento (float): Define quantos pontos vão ser transformados em triângulos na malha

        Returns:
            Malha (Malha): Objeto do tipo Malha com os triângulos correspondentes à superfície

        """

        pontos_bezier = []
        t_values = ajustar_valores(espaçamento)
        s_values = ajustar_valores(espaçamento)

        for t in t_values:
            for s in s_values:
                ponto = self.point_on_surface(t, s) # A definir
                pontos_bezier.append(ponto)

        # Lista para armazenar os triângulos como triplas de índices
        triplas = []
        n = int(1/espaçamento)  # Número de pontos em uma direção

        for i in range(n):
            for j in range(n):
                # Adiciona dois triângulos para cada quadrado da malha
                if (i+1) * (n+1) + j + 1 < len(pontos_bezier) and (i+1) * (n+1) + j < len(pontos_bezier) and i * (n+1) + j + 1 < len(pontos_bezier):
                    triplas.append((i * (n+1) + j, (i+1) * (n+1) + j, i * (n+1) + j + 1))
                    triplas.append(((i+1) * (n+1) + j, (i+1) * (n+1) + j + 1, i * (n+1) + j + 1))

        # Calculando as normais de cada triângulo
        lista_normais = []
        for triangulo in triplas:
            p0 = pontos_bezier[triangulo[0]]
            p1 = pontos_bezier[triangulo[1]]
            p2 = pontos_bezier[triangulo[2]]

            normal = np.cross(p1 - p0, p2 - p0)
            norma = np.linalg.norm(normal)
            normal = normal / norma
            
            lista_normais.append(normal)

        lista_cores = []
        for i in range(len(triplas)):
            lista_cores.append(self.cor)

        # Criação do objeto Malha (alguns parâmetros foram omitidos por simplicidade)
        malha = Malha(n_triangulos=len(triplas), n_vertices=len(pontos_bezier), lista_vertices=pontos_bezier, triplas=triplas,
                    lista_normais=lista_normais, lista_normais_vertices=[], lista_cores_normalizadas=lista_cores, cor=self.cor,
                    k_ambiente=0.5, k_difuso=0.5, k_especular=0.5, n=50, k_reflexao=0, k_refracao=0, ind_refracao=0)

        return malha

class Toro2:
    def __init__(self, centro_y, centro_z, R, r, cor):
        self.centro_y = centro_y
        self.centro_z = centro_z
        self.R = R
        self.r = r
        self.cor = cor

    def point_on_surface(self, theta, alpha):
        x = (self.R + self.r * math.cos(theta)) * math.cos(alpha)
        z = (self.R + self.r * math.cos(theta)) * math.sin(alpha)
        y = self.r * math.sin(theta)
        point = np.array([x,y,z])
        return point
    
    def triangularizar(self,espaçamento):
        """ Recebe um espaçamento e triangulariza o objeto

        Args:
            espaçamento (float): Define quantos pontos vão ser transformados em triângulos na malha

        Returns:
            Malha (Malha): Objeto do tipo Malha com os triângulos correspondentes à superfície

        """

        pontos_bezier = []
        theta_values = ajustar_valores(espaçamento)
        alpha_values = ajustar_valores(espaçamento)

        for theta in theta_values:
            for alpha in alpha_values:
                ponto = self.point_on_surface(theta, alpha)
                pontos_bezier.append(ponto)

        # Lista para armazenar os triângulos como triplas de índices
        triplas = []
        n = int(2 * math.pi/espaçamento)

        for i in range(n):
            for j in range(n):
                if (i+1) * (n+1) + j + 1 < len(pontos_bezier) and (i+1) * (n+1) + j < len(pontos_bezier) and i * (n+1) + j + 1 < len(pontos_bezier):
                    triplas.append((i * (n+1) + j, (i+1) * (n+1) + j, i * (n+1) + j + 1))
                    triplas.append(((i+1) * (n+1) + j, (i+1) * (n+1) + j + 1, i * (n+1) + j + 1))

        lista_normais = []
        for triangulo in triplas:
            p0 = pontos_bezier[triangulo[0]]
            p1 = pontos_bezier[triangulo[1]]
            p2 = pontos_bezier[triangulo[2]]

            normal = np.cross(p1 - p0, p2 - p0)
            norma = np.linalg.norm(normal)
            normal = normal / norma
            
            lista_normais.append(normal)

        lista_cores = []
        for i in range(len(triplas)):
            lista_cores.append(self.cor)

        malha = Malha(n_triangulos=len(triplas), n_vertices=len(pontos_bezier), lista_vertices=pontos_bezier, triplas=triplas,
                    lista_normais=lista_normais, lista_normais_vertices=[], lista_cores_normalizadas=lista_cores, cor=self.cor,
                    k_ambiente=0.5, k_difuso=0.5, k_especular=0.5, n=50, k_reflexao=0, k_refracao=0, ind_refracao=0)
        
        return malha 

    def triangularizar2(self, espacamento):
        """
        Recebe um espaçamento e triangulariza o objeto para formar um toro.
        """
        self.gerar_pontos_de_controle()  # Garante que os pontos de controle estão gerados

        # Ajusta os valores para corresponder à resolução desejada
        u_values = ajustar_valores(espacamento)
        v_values = ajustar_valores(espacamento)

        # Lista para armazenar os pontos da superfície de Bézier
        bezier_points = []

        for u in u_values:
            for v in v_values:
                ponto = self.point_on_surface(u, v)
                bezier_points.append(ponto)

        bezier_points = np.array(bezier_points)

        # Lista para armazenar os triângulos como triplas de índices
        triplas = []
        res = int(1 / espacamento) + 1  # Número de pontos em uma direção

        # Gera os triângulos para a malha
        for i in range(res - 1):
            for j in range(res - 1):
                # Adiciona dois triângulos para cada quadrado da malha
                triplas.append((i * res + j, i * res + (j + 1), (i + 1) * res + j))
                triplas.append(((i + 1) * res + (j + 1), (i + 1) * res + j, i * res + (j + 1)))

        # Criação do objeto Malha (usando os pontos e triplas calculados)
        malha = Malha(n_triangulos=len(triplas),
                      n_vertices=len(bezier_points),
                      lista_vertices=bezier_points.tolist(),
                      triplas=triplas,
                      cor=self.cor)

        return malha
