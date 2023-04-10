"""Tetris pygame"""

import pygame
from copy import deepcopy
from random import choice, randrange
from const import *


def check_borders():
    """Функція, яка відстежує вихід за межі поля"""
    if not 0 <= figure[i].x < WIDTH:
        return False
    elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    """Функція, яка відкриває файл для читання найкращого результату"""
    try:
        with open('record.txt') as file:
            return file.readline()
    except FileNotFoundError:
        with open('record.txt', 'w', encoding='UTF-8') as file:
            file.write('0')


def set_record(record, score):
    """Функція, яка записує новий рекорд до файлу"""
    rec = max(int(record), score)
    with open('record.txt', 'w', encoding='UTF-8') as file:
        file.write(str(rec))

# ініціалізація бібліотеки
pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

# фонова музика
pygame.mixer.init()
pygame.mixer.music.load(MAIN_MUSIC_PATH)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]

figures_pos = [
    [(-2, -1), (-1, -1), (0, -1), (1, -1)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, -1), (0, 0), (-1, 0), (0, 1)],
    [(0, -1), (0, 0), (-1, 0), (-1, 1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, -1), (-1, -1), (-1, 0), (-1, 1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)],
]

figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

ANIM_COUNT, ANIM_SPEED, ANIM_LIMIT = 0, 60, 2000


bg = pygame.image.load('img/bg1.jpg').convert()
game_bg = pygame.image.load('img/bg2.jpg').convert()

main_font = pygame.font.Font('font/font.ttf', 65)
font = pygame.font.Font('font/font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

get_color = lambda: (randrange(50, 256), randrange(50, 256), randrange(50, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

SCORE, lines = 0, 0

while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                ANIM_LIMIT = 100
            elif event.key == pygame.K_UP:
                rotate = True
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    ANIM_COUNT += ANIM_SPEED
    if ANIM_COUNT > ANIM_LIMIT:
        ANIM_COUNT = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                ANIM_LIMIT = 2000
                break
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # check lines
    line, lines = HEIGHT - 1, 0
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < WIDTH:
            line -= 1
        else:
            ANIM_SPEED += 3
            lines += 1
    # compute score
    SCORE += SCORES[lines]
    # draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)
    # draw titles
    sc.blit(title_tetris, (450, 10))
    sc.blit(title_score, (450, 580))
    sc.blit(font.render(str(SCORE), True, pygame.Color('white')), (450, 640))
    sc.blit(title_record, (450, 450))
    sc.blit(font.render(record, True, pygame.Color('gold')), (450, 510))
    # game over
    for i in range(WIDTH):
        if field[0][i]:
            set_record(record, SCORE)
            field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
            ANIM_COUNT, ANIM_SPEED, ANIM_LIMIT = 0, 60, 2000
            SCORE = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
