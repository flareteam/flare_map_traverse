#!/usr/bin/env python3

import glob
import re
import os
import argparse
import pathlib

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", type=pathlib.Path, required=True, help="Path to Flare mod.")
parser.add_argument("--directional", type=str_to_bool, default=True, required=False, help="Force direction similar to game progression. (Default = %(default)s)")
parser.add_argument("--print_npc", type=str_to_bool, default=True, required=False, help="Print NPC map connections. (Default = %(default)s)")
parser.add_argument("--print_dead", type=str_to_bool, default=False, required=False, help="Print/draw unreachable map nodes. (Default = %(default)s)")
parser.add_argument("--graphviz_prefix", type=pathlib.Path, default=pathlib.Path("prefix.dot"), required=False, help="Graphviz prefix file. (Default = %(default)s)")
parser.add_argument("--graphviz_suffix", type=pathlib.Path, default=pathlib.Path("suffix.dot"), required=False, help="Graphviz suffix file. (Default = %(default)s)")
args = parser.parse_args()

with open(args.graphviz_prefix, 'r') as opened_file:
    graphviz = opened_file.read()

if os.path.exists(args.graphviz_suffix):
    with open(args.graphviz_suffix, 'r') as opened_file:
        suffix = opened_file.read()
else:
    suffix = "}"

if not os.path.exists(args.data_dir):
    print("ERROR: Path does not exist: " + str(args.data_dir) + "\n")
    parser.print_help()
    exit(1)

os.chdir(args.data_dir)


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
all_maps = list(map(lambda x: os.path.relpath(x, args.data_dir), all_maps))

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
    if args.directional and (map_name in traversed):
        return " constraint=false"  # already traversed targets should not give graphviz direction
    else:
        return ""

for map_index, map_file in enumerate(to_traverse):
    traversed[map_file] = True
    map_id = clean(map_file)
    if args.print_npc:
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

if args.print_dead:
    for map_file in all_maps:
        map_name = get_map_name(map_file)
        clr = color(clean(map_file)) or "black"
        graphviz += '{} [label="{}" color="{}"]\n'.format(clean(map_file), map_name or map_file, clr)

graphviz += suffix

print(graphviz)
