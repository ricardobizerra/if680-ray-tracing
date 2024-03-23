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

    

    def triangularizar(espaçamento):
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
                ponto = bezier_point(t, s) # A definir
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
            p1 = pontos_bezier[triangulo[2]]
            p2 = pontos_bezier[triangulo[3]]

            normal = np.cross(p1 - p0, p2 - p0)
            norma = np.linalg.norm(normal)
            normal = normal / norma
            
            lista_normais.append(normal)

        cor = np.array([255,255,0])
        lista_cores = []
        for i in range(triplas):
            lista_cores.append(cor)

        # Criação do objeto Malha (alguns parâmetros foram omitidos por simplicidade)
        malha = Malha(n_triangulos=len(triplas), n_vertices=len(pontos_bezier), lista_vertices=pontos_bezier, triplas=triplas,
                    lista_normais=lista_normais, lista_normais_vertices=[], lista_cores_normalizadas=lista_cores, cor=cor,
                    k_ambiente=0.1, k_difuso=0.1, k_especular=0.1, n=50, k_reflexao=0, k_refracao=0, ind_refracao=0)

        return malha

    return xBezier,yBezier,zBezier
