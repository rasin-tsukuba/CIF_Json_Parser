import plotly.graph_objs as go
import networkx as nx

from cif_to_graph import CrystalGraph, letter

cpk_colors = dict(Ar='cyan', B='salmon', Ba='darkgreen', Be='darkgreen', Br='darkred', C='black', Ca='darkgreen',
                  Cl='green', Cs='violet', F='green', Fe='darkorange', Fr='violet', H='white', He='cyan',
                  I='darkviolet', K='violet', Kr='cyan', Li='violet', Mg='darkgreen', N='blue', Na='violet', Ne='cyan',
                  O='red', P='orange', Ra='darkgreen', Rb='violet', S='yellow', Sr='darkgreen', Ti='gray', Xe='cyan')
cpk_color_rest = 'pink'

atomic_radii = dict(Ac=1.88, Ag=1.59, Al=1.35, Am=1.51, As=1.21, Au=1.50, B=0.83, Ba=1.34, Be=0.35, Bi=1.54, Br=1.21,
                    C=0.68, Ca=0.99, Cd=1.69, Ce=1.83, Cl=0.99, Co=1.33, Cr=1.35, Cs=1.67, Cu=1.52, D=0.23, Dy=1.75,
                    Er=1.73, Eu=1.99, F=0.64, Fe=1.34, Ga=1.22, Gd=1.79, Ge=1.17, H=0.23, Hf=1.57, Hg=1.70, Ho=1.74,
                    I=1.40, In=1.63, Ir=1.32, K=1.33, La=1.87, Li=0.68, Lu=1.72, Mg=1.10, Mn=1.35, Mo=1.47, N=0.68,
                    Na=0.97, Nb=1.48, Nd=1.81, Ni=1.50, Np=1.55, O=0.68, Os=1.37, P=1.05, Pa=1.61, Pb=1.54, Pd=1.50,
                    Pm=1.80, Po=1.68, Pr=1.82, Pt=1.50, Pu=1.53, Ra=1.90, Rb=1.47, Re=1.35, Rh=1.45, Ru=1.40, S=1.02,
                    Sb=1.46, Sc=1.44, Se=1.22, Si=1.20, Sm=1.80, Sn=1.46, Sr=1.12, Ta=1.43, Tb=1.76, Tc=1.35, Te=1.47,
                    Th=1.79, Ti=1.47, Tl=1.55, Tm=1.72, U=1.58, V=1.33, W=1.37, Y=1.78, Yb=1.94, Zn=1.45, Zr=1.56)


def to_plotly_figure(graph: CrystalGraph) -> go.Figure:
    """
    Create a Plotly Figure
    :param graph:
    :return:
    """

    def atom_trace():
        """
        Creates an atom trace for the plot
        :return:
        """

        colors = [cpk_colors.get(letter(element), cpk_color_rest) for element in graph.elements]
        sizes = []
        for element in graph.elements:
            sizes.append(atomic_radii.get(letter(element)) * 40)

        markers = dict(color=colors,
                       line=dict(color='lightgray',
                                 width=2),
                       size=sizes,
                       symbol='circle',
                       opacity=0.8)
        trace = go.Scatter3d(
            x=graph.x,
            y=graph.y,
            z=graph.z,
            mode='markers',
            marker=markers,
            text=graph.elements
        )

        return trace

    def bond_trace():
        """
        Creates a bond trace for the plot.
        :return:
        """

        trace = go.Scatter3d(
            x=[],
            y=[],
            z=[],
            hoverinfo='none',
            mode='lines',
            marker=dict(color='gray',
                        size=3,
                        opacity=0.1)
        )

        adjacent_atoms = (
            (atom, neighbour) for atom, neighbours in graph.adj_list.items()
            for neighbour in neighbours)

        for i, j in adjacent_atoms:
            x_i, y_i, z_i = graph.__getitem__(i)[1]
            x_j, y_j, z_j = graph.__getitem__(j)[1]
            trace['x'] += (x_i, x_j, None)
            trace['y'] += (y_i, y_j, None)
            trace['z'] += (z_i, z_j, None)
        return trace

    # print(element for element in graph)
    annotations_elements = [
        dict(text=element,
             x=x,
             y=y,
             z=z,
             showarrow=False,
             yshift=15)
        for element, (x, y, z) in graph
    ]

    annotations_indices = [
        dict(text=number,
             x=x,
             y=y,
             z=z,
             showarrow=False,
             yshift=15)
        for number, (_, (x, y, z)) in enumerate(graph)
    ]

    annotations_bonds = []
    for (i, j), length in graph.bond_lengths.items():
        #print(i, j, length)
        x_i, y_i, z_i = graph.__getitem__(i)[1]
        x_j, y_j, z_j = graph.__getitem__(j)[1]
        x = (x_i + x_j) / 2
        y = (y_i + y_j) / 2
        z = (z_i + z_j) / 2
        annotations_bonds.append(
            dict(
                text=length,
                x=x,
                y=y,
                z=z,
                showarrow=False,
                yshift=15,
                font=dict(color="steelblue")
            )
        )

    updatemenus = list([
        dict(buttons=list([
            dict(label='Elements',
                 method='relayout',
                 args=[{
                     'scene.annotations': annotations_elements
                 }]),
            dict(label='Element & Bond Lengths',
                 method='relayout',
                 args=[{
                     'scene.annotations': annotations_elements + annotations_bonds
                 }]),
            dict(label='Indices',
                 method='relayout',
                 args=[{
                     'scene.annotations': annotations_indices
                 }]),
            dict(label='Indices & Bond Lengths',
                 method='relayout',
                 args=[{
                     'scene.annotations': annotations_indices + annotations_bonds
                 }]),
            dict(label='Bond Lengths',
                 method='relayout',
                 args=[{
                     'scene.annotations': annotations_bonds
                 }]),
            dict(label='Hide All',
                 method='relayout',
                 args=[{
                 }])
        ]),
            direction='down',
            xanchor='left',
            yanchor='top'
        ),
    ])

    data = [atom_trace(), bond_trace()]
    axis_params = dict(
        showgrid=True,
        showbackground=True,
        showticklabels=True,
        zeroline=True,
        titlefont=dict(color='white')
    )
    layout = dict(
        scene=dict(
            xaxis=axis_params,
            yaxis=axis_params,
            zaxis=axis_params,
            annotations=annotations_elements
        ),
        margin=dict(
            r=0,
            l=0,
            b=0,
            t=0
        ),
        showlegend=False,
        updatemenus=updatemenus
    )
    figure = go.Figure(data=data, layout=layout)

    return figure


def to_networkx_graph(graph: CrystalGraph) -> nx.Graph:
    """
    Creates a NetworkX graph
    Atomic elements and coordinates are added to the graph
    as node attributes 'element' and 'xyz" respectively.
    Bond lengths are added to the graph as edge attribute 'length'
    :param graph:
    :return:
    """

    G = nx.Graph(graph.adj_list)
    node_attrs = {
        num: {
            'element': element,
            'xyz': xyz
        } for num, (element, xyz) in enumerate(graph)
    }
    nx.set_node_attributes(G, node_attrs)
    edge_attrs = {
        edge: {
            'length': length
        } for edge, length in graph.bond_lengths.items()
    }
    nx.set_edge_attributes(G, edge_attrs)
    return G
