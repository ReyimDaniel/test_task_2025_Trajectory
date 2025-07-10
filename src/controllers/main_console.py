from src.models.work_schedule import WorkSchedule
from datetime import datetime
from src.config.config import BASE_URL

"""
Консольное приложение.
После запуска будет выдан список доступных дат.
Далее, можно выбрать одну из разработанных функций.
"""


def input_date(schedule):
    """
    Запрос даты и проверка наличия этой даты в расписании
    """
    available_dates = [d.date for d in schedule.days]
    while True:
        date_str = input("Введите дату (ГГГГ-ММ-ДД): ").strip()
        if date_str in available_dates:
            return date_str
        print("Дата отсутствует в расписании. Попробуйте еще раз.")


def input_time(prompt):
    """
    Запрос времени и проверка
    """
    while True:
        time_str = input(prompt).strip()
        try:
            datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            print("Некорректный формат времени (ЧЧ:ММ)")


def input_duration():
    """
    Запрос длительности интервала в минутах
    """
    while True:
        dur_str = input("Введите длительность в минутах: ").strip()
        if dur_str.isdigit() and int(dur_str) > 0:
            return int(dur_str)
        print("Введите положительное целое число.")


def main():
    schedule = WorkSchedule(BASE_URL)

    print("Доступные даты:")
    for d in schedule.days:
        print("-", d.date)

    date = input_date(schedule)

    while True:
        print(f"\nВыбранная дата: {date}")
        print("Меню действий:")
        print("1. Показать занятые интервалы")
        print("2. Показать свободные интервалы")
        print("3. Проверить доступность слота")
        print("4. Найти первый доступный слот нужной длительности")
        print("5. Сменить дату")
        print("6. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            busy = schedule.get_busy_slots(date)
            if busy:
                print("\nЗанятые интервалы:")
                for start, end in busy:
                    print(f"  {start.time()} — {end.time()}")
            else:
                print("Нет занятых интервалов.")

        elif choice == "2":
            free = schedule.get_free_slots(date)
            if free:
                print("\nСвободные интервалы:")
                for start, end in free:
                    print(f"  {start.time()} — {end.time()}")
            else:
                print("Нет свободных интервалов.")

        elif choice == "3":
            start_time = input_time("Введите время начала (ЧЧ:ММ): ")
            end_time = input_time("Введите время окончания (ЧЧ:ММ): ")
            if start_time >= end_time:
                print("Время начала должно быть меньше времени окончания.")
                continue
            available = schedule.is_slot_available(date, start_time, end_time)
            print("Слот доступен" if available else "Слот недоступен")

        elif choice == "4":
            duration = input_duration()
            slot = schedule.find_available_slot(date, duration)
            if slot:
                print(f"Найден слот: {slot[0].time()} — {slot[1].time()}")
            else:
                print("Подходящий слот не найден.")

        elif choice == "5":
            date = input_date(schedule)

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
