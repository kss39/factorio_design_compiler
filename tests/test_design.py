import unittest
import matplotlib.pyplot as plt
import networkx as nx

from factorio_design_compiler.design import FactorioDesignBlock

class MyTestCase(unittest.TestCase):
    def test_something(self):
        s_test = '0eNqd1NFugyAUBuB3Ode0KSCovMqyNNqeLCSKBugyY3j3Yk2WLcNMucTgx58fPTO03QNHq40HNYO+DcaBepvB6Q/TdMszP40ICrTHHgiYpl9W3jbGjYP1pxY7D4GANnf8AkXDOwE0XnuNq/RaTFfz6Fu0ccOWQWAcXHxtMMupkTrRujgLAhMozvlZxEPu2uJt3cIC+WOzIzbftouEzY/YbNuWCbvI60Ts6UTk5RZ7csu8vhc7oZVHNPmtlWmtytNkWquPaOJXtn9bpJe8Gss9ny2lefe/LznLK7lKl0x5XhHVrqxFXhEJPE641zRUP4YngU+0bv0LK1qUNStlzS4VZyE8AQIdvXU='
        fdb = FactorioDesignBlock(s_test).belts_graph.generate_graph()



if __name__ == '__main__':
    unittest.main()
