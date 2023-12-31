from abc import ABC, abstractmethod
from typing import Iterable, Tuple

from networkx import DiGraph


class BeltNode(ABC):
    def __init__(self, position: Tuple[int, int], direction: int,
                 node_graph: DiGraph):
        self.position_raw = position
        self.direction_raw = direction
        self.__graph = node_graph
        self.node_list: Iterable[Tuple[int, int]] = ()
        self.processed: bool = False

    @abstractmethod
    def process_upstream_belts(self):
        pass

    @property
    def graph(self) -> DiGraph:
        return self.__graph

    def add_self_to_graph(self) -> None:
        for node_to_add in self.node_list:
            self.__graph.add_node(
                node_to_add,
                ref_to_beltnode=self,
                pos=(node_to_add[0], -node_to_add[1])
            )


class L1Belt(BeltNode):
    def __init__(self, position: Tuple[int, int], direction: int,
                 node_graph: DiGraph):
        super().__init__(position, direction, node_graph)
        pos_x = int(position[0] * 2)
        pos_y = int(position[1] * 2)
        if direction == 0:  # North
            self.__left = (pos_x-1, pos_y-1)
            self.__right = (pos_x, pos_y-1)
            self.__behind_left = (pos_x-1, pos_y+1)
            self.__behind_right = (pos_x, pos_y+1)
            self.__left_front = (pos_x-2, pos_y-1)
            self.__left_rear = (pos_x-2, pos_y)
            self.__right_front = (pos_x+1, pos_y-1)
            self.__right_rear = (pos_x+1, pos_y)
        elif direction == 2:  # East
            self.__left = (pos_x, pos_y-1)
            self.__right = (pos_x, pos_y)
            self.__behind_left = (pos_x-2, pos_y-1)
            self.__behind_right = (pos_x-2, pos_y)
            self.__left_front = (pos_x, pos_y-2)
            self.__left_rear = (pos_x-1, pos_y-2)
            self.__right_front = (pos_x, pos_y+1)
            self.__right_rear = (pos_x-1, pos_y+1)
        elif direction == 4:  # South
            self.__left = (pos_x, pos_y)
            self.__right = (pos_x-1, pos_y)
            self.__behind_left = (pos_x, pos_y-2)
            self.__behind_right = (pos_x-1, pos_y-2)
            self.__left_front = (pos_x+1, pos_y)
            self.__left_rear = (pos_x+1, pos_y-1)
            self.__right_front = (pos_x-2, pos_y)
            self.__right_rear = (pos_x-2, pos_y-1)
        elif direction == 6:  # West
            self.__left = (pos_x-1, pos_y)
            self.__right = (pos_x-1, pos_y-1)
            self.__behind_left = (pos_x+1, pos_y)
            self.__behind_right = (pos_x+1, pos_y-1)
            self.__left_front = (pos_x-1, pos_y+1)
            self.__left_rear = (pos_x, pos_y+1)
            self.__right_front = (pos_x-1, pos_y-1)
            self.__right_rear = (pos_x, pos_y-1)
        else:
            raise BeltException(f'Unknown belt direction: {direction}')
        self.node_list = (self.__left, self.__right)
        self.add_self_to_graph()

    def process_upstream_belts(self):
        # TODO: Be careful of other belt types, such as underground-belts
        watch_behind = False
        if self.__behind_left in self.graph and \
                self.__behind_right in self.graph:
            self.graph.add_edge(self.__behind_left, self.__left)
            self.graph.add_edge(self.__behind_right, self.__right)
            watch_behind = True
        watch_left, watch_right = False, False
        if self.__left_front in self.graph and self.__left_rear in self.graph:
            watch_left = True
        if self.__right_front in self.graph and self.__right_rear in self.graph:
            watch_right = True
        if watch_behind or (watch_left and watch_right):
            if watch_left:
                self.graph.add_edge(self.__left_front, self.__left)
                self.graph.add_edge(self.__left_rear, self.__left)
            if watch_right:
                self.graph.add_edge(self.__right_front, self.__right)
                self.graph.add_edge(self.__right_rear, self.__right)
        elif watch_left:
            self.graph.add_edge(self.__left_front, self.__left)
            self.graph.add_edge(self.__left_rear, self.__right)
        elif watch_right:
            self.graph.add_edge(self.__right_front, self.__right)
            self.graph.add_edge(self.__right_rear, self.__left)
        self.processed = True


class BeltException(Exception):
    pass
