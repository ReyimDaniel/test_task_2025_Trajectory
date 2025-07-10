from src.models.model_day import Day
from src.models.model_timeslot import TimeSlot
import requests
from datetime import datetime, timedelta


class WorkSchedule:
    """
    Класс для работы с функциями
    Загрузка данных с URL, обработка их в виде объектов Day и TimeSlot (datetime)
    """

    def __init__(self, url):
        """
        Инициализация расписания: загружает данные по ссылке
        :param url: URL с данными расписания
        """
        self.days = []
        self.timeslots = []
        self._load_data(url)

    def _load_data(self, url):
        """
        Загрузка данных с URL
        Преобразование данных в объекты Day и TimeSlot (datetime)
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for d in data.get("days", []):
                self.days.append(Day(d["id"], d["date"], d["start"], d["end"]))

            for ts in data.get("timeslots", []):
                date_str = next(d.date for d in self.days if d.id == ts["day_id"])
                self.timeslots.append(
                    TimeSlot(ts["id"], ts["day_id"], date_str, ts["start"], ts["end"])
                )
        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка загрузки данных: {e}")

    def get_day(self, date):
        """
        Возврат объекта Day по заданной дате
        :param date: дата в формате "YYYY-MM-DD"
        :return: Day или None
        """
        for day in self.days:
            if day.date == date:
                return day
        return None

    def get_busy_slots(self, date):
        """
        Возврат список занятых временных интервалов по заданной дате
        :param date: str
        :return: list of (datetime, datetime)
        """
        day = self.get_day(date)
        if not day:
            return []

        return [(ts.start, ts.end) for ts in self.timeslots if ts.day_id == day.id]

    def get_working_hours(self, date):
        """
        Возврат времени начала и конца рабочего дня
        :param date: str
        :return: (datetime, datetime)
        :raises ValueError: в случае если дата отсутствует
        """
        day = self.get_day(date)
        if not day:
            raise ValueError(f"Нет расписания на дату {date}")
        return day.start, day.end

    def get_free_slots(self, date):
        """
        Возврат списка свободных интервалов времени между занятыми слотами
        :param date: str
        :return: list of (datetime, datetime)
        """
        work_start, work_end = self.get_working_hours(date)
        busy = sorted(self.get_busy_slots(date))
        free = []
        current = work_start

        for start, end in busy:
            if current < start:
                free.append((current, start))
            current = max(current, end)

        if current < work_end:
            free.append((current, work_end))

        return free

    def is_slot_available(self, date, start_time, end_time):
        """
        Проверка, свободен ли заданный временной интервал
        :param date: str - дата
        :param start_time: str - время начала в формате "HH:MM"
        :param end_time: str - время окончания в формате "HH:MM"
        :return: bool - True, если интервал свободен
        """
        check_start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        check_end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        for start, end in self.get_busy_slots(date):
            if not (check_end <= start or check_start >= end):
                return False
        return True

    def find_available_slot(self, date, duration_minutes):
        """
        Первый свободный интервал заданной длительности
        :param date: str - дата
        :param duration_minutes: int - длительность слота в минутах
        :return: tuple(datetime, datetime) или None
        """
        free_slots = self.get_free_slots(date)
        duration = timedelta(minutes=duration_minutes)

        for start, end in free_slots:
            if end - start >= duration:
                return start, start + duration
        return None
