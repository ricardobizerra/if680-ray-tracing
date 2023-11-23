#include "Vectors.hpp"

struct Plano {
    Vector vetor_normal;
    Ponto ponto;

    // Forma Ax + By + Cz + D = 0
    double A;
    double B;
    double C;
    double D;

    Plano(Vector v, Ponto P) {
        vetor_normal = v;
        ponto = P;

        // vetor_normal.x (x - x0) + vetor_normal.y (y - y0) + vetor_normal.z (z - z0) = 0 tal que P = (x0,y0,z0)
        // Convertendo em Ax + By + Cz + D = 0
        A = vetor_normal.x;
        B = vetor_normal.y;
        C = vetor_normal.z;
        D = A * (-ponto.x) + B * (-ponto.y) + C * (-ponto.z);
    }

    bool intersecao_plano_reta(Vector vdiretor, Ponto P) {
        // Verificando se existe interseção
        double aux = produtoEscalar(vdiretor, vetor_normal);
        // Se o produto escalar for muito próximo de 0 os vetores são quase ortogonais (nao vale a pena calcular intersecao)
        if (aux >= 0.2) {
            return true;
        }
        return false;
    }

    Ponto calculo_ponto_intersecao(Vector vdiretor, Ponto P) {
        // A (P.x + vdiretor.x * t) + B (P.y + vdiretor.y * t) + C (P.z + vdiretor.z * t) + D = 0
        // termos que multiplicam t:
        double denominador = vdiretor.x * A + vdiretor.y * B + vdiretor.z * C; // denominador pois passa dividindo pro outro lados
        // Talvez seja possível transformar o calculo do denominador num produto vetorial pra otimizar cálculos
        double numerador = -(A * P.x + B * P.y + C * P.z + D); // fica negativo pois vai passar pro outro lado
        double t = numerador / denominador;

        // Cálculo do ponto
        double X = P.x + vdiretor.x * t;
        double Y = P.y + vdiretor.y * t;
        double Z = P.z + vdiretor.z * t;
        return Ponto(X,Y,Z);
    }
};

struct Esfera {
    Ponto centro;
    double raio;

    Esfera(Ponto P, double r) {
        centro = P;
        raio = r;
    }

    double intersecao_esfera_reta (Vector vdiretor, Ponto P) {
        // E: (x-xc)² + (y-yc)² + (z-zc)² = R²
        // x² - 2 x xc + xc² + y² - 2 y yc + yc² + z² - 2 z zc + zc² = R²
        // (P.x +vdiretor.x * t)² - 2 (P.y +vdiretor.y * t) * xc + xc² + (P.y +vdiretor.y * t)² - 2 (P.y +vdiretor.y * t) * yc + yc² + (P.z +vdiretor.z * t)² - 2 (P.y +vdiretor.y * t) * zc + zc² = R²
        
    }
};