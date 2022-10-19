import pygame


class Cells(pygame.sprite.Sprite):
    def __init__(self, self_numb_x: int, self_numb_y: int, cells_numb_x: int, cells_numb_y: int,
                 player_img: dict, indent_x: int, indent_y: int):
        """
        Клетки игрового поля.
        :param self_numb_x: номер текущей ячейки по горизонтали (с нуля).
        :param self_numb_y: номер текущей ячейки по вертикали (с нуля).
        :param cells_numb_x: количество клеток по ширине.
        :param cells_numb_y: количество клеток по высоте.
        :param player_img: словарь с изображениями для клеток.
        :param indent_x: отступ слева для выравнивания игрового поля в окне.
        :param indent_y: отступ справа для выравнивания игрового поля в окне.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img["cell"]
        self.rect = self.image.get_rect()
        self.cells_numb_x = cells_numb_x
        self.cells_numb_y = cells_numb_y
        self.cell_id = cells_numb_x * self_numb_y + self_numb_x
        self.rect.topleft = (self_numb_x * 50 + 2 + indent_x, self_numb_y * 50 + 2 + indent_y)  # устанавливает позицию спрайта

    def nearby_cells_directions(self, key: str = "square") -> list:
        """
        Возвращает список направлений на соседние ячейки, в котором порядок элемента сопоставим направлению
        расположения аналогичной клавиши на numpad клавиатуре относительно клавиши 5.
        Например, if ...[2] - направление вниз, т.к. клавиша 2 внизу от клавиши 5
        :param key: ключ направлений ("square", "cross", "up", "down", "left", "right")
        :return: список направлений на соседние ячейки
        """
        directions = [0] * 10
        if key == "cross": directions = [n % 2 - 1 for n in range(10)]
        elif key == "up": directions[8] = 1
        elif key == "down": directions[2] = 1
        elif key == "left": directions[4] = 1
        elif key == "right": directions[6] = 1
        elif key == "square": directions = [n for n in range(10)]

        # Проверка, касается ли ячейка стены, и ставит ограничения на направления проверки
        if self.cell_id < self.cells_numb_x:  # верхняя грань
            directions[7] = 0
            directions[8] = 0
            directions[9] = 0
        if self.cell_id % self.cells_numb_x == self.cells_numb_x - 1:  # правая грань
            directions[9] = 0
            directions[6] = 0
            directions[3] = 0

        if self.cell_id % self.cells_numb_x == 0:  # левая грань
            directions[7] = 0
            directions[4] = 0
            directions[1] = 0
        if self.cell_id >= self.cells_numb_x * self.cells_numb_y - self.cells_numb_x:  # нижняя грань
            directions[1] = 0
            directions[2] = 0
            directions[3] = 0
        return directions

    def nearby_cells_id(self, key: str = "square") -> list:
        """
        Возвращает sell_id соседних ячеек согласно полученному ключу key.
        В случае отправки ключа направления и отсутствия ячейки по указанному направлению,
        возвращается текущий sell_id
        :param key: ключ направлений ("square", "cross", "up", "down", "left", "right")
        :return: Список cell_id соседних ячеек
        """
        directions = self.nearby_cells_directions(key)
        nearby_cells_id = []
        if directions[1]: nearby_cells_id.append(self.cell_id + self.cells_numb_x - 1)
        if directions[2]: nearby_cells_id.append(self.cell_id + self.cells_numb_x)
        if directions[3]: nearby_cells_id.append(self.cell_id + self.cells_numb_x + 1)

        if directions[4]: nearby_cells_id.append(self.cell_id - 1)
        if directions[6]: nearby_cells_id.append(self.cell_id + 1)

        if directions[7]: nearby_cells_id.append(self.cell_id - self.cells_numb_x - 1)
        if directions[8]: nearby_cells_id.append(self.cell_id - self.cells_numb_x)
        if directions[9]: nearby_cells_id.append(self.cell_id - self.cells_numb_x + 1)

        if not nearby_cells_id:
            return [self.cell_id]
        return nearby_cells_id
