"""Генератор графика сложности для Упражнения 7 (ЛР № 7)."""
import json
import matplotlib.pyplot as plt


def main():
    with open("benchmark_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    ns = [row["n"] for row in data]
    scan_ms = [row["scan_avg_ms"] for row in data]
    index_ms = [row["index_avg_ms"] for row in data]
    build_ms = [row["build_avg_ms"] for row in data]
    speedups = [row["speedup"] for row in data]

    plt.rcParams.update({
        "font.size": 10,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    fig.suptitle(
        "Сравнение скорости поиска по списку O(N) и по словарю-индексу O(1) (1000 запросов)",
        fontsize=12, fontweight="bold", y=0.98
    )

    # Левый график: линейная шкала (Упражнение 7)
    ax1.plot(ns, scan_ms, marker="o", linewidth=2.2, color="#D9480F", label="Перебор списка — O(N)")
    ax1.plot(ns, index_ms, marker="s", linewidth=2.2, color="#1C7ED6", label="Словарь-индекс — O(1)")
    ax1.plot(ns, build_ms, marker="^", linewidth=1.6, linestyle=":", color="#2B8A3E", label="Построение индекса — O(N)")
    for x, y, sp in zip(ns, scan_ms, speedups):
        ax1.annotate(f"{y:.1f} мс\n({sp:.0f}x)", (x, y),
                     textcoords="offset points", xytext=(-6, 8),
                     ha="center", fontsize=8.5, color="#D9480F")
    ax1.set_title("Линейная шкала (N vs время, мс)")
    ax1.set_xlabel("Размер реестра N (записей)")
    ax1.set_ylabel("Время выполнения, мс")
    ax1.set_ylim(-50, max(scan_ms) * 1.18)
    ax1.legend(loc="upper left", frameon=True)

    # Правый график: логарифмическая шкала (log-log)
    ax2.loglog(ns, scan_ms, marker="o", linewidth=2.2, color="#D9480F", label="Перебор списка — O(N)")
    ax2.loglog(ns, index_ms, marker="s", linewidth=2.2, color="#1C7ED6", label="Словарь-индекс — O(1)")
    ax2.loglog(ns, build_ms, marker="^", linewidth=1.6, linestyle=":", color="#2B8A3E", label="Построение индекса — O(N)")
    for x, y in zip(ns, index_ms):
        ax2.annotate(f"{y:.3f}", (x, y), textcoords="offset points", xytext=(0, -13),
                     ha="center", fontsize=8, color="#1C7ED6")
    ax2.set_title("Логарифмическая шкала (log-log)")
    ax2.set_xlabel("Размер реестра N (записей)")
    ax2.set_ylabel("Время выполнения, мс (log)")
    ax2.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    plt.savefig("plot_complexity.png", dpi=180)
    print("Saved plot_complexity.png")


if __name__ == "__main__":
    main()
