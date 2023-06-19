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
            if row.direction == 0:
                front, left, right, back = south, east, west, north
            elif row.direction == 2:
                front, left, right, back = west, south, north, east
            elif row.direction == 4:
                front, left, right, back = north, west, east, south
            elif row.direction == 6:
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
        print(g)
        for src, row in self.belts_df.iterrows():
            dest = None
            if row.direction == 0:
                dest = f'{row.x},{row.y + 1}'
            elif row.direction == 2:
                dest = f'{row.x - 1},{row.y}'
            elif row.direction == 4:
                dest = f'{row.x},{row.y - 1}'
            elif row.direction == 6:
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

    @property
    def bps(self):
        return self._bps
