import pygame
import pygame.freetype
import config

class player(pygame.sprite.Sprite):

    def __init__(self, image, center, image_folder, text_color, player_number, mode):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.orig_image = pygame.image.load(image)
        if player_number == 2:
            self.orig_image = pygame.transform.flip(self.orig_image, True, False)
        self.center = center
        self.rect = self.image.get_rect(center=self.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.image_folder = image_folder
        self.facing_forward = 1
        self.x_momentum = 0
        self.y_momentum = 1
        self.idle_sequence = []
        self.jumping = False
        self.jump_scale = 1
        self.text_color = text_color
        self.orig_text_color = text_color
        self.player_number = player_number
        self.hp = 0
        self.attack_1_damage = 0
        self.walk_frames = 0
        self.attack_1_frames = 0
        self.jump_frames = 0
        self.jump_height = 0
        self.vert_up_prev = 0
        self.die_frames = 0
        self.attack_1_frames_range = range(0, 0)
        self.die_frames = 0
        self.special_folder = ""
        self.special_frames = 4
        self.special_frames_range = range(3, 5)
        self.special_damage = 1000
        self.special_charge_time = 200
        self.special_ready = False
        self.special_used = False
        self.special_image = pygame.image.load("Images/icons/Skillicon1_01.png")
        self.special_image_frame = pygame.image.load("Images/icon_frames/Frame_01.png")
        self.boosted = False
        self.healing = False
        self.mode = mode
        

        if (self.image_folder == "/homeless_man"):
            self.hp = 500
            self.attack_1_damage = 100
            self.walk_frames = 8
            self.attack_1_frames = 9
            self.jump_frames = 16
            self.jump_height = 24
            self.die_frames = 4
            self.attack_1_frames_range = range(2, 5)
            for i in range (0,32):
                if i > 23:
                    self.idle_sequence.append("Images" + self.image_folder + "/Idle_2/Idle_2_" + str(((i - 23) % 9) + 1) + ".png")
                else:    
                    self.idle_sequence.append("Images" + self.image_folder + "/Idle_1/Idle_1_" + str((i % 6) + 1 ) + ".png")
            for i in range (8):
                self.idle_sequence.append("Images" + self.image_folder + "/Idle_2/Idle_2_" + str(8 - i) + ".png")

        elif (self.image_folder == "/homeless_woman"):
            self.hp = 400
            self.attack_1_damage = 150
            self.walk_frames = 8
            self.attack_1_frames = 10
            self.jump_frames = 12
            self.jump_height = 32
            self.die_frames = 4
            self.attack_1_frames_range = range(8, 11)
            for i in range (0,30):
                if i > 20:
                    self.idle_sequence.append("Images" + self.image_folder + "/Idle_2/Idle_2_" + str(((i - 20) % 9) + 1) + ".png")
                else:    
                    self.idle_sequence.append("Images" + self.image_folder + "/Idle_1/Idle_1_" + str((i % 7) + 1 ) + ".png")

        elif (self.image_folder == "/fighter"):
            self.hp = 450
            self.attack_1_damage = 150
            self.walk_frames = 8
            self.attack_1_frames = 4
            self.jump_frames = 10
            self.jump_height = 48
            self.die_frames = 3
            self.attack_1_frames_range = range(0, 5)
            for i in range(0, 6):
                self.idle_sequence.append("Images" + self.image_folder + "/Idle/Idle_" + str(i + 1) + ".png")
            self.special_folder = "/Attack_3/Attack_3_"
            self.special_frames = 4
            self.special_frames_range = range(3, 5)
            self.special_damage = 300
            self.special_charge_time = 100
            self.special_ready = False
            self.special_used = False
            self.special_image = pygame.image.load("Images/icons/Skillicon13_21.png")
            self.special_image_frame = pygame.image.load("Images/icon_frames/Frame_13.png")

        elif (self.image_folder == "/vampire_countess"):
            self.hp = 300
            self.attack_1_damage = 500
            self.walk_frames = 6
            self.attack_1_frames = 10
            self.jump_frames = 12
            self.jump_height = 32
            self.die_frames = 8
            self.attack_1_frames_range = range(6, 7)
            for i in range(0, 5):
                self.idle_sequence.append("Images" + self.image_folder + "/Idle/Idle_" + str(i + 1) + ".png")
            self.special_folder = "/Attack_3/Attack_3_"
            self.special_frames = 1
            self.special_frames_range = range(0, 2)
            self.special_damage = 100
            self.special_charge_time = 50
            self.special_ready = False
            self.special_used = False
            self.special_image = pygame.image.load("Images/icons/Skillicon11_36.png")
            self.special_image_frame = pygame.image.load("Images/icon_frames/Frame_11.png")

        elif (self.image_folder == "/werewolf_white"):
            self.hp = 600
            self.attack_1_damage = 200
            self.walk_frames = 11
            self.attack_1_frames = 6
            self.jump_frames = 11
            self.jump_height = 40
            self.die_frames = 2
            self.attack_1_frames_range = range(3, 6)
            for i in range(0, 8):
                self.idle_sequence.append("Images" + self.image_folder + "/Idle/Idle_" + str(i + 1) + ".png")
            self.special_folder = "/Run+Attack/Run+Attack_"
            self.special_frames = 7
            self.special_frames_range = range(5, 7)
            self.special_damage = 400
            self.special_charge_time = 100
            self.special_ready = False
            self.special_used = False
            self.special_image = pygame.image.load("Images/icons/Skillicon8_13.png")
            self.special_image_frame = pygame.image.load("Images/icon_frames/Frame_08.png")

        elif (self.image_folder == "/gangsters_1"):
            self.hp = 300
            self.attack_1_damage = 150
            self.walk_frames = 10
            self.attack_1_frames = 6
            self.jump_frames = 10
            self.jump_height = 48
            self.attack_1_frames_range = range(2, 4)
            self.die_frames = 5
            for i in range(3):
                for j in range(6):
                    self.idle_sequence.append("Images" + self.image_folder + "/Idle_1/Idle_" + str(j + 1) + ".png")
            for i in range(11):
                self.idle_sequence.append("Images" + self.image_folder + "/Idle_2/Idle_" + str(i + 1) + ".png")
            self.special_folder = "/Shot/Shot_"
            self.special_frames = 4
            self.special_frames_range = range(2, 5)
            self.special_damage = 1000
            self.special_charge_time = 200
            self.special_ready = False
            self.special_used = False
            self.special_image = pygame.image.load("Images/icons/Skillicon4_24.png")
            self.special_image_frame = pygame.image.load("Images/icon_frames/Frame_04.png")

        
        if mode == "bot":
            self.attack_1_damage *= 2
            self.special_damage *= 2
            self.hp *= 2

        self.max_hp = self.hp


            

    def check_collision(self, object):
        if pygame.sprite.collide_mask(self, object) == None:
            return False    
        else:
            return True
        
    def walk_forward(self):
        self.image = pygame.image.load("Images" + self.image_folder + "/Walk/Walk_" + str((config.counter % self.walk_frames + 1)) + ".png")
        self.rect = self.rect.move([12, 0])
        self.mask = pygame.mask.from_surface(self.image)
        config.screen.blit(self.image, self.rect)
        self.facing_forward = 1
        self.x_momentum = 2

    def walk_backward(self):
        self.image = pygame.transform.flip(pygame.image.load("Images" + self.image_folder + "/Walk/Walk_" + str((config.counter % self.walk_frames + 1)) + ".png"), True, False)
        self.rect = self.rect.move([-12, 0])
        self.mask = pygame.mask.from_surface(self.image)
        config.screen.blit(self.image, self.rect)
        self.facing_forward = -1
        self.x_momentum = -2

    def down(self):
        self.rect = self.rect.move([5 * self.x_momentum, 36])
        config.screen.blit(self.image, self.rect)

    def up(self):
        self.rect = self.rect.move([0, -6])
        config.screen.blit(self.image, self.rect)

    def got_hit(self, side, damage, knockback):
        self.hp -= damage           
        if (side == "left"):
            self.rect = self.rect.move([-100 * knockback, -100 * knockback])
        elif (side == "right"):
            self.rect = self.rect.move([100 * knockback, -100 * knockback])

    def display(self):
        if self.hp < 0:
            self.hp = 0
        if self.boosted:
            self.text_color = (255, 0, 255)
        elif self.hp <= 150:
            self.text_color = (255, 0, 0)
        elif self.hp > 150:
            self.text_color = self.orig_text_color
        text_surface, temp = config.font.render("HP: " + str(self.hp), self.text_color)
        temp = temp.move(300 + 1200 * (self.player_number - 1), 850)
        special_rect = self.special_image.get_rect(center=(500 + 1200 * (self.player_number - 1), 1000))
        if self.special_ready:
            config.screen.blit(self.special_image_frame, special_rect)
            config.screen.blit(self.special_image, special_rect)
        elif self.special_used:
            config.screen.blit(pygame.image.load("Images/icon_frames/Frame_10.png"), special_rect)
            config.screen.blit(pygame.image.load("Images/icons/Skillicon10_28.png"), special_rect)
        config.screen.blit(self.orig_image, temp)
        config.screen.blit(text_surface, temp)
        

    def attack1(self):
        self.image = pygame.image.load("Images" + self.image_folder + "/Attack_1/Attack_1_" + str((config.counter % self.attack_1_frames + 1)) + ".png")
        if self.facing_forward == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        config.screen.blit(self.image, self.rect)
        pygame.display.flip()

    def jump(self):
        self.momentum = self.facing_forward
        self.image = pygame.image.load("Images" + self.image_folder + "/Jump/Jump_" + str(config.counter + 1) + ".png")
        if self.facing_forward == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.vert_up_prev == 0:
            vert_up = self.jump_height
        else:
            vert_up -= self.vert_up_prev
            self.vert_up_prev -= vert_up
        self.rect = self.rect.move([self.facing_forward * 5, vert_up * self.jump_scale * -1])
        self.mask = pygame.mask.from_surface(self.image)
        config.screen.blit(self.image, self.rect)
        pygame.display.flip()

    def fall(self, i):
        pygame.time.delay(50)
        self.x_momentum = 0
        self.image = pygame.image.load("Images" + self.image_folder + "/Jump/Jump_" + str(i + 7) + ".png")
        if self.facing_forward == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.down()
            
    def idle(self):
        self.image = pygame.image.load(self.idle_sequence[config.counter % len(self.idle_sequence)])
        if self.facing_forward == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        config.screen.blit(self.image, self.rect)

    def grounded(self):
        grounded = False
        # false means not grounded and player moves down, true doesn't move
        for floor in config.floorobjects:
            if (self.rect.bottom < floor.rect.top):
                grounded = False 
            elif floor.rect.right > self.rect.left and self.rect.right > floor.rect.left and self.check_collision(floor):        
                if abs(floor.rect.top - self.rect.bottom) <= 50:
                    grounded = True
                    self.snap(floor)
                    return grounded
        return grounded
    
    def snap(self, floor):    
        self.rect = self.rect.move([0, floor.rect.top - self.rect.bottom + 5])
        config.screen.blit(self.image, self.rect)

    def die(self):
        self.image = pygame.image.load("Images" + self.image_folder + "/Dead/Dead_" + str((config.counter % self.die_frames + 1)) + ".png")
        if self.facing_forward == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        config.screen.blit(self.image, self.rect)
        pygame.time.delay(300)
    
    def special(self):
        self.image = pygame.image.load("Images" + self.image_folder + self.special_folder + str((config.counter % self.special_frames + 1)) + ".png")
        if self.facing_forward == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        config.screen.blit(self.image, self.rect)
        pygame.display.flip()
    
    def heal(self, heal_amount):
        self.hp += heal_amount
        if self.max_hp < self.hp:
            self.hp = self.max_hp
