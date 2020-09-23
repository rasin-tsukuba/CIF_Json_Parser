from math import sqrt
from itertools import combinations
import json


def letter(inp):
    return ''.join(filter(str.isalpha, inp))


class CrystalGraph:
    """
    Represents a Crystal Graph.
    """

    __slots__ = [
        'name',
        'elements',
        'x',
        'y',
        'z',
        'adj_list',
        'bond_lengths'
    ]

    def __init__(self):
        self.name = ""
        self.elements = []
        self.x = []
        self.y = []
        self.z = []
        self.adj_list = {}
        self.bond_lengths = {}

    def __getitem__(self, item):
        # print(item)
        if isinstance(item, int):
            return self.elements[item], (self.x[item], self.y[item], self.z[item])
        else:
            position = self.elements.index(item)
            return self.elements[position], (self.x[position], self.y[position], self.z[position])

    def __len__(self):
        return len(self.elements)

    def add_adj_list(self, i, j, distance):
        self.adj_list.setdefault(i, set()).add(j)
        self.adj_list.setdefault(j, set()).add(i)
        self.bond_lengths[frozenset([i, j])] = round(distance, 3)

    def read_json(self, file_path: str):
        """
        Read an CIF file, searches for elements and their
        cartesian coordinates
        :param file_path:
        :return:
        """
        with open(file_path) as file:
            data = json.load(file)

            self.name = data["name"]
            for i in data["atoms"]:
                self.elements.append(i["label"])
                self.x.append(i["x"])
                self.y.append(i["y"])
                self.z.append(i["z"])

            for i in data["bonds"]:
                self.adj_list.setdefault(i["first_atom"], set()).add(i["second_atom"])
                self.adj_list.setdefault(i["second_atom"], set()).add(i["first_atom"])
                self.bond_lengths[frozenset([i["first_atom"], i["second_atom"]])] = i["length"]

        for i, j in combinations(self.elements, 2):
            # print(i, j)
            if i.startswith('H') and j.startswith('O') or i.startswith('O') and j.startswith('H'):
                # print(i, j)
                x_i, y_i, z_i = self.__getitem__(i)[1]
                x_j, y_j, z_j = self.__getitem__(j)[1]
                distance = sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2 + (z_i - z_j) ** 2)

                if 0.9 < distance < 1.1 or 1.4 < distance < 2:
                    # print(self.adj_list, self.bond_lengths)
                    if i in self.adj_list and j in self.adj_list:
                        if j in self.adj_list[i] or i in self.adj_list[j] or frozenset([i, j]) in self.bond_lengths:
                            continue
                        else:
                            self.add_adj_list(i, j, distance)
                    else:
                        self.add_adj_list(i, j, distance)
        print(self.adj_list, self.bond_lengths)

    def edges(self):
        """
        creates an iterator with all graph edges.
        :return:
        """

        edges = set()

        for node, neighbours in self.adj_list.items():
            for neighbour in neighbours:
                edge = frozenset([node, neighbour])
                if edge in edges:
                    continue
                edges.add(edge)

                yield node, neighbour


if __name__ == '__main__':
    c = CrystalGraph()
    c.read_json('/home/rasin/Workspace/Project/Crystal/Data/cartesian_json/neg/H2PO4-PO4(5).json')
