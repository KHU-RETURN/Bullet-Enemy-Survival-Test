import pygame
import sys
import os
import random
import math
import button

pygame.init()

start_game = False
screen_width = 800
screen_height = 640
size = [screen_width, screen_height]  # 창 크기
screen = pygame.display.set_mode(size)

#파이게임 전체화면

title = "swing_knife" #게임 이름
pygame.display.set_caption(title)

# 게임 내 설정
clock = pygame.time.Clock() #전역변수 하나밖에 사용 안함. 따라서 지울것
background_color = (0, 0, 40)

# 폰트 설정
myFont = pygame.font.Font('data1/a옛날목욕탕B.ttf', 30)
game_over_font = pygame.font.Font('data1/a옛날목욕탕B.ttf', 90)

# 이미지 설정
start_img = pygame.image.load('data1/start_btn.png').convert_alpha()
exit_img = pygame.image.load('data1/exit_btn.png').convert_alpha()
background_img = pygame.image.load('data1/img/bg/background.png').convert() #convert, convert_alpha 차이
sword_img = pygame.image.load('data1/img/player/swing/sword.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (int(sword_img.get_width()*1.2), int(sword_img.get_height()*0.3)))
enemy_bullet = pygame.image.load('data1/img/enemy/attack.png').convert_alpha()
enemy_bullet = pygame.transform.scale(enemy_bullet, (int(enemy_bullet.get_width()*0.8), int(enemy_bullet.get_height()*0.6)))
heart = pygame.image.load('data1/img/heart.png').convert_alpha()
empty_heart = pygame.image.load('data1/img/empty_heart.png').convert_alpha()

# 사운드 설정 _s 는 사운드
bgm_s = pygame.mixer.Sound('data1/sound/bgm.mp3')
death_s = pygame.mixer.Sound('data1/sound/death_sound.mp3')
sword_s = pygame.mixer.Sound('data1/sound/sword.mp3')
hit_enemy_s = pygame.mixer.Sound('data1/sound/destroy_enemy.wav')
player_hit_s = pygame.mixer.Sound('data1/sound/player_hit.mp3')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True # 살아있는지

        self.speed = speed
        self.direction = 1 # 좌우 방향
        self.flip = False # 이미지 좌우 반전

        self.animation_list = [] # 애니메이션 리스트
        self.frame_index = 0 # 애니메이션 프레임 인덱스
        self.update_time = pygame.time.get_ticks() # 애니메이션 시간

        self.action = 0 # idle, run, death 상태
        self.weapon_img = sword_img

        self.score = 0
        self.lives = 3 # 목숨

        self.drawing = True
        
        # 애니메이션 리스트 추가
        animation_types = ['idle', 'run', 'death']
        for animation in animation_types:
            temp_list = []
            # 애니메이션 프레임 수 
            num_of_frames = len(os.listdir(f'data1/img/player/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'data1/img/player/{animation}/{animation}{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale*1.7), int(img.get_height() * scale*1.7)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x+30, y+40)

    # 플레이어 이동
    def move(self, moving_left, moving_right, moving_up, moving_down): # 변수 너무 많음

        dx = 0
        dy = 0

        if moving_left and self.rect.x > 10: # weith, height로 계산
            dx = -self.speed
        if moving_right and self.rect.x < 735:
            dx = self.speed
        if moving_up and self.rect.y > 50:
            dy = -self.speed
        if moving_down and self.rect.y < 555:
            dy = self.speed
        
        # 위치 업데이트
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self): # 플레이어 애니메이션 업데이트
        ANIM_COOLDOWN = 150 # 애니메이션 쿨타임

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIM_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action != 2: # death가 아니라면 반복
                self.frame_index = 0
            elif self.action == 2: # death라면 게임 오버
                self.drawing = False
                self.kill()

    def update_action(self, new_action): # 플레이어 액션 상태 업데이트 함수
        if new_action != self.action: # 이전 액션과 같은지 확인
            self.action = new_action

            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def handle_weapon(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x = mouse_x - self.rect.centerx
        rel_y = mouse_y - self.rect.centery

        angle = (180/math.pi) * -math.atan2(rel_y, rel_x)

        img = pygame.transform.scale(self.weapon_img, (int(self.weapon_img.get_width() * 5), int(self.weapon_img.get_height() * 5)))
        player_weapon_copy = pygame.transform.rotate(img, angle)

        display.blit(player_weapon_copy, (self.rect.x+25 - int(player_weapon_copy.get_width() / 2), self.rect.y+30 - int(player_weapon_copy.get_height() / 2))) # 왜 다시 scale 조정?

    def draw(self, display): # 플레이어 화면에 생성
        display.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #transform? 왜사용?

        if player.alive:
            self.handle_weapon(display)


class Spin(pygame.sprite.Sprite): #애니메이션 고치는중, 뒤에 update_animation, update_action 추가 Spin 맨 뒤에 update animation 없음 추가하면 끝
    def __init__(self, x, y, scale, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.drawing = True
        self.flip = False

        animation_types = ['spin']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'data1/img/spin/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'data1/img/spin/{animation}/{animation}{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

        for enemy in enemy_group:
            if enemy.rect.colliderect(self.rect):
                if self.type == "spin":
                    hit_enemy_s.set_volume(0.05)
                    hit_enemy_s.play()
                    enemy.kill()
                    self.kill()
                    player.score += enemy.score
                    print("score:", player.score)

    def update_animation(self):
        ANIM_COOLDOWN = 100

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIM_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action

            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, display): # 플레이어 화면에 생성
        display.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #transform? 왜사용?

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y, type):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.enemy_bullet_speed = 2
        self.type = type

        if self.type == "enemy_bullet":
            self.image = enemy_bullet
        self.rect = self.image.get_rect()

        self.rect.center = (x, y)

        if self.type == "enemy_bullet":
            self.x_vel = dir_x * self.enemy_bullet_speed
            self.y_vel = dir_y * self.enemy_bullet_speed

        self.count = 0 # 총알이 벽에 부딪힌 횟수

    def update(self):
        self.rect.x -= self.x_vel
        self.rect.y -= self.y_vel

        # 벽에 튕기기
        if self.rect.top <= 60 or self.rect.bottom >= screen_height:
            self.y_vel *= -1
            self.count += 1
        if self.rect.right <= 50 or self.rect.left >= 750:
            self.y_vel *= -1
            self.count += 1

        if self.count > 10:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, type):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.type = type

        if type == "shots3":
            self.score = 30
        elif type == "shots4":
            self.score = 40
        elif type == "shots5":
            self.score = 50
        elif type == "shots6":
            self.score = 60
        elif type == "shots8":
            self.score = 80

        self.attack_rate = 100
        self.attack_cooltime = 0
        self.b_attack = False

        self.direction = 1 # 좌우 방향
        self.flip = False # 좌우 반전

        self.animation_list = [] # 애니메이션 리스트
        self.frame_index = 0 # 애니메이션 프레임
        self.update_time = pygame.time.get_ticks() # 애니메이션 시간

        self.action = 0

        #애니메이션 리스트
        animation_type = ['idle', 'move_down', 'move_up']
        for animation in animation_type:
            temp_list = []
            # 애니메이션 프레임 수
            num_of_frames = len(os.listdir(f'data1/img/enemy/{self.type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'data1/img/enemy/{self.type}/{animation}/{animation}{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.attack_cooltime += 1

        # 플레이어 추적해서 이동
        dif_x = player.rect.centerx-self.rect.centerx
        dif_y = player.rect.centery-self.rect.centery

        if dif_x != 0 or dif_y != 0:
            entity_movement = [dif_x/(abs(dif_x)+abs(dif_y))*self.speed, dif_y/(abs(dif_x)+abs(dif_y))*self.speed]
        else:
            entity_movement = [0, 0]

        if entity_movement[0] > 0 and entity_movement[0] < 1:
            entity_movement[0] = 1
        if entity_movement[1] > 0 and entity_movement[1] < 1:
            entity_movement[1] = 1

        self.rect.x += entity_movement[0]
        self.rect.y += entity_movement[1]

        # 좌우 반전
        if self.rect.x < player.rect.centerx:
            self.flip = True
            self.direction = -1
        else:
            self.flip = False
            self.direction = 1

        if entity_movement[1] > 0:
            self.update_action(1)
        else:
            self.update_action(2)

        # 공격
        if self.attack_cooltime >= self.attack_rate:
            self.speed = 0
            self.b_attack = True

            if self.attack_cooltime >= self.attack_rate + 40 and self.b_attack:
                self.attack_cooltime = 0
                self.attack()
                self.speed = 1.5
                self.b_attack = False

    def update_action(self, new_action): # 적 액션 상태 업데이트
        if new_action != self.action: # 이전 액션과 같은지 확인
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self): # 적 애니메이션 업데이트
        ANIM_COOLDOWN = 250 # 애니메이션 쿨타임

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIM_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def attack(self): # 적 공격
        if self.type == "shots3":
            enemy_bullet = Bullet(
                self.rect.centerx, self.rect.centery, 0, -1, "enemy_bullet")
            enemy_bullet1 = Bullet(
                self.rect.centerx, self.rect.centery, -1, 1, "enemy_bullet")
            enemy_bullet2 = Bullet(
                self.rect.centerx, self.rect.centery, 1, 1, "enemy_bullet")
            bullet_group.add(enemy_bullet)
            bullet_group.add(enemy_bullet1)
            bullet_group.add(enemy_bullet2)
        elif self.type == "shots4":
            enemy_bullet = Bullet(
                self.rect.centerx, self.rect.centery, 1, 0, "enemy_bullet")
            enemy_bullet1 = Bullet(
                self.rect.centerx, self.rect.centery, 0, 1, "enemy_bullet")
            enemy_bullet2 = Bullet(
                self.rect.centerx, self.rect.centery, -1, 0, "enemy_bullet")
            enemy_bullet3 = Bullet(
                self.rect.centerx, self.rect.centery, 0, -1, "enemy_bullet")
            bullet_group.add(enemy_bullet)
            bullet_group.add(enemy_bullet1)
            bullet_group.add(enemy_bullet2)
            bullet_group.add(enemy_bullet3)
        elif self.type == "shots5":
            enemy_bullet = Bullet(
                self.rect.centerx, self.rect.centery, 1, 1, "enemy_bullet")
            enemy_bullet1 = Bullet(
                self.rect.centerx, self.rect.centery, -1, 1, "enemy_bullet")
            enemy_bullet2 = Bullet(
                self.rect.centerx, self.rect.centery, 1, -1, "enemy_bullet")
            enemy_bullet3 = Bullet(
                self.rect.centerx, self.rect.centery, -1, -1, "enemy_bullet")
            enemy_bullet4 = Bullet(
                self.rect.centerx, self.rect.centery, 0, -1, "enemy_bullet")
            bullet_group.add(enemy_bullet)
            bullet_group.add(enemy_bullet1)
            bullet_group.add(enemy_bullet2)
            bullet_group.add(enemy_bullet3)
            bullet_group.add(enemy_bullet4)
        elif self.type == "shots6":
            enemy_bullet = Bullet(
                self.rect.centerx, self.rect.centery, 1, 1, "enemy_bullet")
            enemy_bullet1 = Bullet(
                self.rect.centerx, self.rect.centery, -1, 1, "enemy_bullet")
            enemy_bullet2 = Bullet(
                self.rect.centerx, self.rect.centery, 1, -1, "enemy_bullet")
            enemy_bullet3 = Bullet(
                self.rect.centerx, self.rect.centery, -1, -1, "enemy_bullet")
            enemy_bullet4 = Bullet(
                self.rect.centerx, self.rect.centery, 1, 0, "enemy_bullet")
            enemy_bullet5 = Bullet(
                self.rect.centerx, self.rect.centery, -1, 0, "enemy_bullet")
            bullet_group.add(enemy_bullet)
            bullet_group.add(enemy_bullet1)
            bullet_group.add(enemy_bullet2)
            bullet_group.add(enemy_bullet3)
            bullet_group.add(enemy_bullet4)
            bullet_group.add(enemy_bullet5)
        elif self.type == "shots8":
            enemy_bullet = Bullet(
                self.rect.centerx, self.rect.centery, 1, 1, "enemy_bullet")
            enemy_bullet1 = Bullet(
                self.rect.centerx, self.rect.centery, -1, 1, "enemy_bullet")
            enemy_bullet2 = Bullet(
                self.rect.centerx, self.rect.centery, 1, -1, "enemy_bullet")
            enemy_bullet3 = Bullet(
                self.rect.centerx, self.rect.centery, -1, -1, "enemy_bullet")
            enemy_bullet4 = Bullet(
                self.rect.centerx, self.rect.centery, 1, 0, "enemy_bullet")
            enemy_bullet5 = Bullet(
                self.rect.centerx, self.rect.centery, -1, 0, "enemy_bullet")
            enemy_bullet6 = Bullet(
                self.rect.centerx, self.rect.centery, 0, 1, "enemy_bullet")
            enemy_bullet7 = Bullet(
                self.rect.centerx, self.rect.centery, 0, -1, "enemy_bullet")
            bullet_group.add(enemy_bullet)
            bullet_group.add(enemy_bullet1)
            bullet_group.add(enemy_bullet2)
            bullet_group.add(enemy_bullet3)
            bullet_group.add(enemy_bullet4)
            bullet_group.add(enemy_bullet5)
            bullet_group.add(enemy_bullet6)
            bullet_group.add(enemy_bullet7)

    def draw(self, display): # 적 화면 생성
        display.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


def spawn_enemy(): # 적 생성
    random_x = random.randint(100, 750)
    random_y = random.randint(50, 600)
    while abs(random_x - player.rect.centerx) < 100 and abs(random_x - player.rect.centerx) < 100:  # 플레이어 가까이에 생성 안되도록
        random_x = random.randint(100, 750)
        random_y = random.randint(50, 600)
    random_type = random.randint(0, 8)

    if random_type == 0 or random_type == 1:
        enemy = Enemy(random_x, random_y, 1.5, 2, "shots3")
    elif random_type == 2 or random_type == 3:
        enemy = Enemy(random_x, random_y, 1.5, 2, "shots4")
    elif random_type == 4 or random_type == 5:
        enemy = Enemy(random_x, random_y, 1.5, 2, "shots5")
    elif random_type == 6 or random_type == 7:
        enemy = Enemy(random_x, random_y, 1.5, 1, "shots6")
    elif random_type == 8:
        enemy = Enemy(random_x, random_y, 1.5, 0.5, "shots8")
    enemy_group.add(enemy)


def reset_game():
    for enemy in enemy_group:
        enemy.kill()
    for bullet in bullet_group:
        bullet.kill()

    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False

    clicking = False # 플레이어가 클릭하는지

    dt = 1
    attack_rate = 20 # 공격 주기
    attack_cooltime = 10

    fade_in = 0

    spawn_rate = random.randint(50, 200)
    spawn_cooltime = 0 # 적 생성 쿨타임

    pygame.mixer.music.load('data1/sound/bgm.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.01)


bullet_group = pygame.sprite.Group() # Sprite 그룹 생성
enemy_group = pygame.sprite.Group()

player = Player(400, 320, 1.5, 3)

# 버튼 만들기
start_button = button.Button(screen_width // 2 - 130, screen_height // 2 -150, start_img, 1)
exit_button = button.Button(screen_width // 2 -130, screen_height // 2 +50, exit_img, 1)

# 변수 설정a

moving_left = False
moving_right = False
moving_up = False
moving_down = False

clicking = False # 플레이어가 클릭하는지

dt = 1
attack_rate = 20 # 공격 주기
attack_cooltime = 10 # 공격 쿨타임

fade_in = 0

spawn_rate = random.randint(50, 200) # 적 생성 주기
spawn_cooltime = 0 # 적 생성 쿨타임

# 배경음악 재생
pygame.mixer.music.load('data1/sound/bgm.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.01)

game_run = True
while game_run:
    clock.tick(60) # FPS 설정, 1초에 60번 while문이 돌도록

    if start_game == False:
        # 메뉴 표시
        screen.fill(background_color)
        # 버튼 추가
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            game_run = False
    
    else:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        attack_cooltime += dt
        spawn_cooltime += dt

        screen.fill(background_color) # 배경
        screen.blit(background_img, (0, 0)) # 백그라운드 이미지

        # 그룹 업데이트
        bullet_group.update()
        bullet_group.draw(screen) # 총알이 제일 뒤로 보이도록 먼저 그림

        if player.drawing:
            player.update_animation()
            player.draw(screen) # 플레이어 생성

        if player.alive:
            enemy_group.update()

        if player.lives == 3:
            screen.blit(pygame.transform.flip(heart, False, False), (0, 0))
            screen.blit(pygame.transform.flip(heart, False, False), (30, 0))
            screen.blit(pygame.transform.flip(heart, False, False), (60, 0))
        elif player.lives == 2:
            screen.blit(pygame.transform.flip(heart, False, False), (0, 0))
            screen.blit(pygame.transform.flip(heart, False, False), (30, 0))
            screen.blit(pygame.transform.flip(empty_heart, False, False), (60, 0))
        elif player.lives == 1:
            screen.blit(pygame.transform.flip(heart, False, False), (0, 0))
            screen.blit(pygame.transform.flip(empty_heart, False, False), (30, 0))
            screen.blit(pygame.transform.flip(empty_heart, False, False), (60, 0))
        else:
            screen.blit(pygame.transform.flip(empty_heart, False, False), (0, 0))
            screen.blit(pygame.transform.flip(empty_heart, False, False), (30, 0))
            screen.blit(pygame.transform.flip(empty_heart, False, False), (60, 0))

        for enemy in enemy_group:
            enemy.update_animation()
            enemy.draw(screen)
        
        # 화면에 점수 표시
        score_text = myFont.render("Score: " + str(player.score), True, (255, 255, 255))
        screen.blit(score_text, [350, 0])

        # 플레이어 생존 시
        if player.alive:

            if clicking and attack_cooltime >= attack_rate:
                sword_s.play()
                spin = Spin(player.rect.centerx, player.rect.centery, 5, 'spin')
                attack_cooltime = 0

                spin.update_animation()
                spin.draw(screen) # 플레이어 생성

            if moving_left or moving_right or moving_up or moving_down:
                player.update_action(1) # run 애니메이션으로 전환
            else:
                player.update_action(0) # idle 애니메이션으로 전환
            player.move(moving_left, moving_right, moving_up, moving_down)

            if mouse_x < player.rect.x:
                player.flip = True
                player.direction = -1
            else:
                player.flip = False
                player.direction = 1

            # 충돌처리
            for bullet in bullet_group:
                if bullet.rect.colliderect(player.rect):
                    if bullet.type == "enemy_bullet":
                        bullet.kill()
                        player_hit_s.play()
                        player.lives -= 1
                        print("life:", player.lives)

                        if player.lives <= 0:
                            print("Game Over")
                            death_s.set_volume(0.05)
                            death_s.play()
                            player.update_action(2)
                            fade_in = 10
                            player.alive = False

            for enemy in enemy_group:
                if enemy.rect.colliderect(player.rect):
                    player_hit_s.play()
                    player.lives -= 1
                    enemy.kill()
                    print("life:", player.lives)
                    if player.lives <= 0:
                        print("Game Over")
                        death_s.set_volume(0.05)
                        death_s.play()
                        player.update_action(2) # death 애니메이션으로 전환
                        fade_in = 10
                        player.alive = False

        if not player.alive and fade_in > 0:
            fade_in -= 0.1
            black_surf = pygame.Surface((screen_width, screen_height))
            black_surf.set_alpha(int(255*fade_in/10))
            screen.blit(black_surf, (0, 0))
        elif not player.alive and fade_in <= 0:
            screen.blit(pygame.Surface((screen_width, screen_height)), (0, 0))
            game_over_text = game_over_font.render("Game Over ", True, (255, 0, 0))
            press_r_text = myFont.render(
                "press R to replay", True, (255, 255, 255))
            score_text = myFont.render(
                "Score: " + str(player.score), True, (255, 255, 255))

            screen.blit(game_over_text, [
                        screen_width/2 - 250, screen_height/2 - 100])
            screen.blit(press_r_text, [screen_width/2 - 80, screen_height/2])
            screen.blit(score_text, [350, 0])

        # 적 소환
        if spawn_cooltime >= spawn_rate and player.alive:
            if player.score < 500:
                spawn_rate = random.randint(100, 200)
            elif player.score < 700:
                spawn_rate = random.randint(80, 180)
            elif player.score < 1000:
                spawn_rate = random.randint(60, 160)
            else:
                spawn_rate = random.randint(50, 100)

            spawn_enemy()
            spawn_cooltime = 0
        
    # 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False # 종료

        if event.type == pygame.KEYDOWN: # 키 누를때
            if event.key == pygame.K_ESCAPE: # exc키로 종료
                game_run = False
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_r and not player.alive:
                player = Player(400, 320, 1.5, 3) # 플레이어
                reset_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True # 클릭하면 True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False # 클릭 때면 False

    keys = pygame.key.get_pressed()

    # 업데이트
    pygame.display.flip()
    last_frame = screen.copy()

# 게임종료
pygame.quit()
