import pygame


def checker(cells_list: list, cell_id: int, glob_x: int, glob_y: int, left_wall_cells_id: list,
            right_wall_cells_id: list, center_wall_cells_id: list) -> bool:
    """
    Проверяет проходимость поля при установке конкретной ячейки. Если поле проходимо, добавляет id ячейки в
    соответствующий список wall_cells в зависимости от граничности, и запускает проверку смежных неграничных ячеек
     а присваивание им статуса граничных.
    :param cells_list: список всех ячеек поля.
    :param cell_id: id текущей ячейки.
    :param glob_x: количество ячеек в поле по ширине.
    :param glob_y: количество ячеек в поле по высоте.
    :param left_wall_cells_id: список id ячеек, граничных с левой и нижней стеной, или смежными с ними ячейками.
    :param right_wall_cells_id: список id ячеек, граничных с правой и верхней стеной, или смежными с ними ячейками.
    :param center_wall_cells_id: список id ячеек не граничащих со стенами или граничными ячейками.
    :return: True, если поле проходимо при минировании ячейки с текущим id. Иначе False.
    """
    status_l = False
    status_r = False
    # Проверка, касается ли ячейка стены
    if cell_id < glob_x: status_r = True  # верхняя грань
    if cell_id % glob_x == glob_x - 1: status_r = True  # правая грань
    if cell_id % glob_x == 0: status_l = True  # левая грань
    if cell_id >= glob_x * glob_y - glob_x: status_l = True  # нижняя грань

    nearby_cells_id = cells_list[cell_id].nearby_cells_id()

    # проверяет, касается ли ячейка других ячеек, касающихся стен
    for nearby_cell in nearby_cells_id:
        if left_wall_cells_id.count(nearby_cell):
            status_l = True
    for nearby_cell in nearby_cells_id:
        if right_wall_cells_id.count(nearby_cell):
            status_r = True

    if status_l and status_r:  # Ячейка касается смежных противоположным стенам ячеек, зн, поле стало непроходимым.
        return False

    if status_l:
        left_wall_cells_id.append(cell_id)
        for nearby_cell in nearby_cells_id:
            if center_wall_cells_id.count(nearby_cell):
                nearby_cells_status_changer(cells_list, nearby_cell, left_wall_cells_id, center_wall_cells_id)
        return True

    if status_r:
        right_wall_cells_id.append(cell_id)
        for nearby_cell in nearby_cells_id:
            if center_wall_cells_id.count(nearby_cell):
                nearby_cells_status_changer(cells_list, nearby_cell, right_wall_cells_id, center_wall_cells_id)
        return True

    center_wall_cells_id.append(cell_id)
    return True


def nearby_cells_status_changer(cells_list: list, cell_id: int, direction_wall_cells_id: list, center_wall_cells_id: list) -> None:
    """
    Рекурсивно изменяет статус центральных ячеек на соединенные с левой или правой краями игрового поля.
    :param cells_list: список всех ячеек поля.
    :param cell_id: id текущей ячейки.
    :param direction_wall_cells_id: список id ячеек, граничных с одной из стен, или смежными с ними ячейками.
    :param center_wall_cells_id: список id ячеек не граничащих со стенами или граничными ячейками.
    :return: None.
    """
    nearby_cells_id = cells_list[cell_id].nearby_cells_id()

    center_wall_cells_id.remove(cell_id)
    direction_wall_cells_id.append(cell_id)

    for nearby_cell in nearby_cells_id:
        if center_wall_cells_id.count(nearby_cell):
            nearby_cells_status_changer(cells_list, nearby_cell, direction_wall_cells_id, center_wall_cells_id)


def player_move(cells_list: list, cell_id: int, key: str, checked_cells: list, trampled_cells: list, img: dict) -> int:
    """
    Устанавливает статус active новой ячейке, в которую совершено перемещение.
    Если перемещение было совершено, текущей ячейке устанавливается статус trampled и снимается статус active.
    :param cells_list: список всех ячеек.
    :param cell_id: id текущей ячейки.
    :param key: строка, указывающая направление перемещения ("up", "down", "left", "right")
    :param checked_cells: список id отмеченных опасными ячеек.
    :param trampled_cells: список id посещенных ячеек.
    :param img: словарь с изображениями для клеток.
    :return: возвращает id в которую переместился игрок. Если перемещение невозможно, возвращает текущий id.
    """
    new_active_cell_id = cells_list[cell_id].nearby_cells_id(key)[0]
    # if cells_list[new_active_cell_id].checked:
    if checked_cells.count(new_active_cell_id):
        return cell_id
    else:
        trampled_cells.append(cell_id)
        cells_list[cell_id].image = img["trampled_cell"]
        # направление поворота игрока
        if key == "up": active_img = pygame.transform.rotate(img["active_cell"], 90)
        elif key == "down": active_img = pygame.transform.rotate(img["active_cell"], -90)
        elif key == "left": active_img = pygame.transform.rotate(img["active_cell"], 180)
        else: active_img = img["active_cell"]

        cells_list[new_active_cell_id].image = active_img

        return new_active_cell_id
