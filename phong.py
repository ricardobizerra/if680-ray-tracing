
# - Alguns dos parâmetros da equação de Phong acima, não foram exemplificados em nenhum objeto, esses são os seguintes:
#     - O vetor que parte do ponto da superfície do objeto onde a interseção ocorreu e aponta para a luz  $\small {I_{L_n}} \longrightarrow \; {L_n}({ln_1}, {ln_2}, {ln_3}) \; onde, \; {ln_1}, \; {ln_2}, \; {ln_3} \in \mathbb{R} \; e \; 1 \leqslant {n} \leqslant {m};$
#     - A normal no ponto da superfície do objeto onde a interseção ocorreu $\small \longrightarrow \; N({n_1}, {n_2}, {n_3}) \; onde, \; {n_1}, \; {n_2}, \; {n_3} \in \mathbb{R};$
#     - O vetor de reflexão em relação a luz $\small {I_{L_n}} \; no  \; ponto \; da \;superfície \; onde \; a \;interseção \; ocorreu \; \longrightarrow  \; {R_n}({rn_1}, {rn_2}, {rn_3}) \; onde \; {rn_1}, \; {rn_2}, \; {rn_3} \in \mathbb \; {R} \; e \; 1 \leqslant \; {n} \leqslant \; {m};$
#     - O vetor que aponta para o espectador. Para os raios primários, no ray-casting por exemplo, esse espectador  ́e a câmera. O espectador muda quando estamos tratando reflexões e refrações $\small \longrightarrow \; V({v_1}, {v_2}, {v_3}) \; onde, \; {v_1}, \; {v_2}, \; {v_3} \in \mathbb\; {R}$
#     - A cor RGB retornada pelo raio refletido $\small \longrightarrow \; {I_r} \in \; [0,255]^3$
#     - A cor RGB retornada pelo raio refratado
import numpy as np
import math
# na multiplicação de I certifica q tu ta multiplicando valroes e nao arrays  senao tua funcao vai retornar um array quadridimensional
def phong_model():
    # Coeficientes de iluminação
    ka = np.array([0.1, 0.1, 0.1]) #ambiental
    kd = np.array([0.7, 0.7, 0.7]) #difuso
    ks = np.array([0.5, 0.5, 0.5]) #especular
    kr = np.array([0.5, 0.5, 0.5]) #reflexão
    kt = np.array([0.5, 0.5, 0.5]) #transmissão
    n = 10 #coeficiente de rugosidade

    # Cores
    Ia = np.array([255, 255, 255])
    Il = np.array([255, 255, 255])

    # Vetores
    L = np.array([1, 1, 1])
    N = np.array([1, 1, 1])
    V = np.array([1, 1, 1])
    R = np.array([1, 1, 1])

    # Cálculo da cor
    I = (ka * Ia + Il * (kd * (N.dot(L)) + ks * (R.dot(V))**n)) + kr * I + kt * I
    return I

phong_model()
# - Definir as fontes de luz
    
#     **Ela pode ser uma classe com os seguintes atributos:**
    
#     - Luzes
#         - Cada luz é um ponto, que determina sua localização $\small \longrightarrow \; {l}(x, y, z) \; onde, \; x, \; y, \; z \in \mathbb{R}$
#         - Intensidade da luz, uma cor RGB $\small \longrightarrow \; {I_{L_n}} \in \; [0, 255]^3 \; onde \; 1 \leqslant \; {n} \leqslant \; {m}.$
#     - Ambiente
#         - Uma cor ambiente, funciona como um filtro $\small \longrightarrow \; {I_a} \in \;[0, 255]^3.$
# - Implementar o modelo de iluminação de phong;
#     - O programa continuará executando o ray-casting, mas agora ao invés de retornar a apenas a cor dos objetos interceptados para cada pixel; ele irá calcular a cor de acordo com o modelo de iluminação de phong para cada pixel;
#     - Por hora, a parte (kr · Ir + kt · It) da equação de Phong deve ser ignorada j ́a que as reflexões e refrações fazem parte da segunda entrega.

# \small I = (k_a \cdot I_a + \sum^m_{i=1} [I_{Li} * O_d * k_d * (\mathbf{N} \cdot \mathbf{L_i}) + I_{Li} * k_s * (\mathbf{R_i} \cdot \mathbf{V})^n]) + k_r * I_r + k_t * I_t

class FonteLuz:
    def __init__(self, x=0, y=0, z=0, I=0):
        self.x = x
        self.y = y
        self.z = z
        self.I = I
    
    def imprime_fonte_luz(self):
        print(f"({self.x}, {self.y}, {self.z}) - {self.I}")
        