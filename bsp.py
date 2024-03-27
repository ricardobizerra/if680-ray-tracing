import numpy as np

class Triangle:
    def __init__(self, vertice1, vertice2, vertice3, normal):
        self.v1 = vertice1
        self.v2 = vertice2
        self.v3 = vertice3
        self.normal = normal

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
            if self.front is None:
                self.front = BSPNode()
            self.front.add_polygon(polygon)

        elif is_behind(polygon, self.polygon):
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
    return all(d > 0 for d in distances)

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
    return all(d < 0 for d in distances)


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

def split_polygon(triangle, plane_triangle):
    points = [triangle.v1, triangle.v2, triangle.v3]
    distances = [calculate_distance_to_plane(point, plane_triangle.v1, plane_triangle.normal) for point in points]

    front_points = []
    back_points = []

    # Primeiro, adicione vértices exatamente no plano para ambos os lados
    for i, distance in enumerate(distances):
        if distance == 0:
            intersection_point = points[i]
            front_points.append(intersection_point)
            back_points.append(intersection_point)

    # Processa cada aresta para verificar interseções com o plano
    for i in range(3):
        current_point = points[i]
        next_point = points[(i + 1) % 3]
        current_distance = distances[i]
        next_distance = distances[(i + 1) % 3]

        # Adiciona pontos com base na posição relativa ao plano
        if current_distance > 0:
            front_points.append(current_point)
        elif current_distance < 0:
            back_points.append(current_point)

        # Verifica se a aresta entre os pontos atuais intersecta o plano
        if current_distance * next_distance < 0:  # Sinais diferentes indicam interseção
            intersection_point = calculate_intersection_point(current_point, next_point, plane_triangle.v1, plane_triangle.normal)
            front_points.append(intersection_point)
            back_points.append(intersection_point)

    # Construção dos triângulos
    if len(front_points) == 3:
        front_triangle = Triangle(front_points[0], front_points[1], front_points[2], triangle.normal)
    elif len(front_points > 3):
        # Identificar pontos de interseção e vértices originais
        intersection_points = [p for p in front_points if p not in points]
        original_vertices = [p for p in front_points if p in points]
    
        # Calcular as distâncias entre o ponto de interseção de índice 0 e os vértices originais
        distances = [np.linalg.norm(intersection_points[0] - v) for v in original_vertices]
    
        # Encontrar o vértice original mais próximo ao ponto de interseção de índice 0
        closest_vertex_index = np.argmin(distances)
        closest_vertex = original_vertices[closest_vertex_index]
    
        # O outro vértice original é aquele que não é o mais próximo
        other_vertex = original_vertices[1 - closest_vertex_index]
    
        # Formar os novos triângulos garantindo que o ponto de interseção de índice 0 esteja conectado ao vértice mais próximo
        front_triangle_1 = Triangle(intersection_points[0], intersection_points[1], closest_vertex, triangle.normal)
        front_triangle_2 = Triangle(intersection_points[1], closest_vertex, other_vertex, triangle.normal)

        front_triangle = [front_triangle_1, front_triangle_2]
    else:
        front_triangle = None

    if len(back_points) == 3:
        back_triangle = Triangle(back_points[0], back_points[1], back_points[2], triangle.normal)
    elif len(back_points > 3):
        # Identificar pontos de interseção e vértices originais
        intersection_points = [p for p in back_points if p not in points]
        original_vertices = [p for p in back_points if p in points]
    
        # Calcular as distâncias entre o ponto de interseção de índice 0 e os vértices originais
        distances = [np.linalg.norm(intersection_points[0] - v) for v in original_vertices]
    
        # Encontrar o vértice original mais próximo ao ponto de interseção de índice 0
        closest_vertex_index = np.argmin(distances)
        closest_vertex = original_vertices[closest_vertex_index]
    
        # O outro vértice original é aquele que não é o mais próximo
        other_vertex = original_vertices[1 - closest_vertex_index]
    
        # Formar os novos triângulos garantindo que o ponto de interseção de índice 0 esteja conectado ao vértice mais próximo
        back_triangle_1 = Triangle(intersection_points[0], intersection_points[1], closest_vertex, triangle.normal)
        back_triangle_2 = Triangle(intersection_points[1], closest_vertex, other_vertex, triangle.normal)

        back_triangle = [back_triangle_1, back_triangle_2]
    else:
        back_triangle = None

    return front_triangle, back_triangle

# Exemplo de uso
root = BSPNode()
# Aqui você adicionaria polígonos chamando root.add_polygon(polygon) para cada polígono
