#!/bin/python3

import glob
import re
import itertools
import os

data_dir = os.path.abspath(os.environ["data_dir"])


def get_intermaps(filename):
    result = []
    with open(filename, 'rU') as opened_file:
        for line in opened_file:
            ref = re.search('intermap=(maps.*),.*,.*', line)
            if ref:
                ref = ref.group(1)
                result.append(ref)
    return result


def get_npc_files(filename):
    result = []
    with open(filename, 'rU') as opened_file:
        for line in opened_file:
            ref = re.search('filename=(npcs.*)', line)
            if ref:
                ref = ref.group(1)
                result.append(ref)
    return result


map_to_map_direct = {}
map_to_map_npc = {}

all_maps = itertools.chain(
    glob.iglob(data_dir + '/maps/*.txt'),
    glob.iglob(data_dir + '/maps/*/*.txt')
)
for map_name in all_maps:
    relative = os.path.relpath(map_name, data_dir)
    map_to_map_direct[relative] = get_intermaps(map_name)
    map_to_map_npc[relative] = []
    for npc_file in get_npc_files(map_name):
        map_to_map_npc[relative].extend(
            get_intermaps(data_dir + '/' + npc_file)
        )

# print(map_to_map_direct)
# print(map_to_map_npc)


def clean(filename):
    return os.path.splitext(os.path.basename(filename))[0]


with open(os.environ.get("graphviz_prefix", "prefix.dot"), 'rU') as opened_file:
    graphviz = opened_file.read()

traversed = {}
to_traverse = ['maps/spawn.txt']
for map_file in to_traverse:
    traversed[map_file] = True
    map = os.path.splitext(os.path.basename(map_file))[0]
    for npc_child in map_to_map_npc[map_file]:
        graphviz += '{} -> {} [label=npc style=dashed]\n'.format(map, clean(npc_child))
        if npc_child not in traversed:
            to_traverse.append(npc_child)
    for direct_child in map_to_map_direct[map_file]:
        graphviz += '{} -> {}\n'.format(map, clean(direct_child))
        if direct_child not in traversed:
            to_traverse.append(direct_child)

graphviz += "}"

print(graphviz)
