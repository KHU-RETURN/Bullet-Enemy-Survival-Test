import pygame
import sys
import os
import random
import math
from Player import Player
from Bullet import Bullet

pygame.init()

screen_width = 800
screen_height = 640
size = [screen_width, screen_height]  # 창 크기
screen = pygame.display.set_mode(size)

# 파이게임 전체화면

title = "swing_knife"  # 게임 이름
pygame.display.set_caption(title)

# 게임 내 설정
clock = pygame.time.Clock()  # 전역변수 하나밖에 사용 안함. 따라서 지울것
background_color = (0, 0, 40)

# 폰트 설정
myFont = pygame.font.Font('data1/a옛날목욕탕B.ttf', 30)
game_over_font = pygame.font.Font('data1/a옛날목욕탕B.ttf', 90)


# 이미지 설정
background_img = pygame.image.load(
    'data1/img/bg/background.png').convert()  # convert, convert_alpha 차이
sword_img = pygame.image.load(
    'data1/img/player/swing/sword.png').convert_alpha()
sword_img = pygame.transform.scale(
    sword_img, (int(sword_img.get_width()*1.2), int(sword_img.get_height()*0.3)))
enemy_bullet = pygame.image.load('data1/img/enemy/attack.png').convert_alpha()
enemy_bullet = pygame.transform.scale(enemy_bullet, (int(
    enemy_bullet.get_width()*0.8), int(enemy_bullet.get_height()*0.6)))
heart = pygame.image.load('data1/img/heart.png').convert_alpha()
empty_heart = pygame.image.load('data1/img/empty_heart.png').convert_alpha()


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

        self.direction = 1  # 좌우 방향
        self.flip = False  # 좌우 반전

        self.animation_list = []  # 애니메이션 리스트
        self.frame_index = 0  # 애니메이션 프레임
        self.update_time = pygame.time.get_ticks()  # 애니메이션 시간

        self.action = 0

        # 애니메이션 리스트
        animation_type = ['idle', 'move_down', 'move_up']
        for animation in animation_type:
            temp_list = []
            # 애니메이션 프레임 수
            num_of_frames = len(os.listdir(
                f'data1/img/enemy/{self.type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'data1/img/enemy/{self.type}/{animation}/{animation}{i}.png').convert_alpha()
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
            entity_movement = [
                dif_x/(abs(dif_x)+abs(dif_y))*self.speed, dif_y/(abs(dif_x)+abs(dif_y))*self.speed]
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

    def update_action(self, new_action):  # 적 액션 상태 업데이트
        if new_action != self.action:  # 이전 액션과 같은지 확인
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self):  # 적 애니메이션 업데이트
        ANIM_COOLDOWN = 250  # 애니메이션 쿨타임

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIM_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def attack(self):  # 적 공격
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

    def draw(self, display):  # 적 화면 생성
        display.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


bullet_group = pygame.sprite.Group()  # Sprite 그룹 생성

player = Player(400, 320, 1.5, 3)
