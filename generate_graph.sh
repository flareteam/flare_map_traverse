#!/bin/bash -eu

map_dir="${1:-/usr/share/flare/mods/empyrean_campaign/maps}"

for map_full in "$map_dir"/*.txt "$map_dir"/*/*.txt; do
	map="${map_full%.txt}"
	map="${map##*/}"
	for npc_full in $(grep 'filename=npcs' "$map_full"); do
		npc_full="${npc_full##*=}"
		for link_full in $(grep 'intermap=' "$map_dir/../$npc_full"); do
			link="${link_full%.txt*}"
			link="${link##*/}"
			echo "$map -> $link [label=\"npc\" style=dashed]"
		done
	done
	for link_full in $(grep 'intermap=' "$map_full"); do
		link="${link_full%.txt*}"
		link="${link##*/}"
		echo "$map -> $link"
	done
done
