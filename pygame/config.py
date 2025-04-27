import pygame
import pygame.freetype
import floor
pygame.init()
counter = 1
special_counter = 1
screen = pygame.display.set_mode((1920, 1080))
background = pygame.image.load("Images\City1.png")
backrect = background.get_rect(center=(960, 540))
font = pygame.freetype.Font("Pixellettersfull-BnJ5.ttf", 50)
font.fgcolor = (255, 0, 0)
mainfloor = floor.floor(1920, 100, 960, 895)
boxfloor = floor.floor(480, 5, 980, 445)
tirefloor = floor.floor(280, 5, 1620, 505)
box2floor = floor.floor(200, 5, 625, 510)
box3floor = floor.floor(260, 5, 955, 310)
garbagefloor = floor.floor(150, 5, 1720, 280)

floorobjects = [mainfloor, boxfloor, tirefloor, box2floor, box3floor, garbagefloor]
floors = [mainfloor.surface, boxfloor.surface, tirefloor.surface, box2floor.surface, box3floor.surface, garbagefloor.surface]
floorrects = [mainfloor.rect, boxfloor.rect, tirefloor.rect, box2floor.rect, box3floor.rect, garbagefloor.rect]
def update(objects): #objects contains an array of players and an array of active consumables
    global counter
    global special_counter
    counter = counter + 1
    special_counter = special_counter + 1
    screen.blit(background, backrect)
    players = objects[0]    
    if len(objects) > 1:
        consumables = objects[1]
        for consumable in consumables: #handles the effects when players walk into consumables
            if not consumable.isConsumed:
                for player in players:
                    if player.check_collision(consumable):
                        if consumable.effect == "maxHP":
                            player.hp = player.max_hp
                            player.healing = True
                        elif consumable.effect == "damage":
                            player.attack_1_damage += 50
                            player.boosted = True
                        consumable.consumed()
                if not consumable.grounded():
                    consumable.down()  
                screen.blit(consumable.border, consumable.rect)
                screen.blit(consumable.image, consumable.rect)
    for player in players: #makes players get affected by gravity, updates players' frames, knockback, healing
        if not player.grounded() and not player.jumping:
            player.down()
        elif player.grounded():
            player.vert_up_prev = 0 
        if player.special_used:
            player.special_ready = False
        elif special_counter >= player.special_charge_time:
            player.special_ready = True
        screen.blit(player.image, player.rect)
        player.display()
        if player.rect.left < 100:
            player.got_hit("right", 0, 1)
        elif player.rect.right > 1820:
            player.got_hit("left", 0, 1)
        if player.healing and player.hp > 0:
            player.hp += 1
            if player.hp > player.max_hp:
                player.hp = player.max_hp
    pygame.display.flip()
