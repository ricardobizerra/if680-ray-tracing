import numpy as np

class Intersecao_Return:
        def __init__(self, intersecao, t, ponto_intersecao, cor_normalizada, normal_ponto):
            self.intersecao = intersecao
            self.t = t
            self.ponto_intersecao = ponto_intersecao
            self.cor_normalizada = cor_normalizada
            self.normal_ponto = normal_ponto

class Triangle:
    def __init__(self, vertice1, vertice2, vertice3, normal, cor, k_ambiente, k_difuso, k_especular, k_reflexao, k_refracao, ind_refracao, n):
        self.v1 = vertice1
        self.v2 = vertice2
        self.v3 = vertice3
        self.tipo = "Triangle"
        self.normal = normal
        self.cor = cor
        self.k_ambiente = k_ambiente
        self.k_difuso = k_difuso
        self.k_especular = k_especular
        self.k_reflexao = k_reflexao
        self.k_refracao = k_refracao
        self.IOR = ind_refracao
        self.n = n
    
    def calculo_ponto_intersecao(self, vdiretor, P, vetor_normal, ponto_plano):
        temp = np.dot(vetor_normal, vdiretor)
        if temp == 0:
            return Intersecao_Return(False, 1000000, np.array([0, 0, 0]), self.cor, None)
        t = (np.dot(vetor_normal, ponto_plano) - np.dot(vetor_normal,P)) / temp
        x = P[0] + vdiretor[0] * t
        y = P[1] + vdiretor[1] * t
        z = P[2] + vdiretor[2] * t
        return Intersecao_Return(True, t, np.array([x, y, z]), self.cor, vetor_normal)
    
    def intersecao_triangulo_reta(self, vdiretor, P):
        temp = np.dot(self.normal, vdiretor)
        if temp == 0:
            return Intersecao_Return(False, 1000000, np.array([0,0,0]), self.cor, None)
        else:
            # Definindo coordenadas baricêntricas
            p1 = self.v1
            p2 = self.v2
            p3 = self.v3

            p1 = np.array(p1)
            p2 = np.array(p2)
            p3 = np.array(p3)

            intersecao_plano = self.calculo_ponto_intersecao(vdiretor, P, self.normal, p1)

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
                    return Intersecao_Return(True, intersecao_plano.t, ponto_intersecao, self.cor, self.normal)
                else:
                    return Intersecao_Return(False, 1000000, np.array([0,0,0]), self.cor, None)
            else:
                return Intersecao_Return(False, 1000000, np.array([0,0,0]), self.cor, None)

class BSPNode:
    def __init__(self, polygon=None):
        self.polygon = polygon  # O polígono que define o plano deste nó
        self.polygons = [] if polygon is None else [polygon]
        self.front = None
        self.back = None

    def add_polygon(self, polygon):
        # Adiciona um polígono à lista deste nó ou o distribui para os nós filhos
        if self.polygon is None:
            self.polygon = polygon
            self.polygons.append(polygon)
            return
    
        if is_in_front(polygon, self.polygon):
            print("entrou em is_in_front")
            if self.front is None:
                self.front = BSPNode()
            self.front.add_polygon(polygon)

        elif is_behind(polygon, self.polygon):
            print("entrou em is_behind")
            if self.back is None:
                self.back = BSPNode()
            self.back.add_polygon(polygon)

        elif is_intersected(polygon, self.polygon):
            front_part, back_part = split_polygon(polygon, self.polygon)
            # Considerando que split_polygon pode retornar None ou uma lista de triângulos
            if front_part:
                if self.front is None:
                    self.front = BSPNode()

                for part in (front_part if isinstance(front_part, list) else [front_part]):
                    self.front.add_polygon(part)
                
            if back_part:
                if self.back is None:
                    self.back = BSPNode()

                for part in (back_part if isinstance(back_part, list) else [back_part]):
                    self.back.add_polygon(part)

        else:
            print("entrou no else")
            # O polígono está no mesmo plano que o polígono do nó
            self.polygons.append(polygon)


