import pygame
import pygame.freetype
import player
import config
import random
import consumable

pygame.init()
pygame.freetype.init()
mode = "player"
player_1_string = ""
player_2_string = ""
pvp_displays = ["Images/werewolf_white/Dead/Dead_2.png", "Images/vampire_countess/Attack_1/Attack_1_3.png", "Images/gangsters_1/Attack_1/Attack_1_1.png", "Images/fighter/Walk/Walk_1.png"]
folders = ["/werewolf_white", "/vampire_countess", "/gangsters_1", "/fighter"]
start_screen = pygame.display.set_mode((1980, 1080))
#loading screen images-----------------
vs_player_image = pygame.image.load("Images/homeless_man/Idle_2/Idle_2_6.png")
vs_bot_image = pygame.image.load("Images/homeless_woman/Attack_1/Attack_1_10.png")
vs_bot_image = pygame.transform.flip(vs_bot_image, True, False)
play_again_image = pygame.image.load("Images/icons/Skillicon6_10.png")
dont_play_again_image = pygame.image.load("Images/icons/Skillicon10_28.png")
play_again_frame = pygame.image.load("Images/icon_frames/Frame_06.png")
dont_play_again_frame = pygame.image.load("Images/icon_frames/Frame_11.png")
pvp_display_images = [pygame.image.load(display) for display in pvp_displays]
for i in range(len(pvp_displays)):
    pvp_display_images.append(pygame.image.load(pvp_displays[i]))
start_image = pygame.image.load("Images/icons/Skillicon4_08.png")
start_image = pygame.transform.scale_by(start_image, 4)
#--------------------------------------

#loading screen rects-----------------
vs_player_rect = vs_player_image.get_rect(center=(495, 540))
vs_bot_rect = vs_bot_image.get_rect(center = (1485,540))
play_again_rect = play_again_frame.get_rect(center = (950, 300))
dont_play_again_rect = dont_play_again_frame.get_rect(center = (950, 600))
pvp_display_rects = [pvp_display_images[j].get_rect(center=(495 + 990 * (i), 200 * (j + 1))) for i in range(2) for j in range(len(pvp_displays))]
start_rect = start_image.get_rect(center=(990, 600))
#-------------------------------------

#for loading in players and effects----------
alive_stuff = []
effects = ["maxHP", "damage"]
effects_images = ["Images/icons/Skillicon6_11.png", "Images/icons/Skillicon2_15.png"]
effects_borders = ["Images/icon_frames/Frame_06.png", "Images/icon_frames/Frame_02.png"]
#--------------------------------------------

running_play_again = True

