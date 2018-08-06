""" ############### Another SPace Invader Clone ############# """


""" ############### IMPORT MODULES ############# """

import pygame,os,sys,random
pygame.font.init()


""" ############### CLASS DEFINITIONS ############## """

class explosion(pygame.sprite.Sprite):
    """ this class defines the explosion sprites occuring when being hit by
        a bomb or an enemy ship """
    def __init__(self,obj):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("explosion.png")
        self.rect=self.image.get_rect(center=obj.rect.center)
        self.life=3
        return
    def update(self): 
        self.life-=1
        if self.life<1:
            self.kill()
        return
        

class explosion_enemy(pygame.sprite.Sprite):
    
    def __init__(self,obj):
        pygame.sprite.Sprite.__init__(self)
        self.images=["alien1_explod1.png",
                     "alien1_explod1.png",
                     "alien1_explod2.png",
                     "alien1_explod2.png",
                     "alien1_gone.png"]
        self.frame_duration=len(self.images)-1 # 5 frames
        self.image=pygame.image.load(self.images[0])
        self.rect=self.image.get_rect(center=obj.rect.center)
        self.life=0
        return
    def update(self):
        self.image=pygame.image.load(self.images[self.life])
        self.life+=1
        if self.life==self.frame_duration:
            self.kill()
        return
        

class player_obj(pygame.sprite.Sprite):
    
    def __init__(self,starting_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("player.png")
        self.explosions=["expl1.png",
                         "expl2.png",
                         "expl3.png",
                         "expl4.png"]
        self.rect=self.image.get_rect(midbottom=starting_pos.midbottom)
        self.speed=[10,0]
        self.reverse_speed=[-10,0]
        self.stop=[0,0]
        self.life=0
        self.frame_duration=len(self.explosions)-1 # 4 frames
        return
    def update(self,speed,screen_rect):
        self.rect.x+=speed[0]
        if self.rect.right>screen_rect.right or self.rect.left<screen_rect.left:
            self.rect.x-=speed[0]
        return            

    def death_sequence(self,scores):
        self.image=pygame.image.load(self.explosions[self.life])
        self.life+=1
        if self.life==self.frame_duration: return death(scores)
        return            
        
class aliens(pygame.sprite.Sprite):
   
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("alien1.png")
        self.rect=self.image.get_rect()
        self.pos=random.choice([[0,0],[800,0]])
        if self.pos==[0,0]:
            self.speed=[10,30]
        else:
            self.speed=[-10,30]
            self.rect=self.image.get_rect(right=800)
        return           
        
    def update(self,screen_rect):
        self.rect.x+=self.speed[0]
        self.rect.y+=0
        if not screen_rect.contains(self.rect):
            self.speed[0]=-self.speed[0]
            self.rect.y+=self.speed[1]
        return
            
        

class alien_bomb(pygame.sprite.Sprite):
    
    def __init__(self,ship):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("alien_bomb.png")
        self.rect=self.image.get_rect(center=ship.rect.midbottom)
        self.speed=[0,6]
        return
    def update(self,screen_rect):
        self.rect.y+=self.speed[1]
        if not screen_rect.contains(self.rect):
            self.kill()
        return        

class player_shot(pygame.sprite.Sprite):
    
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
    path=sys.path[0]
    os.chdir(path)
       
    """ CALL GAME """
    return game_function() 
    
        
def game_function(): 

    """ INIT """
    clock=pygame.time.Clock()
    framerate=30
    counter1=0 # for respawning enemies
    counter2=0 # for respawning enemy bombs
    scores=0
    player_mov=[0,0] # dummy for moving the player

    """ PARAMETERS """
    n_enemies=12
    respawn_frequency=15
    respawn_prob=7 # 60%
    bomb_firing_rate=23
    bomb_prob=7 #60%
    lifepoints=7
    background_im="space_background.jpg"

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
        elif counter1>=respawn_frequency:
            if random.randint(0,10) in range(respawn_prob): #probability of respawning 
                new_enemy=aliens()
                enemy_group.add(new_enemy)
            counter1=0
        if counter2>=bomb_firing_rate:
            for n in enemy_group:
                if random.randint(0,10) in range(bomb_prob): #probability of shooting
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
            lifepoints-=1
        for crash in collision_player_enemy:
            expl=explosion(crash)
            explosion_group.add(expl)
            lifepoints=0
        for shot in collision_shot_enemy.keys():
            expl=explosion_enemy(collision_shot_enemy[shot][0])
            explosion_enemy_group.add(expl)
            scores+=1

        """ MOVE SECTION """
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

        scores_string=str(scores)
        score_text="Enemies destroyed:" + scores_string
        score_font=pygame.font.Font(None,30)
        score_display=score_font.render(score_text,True,(255,0,0))
        screen.blit(score_display,[width-218,height-25])

        life_string=str(lifepoints)
        life_text="Lifepoints: "+life_string
        life_font=pygame.font.Font(None,30)
        life_display=life_font.render(life_text,True,(255,0,0))
        screen.blit(life_display,[width-139,height-75])
        
        pygame.display.flip()
    
        """ DIFFICULTY  SECTION """
        if scores>10:
            n_enemies=18
            respawn_frequency=12
            bomb_firing_rate=16
        elif scores>20:
            n_enemies=24
            respawn_frequency=10
            bomb_firing_rate=10
        elif scores>30:
            n_enemies=36
            respawn_frequency=8
            bomb_firing_rate=8

        """ DEATH SECTION """
        if lifepoints<1:
            player.death_sequence(scores)

    return            


def death(scores):
    background_im="death_screen.jpg"
    background=pygame.image.load(background_im)
    screen_dimension=background.get_rect()
    width=screen_dimension[2]
    height=screen_dimension[3]
    screen=pygame.display.set_mode([width,height])
    response=None
    scores=str(scores)
    sentence="You destroyed " + scores + " enemy ships!"
    score_font=pygame.font.Font(None,40)
    score_display=score_font.render(sentence,True,(255,0,0))
    while response==None:
        pygame.display.flip()
        screen.blit(background,screen_dimension)
        screen.blit(score_display,[width/2-175,height/2 + 50])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key in [82,114]:
                    response=1
                elif event.key in [81,113]:
                    response=2
    if response==1:
        return game_function()
    if response==2:
        pygame.display.quit()
        sys.exit()
    return    

""" ############### EXECUTION ############## """

if __name__=="__main__": main_function()

