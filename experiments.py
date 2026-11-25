"""Эксперименты варианта Б: хешируемость, Counter, пара ключей, индекс."""
import json
from collections import Counter, defaultdict
from random import Random
from time import perf_counter

from main import RAW_RECORDS, build_registry


def make_rows(n, rng):
    return [{"id": f"SK-{i:06d}", "debit": rng.random() * 100} for i in range(n)]


def find_by_scan(rows, target):
    for row in rows:
        if row["id"] == target:
            return row
    return None


def measure_trials(lookup, queries, passes=1, repeats=3):
    """Возвращает список времён каждого повтора (в миллисекундах) за один проход по queries."""
    times = []
    for _ in range(repeats):
        start = perf_counter()
        for _ in range(passes):
            for target in queries:
                lookup(target)
        elapsed_ms = ((perf_counter() - start) / passes) * 1000
        times.append(elapsed_ms)
    return times


def measure_index_build(rows, repeats=3):
    """Измеряет время построения словаря-индекса (в миллисекундах)."""
    times = []
    for _ in range(repeats):
        start = perf_counter()
        _ = {row["id"]: row for row in rows}
        times.append((perf_counter() - start) * 1000)
    return times


def main():
    records, _ = build_registry(RAW_RECORDS)

    # 1. Почему запись нельзя положить в множество
    try:
        unique_records = {records[0]}
    except TypeError as error:
        print("1) set(запись) ->", type(error).__name__ + ":", error)

    # 2. Обходные пути: кортеж пар и frozenset
    variants = {
        "tuple(items)": {tuple(r.items()) for r in records},
        "frozenset(items)": {frozenset(r.items()) for r in records},
    }
    for name, values in variants.items():
        print(f"2) {name}: уникальных записей {len(values)}")

    # 3. Counter и defaultdict вместо ручного подсчёта
    by_field = Counter(r["field"] for r in records)
    print("3) Counter:", dict(sorted(by_field.items())))

    groups = defaultdict(list)
    for record in records:
        groups[record["status"]].append(record["id"])
    print("   defaultdict:", {k: sorted(v) for k, v in sorted(groups.items())})

    # 4. Группировка по паре ключей и инвариант суммы
    pairs = defaultdict(float)
    for record in records:
        pairs[(record["field"], record["status"])] += record["debit"]
    print("4) сумма по парам (месторождение, статус):")
    for key in sorted(pairs):
        print(f"   {key[0]:<10} {key[1]:<14} {pairs[key]:>7.1f}")
    print("   сумма по парам:", round(sum(pairs.values()), 1),
          "| общая сумма:", round(sum(r["debit"] for r in records), 1))

    # 5. Индекс-словарь против перебора списка
    rng = Random(42)
    print("5) N; list_scan_1000_ms; dict_index_1000_ms; speedup; build_index_ms")
    benchmark_data = []

    for n in (100, 1000, 10000, 100000):
        rows = make_rows(n, rng)
        build_times = measure_index_build(rows, repeats=3)
        index = {row["id"]: row for row in rows}
        queries = [rows[rng.randrange(n)]["id"] for _ in range(1000)]

        scan_times = measure_trials(
            lambda target: find_by_scan(rows, target), queries, passes=1, repeats=3
        )
        index_times = measure_trials(
            lambda target: index[target], queries, passes=50, repeats=3
        )

        scan_avg = sum(scan_times) / len(scan_times)
        index_avg = sum(index_times) / len(index_times)
        build_avg = sum(build_times) / len(build_times)
        speedup = scan_avg / index_avg

        print(
            f"   {n}; {scan_avg:.2f} (min={min(scan_times):.2f}, max={max(scan_times):.2f}); "
            f"{index_avg:.3f} (min={min(index_times):.3f}, max={max(index_times):.3f}); "
            f"{speedup:.0f}x; {build_avg:.3f} (min={min(build_times):.3f}, max={max(build_times):.3f})"
        )

        benchmark_data.append({
            "n": n,
            "scan_times_ms": scan_times,
            "scan_avg_ms": scan_avg,
            "scan_min_ms": min(scan_times),
            "scan_max_ms": max(scan_times),
            "index_times_ms": index_times,
            "index_avg_ms": index_avg,
            "index_min_ms": min(index_times),
            "index_max_ms": max(index_times),
            "build_times_ms": build_times,
            "build_avg_ms": build_avg,
            "build_min_ms": min(build_times),
            "build_max_ms": max(build_times),
            "speedup": speedup,
        })

    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
