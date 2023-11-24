#include "Camera.hpp"


int main(){
    // Camera: 0, 0, 0 [ponto]
    // Alvo: 2, -0.5, 0 [ponto]
    // up: 0, 1, 0 [vector]
    // Centro da esfera: 2, -1, 0 [ponto]
    // ponto do plano: 0, -1, 0 [ponto]
    // Normal ao plano : 0, 1, 0 [vector]

    double camera_x, camera_y, camera_z;
    double alvo_x, alvo_y, alvo_z;
    double up_x, up_y, up_z;
    double centro_esfera_x, centro_esfera_y, centro_esfera_z;
    double ponto_plano_x, ponto_plano_y, ponto_plano_z;
    double normal_plano_x, normal_plano_y, normal_plano_z;

    cout << "Digite os valores da camera, alvo, up, centro da esfera, ponto do plano e normal ao plano" << endl;

    cin >> camera_x >> camera_y >> camera_z;
    cin >> alvo_x >> alvo_y >> alvo_z;
    cin >> up_x >> up_y >> up_z;
    cin >> centro_esfera_x >> centro_esfera_y >> centro_esfera_z;
    cin >> ponto_plano_x >> ponto_plano_y >> ponto_plano_z;
    cin >> normal_plano_x >> normal_plano_y >> normal_plano_z;
    
    Ponto camera_ponto = Ponto(camera_x, camera_y, camera_z);
    Ponto alvo_ponto = Ponto(alvo_x, alvo_y, alvo_z);
    Vector up_vector = Vector(up_x, up_y, up_z);
    Ponto centro_esfera_ponto = Ponto(centro_esfera_x, centro_esfera_y, centro_esfera_z);
    Ponto ponto_plano_ponto = Ponto(ponto_plano_x, ponto_plano_y, ponto_plano_z);
    Vector normal_plano_vector = Vector(normal_plano_x, normal_plano_y, normal_plano_z);
    
    camera cam = camera(camera_ponto, alvo_ponto,up_vector);
    Esfera esfera = Esfera(centro_esfera_ponto, 1);
    Plano plano = Plano(normal_plano_vector, ponto_plano_ponto);
    vector<obj_pointer> objects;
    obj_pointer obj = obj_pointer(&esfera, nullptr, "Esfera");
    obj_pointer obj2 = obj_pointer(nullptr, &plano, "Plano");
    objects.push_back(obj);
    objects.push_back(obj2);

    cam.raycasting(1, 100, 100,objects);
    return 0;

}