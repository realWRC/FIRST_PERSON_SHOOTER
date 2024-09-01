from collections import deque
from functools import lru_cache


class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.map
        self.routes = [
                [-1, 0], [0, -1], [1, 0], [0, 1],
                [-1, -1], [1, -1], [1, 1], [-1, 1]
        ]
        self.graph = {}
        self.constructGraph()

    def constructGraph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), [])\
                            + self.getNextTile(x, y)

    def getNextTile(self, x, y):
        nextTilesList = []
        for dx, dy in self.routes:
            nextPosition = (x + dx, y + dy)
            if nextPosition not in self.game.map.gameWorld:
                nextTilesList.append(nextPosition)
        return nextTilesList

    def breadFirstSearch(self, start, goal, graph):
        queue = deque([start])
        visitedTiles = {start: None}
        while queue:
            currentTile = queue.popleft()
            if currentTile == goal:
                break
            nextTiles = graph[currentTile]
            for nextTile in nextTiles:
                if nextTile not in visitedTiles and nextTile not in \
                        self.game.spriteManager.enemyPositions:
                    queue.append(nextTile)
                    visitedTiles[nextTile] = currentTile
        return visitedTiles

    @lru_cache
    def getRoute(self, start, goal):
        self.visited = self.breadFirstSearch(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]
