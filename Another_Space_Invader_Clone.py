""" ############### KILL ALIENS!############# """

# TODO:
# 1) SCORES
# 2) DEATH AND HEALTH
# 3) TRANSPARENCIES
# 4) edges bumping


""" ############### IMPORT MODULES ############# """

import pygame,os,sys,random


""" ############### CLASS DEFINITIONS ############## """

class explosion(pygame.sprite.Sprite):
    """ this class defines the explosion sprites occuring when being hit by
        a bomb or an enemy ship """
    def __init__(self,obj):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("explosion.gif")
        self.rect=self.image.get_rect(center=obj.rect.center)
        self.life=3
    def update(self): 
        self.life-=1
        if self.life<1:
            self.kill()
        return

class explosion_enemy(pygame.sprite.Sprite):
    """ this class defines the explosion sprites for enemies """
    def __init__(self,obj):
        pygame.sprite.Sprite.__init__(self)
        self.images=["alien1_explod1.png",
                     "alien1_explod1.png",
                     "alien1_explod2.png",
                     "alien1_explod2.png",
                     "alien1_explod3.png",
                     "alien1_explod3.png",
                     "alien1_gone.png",
                     "alien1_gone.png"]
        self.image=pygame.image.load(self.images[0])
        self.rect=self.image.get_rect(center=obj.rect.center)
        self.life=7
        self.i=0
    def update(self):
        self.i+=1
        self.image=pygame.image.load(self.images[self.i])
        self.life-=1
        if self.life<1:
            self.kill()
        return

