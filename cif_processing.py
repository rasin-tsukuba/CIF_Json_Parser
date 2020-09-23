import json
from glob import glob


def cif_parser(cif_dir, json_dir):
    path = sorted(glob(cif_dir))
    for i in path:
        data = {}
        name = i.split('/')[-1].split('\\')[-1].split('.')[0]
        print(name)
        data['name'] = name
        data['info'] = {}
        data['cell'] = {}
        data['atoms'] = []
        data['bonds'] = []
        loop = 0
        for line in open(i, 'r'):
            line = ' '.join(line.split())
            # print(line)
            if line == 'loop_':
                loop += 1
            if loop == 0:
                if line.startswith('_audit_creation_date'):
                    data['info']['creation_date'] = line.split(' ')[-1]
            if loop == 1:
                if line.startswith('_cell_length_a'):
                    data['cell']['a'] = float(line.split(' ')[-1])
                if line.startswith('_cell_length_b'):
                    data['cell']['b'] = float(line.split(' ')[-1])
                if line.startswith('_cell_length_c'):
                    data['cell']['c'] = float(line.split(' ')[-1])
                if line.startswith('_cell_angle_alpha'):
                    data['cell']['alpha'] = float(line.split(' ')[-1])
                if line.startswith('_cell_angle_beta'):
                    data['cell']['beta'] = float(line.split(' ')[-1])
                if line.startswith('_cell_angle_gamma'):
                    data['cell']['gamma'] = float(line.split(' ')[-1])
            if loop == 2:
                if len(line.split(' ')) == 8:
                    # print(line, len(line.split(' ')))
                    atom_info = {'label': line.split(' ')[0],
                                 'type_symbol': line.split(' ')[1],
                                 'x': float(line.split(' ')[2]),
                                 'y': float(line.split(' ')[3]),
                                 'z': float(line.split(' ')[4])
                                 }
                    data['atoms'].append(atom_info)

            if loop == 3:
                if len(line.split(' ')) == 5:
                    bond_info = {'first_atom': line.split(' ')[0],
                                 'second_atom': line.split(' ')[1],
                                 'length': line.split(' ')[2]
                                 }
                    data['bonds'].append(bond_info)

        data2 = json.dumps(data)
        file = open(json_dir + name.strip() + '.json', 'w')
        file.write(data2)


def convert_to_cartesian(src_dir, out_dir):
    path = sorted(glob(src_dir))
    for jfile in path:
        filename = jfile.split('/')[-1].split('\\')[-1].split('.')[0].strip()
        # print(filename)
        # break
        f = open(jfile, 'r')
        data = json.load(f)
        x, y, z = 0, 0, 0
        for i in data['atoms']:
            i['x'] = data['cell']['a'] * i['x']
            i['y'] = data['cell']['b'] * i['y']
            i['z'] = data['cell']['c'] * i['z']

        for i in data['atoms']:
            if i['label'].startswith('P'):
                x, y, z = i['x'], i['y'], i['z']
                break
        for i in data['atoms']:
            i['x'] = round(i['x'] - x, 6)
            i['y'] = round(i['y'] - y, 6)
            i['z'] = round(i['z'] - z, 6)

        data2 = json.dumps(data)
        print(out_dir + filename.strip() + '.json')
        file = open(out_dir + filename.strip() + '.json', 'w')
        file.write(data2)


if __name__ == '__main__':
    cif_parser(cif_dir='/home/rasin/Workspace/Project/Crystal/Data/cif/monomer/*.cif',
               json_dir='/home/rasin/Workspace/Project/Crystal/Data/json/monomer/')
    convert_to_cartesian(src_dir='/home/rasin/Workspace/Project/Crystal/Data/json/monomer/*.json',
                         out_dir='/home/rasin/Workspace/Project/Crystal/Data/cartesian_json/monomer/')
