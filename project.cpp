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


struct Vector {
    double x, y, z;
    // Construtor padrão
    Vector() : x(0.0), y(0.0), z(0.0) {}
    // Construtor com parâmetros
    Vector(double xCoord, double yCoord, double zCoord) : x(xCoord), y(yCoord), z(zCoord) {}
};

// Definição de operações sobre vetores:

//Soma de vetores
Vector somaVetores(Vector v1, Vector v2) {
    Vector v;
    v.x = v1.x + v2.x;
    v.y = v1.y + v2.y;
    v.z = v1.z + v2.z;
    return v;
}

//Subtração de vetores
Vector subtraiVetores(Vector v1, Vector v2) {
    Vector v;
    v.x = v1.x - v2.x;
    v.y = v1.y - v2.y;
    v.z = v1.z - v2.z;
    return v;
}

//Produto escalar de vetores
double produtoEscalar(Vector v1, Vector v2) {
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z;
}

//Produto vetorial de vetores
Vector produtoVetorial(Vector v1, Vector v2) {
    Vector v;
    v.x = v1.y * v2.z - v1.z * v2.y;
    v.y = v1.z * v2.x - v1.x * v2.z;
    v.z = v1.x * v2.y - v1.y * v2.x;
    return v;
}

//Multiplicação de vetores por escalar
Vector multiplicaVetorPorEscalar(Vector v1, double escalar) {
    Vector v;
    v.x = v1.x * escalar;
    v.y = v1.y * escalar;
    v.z = v1.z * escalar;
    return v;
}

//Norma do vetor
double normaVetor(Vector v) {
    return sqrt(v.x*v.x + v.y*v.y + v.z*v.z);
}


//Impressão do vetor
void imprimeVetor(Vector v) {
    cout << "(" << v.x << ", " << v.y << ", " << v.z << ")" << endl;
}




// Função principal
int main() {

    return 0;
}