from src.models.work_schedule import WorkSchedule
from src.config.config import BASE_URL, TEST_START, TEST_END, DURATION_MINUTES


def main():
    schedule = WorkSchedule(BASE_URL)
    available_dates = [day.date for day in schedule.days]

    print("\nДоступные даты:")
    for i, d in enumerate(available_dates, 1):
        print(f"{i}. {d}")

    # Проверка наличия доступных дат
    if not available_dates:
        print("\nНет доступных дат в расписании.")
        return

    # Используем первую доступную дату
    date = available_dates[0]
    print(f"\nИспользуем дату: {date}")

    # Занятые интервалы
    print("\nЗанятые интервалы:")
    busy_slots = schedule.get_busy_slots(date)
    if busy_slots:
        for start, end in busy_slots:
            print(f"{start.time()} — {end.time()}")
    else:
        print("Нет занятых интервалов.")

    # Свободные интервалы
    print("\nСвободные интервалы:")
    free_slots = schedule.get_free_slots(date)
    if free_slots:
        for start, end in free_slots:
            print(f"{start.time()} — {end.time()}")
    else:
        print("Нет свободных интервалов.")

    # Проверка доступности заданного интервала
    print(f"\nПроверка доступности интервала {TEST_START} — {TEST_END}:")
    is_available = schedule.is_slot_available(date, TEST_START, TEST_END)
    print("Доступен" if is_available else "Недоступен")

    # Поиск первого подходящего свободного слота
    print(f"\nПоиск первого свободного слота на {DURATION_MINUTES} минут:")
    found = schedule.find_available_slot(date, DURATION_MINUTES)
    if found:
        print(f"Найден: {found[0].time()} — {found[1].time()}")
    else:
        print("Нет подходящего слота.")


if __name__ == "__main__":
    main()