def calculate_distance_to_plane(point, plane_point, plane_normal):
    """
    Calcula a distância de um ponto até um plano.
    
    Args:
    - point: Ponto (np.array) para o qual a distância até o plano será calculada.
    - plane_point: Um ponto (np.array) no plano.
    - plane_normal: A normal (np.array) do plano.
    
    Returns:
    - A distância (float) do ponto até o plano.
    """
    distance = np.dot((point - plane_point), plane_normal)
    return distance

def is_in_front(triangle, plane_triangle):
    """
    Determina se um triângulo está inteiramente na frente do plano definido por outro triângulo.
    
    Args:
    - triangle: O triângulo (Triangle) para verificar.
    - plane_triangle: O triângulo (Triangle) que define o plano.
    
    Returns:
    - True se o triângulo estiver inteiramente na frente do plano, False caso contrário.
    """
    distances = [
        calculate_distance_to_plane(triangle.v1, plane_triangle.v1, plane_triangle.normal),
        calculate_distance_to_plane(triangle.v2, plane_triangle.v1, plane_triangle.normal),
        calculate_distance_to_plane(triangle.v3, plane_triangle.v1, plane_triangle.normal)
    ]

    non_zero_distances = [d > 0.001 or d < 0.001 for d in distances]
    return len(non_zero_distances) > 0 and all(d >= 0 for d in distances)

def is_behind(triangle, plane_triangle):
    """
    Determina se um triângulo está inteiramente atrás do plano definido por outro triângulo.
    
    Args:
    - triangle: O triângulo (Triangle) para verificar.
    - plane_triangle: O triângulo (Triangle) que define o plano.
    
    Returns:
    - True se o triângulo estiver inteiramente atrás do plano, False caso contrário.
    """
    distances = [
        calculate_distance_to_plane(triangle.v1, plane_triangle.v1, plane_triangle.normal),
        calculate_distance_to_plane(triangle.v2, plane_triangle.v1, plane_triangle.normal),
        calculate_distance_to_plane(triangle.v3, plane_triangle.v1, plane_triangle.normal)
    ]

    non_zero_distances = [d > 0.001 or d < 0.001 for d in distances]
    return len(non_zero_distances) > 0 and all(d <= 0 for d in distances)


def is_intersected(triangle, plane_triangle):
    distances = [
        calculate_distance_to_plane(triangle.v1, plane_triangle.v1, plane_triangle.normal),
        calculate_distance_to_plane(triangle.v2, plane_triangle.v1, plane_triangle.normal),
        calculate_distance_to_plane(triangle.v3, plane_triangle.v1, plane_triangle.normal)
    ]
    return any(d > 0 for d in distances) and any(d < 0 for d in distances)

def calculate_intersection_point(p1, p2, plane_point, plane_normal):
    # Esta função calcula o ponto de interseção entre a linha formada por p1 e p2 e o plano
    line_direction = p2 - p1
    plane_to_p1 = p1 - plane_point
    t = -np.dot(plane_normal, plane_to_p1) / np.dot(plane_normal, line_direction)
    intersection_point = p1 + t * line_direction
    return intersection_point

def pontos_sao_iguais(p1, p2, tol=1e-6):
    return np.linalg.norm(p1 - p2) < tol

