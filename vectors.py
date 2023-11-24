import math

class Ponto:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

def imprime_ponto(p):
    print(f"({p.x}, {p.y}, {p.z})")

def soma_pontos(p1, p2):
    return Ponto(p1.x + p2.x, p1.y + p2.y, p1.z + p2.z)

def subtrai_pontos(p1, p2):
    return Ponto(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)

def distancia_pontos(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dz = p1.z - p2.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)

def produto_escalar(p1, p2):
    return p1.x * p2.x + p1.y * p2.y + p1.z * p2.z

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

def soma_vetores(v1, v2):
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def subtrai_vetores(v1, v2):
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def produto_escalar_vetores(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def produto_vetorial(v1, v2):
    return Vector(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)

def multiplica_vetor_por_escalar(v, escalar):
    return Vector(v.x * escalar, v.y * escalar, v.z * escalar)

def norma_vetor(v):
    return math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)

def imprime_vetor(v):
    print(f"({v.x}, {v.y}, {v.z})")
