import pygame
import sys
import os
import random
import math

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

        self.count = 0  # 총알이 벽에 부딪힌 횟수

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