while running_play_again:
    running_start = True
    running = True
    running_player_select = False
    running_decide_play_again = True
    config.counter = 1
    config.special_counter = 1

    #select player or bot mode-----------------------------
    while running_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_start = False
                running = False
        start_screen.blit(vs_player_image, vs_player_rect)
        start_screen.blit(vs_bot_image, vs_bot_rect)
        pygame.display.flip()
        if pygame.mouse.get_pressed()[0]:
            if vs_player_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "player"
                running_player_select = True
                running_start = False
            elif vs_bot_rect.collidepoint(pygame.mouse.get_pos()):
                mode = "bot"
                running_start = False
    #------------------------------------------------------
            
    #select characters in player mode----------------------
    while running_player_select:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_start = False
                running = False
                running_player_select = False
        start_screen.fill("black")
        start_screen.blit(start_image, start_rect)
        for i in range(len(pvp_display_rects)):
            img = pvp_display_images[i]
            rect = pvp_display_rects[i]
            if i % 2 == 1:
                img = pygame.transform.flip(img, True, False)
            start_screen.blit(img, rect)
        if pygame.mouse.get_pressed()[0]:
            for i in range(len(pvp_display_rects)):
                if pvp_display_rects[i].collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pos()[0] < 800:
                        player_1_string = pvp_displays[i % len(pvp_displays)]
                        player_1_folder = folders[i % len(folders)]
                    else:
                        player_2_string = pvp_displays[i % len(pvp_displays)]
                        player_2_folder = folders[i % len(folders)]
            if (player_1_string != "") and (player_2_string != "") and start_rect.collidepoint(pygame.mouse.get_pos()):
                running_player_select = False
    #-------------------------------------------------------

    #loading in consumables----------------------------------
    effect_num = random.randint(0, 1)
    munch = consumable.consumable(image=effects_images[effect_num], center=(random.randint(600, 1500), 200), effect=effects[effect_num], border=effects_borders[effect_num])
    time_to_munch = random.randint(30, 100)
    #--------------------------------------------------------
    #loading in characters----------------------------------
    if mode == "player":
        p1 = player.player(image=player_1_string, center=(675, 450), image_folder=player_1_folder, text_color=(100,200,0), player_number=1, mode="player")
        p2 = player.player(image=player_2_string, center=(1700, 220), image_folder=player_2_folder, text_color=(50,0,200), player_number=2, mode="player")
        p2.facing_forward = -1
        alive_stuff.append([p1, p2])

    else:
        p1 = player.player(image="Images/homeless_man/Walk/Walk_1.png", center=(675, 450), image_folder="/homeless_man", text_color=(100,200,0), player_number=1, mode="player")
        bot_select = random.randint(0, len(folders) - 1)
        enemy = player.player(image=pvp_displays[bot_select], center=(1700, 220), image_folder=folders[bot_select], text_color=(50,0,200), player_number=2, mode="bot")
        enemy.facing_forward = -1
        alive_stuff.append([p1, enemy])
    #--------------------------------------------------------

    #main game loop---------------------------------------
    while running:

        pygame.time.delay(50)
        if len(alive_stuff) == 1 and config.special_counter > time_to_munch:
            alive_stuff.append([munch])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        #player 1 controls--------------------------------
        #jumping-------
        if p1.jumping:
            if pygame.key.get_pressed()[pygame.K_s]:
                p1.jumping = False
                if p1.rect.bottom < 800:
                    for i in range(3):
                        p1.fall(i)
                        config.screen.blit(p1.image, p1.rect)

            p1.jump()
            if config.counter == p1.jump_frames - 1 or p1.rect.top < -20:
                p1.jumping = False

            if config.counter >= 1 and p1.grounded():
                p1.jumping = False
        #--------------
                        
        if p1.grounded():
            #walking------
            if pygame.key.get_pressed()[pygame.K_a]:
                p1.walk_backward()

            elif pygame.key.get_pressed()[pygame.K_d]:
                p1.walk_forward()
            #-------------

            #attacking--------
            elif pygame.key.get_pressed()[pygame.K_LSHIFT]:
                p1.attack1()
                if ((config.counter % p1.attack_1_frames + 1) in p1.attack_1_frames_range):
                    if mode == "player":
                        if p1.check_collision(p2):
                            if p1.rect.left < p2.rect.left:
                                p2.got_hit("right", p1.attack_1_damage, 1)
                                p1.got_hit("left", 0, 1)
                            else:
                                p2.got_hit("left", p1.attack_1_damage, 1)
                                p1.got_hit("right", 0, 1)
                    elif mode == "bot":
                        if p1.check_collision(enemy):
                            if p1.rect.left < enemy.rect.left:
                                enemy.got_hit("right", p1.attack_1_damage, 1)
                                p1.got_hit("left", 0, 1)
                            else:
                                enemy.got_hit("left", p1.attack_1_damage, 1)
                                p1.got_hit("right", 0, 1)

            elif pygame.key.get_pressed()[pygame.K_q]:
                if p1.special_folder != "" and p1.special_ready:
                    p1.special()
                    if ((config.counter % p1.special_frames + 1) in p1.special_frames_range):
                        p1.special_used = True
                    #gangsters_1 special----------------
                    if p1.image_folder == "/gangsters_1":
                        if mode == "player":
                            if abs(p1.rect.y - p2.rect.y) <= 50:
                                p2.got_hit("right", p1.special_damage, 1)
                        elif mode == "bot":
                            if abs(p1.rect.y - enemy.rect.y) <= 50:
                                enemy.got_hit("right", p1.special_damage, 1)
                    #werewolf_white special-------------
                    elif p1.image_folder == "/werewolf_white":
                        p1.rect = p1.rect.move([p1.facing_forward * 80, 0])
                        config.update(alive_stuff)
                        if mode == "player":
                            if p1.check_collision(p2):
                                p1.heal(200)
                                if p1.rect.left < p2.rect.left:
                                    p2.got_hit("right", p1.special_damage, 1)
                                else:
                                    p2.got_hit("left", p1.special_damage, 1)
                        elif mode == "bot":
                            if p1.check_collision(enemy):
                                p1.heal(200)
                                if p1.rect.left < enemy.rect.left:
                                    enemy.got_hit("right", p1.special_damage, 1)
                                else:
                                    enemy.got_hit("left", p1.special_damage, 1)
                    #fighter special--------------------
                    elif p1.image_folder == "/fighter":
                        if mode == "player":
                            if p1.check_collision(p2):
                                if p1.rect.left < p2.rect.left:
                                    p2.got_hit("right", p1.special_damage, 5)
                                else:
                                    p2.got_hit("left", p1.special_damage, 5)
                        elif mode == "bot":
                            if p1.check_collision(enemy):
                                if p1.rect.left < enemy.rect.left:
                                    enemy.got_hit("right", p1.special_damage, 5)
                                else:
                                    enemy.got_hit("left", p1.special_damage, 5)
                    #vampire_countess special-----------
                    elif p1.image_folder == "/vampire_countess":
                        if mode == "player":
                            if p1.check_collision(p2):
                                p2.special_used = True
                                if p1.rect.left < p2.rect.left:
                                    p2.got_hit("right", p1.special_damage, 1)
                                else:
                                    p2.got_hit("left", p1.special_damage, 1)
                        elif mode == "bot":
                            if p1.check_collision(enemy):
                                enemy.special_used = True
                                if p1.rect.left < enemy.rect.left:
                                    enemy.got_hit("right", p1.special_damage, 1)
                                else:
                                    enemy.got_hit("left", p1.special_damage, 1)
            #-----------------

            #big and small jumps----
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                config.counter = 0
                p1.jumping = True
                p1.jump_scale = 1.2

            elif pygame.key.get_pressed()[pygame.K_w]:
                config.counter = 0
                p1.jumping = True
                p1.jump_scale = 0.8
            #-----------------------

            #fall through ground-----
            elif pygame.key.get_pressed()[pygame.K_s]:
                if p1.rect.bottom < 800:
                    for i in range(3):
                        p1.fall(i)
                        config.screen.blit(p1.image, p1.rect)
            #-----------------------

            else:
                p1.idle()
        #--------------------------------------------

        #player 2 controls---------------------------
        if mode == "player":
            #jumping-------
            if p2.jumping: 
                if pygame.key.get_pressed()[pygame.K_DOWN]: 
                    p2.jumping = False 
                    if p2.rect.bottom < 800: 
                        for i in range(3): 
                            p2.fall(i) 
                            config.screen.blit(p2.image, p2.rect)
                p2.jump() 

                if config.counter == p2.jump_frames - 1 or p2.rect.top < 0: 
                    p2.jumping = False 

                if config.counter >= 1 and p2.grounded(): 
                    p2.jumping = False     
            #--------------                

            if p2.grounded(): 
                #walking------
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    p2.walk_backward()

                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    p2.walk_forward()
                #-------------

                #attacking--------
                elif pygame.key.get_pressed()[pygame.K_SLASH]: 
                    p2.attack1() 
                    if ((config.counter % p2.attack_1_frames + 1) in p2.attack_1_frames_range):
                        if p2.check_collision(p1): 
                            if p2.rect.left < p1.rect.left: 
                                p1.got_hit("right", p2.attack_1_damage, 1) 
                                p2.got_hit("left", 0, 1) 

                            else: 
                                p1.got_hit("left", p2.attack_1_damage, 1) 
                                p2.got_hit("right", 0, 1) 

                elif pygame.key.get_pressed()[pygame.K_RETURN]:
                    if p2.special_folder != "" and p2.special_ready:
                        p2.special()
                        if ((config.counter % p2.special_frames + 1) in p2.special_frames_range):
                            p2.special_used = True
                        #gangsters_1 special----------------
                        if p1.image_folder == "/gangsters_1":
                            if mode == "player":
                                if abs(p2.rect.y - p1.rect.y) <= 50:
                                    p1.got_hit("right", p2.special_damage, 1)
                            elif mode == "bot":
                                if abs(p2.rect.y - enemy.rect.y) <= 50:
                                    enemy.got_hit("right", p2.special_damage, 1)
                        #werewolf_white special-------------
                        elif p2.image_folder == "/werewolf_white":
                            p2.rect = p2.rect.move([p2.facing_forward * 80, 0])
                            config.update(alive_stuff)
                            if mode == "player":
                                if p2.check_collision(p1):
                                    p2.heal(200)
                                    if p2.rect.left < p1.rect.left:
                                        p1.got_hit("right", p2.special_damage, 1)
                                    else:
                                       p1.got_hit("left", p2.special_damage, 1)
                            elif mode == "bot":
                                if p2.check_collision(enemy):
                                    p2.heal(200)
                                    if p2.rect.left < enemy.rect.left:
                                        enemy.got_hit("right", p2.special_damage, 1)
                                    else:
                                        enemy.got_hit("left", p2.special_damage, 1)
                        #fighter special--------------------
                        elif p2.image_folder == "/fighter":
                            if mode == "player":
                                if p2.check_collision(p1):
                                    if p2.rect.left < p1.rect.left:
                                        p1.got_hit("right", p2.special_damage, 5)
                                    else:
                                        p1.got_hit("left", p2.special_damage, 5)
                            elif mode == "bot":
                                if p2.check_collision(enemy):
                                    if p2.rect.left < enemy.rect.left:
                                        enemy.got_hit("right", p2.special_damage, 5)
                                    else:
                                        enemy.got_hit("left", p2.special_damage, 5)
                        #vampire_countess special-----------
                        elif p2.image_folder == "/vampire_countess":
                            if mode == "player":
                                if p2.check_collision(p1):
                                    p1.special_used = True
                                    if p2.rect.left < p1.rect.left:
                                        p1.got_hit("right", p2.special_damage, 1)
                                    else:
                                        p1.got_hit("left", p2.special_damage, 1)
                            elif mode == "bot":
                                if p2.check_collision(enemy):
                                    enemy.special_used = True
                                    if p2.rect.left < enemy.rect.left:
                                        enemy.got_hit("right", p2.special_damage, 1)
                                    else:
                                        enemy.got_hit("left", p2.special_damage, 1)
                #-----------------

                #big and small jumps----
                elif pygame.key.get_pressed()[pygame.K_RSHIFT]: 
                    config.counter = 0 
                    p2.jumping = True 
                    p2.jump_scale = 1.2 

                elif pygame.key.get_pressed()[pygame.K_UP]: 
                    config.counter = 0 
                    p2.jumping = True 
                    p2.jump_scale = 0.8
                #----------------------- 

                #fall through ground-----
                elif pygame.key.get_pressed()[pygame.K_DOWN]: 
                    if p2.rect.bottom < 800: 
                        for i in range(3): 
                            p2.fall(i) 
                            config.screen.blit(p2.image, p2.rect) 
                #-----------------------

                else:
                    p2.idle() 
        #---------------------------------------

        #bot logic-------------------------------   
        if mode == "bot":
            if enemy.jumping:
                enemy.jump()
                if config.counter == enemy.jump_frames - 1 or enemy.rect.top < -20:
                    enemy.jumping = False

                if config.counter >= 1 and enemy.grounded():
                    enemy.jumping = False

            if enemy.grounded():
                if p1.rect.left - enemy.rect.right > 30:
                    enemy.walk_forward()
                elif enemy.rect.left - p1.rect.right > 30:
                    enemy.walk_backward()
                elif p1.rect.left - enemy.rect.right < 5 and abs(enemy.rect.top - p1.rect.top) <= 60:
                    if (random.randint(1, 3) == 2):
                        enemy.attack1()
                        if ((config.counter % enemy.attack_1_frames + 1) in enemy.attack_1_frames_range):
                            config.update(alive_stuff)
                            if enemy.check_collision(p1):
                                if enemy.rect.left < p1.rect.left:
                                    p1.got_hit("right", enemy.attack_1_damage, 1)
                                    enemy.got_hit("left", 0, 1)
                                else:
                                    p1.got_hit("left", enemy.attack_1_damage, 1)
                                    enemy.got_hit("right", 0, 1)
                elif enemy.rect.left - p1.rect.right < 5 and abs(enemy.rect.top - p1.rect.top) <= 60:
                    if (random.randint(1, 2) == 2):
                        enemy.attack1()
                        if ((config.counter % enemy.attack_1_frames + 1) in enemy.attack_1_frames_range):
                            config.update(alive_stuff)
                            if enemy.check_collision(p1):
                                if enemy.rect.left < p1.rect.left:
                                    p1.got_hit("right", enemy.attack_1_damage, 1)
                                    enemy.got_hit("left", 0, 1)
                                else:
                                    p1.got_hit("left", enemy.attack_1_damage, 1)
                                    enemy.got_hit("right", 0, 1)
                elif enemy.rect.top - p1.rect.bottom > 80:
                    config.counter = 0 
                    enemy.jumping = True 
                    enemy.jump_scale = 1.2

                elif enemy.rect.top - p1.rect.bottom > 25:
                    config.counter = 0
                    enemy_jumping = True
                    enemy.jump_scale = 0.65 
                
                else:
                    enemy.idle()
        #--------------------------------
                
        #end game---------------
        if mode == "player":
            config.update(alive_stuff)
            pygame.display.flip()
            #check if players dead-----
            if p2.hp <= 0:
                config.counter = 0
                for i in range(p2.die_frames):
                    p2.die()
                    config.update(alive_stuff)
                print("Player 1 wins!")
                running = False
            if p1.hp <= 0:
                config.counter = 0
                for i in range(p1.die_frames):
                    p1.die()
                    config.update(alive_stuff)
                print("Player 2 wins!")
                running = False
            #--------------------------
        elif mode == "bot":
            config.update(alive_stuff)
            pygame.display.flip()
            #check if players dead-----
            if enemy.hp <= 0:
                config.counter = 0
                for i in range(enemy.die_frames):
                    enemy.die()
                    config.update(alive_stuff)
                print("Player 1 wins!")
                running = False
            if p1.hp <= 0:
                config.counter = 0
                for i in range(p1.die_frames):
                    p1.die()
                    config.update(alive_stuff)
                print("Enemy wins!")
                running = False
            #--------------------------
        #-------------------------------------
    #--------------------------------------------
    
    #play again screen---------------------------
    while running_decide_play_again:
        alive_stuff = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_start = False
                running = False
                running_play_again = False
                running_decide_play_again = False
        start_screen.fill("black")
        start_screen.blit(play_again_frame, play_again_rect)
        start_screen.blit(dont_play_again_frame, dont_play_again_rect)
        start_screen.blit(play_again_image, play_again_rect)
        start_screen.blit(dont_play_again_image, dont_play_again_rect)
        pygame.display.flip()
        if pygame.mouse.get_pressed()[0]:
            if play_again_rect.collidepoint(pygame.mouse.get_pos()):
                running_play_again = True
                running_decide_play_again = False
                start_screen.fill("black")
            elif dont_play_again_rect.collidepoint(pygame.mouse.get_pos()):
                running_play_again = False
                running_decide_play_again = False
    #---------------------------------------------

pygame.quit()