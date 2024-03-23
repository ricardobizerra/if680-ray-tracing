from vectors import Ponto, Vector, produto_escalar, produto_vetorial, multiplica_vetor_por_escalar, norma_vetor, soma_vetores
from objects import Plano, Esfera, Malha
import cv2 as cv
import numpy as np
import math


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