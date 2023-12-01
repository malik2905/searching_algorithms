import GUI


class Node:
    def __init__(self, state, parent=None, steps=0, end=None):
        self.state = state
        self.parent = parent
        self.steps = steps
        self.manhattan_distance = GUI.get_manhattan_distance(end, state)
        self.a_star = GUI.get_a_star_distance(steps, state, end)

    def __eq__(self, node):
        return self.state == node.state and self.parent == node.parent


class DFS():
    def __init__(self):
        self.stack = []

    def add(self, node):
        self.stack.append(node)

    def empty(self):
        return not bool(self.stack)

    def get_next_node(self):
        try:
            node = self.stack.pop()
        except IndexError:
            raise Exception('Stack is empty!')
        return node
        

class BFS():
    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append(node)

    def empty(self):
        return not bool(self.queue)

    def get_next_node(self):
        try:
            node = self.queue.pop(0)
        except IndexError:
            raise Exception('Queue is empty!')
        return node


class GBFS():
    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append((node, node.manhattan_distance))

    def empty(self):
        return not bool(self.queue)

    def get_next_node(self):
        for i in range(13 * 11):
            for j in range(len(self.queue)):
                if self.queue[j][1] == i:
                    try:
                        node, _ = self.queue.pop(j)
                    except IndexError:
                        raise Exception('Queue is empty!')
                    return node


class A_STAR():
    def __init__(self):
        self.queue = []
        self.start = 0

    def add(self, node):
        self.queue.append(node)

    def empty(self):
        return not bool(self.queue)

    def get_next_node(self):
        for i in range(13 * 11):
            for j, val in enumerate(self.queue):
                if val.a_star == i:
                    try:
                        node = self.queue.pop(j)
                    except IndexError:
                        raise Exception('Queue is empty!')
                    return node