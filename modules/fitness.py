from subprocess import Popen, PIPE
import os
import configparser
import numpy as np
from utils.files import get_full_path
from utils.functions import get_coords

etc_folder = get_full_path('etc')
ini = configparser.ConfigParser(os.environ)
ini.read(os.path.join(etc_folder, 'gadock.ini'), encoding='utf-8')
native = ini.get('reference', 'native_pdb')

dockq_exe = ini.get('third_party', 'dockq_exe')
dcomplex_exe = ini.get('third_party', 'dcomplex_exe')
contact_exe = ini.get('third_party', 'contact_exe')


def calc_irmsd(pdb_f):
    """

    :param pdb_f:
    :return:
    """
    cmd = f'{dockq_exe} {pdb_f} {native}'
    proc = Popen(cmd.split(), shell=True, stdout=PIPE)
    result = proc.stdout.read().decode('utf-8')
    irmsd = float(result.split('\n')[-6].split()[-1])
    return irmsd


def dcomplex(pdb_f):
    """

    :param pdb_f:
    :return:
    """
    cmd = f'{dcomplex_exe} {pdb_f} A B'
    proc = Popen(cmd.split(), shell=True, stdout=PIPE)
    energ = float(proc.stdout.read().decode('utf-8').split('\n')[-2].split()[1])
    return energ


def calc_clash(pdb_f, cutoff=2.0):
    """

    :param pdb_f:
    :param cutoff:
    :return:
    """
    cmd = f'{contact_exe} {pdb_f} {cutoff}'
    proc = Popen(cmd.split(), shell=True, stdout=PIPE)
    out = proc.stdout.read().decode('utf-8')
    if out:
        clash = len(out.split('\n'))
    else:
        clash = 0
    return clash


def calc_centerdistance(pdb_f):
    """

    :param pdb_f:
    :return:
    """
    # calculate the distance between two centers
    coord_a = get_coords(pdb_f, 'A')
    coord_b = get_coords(pdb_f, 'B')

    center_a = coord_a.mean(axis=0)
    center_b = coord_b.mean(axis=0)
    dist = np.linalg.norm(center_a - center_b)
    return dist
