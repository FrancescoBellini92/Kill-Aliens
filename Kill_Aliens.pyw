import pygame, os, sys, random
from explosions import *
from shots import *
from ships import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.font.init()

UP_KEY = 273
DOWN_KEY = 274
RIGHT_KEY = 275
LEFT_KEY = 276
SPACE_KEY = 32


def main():

    """ INIT """
    clock = pygame.time.Clock()
    framerate = 30
    enemy_respawn_clock = 0
    bomb_firing_clock = 0
    scores = 0
    player_mov = [0, 0]


    """ PARAMETERS """
    n_enemies = 12
    respawn_frequency = 15
    respawn_prob = 7 # 60%
    bomb_firing_rate = [18, 21, 24, 27]
    bomb_prob = 7 #60%
    lifepoints = 7
    background_im = "assets/images/misc/space_background.jpg"


    """ MUSIC """
    pygame.mixer.init()
    soundtrack  =  "assets/audio/soundtrack.mp3"
    pygame.mixer.music.load(soundtrack)
    pygame.mixer.music.play(-1)


    """ DISPLAY """
    background = pygame.image.load(background_im)
    screen_dimension = background.get_rect()
    width = screen_dimension[2]
    height = screen_dimension[3]
    screen = pygame.display.set_mode([width,height])
    screen_rect = screen.get_rect()


    """ DECORATING DISPLAY BAR """
    icon = pygame.image.load("assets/images/alien/alien.png")
    icon = pygame.transform.scale(icon,(32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Kill Aliens!")
    pygame.mouse.set_visible(1)


    """ OBJECTS """
    enemy = Alien()
    player = Player(screen_rect)
    enemy_group = pygame.sprite.Group(enemy)
    bomb_group = pygame.sprite.Group(EnemyShot(enemy))
    player_group = pygame.sprite.Group(player)

    shot_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    explosion_enemy_group = pygame.sprite.Group()


    """ MAIN LOOP """
    while True:
        enemy_respawn_clock += 1
        bomb_firing_clock += 1


        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.mixer.music.fadeout(2000)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == RIGHT_KEY:
                    player_mov = player.speed
                elif event.key == LEFT_KEY:
                    player_mov = player.reverse_speed
                if event.key == SPACE_KEY:
                    shot = PlayerShot(player.rect.midtop)
                    shot_group.add(shot)
            elif event.type == pygame.KEYUP and event.key in [RIGHT_KEY, LEFT_KEY]:
                player_mov = player.stop


        # RESPAWN HANDLING
        if len(enemy_group) > n_enemies:
            enemy_respawn_clock = 0
        elif enemy_respawn_clock >= respawn_frequency:
            if random.randint(0, 10) in range(respawn_prob): # probability of respawning
                enemy_group.add(Alien())
            enemy_respawn_clock = 0
        if bomb_firing_clock >= random.choice(bomb_firing_rate): # by using a list of numbers, bomb firing rate is jittered
            for n in enemy_group:
                if random.randint(0, 10) in range(bomb_prob): # probability of shooting
                    bomb_group.add(EnemyShot(n))
            bomb_firing_clock = 0


        # COLLISION HANDLING
        collision_player_bomb = pygame.sprite.spritecollide(player, bomb_group, True)
        collision_player_enemy = pygame.sprite.spritecollide(player, enemy_group, True)
        collision_shot_enemy = pygame.sprite.groupcollide(shot_group, enemy_group, True, True)
        for bomb in collision_player_bomb:
            expl = Explosion(bomb)
            explosion_group.add(expl)
            lifepoints -= 1
        for crash in collision_player_enemy:
            expl = Explosion(crash)
            explosion_group.add(expl)
            lifepoints = 0
        for shot in collision_shot_enemy.keys():
            expl = EnemyExplosion(collision_shot_enemy[shot][0])
            explosion_enemy_group.add(expl)
            scores += 1


        # MOVEMENT HANDLING
        enemy_group.update(screen_rect)
        bomb_group.update(screen_rect)
        player_group.update(player_mov, screen_rect)
        shot_group.update(screen_rect)
        explosion_group.update()
        explosion_enemy_group.update()


        # MAIN ANIMATION
        clock.tick(framerate)
        screen.blit(background, screen_dimension)
        enemy_group.draw(screen)
        bomb_group.draw(screen)
        player_group.draw(screen)
        shot_group.draw(screen)
        explosion_group.draw(screen)
        explosion_enemy_group.draw(screen)

        scores_string = str(scores)
        score_text = "Enemies destroyed:" + scores_string
        score_font = pygame.font.Font(None, 30)
        score_display = score_font.render(score_text, True, (255, 0, 0))
        screen.blit(score_display, [width - 218, height - 25])

        life_string = str(lifepoints)
        life_text = "Lifepoints: " + life_string
        life_font = pygame.font.Font(None, 30)
        life_display = life_font.render(life_text, True, (255, 0, 0))
        screen.blit(life_display,[width - 139, height - 75])

        pygame.display.flip()


        # DIFFICULTY HANDLING
        if scores > 10:
            n_enemies = 18
            respawn_frequency = 12
            bomb_firing_rate = [15, 18, 21, 24]
        elif scores > 20:
            n_enemies = 24
            respawn_frequency = 10
            bomb_firing_rate = 10
            bomb_firing_rate = [12, 15, 18, 24]
        elif scores > 30:
            n_enemies = 36
            respawn_frequency = 8
            bomb_firing_rate = 8
            bomb_firing_rate = [9, 12, 15, 18]


        # DEATH HANDLING
        if lifepoints < 1:
            player.death_sequence(scores, death)


def death(scores):
    background_im = "assets/images/misc/death_screen.jpg"
    background = pygame.image.load(background_im)
    screen_dimension = background.get_rect()
    width = screen_dimension[2]
    height = screen_dimension[3]
    screen = pygame.display.set_mode([width,height])
    response = None

    scores = str(scores)
    sentence = "You destroyed " + scores + " enemy ships!"
    score_font = pygame.font.Font(None, 40)
    score_display = score_font.render(sentence, True, (255, 0, 0))

    while response is None:
        pygame.mixer.music.fadeout(2000)
        pygame.display.flip()
        screen.blit(background,screen_dimension)
        screen.blit(score_display,[width/2-195, height/2 + 50])
        pygame.display.flip()

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [82, 114]:
                    return game_function()
                elif event.key in [81, 113]:
                    pygame.display.quit()
                    sys.exit()


if __name__ == "__main__":
    main()

