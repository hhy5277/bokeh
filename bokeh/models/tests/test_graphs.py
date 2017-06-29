import networkx as nx
import numpy as np

from bokeh.models.graphs import GraphDataSource, StaticLayoutProvider
from bokeh.models.sources import ColumnDataSource

def test_staticlayoutprovider_init_props():
    provider = StaticLayoutProvider()
    assert provider.graph_layout == {}

def test_graphdatasource_init_props():
    source = GraphDataSource()
    assert source.nodes.data == dict(index=[])
    assert source.edges.data == dict(start=[], end=[])
    assert source.layout_provider is None

def test_graphdatasource_check_missing_subcolumn_no_errors():
    source = GraphDataSource()

    check = source._check_missing_subcolumns()
    assert check == []

def test_graphdatasource_check_missing_subcolumn_no_node_index():
    node_source = ColumnDataSource()
    source = GraphDataSource(nodes=node_source)

    check = source._check_missing_subcolumns()
    assert check != []

def test_graphdatasource_check_missing_subcolumn_no_edge_start_or_end():
    edge_source = ColumnDataSource()
    source = GraphDataSource(edges=edge_source)

    check = source._check_missing_subcolumns()
    assert check != []

def test_graphdatasource_from_networkx():
    G=nx.Graph()
    G.add_nodes_from([0,1,2,3])
    G.add_edges_from([[0,1], [0,2], [2,3]])

    source = GraphDataSource.from_networkx(G)
    assert source.nodes.data["index"] == [0,1,2,3]
    assert source.edges.data["start"] == [0,0,2]
    assert source.edges.data["end"] == [1,2,3]

    gl = source.layout_provider.graph_layout
    assert set(gl.keys()) == set([0,1,2,3])
    assert np.array_equal(gl[0], np.array([1., 0.]))