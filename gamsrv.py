import heapq


if __name__ == '__main__':
    with open('gamsrv.in', 'r') as f:
        all_lines = f.readlines()

    n, m = map(int, all_lines[0].split())
    clients = list(map(int, all_lines[1].split()))

    graph = [[] for _ in range(n + 1)]
    for i in range(2, 2 + m):
        u, v, w = map(int, all_lines[i].split())
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

    with open('gamsrv.out', 'w') as f:
        f.write(str(best) + '\n')