def split_polygon(triangle, plane_triangle):
    points = [triangle.v1, triangle.v2, triangle.v3]
    distances = [calculate_distance_to_plane(point, plane_triangle.v1, plane_triangle.normal) for point in points]

    front_points = []
    back_points = []
    intersection_points = []
    original_front_vertices = []
    original_back_vertices = []

    for i, distance in enumerate(distances):
        current_point = points[i]
        current_distance = distances[i]

        # Verifica se a aresta entre os pontos atuais intersecta o plano
        next_index = (i + 1) % 3
        next_point = points[next_index]
        next_distance = distances[next_index]

        if distance > 0:
            if not any(pontos_sao_iguais(current_point, p, 0) for p in front_points):
                front_points.append(current_point)
                original_front_vertices.append(current_point)
        elif distance < 0:
            if not any(pontos_sao_iguais(current_point, p, 0) for p in back_points):
                back_points.append(current_point)
                original_back_vertices.append(current_point)
        
        if distance == 0 or next_distance == 0 or current_distance * next_distance < 0:
            intersection_point = calculate_intersection_point(current_point, next_point, plane_triangle.v1, plane_triangle.normal)
            if not any(pontos_sao_iguais(intersection_point, p, 0) for p in intersection_points):
                intersection_points.append(intersection_point)
                if distance >= 0:  # Inclui casos de estar no plano e à frente dele
                    front_points.append(intersection_point)
                if distance <= 0:  # Inclui casos de estar no plano e atrás dele
                    back_points.append(intersection_point)

    # Construção dos triângulos
    if len(front_points) == 3:
        front_triangle = Triangle(front_points[0], front_points[1], front_points[2], triangle.normal,
                                  cor=triangle.cor,
                                  k_ambiente=triangle.k_ambiente,
                                  k_difuso=triangle.k_difuso,
                                  k_especular=triangle.k_especular,
                                  k_reflexao=triangle.k_reflexao,
                                  k_refracao=triangle.k_refracao,
                                  ind_refracao=triangle.IOR,
                                  n=triangle.n)
    elif len(front_points) > 3:
        # Calcular as distâncias entre o ponto de interseção de índice 0 e os vértices originais
        distances = [np.linalg.norm(intersection_points[0] - v) for v in original_front_vertices]
    
        # Encontrar o vértice original mais próximo ao ponto de interseção de índice 0
        closest_vertex_index = np.argmin(distances)
        closest_vertex = original_front_vertices[closest_vertex_index]
    
        # O outro vértice original é aquele que não é o mais próximo
        other_vertex = original_front_vertices[1 - closest_vertex_index]
    
        # Formar os novos triângulos garantindo que o ponto de interseção de índice 0 esteja conectado ao vértice mais próximo
        front_triangle_1 = Triangle(intersection_points[0], intersection_points[1], closest_vertex, triangle.normal,
                                  cor=triangle.cor,
                                  k_ambiente=triangle.k_ambiente,
                                  k_difuso=triangle.k_difuso,
                                  k_especular=triangle.k_especular,
                                  k_reflexao=triangle.k_reflexao,
                                  k_refracao=triangle.k_refracao,
                                  ind_refracao=triangle.IOR,
                                  n=triangle.n)
        front_triangle_2 = Triangle(intersection_points[1], closest_vertex, other_vertex, triangle.normal,
                                  cor=triangle.cor,
                                  k_ambiente=triangle.k_ambiente,
                                  k_difuso=triangle.k_difuso,
                                  k_especular=triangle.k_especular,
                                  k_reflexao=triangle.k_reflexao,
                                  k_refracao=triangle.k_refracao,
                                  ind_refracao=triangle.IOR,
                                  n=triangle.n)
        print("Entrou em front_points no split")
        print(intersection_points)
        print(original_front_vertices)

        front_triangle = [front_triangle_1, front_triangle_2]
    else:
        front_triangle = None

    if len(back_points) == 3:
        back_triangle = Triangle(back_points[0], back_points[1], back_points[2], triangle.normal,
                                  cor=triangle.cor,
                                  k_ambiente=triangle.k_ambiente,
                                  k_difuso=triangle.k_difuso,
                                  k_especular=triangle.k_especular,
                                  k_reflexao=triangle.k_reflexao,
                                  k_refracao=triangle.k_refracao,
                                  ind_refracao=triangle.IOR,
                                  n=triangle.n)
    elif len(back_points) > 3:
        # Calcular as distâncias entre o ponto de interseção de índice 0 e os vértices originais
        distances = [np.linalg.norm(intersection_points[0] - v) for v in original_back_vertices]
    
        # Encontrar o vértice original mais próximo ao ponto de interseção de índice 0
        closest_vertex_index = np.argmin(distances)
        closest_vertex = original_back_vertices[closest_vertex_index]
    
        # O outro vértice original é aquele que não é o mais próximo
        other_vertex = original_back_vertices[1 - closest_vertex_index]
    
        # Formar os novos triângulos garantindo que o ponto de interseção de índice 0 esteja conectado ao vértice mais próximo
        back_triangle_1 = Triangle(intersection_points[0], intersection_points[1], closest_vertex, triangle.normal,
                                  cor=triangle.cor,
                                  k_ambiente=triangle.k_ambiente,
                                  k_difuso=triangle.k_difuso,
                                  k_especular=triangle.k_especular,
                                  k_reflexao=triangle.k_reflexao,
                                  k_refracao=triangle.k_refracao,
                                  ind_refracao=triangle.IOR,
                                  n=triangle.n)
        back_triangle_2 = Triangle(intersection_points[1], closest_vertex, other_vertex, triangle.normal,
                                  cor=triangle.cor,
                                  k_ambiente=triangle.k_ambiente,
                                  k_difuso=triangle.k_difuso,
                                  k_especular=triangle.k_especular,
                                  k_reflexao=triangle.k_reflexao,
                                  k_refracao=triangle.k_refracao,
                                  ind_refracao=triangle.IOR,
                                  n=triangle.n)
        print("Entrou em back points no split")
        print(intersection_points)
        print(original_back_vertices)

        back_triangle = [back_triangle_1, back_triangle_2]
    else:
        back_triangle = None

    return front_triangle, back_triangle

