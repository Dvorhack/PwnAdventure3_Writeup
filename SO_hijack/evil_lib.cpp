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

void parse_action(const char * m){
    if(strncmp(m+1,"speed ",6) == 0){
        float new_speed = 0;
        printf("%c\n",m[6+1]);
        switch (m[1+6]) {
        case 's' : {// slow
            new_speed = 100;
            break;
        }
        case 'm': { // medium
            new_speed = 1000;
            break;
        }
        case 'f': {
            new_speed = 9000;
            break;
        }
        default: {
            new_speed = 400;
            break;
        }
        }
        
        if (new_speed != 0 ){
            printf("Changing speed from %f to %f\n", my_player->m_walkingSpeed, new_speed);
            my_player->m_walkingSpeed = new_speed;
        }else{
            printf("Actual speed %f\n", my_player->GetWalkingSpeed());
        }
    }else{
        printf("Unknown command\n");
    }
}

void Player::SetJumpState(bool b){
    printf("[*] SetJumpState(%d)\n", b);
}

void Player::Chat(const char * message){

    #define ACTION_CHAR ':'

    printf("Messsage: %s\n", message);
    if (message[0] == ACTION_CHAR){
        parse_action(message);
    }
}