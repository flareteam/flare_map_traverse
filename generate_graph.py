#!/bin/python3

import glob
import re
import os

data_dir = os.path.abspath(os.environ["data_dir"])
graphviz_prefix_file = os.environ.get("graphviz_prefix", "prefix.dot")
graphviz_suffix_file = os.environ.get("graphviz_suffix", "suffix.dot")
print_dead = os.environ.get("print_dead", "false").lower() in ("yes", "true", "1")
print_npc = os.environ.get("npc", "true").lower() in ("yes", "true", "1")
directional = os.environ.get("directional", "true").lower() in ("yes", "true", "1")

with open(graphviz_prefix_file, 'r') as opened_file:
    graphviz = opened_file.read()

if os.path.exists(graphviz_suffix_file):
    with open(graphviz_suffix_file, 'r') as opened_file:
        suffix = opened_file.read()
else:
    suffix = "}"

os.chdir(os.path.abspath(os.environ["data_dir"]))


def color(map_name):
    return os.environ.get("colorize_" + map_name)

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
def add_to_queue(index, map_name):
    if (map_name not in traversed) and (map_name not in to_traverse):
        to_traverse.insert(index + 1, map_name)  # yes, list insertions are slow, and we don't care
def graphviz_edge_attribute_down(map_name):
    if directional and (map_name in traversed):
        return " constraint=false"  # already traversed targets should not give graphviz direction
    else:
        return ""

for map_index, map_file in enumerate(to_traverse):
    traversed[map_file] = True
    map_id = clean(map_file)
    if print_npc:
        for npc_child in map_to_map_npc[map_file]:
            clr = color(map_id) or color(clean(npc_child)) or "black"
            direction = graphviz_edge_attribute_down(npc_child)
            graphviz += '{} -> {} [label=npc {} style=dashed color={}]\n'.format(map_id, clean(npc_child), direction, clr)
            add_to_queue(map_index, npc_child)
    for direct_child in map_to_map_direct[map_file]:
        clr = color(map_id) or color(clean(direct_child)) or "black"
        direction = graphviz_edge_attribute_down(direct_child)
        graphviz += '{} -> {} [{} color={}]\n'.format(map_id, clean(direct_child), direction, clr)
        add_to_queue(map_index, direct_child)
    graphviz += '{} [label="{}"]\n'.format(map_id, get_map_name(map_file) or map_file)

if print_dead:
    for map_file in all_maps:
        map_name = get_map_name(map_file)
        clr = color(clean(map_file)) or "black"
        graphviz += '{} [label="{}" color="{}"]\n'.format(clean(map_file), map_name or map_file, clr)

graphviz += suffix

print(graphviz)
