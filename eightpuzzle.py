import collections
import time

class Board:
    """
    A class representing a 3*3 '8-puzzle'.
    - 'position' is a string containing the numbers 0..9
       e.g. 123406758
    """
    def __init__(self, position):
        self.width = 3
        self.position = position

    @property
    def solved(self):

        return self.position == '012345678'

    @property
    def legalactions(self):
        """
        Return a list of (position, move) pairs,
        representing the legal actions possible given a current position
        """

        def swap(str, at, to):
            seq = list(str)
            seq[at], seq[to] = seq[to], seq[at]
            return ''.join(seq)

        moves = []

        """locate the 0"""
        i = self.position.find('0')

        """move right"""
        to = i + 1
        if to % self.width <> 0:
            moves.append((swap(self.position, i, to), 'Right'))
        """move left"""
        if i % self.width <> 0:
            to = i - 1
            moves.append((swap(self.position, i, to), 'Left'))
        """move down"""
        to = i + self.width
        if to <= (self.width*self.width - 1):
            moves.append((swap(self.position, i, to), 'Down'))
        """move up"""
        to = i - self.width
        if to >= 0:
            moves.append((swap(self.position, i, to), 'Up'))

        return moves

class Node:
    """
    A class representing a Node in the search graph produced by the Solver
    - 'board' is a Board object, which is used to offload the intrinsic n-puzzle logic
    - 'parent' is the preceding node, if any
    - 'action' is the action taken to produce this node, if any
    """
    def __init__(self, position, parent=None, action=None):
        self._board = Board(position)
        self.parent = parent
        self.action = action
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    @property
    def state(self):

        return self._board.position

    @property
    def solved(self):
        """ Wrapper to check if the board is solved """
        return self._board.solved

    def calculatepath(self):
        """
        Reconstruct a path from self to the root 'parent'
        """
        node, p = self, []
        while node:
            if node.action:
                p.append(node.action)
            node = node.parent
        return p

    def expand(self):

        children = []

        for position, move in self._board.legalactions:
            children.append(Node(position, self, move))

        return children

    def __hash__(self):

        return self._board

class Solver:
    """
    An '8-puzzle' solver
    - 'startPosition' is a array of numbers 0..9 in any order
    """
    def __init__(self, startposition):

        """Convert startPosition to a String"""
        self.startposition = "".join(str(s) for s in startposition)


    def bfs(self):
        """
        Perform breadth first search and return a path
        to the solution, if it exists
        Node is a wrapper class around the more physical Board,
        representing a node in the graph that is built while
        doing the search
        """
        print("---------- Performing Breadth First Search ------------")
        before = time.time()

        root = Node(self.startposition)
        frontier = collections.deque([root])
        """using a set with state only increases speed dramatically"""
        frontier_hash = {root.state}

        explored = set()
        max_depth = 0

        while frontier:
            node = frontier.popleft()
            explored.add(node.state)
            max_depth = max(max_depth, node.depth)

            if node.solved:
                path = node.calculatepath()
                return {'path_to_goal': path[::-1],
                        'cost_of_path': len(path),
                        'nodes_expanded': len(explored)-1,
                        'search_depth': node.depth,
                        'max_search_depth': max_depth,
                        'fringe_size': len(frontier),
                        'running_time': time.time() - before}

            for child in node.expand():

                if child.state not in frontier_hash and child.state not in explored:
                    frontier.append(child)
                    frontier_hash.add(child.state)

        return false

    def dfs(self):
        """
        Perform depth first search and return a dict with some stats
        and a path to the solution, if it exists
        Node is a wrapper class around the more physical Board,
        representing a node in the graph that is built while
        doing the search
        """
        print("---------- Performing Depth First Search ------------")
        before = time.time()

        root = Node(self.startposition)
        frontier = [root]
        """using a set with state only increases speed dramatically"""
        frontier_hash = {root.state}

        explored = set()
        max_depth = 0

        while frontier:
            node = frontier.pop()
            explored.add(node.state)
            max_depth = max(max_depth, node.depth)

            if node.solved:
                path = node.calculatepath()
                return {'path_to_goal': path[::-1],
                        'cost_of_path': len(path),
                        'nodes_expanded': len(explored)-1,
                        'search_depth': node.depth,
                        'max_search_depth': max_depth,
                        'fringe_size': len(frontier),
                        'running_time': time.time() - before}

            for child in node.expand():

                if child.state not in frontier_hash and child.state not in explored:
                    frontier.append(child)
                    frontier_hash.add(child.state)

        return false

"""position = [6,1,8,4,0,2,7,3,5]"""
position = [8,6,4,2,1,3,5,7,0]

s = Solver(position)
p = s.bfs()

for key in p:
    print(key + ': ' + str(p[key]))

p = s.dfs()

for key in p:
    print(key + ': ' + str(p[key]))