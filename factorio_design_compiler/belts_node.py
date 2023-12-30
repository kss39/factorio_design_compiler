from abc import ABC, abstractmethod
from typing import Iterable, Tuple

from networkx import DiGraph


class BeltNode(ABC):
    def __init__(self, position: Tuple[int, int], direction: int,
                 node_graph: DiGraph):
        self.position_raw = position
        self.direction_raw = direction
        self.__graph = node_graph
        self.__node_list = ()

    @abstractmethod
    def process_upstream_belts(self):
        pass

    @property
    def node_list(self) -> Iterable[Tuple[int, int]]:
        return self.__node_list

    def __add_self_to_graph(self) -> None:
        for node_to_add in self.node_list:
            self.__graph.add_node(
                node_to_add,
                ref_to_beltnode=self
            )


class L1Belt(BeltNode):
    def __init__(self, position: Tuple[int, int], direction: int,
                 node_graph: DiGraph):
        super().__init__(position, direction, node_graph)
        pos_x = int(position[0] * 2)
        pos_y = int(position[1] * 2)
        if direction == 0:  # North
            self.__node_list = ((pos_x - 1, pos_y - 1), (pos_x, pos_y - 1))
            self.__behind = ((pos_x-1, pos_y+1), (pos_x, pos_y+1))
            self.__left_front = (pos_x-2, pos_y-1)
            self.__left_rear = (pos_x-2, pos_y)
            self.__right_front = (pos_x+1, pos_y-1)
            self.__right_rear = (pos_x+1, pos_y)
        elif direction == 2:  # East
            self.__node_list = ((pos_x, pos_y), (pos_x, pos_y - 1))
            self.__behind = ((pos_x-2, pos_y), (pos_x-2, pos_y-1))
            self.__left_front = (pos_x, pos_y-2)
            self.__left_rear = (pos_x-1, pos_y-2)
            self.__right_front = (pos_x, pos_y+1)
            self.__right_rear = (pos_x-1, pos_y+1)
        elif direction == 4:  # South
            self.__node_list = ((pos_x, pos_y), (pos_x - 1, pos_y))
            self.__behind = ((pos_x, pos_y-2), (pos_x-1, pos_y-2))
            self.__left_front = (pos_x+1, pos_y)
            self.__left_rear = (pos_x+1, pos_y-1)
            self.__right_front = (pos_x-1, pos_y)
            self.__right_rear = (pos_x-1, pos_y-1)
        elif direction == 6:  # West
            self.__node_list = ((pos_x - 1, pos_y), (pos_x - 1, pos_y - 1))
            self.__behind = ((pos_x+1, pos_y), (pos_x+1, pos_y-1))
            self.__left_front = (pos_x-1, pos_y+1)
            self.__left_rear = (pos_x, pos_y+1)
            self.__right_front = (pos_x-1, pos_y-1)
            self.__right_rear = (pos_x, pos_y-1)
        else:
            raise BeltException(f'Unknown belt direction: {direction}')
        self.__add_self_to_graph()

    def process_upstream_belts(self):
        raise NotImplementedError


class BeltException(Exception):
    pass
