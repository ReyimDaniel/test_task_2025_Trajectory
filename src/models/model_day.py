from datetime import datetime


class Day:
    """
    Класс, представляющий рабочий день
    :param id: int — уникальный идентификатор дня
    :param date_str: str — дата в формате "YYYY-MM-DD"
    :param start_str: str — время начала в формате "HH:MM"
    :param end_str: str — время окончания в формате "HH:MM"
    """

    def __init__(self, id, date_str, start_str, end_str):
        self.id = id
        self.date = date_str
        self.start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
        self.end = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")

    def __repr__(self):
        """
        Строковое представление
        """
        return f"<Day {self.date} {self.start.time()}–{self.end.time()}>"
