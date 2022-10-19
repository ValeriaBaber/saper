import pygame
from os import path

from cells import Cells
import functions as foo
import start_game as sg


minWidth = 700
minHeight = 300
FPS = 30

cellsNumber_x = 15  # количество клеток по горизонтали и вертикали
cellsNumber_y = 15
difficulty = 30  # Процент заминированных клеток

indent_x = indent_y = 0

if minWidth <= cellsNumber_x * 50 + 200:
    minWidth = cellsNumber_x * 50 + 200
else: indent_x = (minWidth - 200 - cellsNumber_x * 50) / 2
if minHeight <= cellsNumber_y * 50 + 2:
    minHeight = cellsNumber_y * 50 + 2
else: indent_y = (minHeight - cellsNumber_y * 50) / 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (0, 255, 0)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((minWidth, minHeight))
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()

# настройка папки ассетов для загрузки файлов с диска
img_cells_dict = dict()
game_folder = path.dirname(__file__)
img_dir = path.join(game_folder, "img")
# Фон.
background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background = pygame.transform.scale(background, (minWidth, minHeight))
background_rect = background.get_rect()
# Фон меню.
menu_background = pygame.image.load(path.join(img_dir, "background_menu.png")).convert_alpha()
menu_background = pygame.transform.scale(menu_background, (195, minHeight))
menu_background_rect = background.get_rect()
menu_background_rect.x = minWidth - 195
# Клетки поля.
img_cells_dict["cell"] = pygame.image.load(path.join(img_dir, "cell.png")).convert_alpha()
img_cells_dict["active_cell"] = pygame.image.load(path.join(img_dir, "cell_active.png")).convert_alpha()
img_cells_dict["trampled_cell"] = pygame.image.load(path.join(img_dir, "cell_trampled.png")).convert_alpha()
img_cells_dict["checked_cell"] = pygame.image.load(path.join(img_dir, "cell_checked.png")).convert_alpha()
img_cells_dict["finish_cell"] = pygame.image.load(path.join(img_dir, "finish_cell.png")).convert_alpha()
# Кнопки сканера.
img_cross_active = pygame.image.load(path.join(img_dir, 'btn_cross_act.png')).convert()
img_cross_disabled = pygame.image.load(path.join(img_dir, 'btn_cross_dis.png')).convert()
img_btn_cross = img_cross_active
img_btn_cross_rect = img_btn_cross.get_rect()
img_square_active = pygame.image.load(path.join(img_dir, 'btn_square_act.png')).convert()
img_square_disabled = pygame.image.load(path.join(img_dir, 'btn_square_dis.png')).convert()
img_btn_square = img_square_disabled
img_btn_square_rect = img_square_disabled.get_rect()
indent_top_btn = 30
img_btn_cross_rect.topleft = (minWidth - 195 + indent_top_btn, indent_top_btn)
img_btn_square_rect.topright = (minWidth - indent_top_btn, indent_top_btn)
# Кнопки Новая игра
img_btn_new_game = pygame.image.load(path.join(img_dir, 'btn_new_game.png')).convert()
img_btn_new_game_rect = img_btn_new_game.get_rect()
img_btn_new_game_rect.bottomright = (minWidth - 3, minHeight - 3)
# Кнопки Новая игра и Победитель
img_game_over = pygame.image.load(path.join(img_dir, 'game_over.png')).convert()
img_game_over_rect = img_game_over.get_rect()
img_game_over_rect.center = ((minWidth-200) / 2, minHeight / 2)
img_winner = pygame.image.load(path.join(img_dir, 'winner.png')).convert()
img_winner_rect = img_winner.get_rect()
img_winner_rect.center = ((minWidth-200) / 2, minHeight / 2)
# Цифры
img_nums = list()
img_nums.append(pygame.image.load(path.join(img_dir, 'num0.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num1.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num2.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num3.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num4.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num5.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num6.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num7.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num8.png')).convert_alpha())
img_nums.append(pygame.image.load(path.join(img_dir, 'num9.png')).convert_alpha())

img_scaner_count = img_nums[0]
img_scaner_count_rect = img_scaner_count.get_rect()
img_scaner_count_rect.center = (195 / 2, 150)

