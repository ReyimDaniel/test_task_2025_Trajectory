import unittest
from src.models.work_schedule import WorkSchedule
from src.config.config import BASE_URL


class TestSchedule(unittest.TestCase):
    def setUp(self):
        """Создание объекта расписания перед каждым тестом"""
        self.schedule = WorkSchedule(BASE_URL)

    def test_get_busy_slots(self):
        """Проверка получения списка занятых интервалов для конкретной даты"""
        slots = self.schedule.get_busy_slots("2025-02-16")
        self.assertIsInstance(slots, list)
        for slot in slots:
            self.assertEqual(len(slot), 2)
            self.assertTrue(hasattr(slot[0], "hour") and hasattr(slot[1], "minute"))

    def test_get_free_slots(self):
        """Проверка получения списка свободных интервалов для конкретной даты"""
        free = self.schedule.get_free_slots("2025-02-15")
        self.assertIsInstance(free, list)
        for slot in free:
            self.assertEqual(len(slot), 2)
            self.assertTrue(slot[0] < slot[1])

    def test_is_slot_available(self):
        """Проверка, доступен ли указанный временной интервал"""
        available = self.schedule.is_slot_available("2025-02-15", "09:00", "09:30")
        self.assertIsInstance(available, bool)

    def test_find_available_slot(self):
        """Поиск первого подходящего свободного интервала конкретной длительности в минутах"""
        slot = self.schedule.find_available_slot("2025-02-15", 30)
        self.assertTrue(slot is None or (isinstance(slot, tuple) and len(slot) == 2))

    def test_get_working_hours(self):
        """Проверка получения начала и конца рабочего дня"""
        start, end = self.schedule.get_working_hours("2025-02-15")
        self.assertTrue(start < end)
        self.assertEqual(start.date(), end.date())

    def test_invalid_date_raises_error(self):
        """Проверка исключения при запросе даты не существующей в расписании"""
        with self.assertRaises(ValueError):
            self.schedule.get_working_hours("2099-01-01")

    def test_no_busy_slots_returns_empty_list(self):
        """Проверка, что при отсутствии слотов возвращается пустой список"""
        result = self.schedule.get_busy_slots("2099-01-01")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
