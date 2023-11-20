#include <iostream>

// Definição da estrutura para representar um ponto no espaço 3D
struct Point {
    double x, y, z;

    // Construtor para inicializar um ponto
    Point(double x_coord, double y_coord, double z_coord) : x(x_coord), y(y_coord), z(z_coord) {}

    // Método para adicionar outro ponto a este ponto
    void add(const Point& other) {
        x += other.x;
        y += other.y;
        z += other.z;
    }

    // Método para subtrair outro ponto deste ponto
    void subtract(const Point& other) {
        x -= other.x;
        y -= other.y;
        z -= other.z;
    }

    // Método para calcular o produto escalar com outro ponto
    double dotProduct(const Point& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    // Método para calcular o produto vetorial com outro ponto
    Point crossProduct(const Point& other) const {
        return Point(y * other.z - z * other.y, z * other.x - x * other.z, x * other.y - y * other.x);
    }
};

int main() {
    // Declaração de variáveis, execução do código
    return 0;
}
