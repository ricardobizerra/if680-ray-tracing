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

    struct Intersecao_Return {
        bool intersecao;
        double t;
        Ponto ponto_intersecao;
    };

    Intersecao_Return calculo_ponto_intersecao(Vector vdiretor, Ponto P) {
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
        return {
            true,
            t,
            Ponto(X, Y, Z)
        };
    }
};

struct Esfera {
    Ponto centro;
    double raio;

    Esfera(Ponto P, double r) {
        centro = P;
        raio = r;
    }
    
    struct Intersecaso_Return {
        bool intersecao;
        double t;
        Ponto ponto_intersecao;
    };

    Intersecao_Return intersecao_esfera_reta (Vector vdiretor, Ponto P) {
        // E: (x-xc)² + (y-yc)² + (z-zc)² = R²
        // (Q - C) . (Q - C) = R²
        // Q é um ponto qualquer (x,y,z), entao podemos substituir a equacao parametrica da reta
        // ((P + vdiretor * t) - C) . ((P + vdiretor * t) - C) = R²
        // (t * vdiretor + (P - C)) . (t * vdiretor + (P - C)) = R²
        // t² * vdiretor . vdiretor + 2t vdiretor . (P - C) + (P - C) . (P - C) = R²
        // t² * vdiretor . vdiretor + 2t vdiretor . (P - C) + (P - C) . (P - C) - R² = 0
        // logo, a = vdiretor . vdiretor, b = 2 * vdiretor . (P - C), c = (P - C) . (P - C) - R²
        // dito isso, podemos calcular delta
        Vector CP = Vector(P.x - centro.x, P.y - centro.y, P.z - centro.z);
        double a = produtoEscalar(vdiretor, vdiretor);
        double b = 2 * produtoEscalar(vdiretor,CP);
        double c = produtoEscalar(CP, CP) - raio * raio;
        double delta = b * b - 4 * a * c;
        if (delta >= 0) {
            double bhaskara_upper = -b + sqrt(delta);
            double bhaskara_lower = 2 * a;
            double t = bhaskara_upper / bhaskara_lower;

            return {
                true,
                t,
                Ponto(P.x + vdiretor.x * t, P.y + vdiretor.y * t, P.z + vdiretor.z * t)
            };
        }
        return {
            false,
            0,
            Ponto(0,0,0)
        };
    }
};