#!/bin/python3

import glob
import re
import os

data_dir = os.path.abspath(os.environ["data_dir"])
graphviz_prefix_file = os.environ.get("graphviz_prefix", "prefix.dot")
print_dead = os.environ.get("print_dead", "false").lower() in ("yes", "true", "1")
print_npc = os.environ.get("npc", "true").lower() in ("yes", "true", "1")

with open(graphviz_prefix_file, 'r') as opened_file:
    graphviz = opened_file.read()

os.chdir(os.path.abspath(os.environ["data_dir"]))


def get_intermaps(filename):
    result = []
    with open(filename, 'r') as opened_file:
        for line in opened_file:
            ref = re.search('intermap=(maps.*),.*,.*', line)
            if ref:
                ref = ref.group(1)
                result.append(ref)
    return result


def get_npc_files(filename):
    result = []
    with open(filename, 'r') as opened_file:
        for line in opened_file:
            ref = re.search('filename=(npcs.*)', line)
            if ref:
                ref = ref.group(1)
                result.append(ref)
    return result


def get_map_name(filename):
    with open(filename, 'r') as opened_file:
        for line in opened_file:
            ref = re.search('title=(.*)', line)
            if ref:
                return ref.group(1)


map_to_map_direct = {}
map_to_map_npc = {}

all_maps = list(glob.iglob('maps/*.txt')) + \
           list(glob.iglob('maps/*/*.txt'))
all_maps = list(map(lambda x: os.path.relpath(x, data_dir), all_maps))

for map_file in all_maps:
    map_to_map_direct[map_file] = get_intermaps(map_file)
    map_to_map_npc[map_file] = []
    for npc_file in get_npc_files(map_file):
        map_to_map_npc[map_file].extend(
            get_intermaps(npc_file)
        )

# print(map_to_map_direct)
# print(map_to_map_npc)


def clean(filename):
    return os.path.splitext(os.path.basename(filename))[0]


traversed = {}
to_traverse = ['maps/spawn.txt']
for map_file in to_traverse:
    traversed[map_file] = True
    map_id = clean(map_file)
    if print_npc:
        for npc_child in map_to_map_npc[map_file]:
            graphviz += '{} -> {} [label=npc style=dashed]\n'.format(map_id, clean(npc_child))
            if npc_child not in traversed:
                to_traverse.append(npc_child)
    for direct_child in map_to_map_direct[map_file]:
        graphviz += '{} -> {}\n'.format(map_id, clean(direct_child))
        if direct_child not in traversed:
            to_traverse.append(direct_child)
    graphviz += '{} [label="{}"]\n'.format(map_id, get_map_name(map_file) or map_file)

if print_dead:
    for map_file in all_maps:
        map_name = get_map_name(map_file)
        graphviz += '{} [label="{}"]\n'.format(clean(map_file), map_name or map_file)


graphviz += "}"

print(graphviz)
