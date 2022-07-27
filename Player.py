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


# 파이게임 전체화면

title = "swing_knife"  # 게임 이름
pygame.display.set_caption(title)

# 게임 내 설정
clock = pygame.time.Clock()  # 전역변수 하나밖에 사용 안함. 따라서 지울것
background_color = (0, 0, 40)

# 폰트 설정
myFont = pygame.font.Font('data1/a옛날목욕탕B.ttf', 30)
game_over_font = pygame.font.Font('data1/a옛날목욕탕B.ttf', 90)

sword_img = pygame.image.load(
    'data1/img/player/swing/sword.png').convert_alpha()
sword_img = pygame.transform.scale(
    sword_img, (int(sword_img.get_width()*1.2), int(sword_img.get_height()*0.3)))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True  # 살아있는지

        self.speed = speed
        self.direction = 1  # 좌우 방향
        self.flip = False  # 이미지 좌우 반전

        self.animation_list = []  # 애니메이션 리스트
        self.frame_index = 0  # 애니메이션 프레임 인덱스
        self.update_time = pygame.time.get_ticks()  # 애니메이션 시간

        self.action = 0  # idle, run, death 상태
        self.weapon_img = sword_img

        self.score = 0
        self.lives = 3  # 목숨

        self.drawing = True

        # 애니메이션 리스트 추가
        animation_types = ['idle', 'run', 'death']
        for animation in animation_types:
            temp_list = []
            # 애니메이션 프레임 수
            num_of_frames = len(os.listdir(f'data1/img/player/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'data1/img/player/{animation}/{animation}{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale*1.7), int(img.get_height() * scale*1.7)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x+30, y+40)

    # 플레이어 이동
    def move(self, moving_left, moving_right, moving_up, moving_down):  # 변수 너무 많음

        dx = 0
        dy = 0

        if moving_left and self.rect.x > 10:  # weith, height로 계산
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

    def update_animation(self):  # 플레이어 애니메이션 업데이트
        ANIM_COOLDOWN = 150  # 애니메이션 쿨타임

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIM_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action != 2:  # death가 아니라면 반복
                self.frame_index = 0
            elif self.action == 2:  # death라면 게임 오버
                self.drawing = False
                self.kill()

    def update_action(self, new_action):  # 플레이어 액션 상태 업데이트 함수
        if new_action != self.action:  # 이전 액션과 같은지 확인
            self.action = new_action

            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def handle_weapon(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x = mouse_x - self.rect.centerx
        rel_y = mouse_y - self.rect.centery

        angle = (180/math.pi) * -math.atan2(rel_y, rel_x)

        img = pygame.transform.scale(self.weapon_img, (int(
            self.weapon_img.get_width() * 5), int(self.weapon_img.get_height() * 5)))
        player_weapon_copy = pygame.transform.rotate(img, angle)

        display.blit(player_weapon_copy, (self.rect.x+25 - int(player_weapon_copy.get_width() / 2),
                     self.rect.y+30 - int(player_weapon_copy.get_height() / 2)))  # 왜 다시 scale 조정?

    def draw(self, display):  # 플레이어 화면에 생성
        display.blit(pygame.transform.flip(self.image, self.flip,
                     False), self.rect)  # transform? 왜사용?

        if player.alive:
            self.handle_weapon(display)


player = Player(400, 320, 1.5, 3)
