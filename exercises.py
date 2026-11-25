"""Проверка и демонстрация обязательных упражнений 1-6 (ЛР № 7)."""
from collections import defaultdict
from main import RAW_RECORDS, build_registry, aggregate, ids_where, ids_in_range


def ex1_manual_trace(records):
    print("=== Упражнение 1. Пошаговая трассировка агрегации (первые 5 записей) ===")
    result = {}
    for step, record in enumerate(records[:5], start=1):
        key = record["field"]
        bucket = result.get(key)
        if bucket is None:
            bucket = {"count": 0, "sum": 0.0,
                      "min": record["debit"], "max": record["debit"]}
            result[key] = bucket
        value = record["debit"]
        bucket["count"] += 1
        bucket["sum"] += value
        bucket["min"] = min(bucket["min"], value)
        bucket["max"] = max(bucket["max"], value)
        snapshot = {k: {"count": v["count"], "sum": round(v["sum"], 1)} for k, v in result.items()}
        print(f"Шаг {step} ({record['id']}, field={key}, debit={value}): {snapshot}")


def ex3_unhashable(records):
    print("\n=== Упражнение 3. Хешируемые и нехешируемые значения ===")
    samples = [
        ("int (42)", 42),
        ("str ('SK-101')", "SK-101"),
        ("tuple из чисел (1, 2, 3)", (1, 2, 3)),
        ("tuple с вложенным списком (1, [2, 3])", (1, [2, 3])),
        ("запись-словарь records[0]", records[0]),
    ]
    for label, obj in samples:
        try:
            s = {obj}
            print(f"  OK: {label} -> {s}")
        except TypeError as e:
            print(f"  ERR: {label} -> {type(e).__name__}: {e}")


def ex4_duplicates():
    print("\n=== Упражнение 4. Дубликаты ===")
    raw_with_dup = RAW_RECORDS + [
        {"id": "SK-101", "field": "Южное", "type": "нагнетательная",
         "status": "в простое", "debit": 10.0, "water_cut": 5.0}
    ]
    recs, errs = build_registry(raw_with_dup)
    print(f"  Входных записей: {len(raw_with_dup)}, корректных: {len(recs)}, ошибок: {len(errs)}")
    for idx, code in errs:
        print(f"    строка {idx}: {code}")


def aggregate_defaultdict(records, group_field, metric_field):
    """Агрегация через defaultdict(list)."""
    groups = defaultdict(list)
    for record in records:
        groups[record[group_field]].append(record[metric_field])
    result = {}
    for key, values in groups.items():
        total = sum(values)
        result[key] = {
            "count": len(values),
            "sum": total,
            "min": min(values),
            "max": max(values),
            "avg": total / len(values),
        }
    return result


def ex5_defaultdict(records):
    print("\n=== Упражнение 5. Агрегация через defaultdict(list) ===")
    orig = aggregate(records, "field", "debit")
    dd = aggregate_defaultdict(records, "field", "debit")
    assert orig == dd, "Результаты должны совпадать!"
    print("  Результаты aggregate и aggregate_defaultdict полностью совпадают:", dd)


def ex6_stability(records):
    print("\n=== Упражнение 6. Стабильность вывода множеств ===")
    active = ids_where(records, "status", {"в работе"})
    wet = ids_in_range(records, "water_cut", 60, 100)
    print("  Без sorted():", active)
    print("  С sorted():  ", sorted(active))
    print("  Разность с sorted():", sorted(active - wet))


def main():
    records, _ = build_registry(RAW_RECORDS)
    ex1_manual_trace(records)
    ex3_unhashable(records)
    ex4_duplicates()
    ex5_defaultdict(records)
    ex6_stability(records)


if __name__ == "__main__":
    main()
