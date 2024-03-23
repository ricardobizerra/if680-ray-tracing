from vectors import Ponto, Vector, produto_escalar, produto_vetorial, multiplica_vetor_por_escalar, norma_vetor, soma_vetores
from objects import Plano, Esfera, Malha
import cv2 as cv
import numpy as np
import math

def ajustar_valores(espacamento):
    valores = np.arange(0, 1 + espacamento, espacamento)
    if valores[-1] > 1:
        # Remove o último valor se for maior que 1
        valores = valores[:-1]
    # Certifica-se de que 1 está incluído
    if valores[-1] < 1:
        valores = np.append(valores, 1.0)
    return valores


class Bezier:
    def __init__(self, control_points):
       
        self.control_points = control_points

    @staticmethod
    def _binomial_coefficient(n, k):
        
        return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))

    @staticmethod
    def _bernstein_polynomial(n, i, t):
        
        return Bezier._binomial_coefficient(n, i) * (t ** i) * ((1 - t) ** (n - i))
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

        cor = np.array([255,255,0])
        lista_cores = []
        for i in range(len(triplas)):
            lista_cores.append(cor)

        # Criação do objeto Malha (alguns parâmetros foram omitidos por simplicidade)
        malha = Malha(n_triangulos=len(triplas), n_vertices=len(pontos_bezier), lista_vertices=pontos_bezier, triplas=triplas,
                    lista_normais=lista_normais, lista_normais_vertices=[], lista_cores_normalizadas=lista_cores, cor=cor,
                    k_ambiente=0.1, k_difuso=0.1, k_especular=0.1, n=50, k_reflexao=0, k_refracao=0, ind_refracao=0)

        return malha

    
