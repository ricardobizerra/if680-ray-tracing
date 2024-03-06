from vectors import Ponto, Vector, produto_escalar, produto_vetorial, multiplica_vetor_por_escalar, norma_vetor, soma_vetores
from objects import Plano, Esfera, Malha
import cv2 as cv
import numpy as np
import math

def bezierSurface(x,y,z,uCELLS, wCELLS):
    print("Alagoas")
    #Pontos de controle
    #x = np.array([])
    #y = np.array([])
    #z = np.array([])

    #Numero de celulas para cada direção

    #uCELLS = 12
    #wCELLS = 10

    #Número total de pontos de controle em U
    uPTS = np.size(x, 0)
    wPTS = np.size(x, 1)

    # Numero total de subdivisoes

    n = uPTS - 1
    m = wPTS - 1

    # Variaveis parametricas

    u = np.linspace(0, 1, uCELLS)
    w = np.linspace(0, 1, wCELLS)

    #Inicializar matriz vazia para as curvas de bezier de X,Y e Z

    xBezier = np.zeros((uCELLS,wCELLS))
    yBezier = np.zeros((uCELLS,wCELLS))
    zBezier = np.zeros((uCELLS,wCELLS))

    #Coeficientes Binomiais

    def Ni(n, i):
        return np.math.factorial(n) / (np.math.factorial(i) * np.math.factorial(n- i))
    def Mj(m, j):
        return np.math.factorial(m) / (np.math.factorial(j) * np.math.factorial(m- j))    

    # Base Polinomial de Bernstein

    def J(n, i, u):
        return np.matrix(Ni(n,i) * (u** i) * (1 - u) ** (n-i))
    
    def K(m, j, w):
        return np.matrix(Mj(m,j) * (w** j) * (1 - w) ** (m-j))
    
    #Variaveis para guaraar as bases polinomiais de bernstein
    b = []
    d = []
    #Loop principal
    #Basicamente percorremos a matriz u x w
    
    for i in range(0,uPTS):

        for j in range(0,wPTS):
            b.append(J(n,i,u))
            d.append(K(m,j,w))
            #Fazer a transposta do array J
            Jt = J(n,i,u).transpose()

            # Calculo da curva de bezier
            xBezier = Jt * K(m,j,w) * x[i,j] + xBezier
            yBezier = Jt * K(m,j,w) * y[i,j] + yBezier
            zBezier = Jt * K(m,j,w) * z[i,j] + zBezier

    
    return xBezier,yBezier,zBezier
