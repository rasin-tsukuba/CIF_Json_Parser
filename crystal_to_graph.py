import json
from glob import glob
import pickle


class ToString:
    def getDescription(self):
        # 利用str的format格式化字符串
        # 利用生成器推导式去获取key和self中key对应的值的集合
        return ",".join("{}={}".format(key, getattr(self, key)) for key in self.__dict__.keys())

    # 重写__str__定义对象的打印内容
    def __str__(self):
        return "{}->({})".format(self.__class__.__name__, self.getDescription())


class Vertex(ToString):
    def __init__(self, name, type, x, y, z):
        self.id = name
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.connections = dict()

    def add_neighbour(self, neighbour, weight=0):
        self.connections[neighbour.id] = weight

    def get_id(self):
        return self.id

    def get_connections(self):
        return self.connections.keys()

    def get_weight(self, neighbour):
        return self.connections[neighbour.id]


class Graph(ToString):
    def __init__(self, name):
        self.name = name
        self.vertex_dict = dict()
        self.vertem_num = 0

    def get_graph(self):
        print("name:", self.name, "vertex_num:", self.vertem_num, "vertex_dict:")
        # for i in self.vertex_dict:
        #     print(self.vertex_dict[i])
        print(self)

    def add_vertex(self, vertex):
        if vertex.id not in self.vertex_dict.keys():
            new_vertex = vertex
            self.vertex_dict[vertex.id] = new_vertex
            self.vertem_num += 1

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.vertex_dict:
            self.add_vertex(vertex1)
        if vertex2 not in self.vertex_dict:
            self.add_vertex(vertex2)
        self.vertex_dict[vertex1.id].add_neighbour(self.vertex_dict[vertex2.id], weight)
        self.vertex_dict[vertex2.id].add_neighbour(self.vertex_dict[vertex1.id], weight)

    def get_vertex(self, name):
        if name in self.vertex_dict.keys():
            return self.vertex_dict[name]
        else:
            print('No existing vertex!')
            return None

    # 重载迭代器，返回对应迭代器
    def __iter__(self):
        return iter(self.vertex_dict.values())

    # 重载字符串化方法，返回字符串
    def __str__(self):
        o_str = str()
        for item in self:
            o_str = o_str + str(item) + '\n'
        return o_str


def read_json(file, out):
    name = file.split('/')[-1].split('.')[0].split('\\')[-1]
    #print(name)
    f = open(file, 'r')
    data = json.load(f)

    g = Graph(data['name'])

    for i in data['atoms']:
        v = Vertex(i['label'], i['type_symbol'], i['x'], i['y'], i['z'])
        g.add_vertex(v)

    for i in data['bonds']:
        first_atom = i['first_atom']
        second_atom = i['second_atom']
        weight = i['length']

        g.add_edge(g.vertex_dict[first_atom],
                   g.vertex_dict[second_atom],
                   weight)
    #g.get_graph()
    f = open(out + name + '.pkl', 'wb+')
    pickle.dump(g, f)
    print(out+name+'.pkl Done.')


if __name__ == '__main__':
    pos_path = sorted(glob('Data/cartesian_json/pos/*.json'))
    neg_path = sorted(glob('Data/cartesian_json/neg/*.json'))
    pos_out = 'Data/graph/pos/'
    neg_out = 'Data/graph/neg/'

    # for i in pos_path:
    #     read_json(i, pos_out)
    #
    # for i in neg_path:
    #     read_json(i, neg_out)
    f = open('Data/graph/neg/H2PO4-H2PO4(3).pkl', 'rb')
    object = pickle.load(f)
    object.get_graph()

