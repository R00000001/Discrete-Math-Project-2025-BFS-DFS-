import random
import time
import multiprocessing as mp
from tqdm import tqdm
import csv
from collections import deque

# -------------------------------
# Клас графа із представленням у вигляді матриці суміжності
# -------------------------------
class Graph:
    def __init__(self, n):
        self.n = n
        self.adj_matrix = [[0] * n for _ in range(n)]  # Ініціалізація n x n матриці

    def add_edge(self, u, v):
        # Додає неорієнтоване ребро між вершинами u та v
        if u != v:
            self.adj_matrix[u][v] = 1
            self.adj_matrix[v][u] = 1

    def to_adj_list(self):
        # Перетворює матрицю суміжності у список суміжності
        adj_list = {i: [] for i in range(self.n)}
        for i in range(self.n):
            for j in range(self.n):
                if self.adj_matrix[i][j]:
                    adj_list[i].append(j)
        return adj_list

# -------------------------------
# Функція генерації випадкового графа
# -------------------------------
def generate_random_graph(n, density):
    graph = Graph(n)
    max_edges = n * (n - 1) // 2  # Максимальна кількість ребер у неорієнтованому графі
    target_edges = int(max_edges * (density / 100))  # Цільова кількість ребер залежно від щільності
    edges = set()

    while len(edges) < target_edges:
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            edge = tuple(sorted((u, v)))  # Сортуємо, щоб уникнути дублювань (u, v) і (v, u)
            if edge not in edges:
                edges.add(edge)
                graph.add_edge(*edge)

    return graph

# -------------------------------
# Робітник для BFS (паралельне виконання)
# -------------------------------
def bfs(args):
    graph_data, start, rep_type = args
    n = len(graph_data) if rep_type == "matrix" else len(graph_data)
    visited = [False] * n
    queue = deque([start])
    visited[start] = True

    while queue:
        node = queue.popleft()
        # Визначаємо сусідів залежно від представлення графа
        neighbors = (
            graph_data[node]
            if rep_type == "list"
            else [i for i, connected in enumerate(graph_data[node]) if connected]
        )
        for neighbor in neighbors:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    return visited

# -------------------------------
# Робітник для DFS (паралельне виконання)
# -------------------------------
def dfs(args):
    graph_data, start, rep_type = args
    n = len(graph_data) if rep_type == "matrix" else len(graph_data)
    visited = [False] * n

    def explore(node):
        visited[node] = True
        neighbors = (
            graph_data[node]
            if rep_type == "list"
            else [i for i, connected in enumerate(graph_data[node]) if connected]
        )
        for neighbor in neighbors:
            if not visited[neighbor]:
                explore(neighbor)

    explore(start)
    return visited

# -------------------------------
# Обчислення матриці досяжності з використанням BFS або DFS
# -------------------------------
def compute_reachability(graph, method="BFS", rep_type="matrix", show_progress=True):
    n = graph.n
    graph_data = graph.adj_matrix if rep_type == "matrix" else graph.to_adj_list()
    worker = bfs if method.upper() == "BFS" else dfs
    tasks = [(graph_data, i, rep_type) for i in range(n)]
    results = []

    # Використання пулу процесів для паралельної обробки
    with mp.Pool(processes=mp.cpu_count()) as pool:
        iterator = pool.imap(worker, tasks)
        if show_progress:
            iterator = tqdm(iterator, total=n, desc=f"{method} ({rep_type})")
        results.extend(iterator)

    return results

# -------------------------------
# Проведення одного експерименту для заданих параметрів
# -------------------------------
def run_experiment(n, density, method, rep_type, iterations, progress_bar):
    total_time = 0
    for _ in range(iterations):
        graph = generate_random_graph(n, density)
        start = time.perf_counter()
        compute_reachability(graph, method=method, rep_type=rep_type, show_progress=False)
        total_time += time.perf_counter() - start
        progress_bar.update(1)
    return total_time / iterations  # Повертаємо середній час виконання

# -------------------------------
# Запуск повного набору експериментів для всіх параметрів
# -------------------------------
def run_all_experiments():
    results = []
    node_counts = [20, 50, 80, 110, 140, 170, 200]  # Розміри графів
    densities = [15, 35, 55, 75, 95]  # Щільності графів
    methods = ["BFS", "DFS"]  # Метод обходу
    representations = ["matrix", "list"]  # Представлення графа
    iterations = 100  # Кількість повторень для кожного експерименту

    total_jobs = len(node_counts) * len(densities) * len(methods) * len(representations) * iterations

    # Прогрес-бар для відслідковування загального прогресу
    with tqdm(total=total_jobs, desc="Загальний прогрес", unit="граф", dynamic_ncols=True) as pbar:
        for n in node_counts:
            for density in densities:
                for method in methods:
                    for rep in representations:
                        avg_time = run_experiment(n, density, method, rep, iterations, pbar)
                        results.append({
                            "method": method,
                            "representation": rep,
                            "nodes": n,
                            "density": density,
                            "average_time_sec": avg_time
                        })

    return results

# -------------------------------
# Збереження результатів у TSV-файл
# -------------------------------
def save_results(results, filename="results.tsv"):
    if not results:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(results)

# -------------------------------
# Точка входу в програму
# -------------------------------
def main():
    print("Запуск експериментів...")
    results = run_all_experiments()
    print("Експерименти завершено. Збереження результатів...")
    save_results(results)
    print("Результати збережено у файл results.tsv")

if __name__ == "__main__":
    main()
