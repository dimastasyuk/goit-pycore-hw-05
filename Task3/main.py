import sys
from datetime import datetime


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        raise ValueError("Рядок має містити дату, час, рівень і повідомлення.")

    date, time, level, message = parts
    datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

    if level not in ("INFO", "DEBUG", "ERROR", "WARNING"):
        raise ValueError(f"Невідомий рівень логування: {level}")

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> list:
    logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                raise ValueError(f"Неправильний формат у рядку {number}: {error}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log["level"] == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    counts = {"INFO": 0, "DEBUG": 0, "ERROR": 0, "WARNING": 0}

    for log in logs:
        counts[log["level"]] += 1

    return counts


def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<16} | Кількість")
    print("-" * 17 + "|" + "-" * 10)

    for level, count in counts.items():
        print(f"{level:<16} | {count}")


def main():
    if len(sys.argv) not in (2, 3):
        print("Використання: python main.py шлях_до_файлу [рівень]")
        return

    level = sys.argv[2].upper() if len(sys.argv) == 3 else None

    if level is not None and level not in ("INFO", "DEBUG", "ERROR", "WARNING"):
        print("Помилка: оберіть рівень INFO, DEBUG, ERROR або WARNING.")
        return

    try:
        logs = load_logs(sys.argv[1])
    except FileNotFoundError:
        print("Помилка: файл не знайдено.")
        return
    except (OSError, UnicodeError) as error:
        print(f"Помилка читання файлу: {error}")
        return
    except ValueError as error:
        print(f"Помилка: {error}")
        return

    display_log_counts(count_logs_by_level(logs))

    if level is not None:
        print(f"\nДеталі логів для рівня '{level}':")
        filtered_logs = filter_logs_by_level(logs, level)

        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")

        if not filtered_logs:
            print("Записів цього рівня немає.")


if __name__ == "__main__":
    main()