class player_obj(pygame.sprite.Sprite):
    """ this class defines the player controlled sprite """
    def __init__(self,starting_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("player.png")
        self.rect=self.image.get_rect(midbottom=starting_pos.midbottom)
        self.speed=[6,0]
        self.reverse_speed=[-6,0]
        self.stop=[0,0]
    def update(self,speed,screen_rect):
        self.rect.x+=speed[0]
    

class aliens(pygame.sprite.Sprite):
    """ this class defines the enemy ship sprites """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("alien1.png")
        self.rect=self.image.get_rect()
        self.speed=[6,30]
        
    def update(self,screen_rect):
        self.rect.x+=self.speed[0]
        self.rect.y+=0
        if not screen_rect.contains(self.rect):
            self.speed[0]=-self.speed[0]
            self.rect.y+=self.speed[1]
        return

class alien_bomb(pygame.sprite.Sprite):
    """ this class defines the enemy bomb sprites """
    def __init__(self,ship):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("alien_bomb.png")
        self.rect=self.image.get_rect(center=ship.rect.midbottom)
        self.speed=[0,4] 
    def update(self,screen_rect):
        self.rect.y+=self.speed[1]
        if not screen_rect.contains(self.rect):
            self.kill()
        return

class player_shot(pygame.sprite.Sprite):
    """ this class defines the player shot sprites """
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("shot.png")
        self.rect=self.image.get_rect(midbottom=pos)
        self.speed=[0,-8]
    def update(self,screen_rect):
        self.rect.y+=self.speed[1]
        if not screen_rect.contains(self.rect):
            self.kill
        return

""" ############### FUNCTION DEFINITIONS ############## """


def main_function():

    """ DEFINE PATH  """
    path_E200HA="D:\\Google Drive\\2) Programming\\Python\\Games\\Kill Aliens!"
    path_X555LJ="C:\\Users\\Francesco Bellini\\Google Drive\\2) Programming\\Python\\Games\\Kill Aliens!"
    if os.path.exists(path_E200HA): os.chdir(path_E200HA)
    else: os.chdir(path_X555LJ)
       
    """ CALL GAME """
    return game_function(6,30,30,3,"space_background.jpg") 
    
        
def game_function(n_enemies,respawn_frequency,bomb_firing_rate,lifepoints,background_im): 

    """ INIT """
    clock=pygame.time.Clock()
    framerate=30
    counter1=0 # for respawning enemies
    counter2=0 # for enemy bombs
    hits=0 # hit counter
    dead_counter=0 # frames after death
    dead=None
    player_mov=[0,0] # dummy for moving the player

    """ DISPLAY """
    background=pygame.image.load(background_im)
    screen_dimension=background.get_rect()
    width=screen_dimension[2]
    height=screen_dimension[3]
    screen=pygame.display.set_mode([width,height])
    screen_rect=screen.get_rect()

    """ DECORATING DISPLAY BAR """
    icon=pygame.image.load("alien1.png")
    icon=pygame.transform.scale(icon,(32,32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Kill Aliens!")
    pygame.mouse.set_visible(1)# better to see the cursor

    """ OBJECTS """
    enemy=aliens()
    enemy_group=pygame.sprite.Group(enemy)

    bomb=alien_bomb(enemy)
    bomb_group=pygame.sprite.Group(bomb)

    player=player_obj(screen_rect)
    player_group=pygame.sprite.Group(player)

    shot_group=pygame.sprite.Group()
    explosion_group=pygame.sprite.Group()
    explosion_enemy_group=pygame.sprite.Group()

    """ MAIN LOOP """
    while True:
        counter1+=1
        counter2+=1

        """ EVENT SECTION """
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN: # up 273, down 274, right 275, left 276, spacebar 32
                if event.key==275:
                    player_mov=player.speed
                elif event.key==276:
                    player_mov=player.reverse_speed
                if event.key==32:
                    shot=player_shot(player.rect.midtop)
                    shot_group.add(shot)
            elif event.type==pygame.KEYUP and event.key in [275,276]:
                player_mov=player.stop

        """ RESPAWN SECTION """
        if len(enemy_group)>n_enemies:
            counter1=0
        elif counter1==respawn_frequency:
            if random.randint(0,10) in range(6): #probability of respawning = 50% 
                new_enemy=aliens()
                enemy_group.add(new_enemy)
            counter1=0
        if counter2==bomb_firing_rate:
            for n in enemy_group:
                if random.randint(0,10) in range(6): #probability of shooting = 50% 
                    new_bomb=alien_bomb(n)
                    bomb_group.add(new_bomb)
            counter2=0
                
        """ COLLISION SECTION """
        collision_player_bomb=pygame.sprite.spritecollide(player,bomb_group,True)
        collision_player_enemy=pygame.sprite.spritecollide(player,enemy_group,True)
        collision_shot_enemy=pygame.sprite.groupcollide(shot_group,enemy_group,True,True)
        for bomb in collision_player_bomb:
            expl=explosion(bomb)
            explosion_group.add(expl)
            hits+=1
        for crash in collision_player_enemy:
            expl=explosion(crash)
            explosion_group.add(expl)
            hits=lifepoints
        for shot in collision_shot_enemy.keys():
            expl=explosion_enemy(collision_shot_enemy[shot][0])
            explosion_enemy_group.add(expl) 

        """ MOVE SECTION """
        if player.rect.right==screen_rect.right:
            player_mov=player.stop
        elif player.rect.left==screen_rect.left:
            player_mov=player.stop
        enemy_group.update(screen_rect)
        bomb_group.update(screen_rect)
        player_group.update(player_mov,screen_rect)
        shot_group.update(screen_rect)
        explosion_group.update()
        explosion_enemy_group.update()
        

        """ MAIN ANIMATION SECTION """
        clock.tick(framerate)
        screen.blit(background,screen_dimension)
        enemy_group.draw(screen)
        bomb_group.draw(screen)
        player_group.draw(screen)
        shot_group.draw(screen)
        explosion_group.draw(screen)
        explosion_enemy_group.draw(screen)
        pygame.display.flip()

        """ DEATH SECTION """
        if dead and dead_counter>15:
            return death()
        if hits > lifepoints:
            player.image=pygame.image.load("explosion_big.png")
            dead_counter+=1
            dead=True
        
    return

def death():
    background_im="death_screen.jpg"
    background=pygame.image.load(background_im)
    screen_dimension=background.get_rect()
    width=screen_dimension[2]
    height=screen_dimension[3]
    screen=pygame.display.set_mode([width,height])
    response=None
    while response==None:
        pygame.display.flip()
        screen.blit(background,screen_dimension)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key in [82,114]:
                    response=1
                elif event.key in [81,113]:
                    response=2
    if response==1:
        return game_function(6,30,30,3,"space_background.jpg")
    if response==2:
        pygame.display.quit()
        sys.exit()

""" ############### EXECUTION ############## """

if __name__=="__main__": main_function()

