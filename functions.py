import random
import time
import numpy as np

def get_coords(pdb_f):
    # read PDB and return array with all atoms
    coord = []
    with open(pdb_f, 'r') as fh:
        for line in fh.readlines():
            if line.startswith('ATOM'):
                x = float(line[31:38])
                y = float(line[39:46])
                z = float(line[47:54])
                coord.append((x, y, z))
    return np.array(coord)

def add_dummy(pdb_f, output_f, dummy_coord):
    new_pdb = []
    with open(pdb_f, 'r') as ref_fh:
        for line in ref_fh.readlines():
            if line.startswith('ATOM'):
                new_pdb.append(line)
    ref_fh.close()

    dum_x = f'{dummy_coord[0]:.3f}'.rjust(7, ' ')
    dum_y = f'{dummy_coord[1]:.3f}'.rjust(7, ' ')
    dum_z = f'{dummy_coord[2]:.3f}'.rjust(7, ' ')
    dummy_line = f'ATOM    999  H   DUM X   1      {dum_x} {dum_y} {dum_z}   1.00  1.00           H  \n'
    new_pdb.append(dummy_line)

    with open(output_f, 'w') as out_fh:
        for line in new_pdb:
            out_fh.write(line)
    out_fh.close()
    return True

def write_coords(pdb_f,output_f, coords):
    c = 0
    with open(output_f, 'w') as out_fh:
        with open(pdb_f, 'r') as ref_fh:
            for line in ref_fh.readlines():
                if line.startswith('ATOM'):
                    new_x = f'{coords[c][0]:.3f}'.rjust(7, ' ')
                    new_y = f'{coords[c][1]:.3f}'.rjust(7, ' ')
                    new_z = f'{coords[c][2]:.3f}'.rjust(7, ' ')
                    new_line = f'{line[:30]} {new_x} {new_y} {new_z} {line[55:]}'
                    out_fh.write(new_line)
                    c += 1
        ref_fh.close()
    out_fh.close()
    return True

def draw_dummy(output_f, dummy_coord):
    with open(output_f, 'w') as out_fh:
        dum_x = f'{dummy_coord[0]:.3f}'.rjust(7, ' ')
        dum_y = f'{dummy_coord[1]:.3f}'.rjust(7, ' ')
        dum_z = f'{dummy_coord[2]:.3f}'.rjust(7, ' ')
        dummy_line = f'ATOM    999  H   DUM X   1     {dum_x} {dum_y} {dum_z}     1.00  1.00           H  \n'
        out_fh.write(dummy_line)
    out_fh.close()

def gen_quat_seq():
    seq = []
    for i in range(4):
        seq.append(random.choice(np.arange(-1, 1, 0.1)))
    return seq

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