def build_BSP_tree(triangle_list):
    root = BSPNode()
    for triangle in triangle_list:
        root.add_polygon(triangle)
    
    return root

def side_of_plane(point, triangle):
    d = calculate_distance_to_plane(point, triangle.v1, triangle.normal)
    return "FRONT" if d > 0 else "BACK"

def traverse_bsp_and_collect_triangles(node, ray_origin, ray_direction, triangles=None):
    if triangles is None:
        triangles = []
    if node is None:
        return triangles
    if node.front is None and node.back is None:  # Nó folha
        triangles.extend(node.polygons)
        return triangles
    
    # Verifica qual lado do plano o raio começa
    start_side = side_of_plane(ray_origin, node.polygon)
    if start_side == "FRONT":
        first_node, second_node = node.front, node.back
    else:
        first_node, second_node = node.back, node.front
    
    # Traverse o primeiro nó e coleta os triângulos
    traverse_bsp_and_collect_triangles(first_node, ray_origin, ray_direction, triangles)
    
    # Traverse o segundo nó e coleta os triângulos
    traverse_bsp_and_collect_triangles(second_node, ray_origin, ray_direction, triangles)
    
    return triangles

def print_bsp_tree(node, depth=0):
    # Base case: se o nó for None, a função retorna
    if node is None:
        return
    
    # Imprime a profundidade para dar uma noção da estrutura da árvore
    indent = "  " * depth  # Cria um recuo baseado na profundidade do nó
    
    # Se o nó não contiver um polígono, ele é um nó folha
    if node.polygon is None:
        print(f"{indent}Nó Folha: {len(node.polygons)} polígono(s)")
    else:
        print(f"{indent}Nó com polígono: 1 polígono principal, {len(node.polygons) - 1} polígono(s) coplanares")
    
    # Para cada polígono no nó, imprime informações básicas
    for polygon in node.polygons:
        print(f"{indent}  Polígono: V1: {polygon.v1}, V2: {polygon.v2}, V3: {polygon.v3}, Normal: {polygon.normal}")
    
    # Recursivamente imprime os nós filhos, aumentando a profundidade
    if node.front:
        print(f"{indent}Front:")
        print_bsp_tree(node.front, depth + 1)
    
    if node.back:
        print(f"{indent}Back:")
        print_bsp_tree(node.back, depth + 1)