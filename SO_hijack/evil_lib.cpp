#include "libGameLogic.h"
#include <dlfcn.h>
#include <string.h>

ClientWorld* world = 0;
Player* my_player = 0;

bool Player::CanJump(){
    return true;
}


void World::Tick(float){
    // Get Global variable world
    world = *((ClientWorld**)(dlsym(RTLD_NEXT, "GameWorld")));

    // Get my player
    IPlayer* iplayer = world->m_activePlayer.m_object;
    my_player = ((Player*)iplayer);


    // printf("[LO] Player name: %s", player->GetPlayerName());
    // printf("[LO] player->m_mana: %d", player->m_mana);

    my_player->m_jumpHoldTime = 999;
    my_player->m_jumpSpeed = 1999;

}



void Player::SetJumpState(bool b){
    printf("[*] SetJumpState(%d)\n", b);
}

void Player::Chat(const char * m){

    #define ACTION_CHAR ':'

    printf("Messsage: %s\n", m);
    if (m[0] == ACTION_CHAR){
        if(strncmp(m+1,"speed ",6) == 0){
        int new_speed = atoi(m+6+1);
        
        if (new_speed != 0 ){
            printf("Changing speed from %f to %f\n", my_player->m_walkingSpeed,(float) new_speed);
            my_player->m_walkingSpeed = (float)new_speed;
        }else{
            printf("Actual speed %f\n", my_player->GetWalkingSpeed());
        }
    }else if(strncmp(m+1,"tp ",3) == 0){
        Vector3* new_pos = new Vector3();
        sscanf(m+1+3, "%f %f %f", &(new_pos->x),&(new_pos->y),&(new_pos->z));
        printf("New pos: %f %f %f",(new_pos->x),(new_pos->y),(new_pos->z));
        this->SetPosition(*new_pos);
    
    }else{
        printf("Unknown command\n");
    }
    }
}