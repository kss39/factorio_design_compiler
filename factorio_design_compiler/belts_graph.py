import networkx as nx
import pandas as pd

from factorio_design_compiler.fdc_utils import bp_string_to_json


def get_position_int_x(d: dict) -> int:
    x_raw_float = d.get('x')
    x_int = int(x_raw_float * 2)
    return x_int


def get_position_int_y(d: dict) -> int:
    y_raw_float = d.get('y')
    y_int = int(y_raw_float * 2)
    return y_int


def construct_belts_df(bp_json) -> pd.DataFrame:
    entities = bp_json['blueprint']['entities']
    df = pd.DataFrame.from_dict(entities)
    df = df[df.name == 'transport-belt']
    df.drop('entity_number', axis=1, inplace=True, errors='ignore')
    df['x'] = df.position.map(get_position_int_x)
    df['y'] = df.position.map(get_position_int_y)
    df.drop('position', axis=1, inplace=True, errors='ignore')
    df['direction_we'] = ((df.direction // 2) % 2).astype(int)
    df['direction_ns'] = ((df.direction // 2 + 1) % 2).astype(int)
    df['direction_ne'] = ((df.direction // 2) < 2).astype(int)
    df['x_snap'] = df.x // 2 * 2
    df['y_snap'] = df.y // 2 * 2
    df['x_with_side'] = list(zip(df.x - df.direction_ns, df.x))
    df['x_spouse'] = list(zip(df.x, df.x - df.direction_ns))
    df['y_with_side'] = list(zip(df.y - df.direction_we, df.y))
    df['y_spouse'] = list(zip(df.y, df.y - df.direction_we))
    df = df.explode(
        column=['x_with_side', 'y_with_side', 'x_spouse', 'y_spouse'])
    df['x_with_side'] -= df.direction_we * (1 - df.direction_ne)
    df['y_with_side'] -= df.direction_ns * df.direction_ne
    df['x_spouse'] -= df.direction_we * (1 - df.direction_ne)
    df['y_spouse'] -= df.direction_ns * df.direction_ne
    df.name = df.name + '-side'
    df['x_delta'] = df.direction_we * 2 * (df.direction_ne * 2 - 1)
    df['y_delta'] = df.direction_ns * 2 * (1 - df.direction_ne * 2)
    df['direction'] //= 2
    return df


class BeltsGraph(object):
    def __init__(self, bp_string: str):
        bp_json = bp_string_to_json(bp_string)
        self.__df = construct_belts_df(bp_json)
        self.graph = self.__construct_belts_graph()

    def __construct_belts_graph(self) -> nx.DiGraph:
        belts_graph = nx.DiGraph()
        for i, row in self.__df.iterrows():
            belts_graph.add_node(
                (row.x_with_side, row.y_with_side),
                entity_pos=(row.x, row.y),
                pos=(row.x_with_side, -row.y_with_side),
                delta=(row.x_delta, row.y_delta),
                spouse=(row.x_spouse, row.y_spouse),
                direction=row.direction
            )
        for n in list(belts_graph.nodes):
            if (n[0] + n[1]) % 2:
                node = belts_graph.nodes.get(n)
                n_spouse = node['spouse']
                behind = (n[0] - node['delta'][0], n[1] - node['delta'][1])
                behind_spouse = (
                    n_spouse[0] - node['delta'][0],
                    n_spouse[1] - node['delta'][1])
                behind_node = belts_graph.nodes.get(behind)
                if behind_node:
                    belts_graph.add_edge(behind, n)
                    belts_graph.add_edge(behind_spouse, n_spouse)
                if node['direction'] == 1:
                    left_n = (n[0], min(n[1], n_spouse[1]))
                    right_n = (n[0], max(n[1], n_spouse[1]))
                    lf_n = (left_n[0], left_n[1] - 1)
                    lr_n = (left_n[0] - 1, left_n[1] - 1)
                    rf_n = (right_n[0], right_n[1] + 1)
                    rr_n = (right_n[0] - 1, right_n[1] + 1)
                elif node['direction'] == 2:
                    left_n = (max(n[0], n_spouse[0]), n[1])
                    right_n = (min(n[0], n_spouse[0]), n[1])
                    lf_n = (left_n[0] + 1, left_n[1])
                    lr_n = (left_n[0] + 1, left_n[1] - 1)
                    rf_n = (right_n[0] - 1, right_n[1])
                    rr_n = (right_n[0] - 1, right_n[1] - 1)
                elif node['direction'] == 3:
                    left_n = (n[0], max(n[1], n_spouse[1]))
                    right_n = (n[0], min(n[1], n_spouse[1]))
                    lf_n = (left_n[0], left_n[1] + 1)
                    lr_n = (left_n[0] + 1, left_n[1] + 1)
                    rf_n = (right_n[0], right_n[1] - 1)
                    rr_n = (right_n[0] - 1, right_n[1] - 1)
                else:
                    left_n = (min(n[0], n_spouse[0]), n[1])
                    right_n = (max(n[0], n_spouse[0]), n[1])
                    lf_n = (left_n[0] - 1, left_n[1])
                    lr_n = (left_n[0] - 1, left_n[1] + 1)
                    rf_n = (right_n[0] + 1, right_n[1])
                    rr_n = (right_n[0] + 1, right_n[1] + 1)
                assert (left_n == n) or (right_n == n)
                assert (left_n == n_spouse) or (right_n == n_spouse)
                watch_left, watch_right = False, False
                if lf_n in belts_graph and lr_n in belts_graph:
                    watch_left = True
                if rf_n in belts_graph and rr_n in belts_graph:
                    watch_right = True
                if behind_node or (watch_left and watch_right):
                    if watch_left:
                        belts_graph.add_edge(lf_n, left_n)
                        belts_graph.add_edge(lr_n, left_n)
                    if watch_right:
                        belts_graph.add_edge(rf_n, right_n)
                        belts_graph.add_edge(rr_n, right_n)
                elif watch_left:
                    belts_graph.add_edge(lf_n, left_n)
                    belts_graph.add_edge(lr_n, right_n)
                elif watch_right:
                    belts_graph.add_edge(rf_n, right_n)
                    belts_graph.add_edge(rr_n, left_n)
        return belts_graph
