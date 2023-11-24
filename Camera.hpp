#include "Vectors.hpp"
#include "objects.cpp"

#include <iostream>
#include <stack>
#include <vector>
#include <opencv2/opencv.hpp>

using namespace std;

struct obj_pointer {
    Esfera * ptr_esfera;
    Plano * ptr_plano;
    string tipo;

    obj_pointer(Esfera * ponteiro_esfera = nullptr, Plano * ponteiro_plano = nullptr, string tipo_objeto) {
        ptr_esfera = ponteiro_esfera;
        ptr_plano = ponteiro_plano;
        tipo = tipo_objeto;
    }
};

struct camera{
    double x, y, z;
    Ponto posicao;
    Vector W; // Centro da tela
    Vector U; // Aponta para o lado a direita da camera
    Vector UP;
    int dcamera;
    int altura;
    int largura;
    camera(Ponto posicao, Ponto target) {
        Vector k = Vector(0,0,1);
        W = Vector(posicao.x - target.x, posicao.y - target.y, posicao.z - target.z);
        double norma_w = normaVetor(W);
        W.x = W.x/norma_w;
        W.y = W.y/norma_w;
        W.z = W.z/norma_w;
        //Implemente a op de normalizar um vetor
        U = produtoVetorial(k,W);
        double norma_u = normaVetor(U);
        U.x = U.x/norma_u;
        U.y = U.y/norma_u;
        U.z = U.z/norma_u;

        UP = produtoVetorial(W,U);
        double norma_UP = normaVetor(UP);
        UP.x = UP.x/norma_UP;
        UP.y = UP.y/norma_UP;
        UP.z = UP.z/norma_UP;
    }

    void raycasting(double distancia, int hres, int vres) {
        Vector centro_tela = multiplicaVetorPorEscalar(W, distancia);
        Vector topo_tela = multiplicaVetorPorEscalar(UP, vres/2);
        Vector esquerda_tela = multiplicaVetorPorEscalar(U, hres/2);
        Vector pixel_0_0 = somaVetores(somaVetores(centro_tela, topo_tela),esquerda_tela);
        vector<obj_pointer> objects;
        double scene[hres][vres];
        for (int i = 0; i < vres; i++) {
            for (int j = 0; j < hres; j++) {
                // Vetor que aponta para o pixel (soma do vetor pro pixel 0-0 para algum outro lugar)
                Vector pixel = somaVetores(pixel_0_0, multiplicaVetorPorEscalar(U, j));
                for (auto object:objects) {
                    if (object.tipo == "Esfera") {
                        Esfera esfera = *object.ptr_esfera;
                        Esfera::Intersecao_Return inter_esfera = esfera.intersecao_esfera_reta(pixel, posicao);
                        // Se houver intersecao armazena
                        if (inter_esfera.intersecao) {
                        // scene[i][j] = (255,245,130); // Cor para uma interse ção com uma esfera
                        scene[i][j] = color(255, 0, 0);
                        }
                    }
                    else if (object.tipo == "Plano") {
                        Plano plano = *object.ptr_plano;
                        bool inter_plano = plano.intersecao_plano_reta(pixel, posicao);
                        // Se houver intersecao armazena
                        if (inter_plano){
                            scene[i][j](x,y,z) = color(0,0,255);
                        // scene[i][j] = (150,25,49); // Cor para uma interseção com o plano
                        }
                    }
                }
                // Tratar as intersecoes e colorir o pixel na matriz scene
                // matriz[i][j] = cor
            }
            somaVetores(pixel_0_0, multiplicaVetorPorEscalar(UP, -i));
        }
    }
};


