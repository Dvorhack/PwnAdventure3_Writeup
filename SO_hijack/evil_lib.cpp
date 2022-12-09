#include <dlfcn.h>
#include <set>
#include <map>
#include <functional>
#include <string>
#include <vector>
#include <cstring>
#include "libGameLogic.h"


ClientWorld* world = 0;
Player* my_player = 0;
Vector3 hover_pos;
bool hover = false;

bool Player::CanJump(){
    return true;
}


void World::Tick(float f){
    // Get Global variable world
    world = *((ClientWorld**)(dlsym(RTLD_NEXT, "GameWorld")));

    // Get my player
    IPlayer* iplayer = world->m_activePlayer.m_object;
    Player* player = ((Player*)iplayer);


    // printf("[LO] Player name: %s", player->GetPlayerName());
    // printf("[LO] player->m_mana: %d", player->m_mana);

    player->m_jumpHoldTime = 999;
    player->m_jumpSpeed = 999;

    if(hover){
        my_player->SetPosition(hover_pos);
    }

}



void Player::SetJumpState(bool b){
    printf("[*] SetJumpState(%d)\n", b);
}

void Player::Chat(const char * m){
    my_player = this;

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
        printf("New pos: %f %f %f\n",(new_pos->x),(new_pos->y),(new_pos->z));
        hover_pos = *new_pos;
        this->SetPosition(*new_pos);

    }else if(strncmp(m+1,"tpx ",4) == 0){
        Vector3 new_pos = this->GetPosition();
        sscanf(m+1+4, "%f", &(new_pos.x));
        printf("New pos: %f %f %f\n",(new_pos.x),(new_pos.y),(new_pos.z));
        hover_pos = new_pos;
        this->SetPosition(new_pos);

    }else if(strncmp(m+1,"tpy ",4) == 0){
        Vector3 new_pos = this->GetPosition();
        sscanf(m+1+4, "%f", &(new_pos.y));
        printf("New pos: %f %f %f\n",(new_pos.x),(new_pos.y),(new_pos.z));
        hover_pos = new_pos;
        this->SetPosition(new_pos);

    }else if(strncmp(m+1,"tpz ",4) == 0){
        Vector3 new_pos = this->GetPosition();
        sscanf(m+1+4, "%f", &(new_pos.z));
        printf("New pos: %f %f %f\n",(new_pos.x),(new_pos.y),(new_pos.z));
        hover_pos = new_pos;
        this->SetPosition(new_pos);

    }else if(strncmp(m+1,"jump ",5) == 0){
        int new_speed = atoi(m+5+1);
        
        if (new_speed != 0 ){
            printf("Changing jum; from %f to %f\n", my_player->m_jumpSpeed,(float) new_speed);
            my_player->m_jumpSpeed = (float)new_speed;
        }else{
            printf("Actual speed %f\n", my_player->GetWalkingSpeed());
        }
    
    }else if(strncmp(m+1, "hover", 5) == 0){
        printf("%lx %lx\n",this, my_player);
        hover_pos = this->GetPosition();
        if(hover) hover = false;
        else hover = true;

    
    }else{
        printf("Unknown command\n");
    }
    }
}