import functions
import random


def start_game(all_cells: list, cells_number_x: int, cells_number_y: int, difficulty: int) -> list:
    """
    Функция генерирует параметры игрового поля с проверкой проходимости уровня.
    :param all_cells: список всех ячеек.
    :param cells_number_x: количество клеток по ширине.
    :param cells_number_y: количество клеток по высоте.
    :param difficulty: процент заминированных ячеек.
    :return: список id заминированных ячеек
    """
    # Генерация списка id заминированных ячеек с проверкой игрового поля на проходимость
    create_field = False
    while not create_field:
        bombs_number = int(cells_number_x * cells_number_y * difficulty / 100)  # количество мин
        cells_number = cells_number_x * cells_number_y

        cells_rand_id_list = [x for x in range(cells_number)]
        # удаление зарезервированных клеток из списка проверки минирования
        cells_rand_id_list.remove(0)
        cells_rand_id_list.remove(1)
        cells_rand_id_list.remove(cells_number_x)
        cells_rand_id_list.remove(cells_number_x + 1)
        cells_rand_id_list.remove(cells_number_x * cells_number_y - 1)

        random.shuffle(cells_rand_id_list)
        mined_cells = []
        bombs_counter = 0
        i = 0
        left_wall_cells_id = []
        right_wall_cells_id = []
        center_wall_cells_id = []

        while bombs_counter < bombs_number:
            if functions.checker(all_cells, cells_rand_id_list[i], cells_number_x, cells_number_y, left_wall_cells_id,
                           right_wall_cells_id, center_wall_cells_id):
                mined_cells.append(cells_rand_id_list[i])
                bombs_counter += 1
            i += 1

        create_field = True

    return mined_cells
