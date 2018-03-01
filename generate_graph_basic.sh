#!/bin/bash -eu

map_dir="${1:-/usr/share/flare/mods/empyrean_campaign/maps}"

for map_full in "$map_dir"/*.txt "$map_dir"/*/*.txt; do
	map="${map_full%.txt}"
	map="${map##*/}"
	for link in $(grep 'intermap=' "$map_full"); do
		link="${link%.txt*}"
		link="${link##*/}"
		echo "$map -> $link"
	done
done