# Спрайты
all_sprites = pygame.sprite.Group()
cellsSprite_Group = pygame.sprite.Group()
cells_list = []
for c_y in range(cellsNumber_y):
    for c_x in range(cellsNumber_x):
        cell = Cells(c_x, c_y, cellsNumber_x, cellsNumber_y, img_cells_dict, indent_x, indent_y)
        all_sprites.add(cell)
        cellsSprite_Group.add(cell)
        cells_list.append(cell)

mined_cells = sg.start_game(cells_list, cellsNumber_x, cellsNumber_y, difficulty)
active_cell_id = 0
cells_list[active_cell_id].image = img_cells_dict["active_cell"]
checked_cells = []
trampled_cells = []
scanner_mode = "cross"
cells_list[cellsNumber_x * cellsNumber_y - 1].image = img_cells_dict["finish_cell"]

# Основной цикл
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not winner and not game_over:
            if event.key == pygame.K_LEFT:
                active_cell_id = foo.player_move(cells_list, active_cell_id, "left", checked_cells, trampled_cells, img_cells_dict)
            elif event.key == pygame.K_RIGHT:
                active_cell_id = foo.player_move(cells_list, active_cell_id, "right", checked_cells, trampled_cells, img_cells_dict)
            elif event.key == pygame.K_UP:
                active_cell_id = foo.player_move(cells_list, active_cell_id, "up", checked_cells, trampled_cells, img_cells_dict)
            elif event.key == pygame.K_DOWN:
                active_cell_id = foo.player_move(cells_list, active_cell_id, "down", checked_cells, trampled_cells, img_cells_dict)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for cell in cells_list:
                if cell.rect.collidepoint(event.pos):
                    if checked_cells.count(cell.cell_id):  # если отметка есть
                        checked_cells.remove(cell.cell_id)
                        cell.image = img_cells_dict["cell"]
                    elif active_cell_id != cell.cell_id and not trampled_cells.count(cell.cell_id)\
                            and not cell.cell_id == cellsNumber_x * cellsNumber_y - 1:  # если отметки нет
                        checked_cells.append(cell.cell_id)
                        cell.image = img_cells_dict["checked_cell"]

            if img_btn_square_rect.collidepoint(event.pos):
                scanner_mode = "square"
            if img_btn_cross_rect.collidepoint(event.pos):
                scanner_mode = "cross"

            # Новая игра
            if img_btn_new_game_rect.collidepoint(event.pos):
                mined_cells = sg.start_game(cells_list, cellsNumber_x, cellsNumber_y, difficulty)
                for i in range(cellsNumber_x * cellsNumber_y):
                    cells_list[i].image = img_cells_dict["cell"]
                active_cell_id = 0
                cells_list[active_cell_id].image = img_cells_dict["active_cell"]
                checked_cells = []
                trampled_cells = []
                scanner_mode = "cross"

        if scanner_mode == "cross":
            img_btn_square = img_square_disabled
            img_btn_cross = img_cross_active
        else:
            img_btn_square = img_square_active
            img_btn_cross = img_cross_disabled

        # Картинка для значения счетчика бомб
        img_scaner_count = img_nums[len(list(set(cells_list[active_cell_id].nearby_cells_id(scanner_mode)) & set(mined_cells)))]

        # Победа и поражение
        if active_cell_id == cellsNumber_x * cellsNumber_y - 1:
            winner = 1
        else:
            winner = 0
        if mined_cells.count(active_cell_id):
            game_over = 1
        else:
            game_over = 0

    # Обновление
    all_sprites.update()

    # for cell in cells_list:  # TODO ОТЛАДКА: мины на поле
    #     if mined_cells.count(cell.cell_id):
    #         cell.image = img_cells_dict["checked_cell"]

    # Рендеринг
    screen.blit(background, background_rect)
    screen.blit(menu_background, menu_background_rect)
    # Кнопки сканера
    screen.blit(img_btn_cross, img_btn_cross_rect)
    screen.blit(img_btn_square, img_btn_square_rect)
    screen.blit(img_btn_new_game, img_btn_new_game_rect)
    menu_background.blit(img_scaner_count, img_scaner_count_rect)

    all_sprites.draw(screen)
    if winner:
        screen.blit(img_winner, img_winner_rect)
    elif game_over:
        screen.blit(img_game_over, img_game_over_rect)
    pygame.display.flip()

pygame.quit()
