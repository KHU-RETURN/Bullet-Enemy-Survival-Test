import pygame
import sys
import os
import random
import math
from Player import Player

pygame.init()

screen_width = 800
screen_height = 640
size = [screen_width, screen_height]  # 창 크기
screen = pygame.display.set_mode(size)

hit_enemy_s = pygame.mixer.Sound('data1/sound/destroy_enemy.wav')

# 애니메이션 고치는중, 뒤에 update_animation, update_action 추가 Spin 맨 뒤에 update animation 없음 추가하면 끝


class Spin(pygame.sprite.Sprite):
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
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

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
        ANIM_COOLDOWN = 10

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


player = Player(400, 320, 1.5, 3)

enemy_group = pygame.sprite.Group()
