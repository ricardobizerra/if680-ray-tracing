#include "Vectors.hpp"

struct camera{
    double x, y, z;
    Vector posicao;
    Vector V;
    Vector W; // Centro da tela
    Vector U; // Aponta para o lado a direita da camera
    int dcamera;
    int altura;
    int largura;
    camera(Vector& posicao, Vector& target,Vector& UP): posicao(posicao){
        W = posicao - target;
        W.x = W.x/normaVetor(W);
        W.y = W.y/normaVetor(W);
        W.z = W.z/normaVetor(W);
        //Implemente a op de normalizar um vetor
        U = produtoVetorial(UP,W);
        U.x = U.x/normaVetor(U);
        U.y = U.y/normaVetor(U);
        U.z = U.z/normaVetor(U);

        V= produtoVetorial(W,U);
    }





};


