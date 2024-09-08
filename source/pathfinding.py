from collections import deque
from functools import lru_cache


class PathFinding:
    """
    The PathFinding class implements a pathfinding algorithm using
    a graph representation of the game map. It allows enemies to
    calculate the optimal route to a target (e.g., the player) by
    avoiding obstacles and walls.

    Core Attributes:
        game (Game): A reference to the main game instance.
        map (list): A 2D grid representing the game map layout.
        routes (list): Possible directions for movement, including
                       diagonals.
        graph (dict): Graph representation of the map where nodes
                      are tiles, and edges represent possible
                      movement directions.
    """

    def __init__(self, game):
        """
        Initializes the PathFinding class by constructing a graph
        based on the game map layout and available routes for
        movement.
        """
        self.game = game
        self.map = game.map.map
        self.routes = [
                [-1, 0], [0, -1], [1, 0], [0, 1],
                [-1, -1], [1, -1], [1, 1], [-1, 1]
        ]
        self.graph = {}
        self.constructGraph()

    def constructGraph(self):
        """
        Constructs a graph representation of the game map where each
        walkable tile is a node, and edges connect adjacent,
        accessible tiles.
        """
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), [])\
                            + self.getNextTile(x, y)

    def getNextTile(self, x, y):
        """
        Identifies and returns the valid adjacent tiles for a given
        position (x, y).
        """
        nextTilesList = []
        for dx, dy in self.routes:
            nextPosition = (x + dx, y + dy)
            if nextPosition not in self.game.map.gameWorld:
                nextTilesList.append(nextPosition)
        return nextTilesList

    def breadFirstSearch(self, start, goal, graph):
        """
        Implements a breadth-first search algorithm to find the
        shortest path from the start position to the goal within
        the given graph.
        """
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
        """
        Computes and returns the next position in the optimal path from
        the start to the goal using the results of the breadth-first
        search algorithm.
        """
        self.visited = self.breadFirstSearch(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]
