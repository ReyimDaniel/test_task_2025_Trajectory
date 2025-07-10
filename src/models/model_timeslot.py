from datetime import datetime


class TimeSlot:
    """
    Класс, представляющий занятый временной интервал в конкретный день
    :param id: int - уникальный идентификатор слота
    :param day_id: int - идентификатор дня, к которому относится слот
    :param date_str: str - дата в формате "YYYY-MM-DD"
    :param start_str: str - время начала слота в формате "HH:MM"
    :param end_str: str - время окончания слота в формате "HH:MM"
    """

    def __init__(self, id, day_id, date_str, start_str, end_str):
        self.id = id
        self.day_id = day_id
        self.start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
        self.end = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")

    def overlaps(self, start, end):
        """
        Проверяет, пересекается ли слот с заданным интервалом времени.
        :param start: datetime - начало проверяемого интервала
        :param end: datetime - конец проверяемого интервала
        :return: bool - True, если есть пересечение
        """
        return not (self.end <= start or self.start >= end)

    def __repr__(self):
        """
        Строковое представление
        """
        return f"<Slot {self.start.time()}–{self.end.time()}>"
