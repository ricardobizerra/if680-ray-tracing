#include <iostream>
#include <cmath>

using namespace std;

struct Ponto {
    double x, y, z;
    // Construtor padrão
    Ponto() : x(0.0), y(0.0), z(0.0) {}
    // Construtor com parâmetros
    Ponto(double xCoord, double yCoord, double zCoord) : x(xCoord), y(yCoord), z(zCoord) {}
};

// Definição de operações sobre pontos

// Função para imprimir um ponto
void imprimePonto(Ponto p) {
    cout << "(" << p.x << ", " << p.y << ", " << p.z << ")" << endl;
}

// Função para somar dois pontos
Ponto somaPontos(Ponto p1, Ponto p2) {
    Ponto p;
    p.x = p1.x + p2.x;
    p.y = p1.y + p2.y;
    p.z = p1.z + p2.z;
    return p;
}

// Função para subtrair dois pontos
Ponto subtraiPontos(Ponto p1, Ponto p2) {
    Ponto p;
    p.x = p1.x - p2.x;
    p.y = p1.y - p2.y;
    p.z = p1.z - p2.z;
    return p;
}

// Função para calcular a distância entre dois pontos
double distanciaPontos(Ponto p1, Ponto p2) {
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;
    double dz = p1.z - p2.z;
    return sqrt(dx*dx + dy*dy + dz*dz);
}

// Função para calcular o produto escalar entre dois pontos
double produtoEscalar(Ponto p1, Ponto p2) {
    return p1.x*p2.x + p1.y*p2.y + p1.z*p2.z;
}

// Função principal
int main() {
    Ponto p1 = {1.0, 2.0, 3.0}; // Inicialização direta usando chaves
    Ponto p2(4.0, 5.0, 6.0);    // Inicialização por construção usando parênteses
    // adicionar p1 e p2
    Ponto p3 = somaPontos(p1, p2);
    return 0;
}