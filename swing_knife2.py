import pygame
import sys
import os
import random
import math
from Player import Player
from Enemy import Enemy
from Spin import Spin

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

# 사운드 설정 _s 는 사운드
bgm_s = pygame.mixer.Sound('data1/sound/bgm.mp3')
death_s = pygame.mixer.Sound('data1/sound/death_sound.mp3')
sword_s = pygame.mixer.Sound('data1/sound/sword.mp3')
hit_enemy_s = pygame.mixer.Sound('data1/sound/destroy_enemy.wav')
player_hit_s = pygame.mixer.Sound('data1/sound/player_hit.mp3')


def spawn_enemy():  # 적 생성
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

    clicking = False  # 플레이어가 클릭하는지

    dt = 1
    attack_rate = 20  # 공격 주기
    attack_cooltime = 10

    fade_in = 0

    spawn_rate = random.randint(50, 200)
    spawn_cooltime = 0  # 적 생성 쿨타임

    pygame.mixer.music.load('data1/sound/bgm.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.01)


bullet_group = pygame.sprite.Group()  # Sprite 그룹 생성
enemy_group = pygame.sprite.Group()

player = Player(400, 320, 1.5, 3)

# 변수 설정

moving_left = False
moving_right = False
moving_up = False
moving_down = False

clicking = False  # 플레이어가 클릭하는지

dt = 1
attack_rate = 20  # 공격 주기
attack_cooltime = 10  # 공격 쿨타임

fade_in = 0

spawn_rate = random.randint(50, 200)  # 적 생성 주기
spawn_cooltime = 0  # 적 생성 쿨타임

# 배경음악 재생
pygame.mixer.music.load('data1/sound/bgm.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.01)

game_run = True
while game_run:
    clock.tick(60)  # FPS 설정, 1초에 60번 while문이 돌도록

    mouse_x, mouse_y = pygame.mouse.get_pos()

    attack_cooltime += dt
    spawn_cooltime += dt

    screen.fill(background_color)  # 배경
    screen.blit(background_img, (0, 0))  # 백그라운드 이미지

    # 그룹 업데이트
    bullet_group.update()
    bullet_group.draw(screen)  # 총알이 제일 뒤로 보이도록 먼저 그림

    if player.drawing:
        player.update_animation()
        player.draw(screen)  # 플레이어 생성

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
    score_text = myFont.render(
        "Score: " + str(player.score), True, (255, 255, 255))
    screen.blit(score_text, [350, 0])

    # 플레이어 생존 시
    if player.alive:

        if clicking and attack_cooltime >= attack_rate:
            sword_s.play()
            spin = Spin(player.rect.centerx, player.rect.centery, 5, 'spin')
            attack_cooltime = 0

        if moving_left or moving_right or moving_up or moving_down:
            player.update_action(1)  # run 애니메이션으로 전환
        else:
            player.update_action(0)  # idle 애니메이션으로 전환
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
                    player.update_action(2)  # death 애니메이션으로 전환
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
            game_run = False  # 종료

        if event.type == pygame.KEYDOWN:  # 키 누를때
            if event.key == pygame.K_ESCAPE:  # exc키로 종료
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
                player = Player(400, 320, 1.5, 3)  # 플레이어
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
                clicking = True  # 클릭하면 True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False  # 클릭 때면 False

    keys = pygame.key.get_pressed()

    # 업데이트
    pygame.display.flip()
    last_frame = screen.copy()

# 게임종료
pygame.quit()
