import heapq
import unittest


def solve(n, clients, edges):
    graph = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    client_set = set(clients)
    best = float('inf')

    for server in range(1, n + 1):
        if server in client_set:
            continue

        dist = [float('inf')] * (n + 1)
        dist[server] = 0
        pq = [(0, server)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))

        max_delay = max(dist[c] for c in clients)
        best = min(best, max_delay)

    return best


class TestGamsrv(unittest.TestCase):

    def test_example_1(self):
        edges = [(1, 3, 10), (3, 4, 80), (4, 5, 50), (5, 6, 20),
                 (2, 3, 40), (2, 4, 100)]
        result = solve(6, [1, 2, 6], edges)
        print(f'\ntest_example_1: result={result}, expected=100')
        self.assertEqual(result, 100)

    def test_example_2(self):
        edges = [(1, 2, 20), (2, 3, 20), (3, 6, 20), (6, 9, 20),
                 (9, 8, 20), (8, 7, 20), (7, 4, 20), (4, 1, 20),
                 (5, 2, 10), (5, 4, 10), (5, 6, 10), (5, 8, 10)]
        result = solve(9, [2, 4, 6], edges)
        print(f'\ntest_example_2: result={result}, expected=10')
        self.assertEqual(result, 10)

    def test_example_3(self):
        edges = [(1, 2, 50), (2, 3, 1000000000)]
        result = solve(3, [1, 3], edges)
        print(f'\ntest_example_3: result={result}, expected=1000000000')
        self.assertEqual(result, 1000000000)

    def test_server_between_two_clients(self):
        edges = [(1, 2, 10), (2, 3, 10)]
        result = solve(3, [1, 3], edges)
        print(f'\ntest_server_between_two_clients: result={result}, expected=10')
        self.assertEqual(result, 10)

    def test_server_closer_to_one_client(self):
        edges = [(1, 2, 1), (2, 3, 100)]
        result = solve(3, [1, 3], edges)
        print(f'\ntest_server_closer_to_one_client: result={result}, expected=100')
        self.assertEqual(result, 100)

    def test_multiple_paths(self):
        edges = [(1, 3, 5), (1, 2, 100), (2, 3, 1)]
        result = solve(3, [1, 2], edges)
        print(f'\ntest_multiple_paths: result={result}, expected=5')
        self.assertEqual(result, 5)

    def test_single_router(self):
        edges = [(1, 2, 30), (2, 3, 70)]
        result = solve(3, [1, 3], edges)
        print(f'\ntest_single_router: result={result}, expected=70')
        self.assertEqual(result, 70)


if __name__ == '__main__':
    unittest.main()