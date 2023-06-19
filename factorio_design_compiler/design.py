"""
Parsing layout data into block information and metadata.
"""
import networkx as nx
import pandas as pd

from factorio_design_compiler.fdc_utils import bp_string_to_json


class BeltsGraph:
    def __init__(self, df: pd.DataFrame):
        self._belts_df = df.copy()
        self.graph = self.generate_graph()

    @property
    def belts_df(self):
        return self._belts_df

    def generate_graph(self):
        g = nx.DiGraph()
        dest_graph = self._destination_graph()
        for ind, row in self.belts_df.iterrows():
            north = f'{row.x},{row.y-1}'
            south = f'{row.x},{row.y+1}'
            west = f'{row.x-1},{row.y}'
            east = f'{row.x+1},{row.y}'
            if row.direction == 4:
                front, left, right, back = south, east, west, north
            elif row.direction == 6:
                front, left, right, back = west, south, north, east
            elif row.direction == 0:
                front, left, right, back = north, west, east, south
            elif row.direction == 2:
                front, left, right, back = east, north, south, west
            else:
                assert False, 'invalid direction'
            g.add_node(f'{ind},left', front=front, left=left, right=right, back=back)
            g.add_node(f'{ind},right', front=front, left=left, right=right, back=back)
        for ind, row in self.belts_df.iterrows():
            node = g.nodes[f'{ind},left']
            back = node['back']
            left = node['left']
            right = node['right']
            if (back, ind) in dest_graph.edges or \
                ((left, ind) in dest_graph.edges and
                 (right, ind) in dest_graph.edges):
                g.add_edge(f'{back},left', f'{ind},left')
                g.add_edge(f'{back},right', f'{ind},right')
                if (left, ind) in dest_graph.edges:
                    g.add_edge(f'{left},left', f'{ind},left')
                    g.add_edge(f'{left},right', f'{ind},left')
                if (right, ind) in dest_graph.edges:
                    g.add_edge(f'{right},left', f'{ind},right')
                    g.add_edge(f'{right},right', f'{ind},right')
            elif (left, ind) in dest_graph.edges:
                g.add_edge(f'{left},left', f'{ind},left')
                g.add_edge(f'{left},right', f'{ind},right')
            elif (right, ind) in dest_graph.edges:
                g.add_edge(f'{right},left', f'{ind},left')
                g.add_edge(f'{right},right', f'{ind},right')
        return g

    def _destination_graph(self):
        g = nx.DiGraph()
        for ind, row in self.belts_df.iterrows():
            g.add_node(ind, x=row.x, y=row.y)
        for src, row in self.belts_df.iterrows():
            dest = None
            if row.direction == 4:
                dest = f'{row.x},{row.y + 1}'
            elif row.direction == 6:
                dest = f'{row.x - 1},{row.y}'
            elif row.direction == 0:
                dest = f'{row.x},{row.y - 1}'
            elif row.direction == 2:
                dest = f'{row.x + 1},{row.y}'
            else:
                assert False
            if dest in g:
                g.add_edge(src, dest)
        return g


class FactorioDesignBlock:
    def __init__(self, blueprint_string: str):
        self._bps = blueprint_string
        self._json_obj = bp_string_to_json(self._bps)
        self._belts_df = self._generate_belts_df()
        self._belts_graph = BeltsGraph(self._belts_df)

    @property
    def bps(self):
        return self._bps

    @property
    def belts_graph(self) -> BeltsGraph:
        return self._belts_graph

    def _generate_belts_df(self):
        df = pd.DataFrame(self._json_obj['blueprint']['entities'])
        df.direction.fillna(0, inplace=True)
        df.direction = df.direction.astype(int)
        df['x'] = df.position.map(lambda p: p['x'])
        df['y'] = df.position.map(lambda p: p['y'])
        print(df)
        df.x -= df.x.min()
        df.y -= df.y.min()
        df['x'] = df.x.astype(int)
        df['y'] = df.y.astype(int)
        df.set_index(df.entity_number, inplace=True)
        df.drop(columns=['entity_number', 'position'], inplace=True)
        belts = df[df.name == 'transport-belt']
        belts.set_index(belts.x.astype(str) + ',' + belts.y.astype(str),
                        inplace=True)
        return belts
