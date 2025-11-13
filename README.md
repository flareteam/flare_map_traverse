## About

`generate_graph` is a tool that constructs a graph image from a well structured flare_game mod. It does so by traversing maps and extracting relevant "map connections".

It is kinda "untyped", relying on regular expressions, yet it works just fine on the empyrean campaign (and probably others).

## Usage

```bash
data_dir="/path/to/mod/" ./generate_graph.py | tee output.graphviz | dot -Tpng > output.png
```

Additionally, you can set environment variables:  
`directional=1` to force direction similar to game progression (default=1),  
`print_npc=1` to print npc map connections (default=1),  
`print_dead=1` to print/draw unreachable map nodes (default=0),  
`graphviz_prefix` to specify a Graphviz prefix file (default=prefix.dot),  
`graphviz_suffix` to specify a Graphviz suffix file (default=suffix.dot).

Also, you can replace "png" with "svg" or many other other picture formats,
see `dot` (graphviz) for documentation on that.

## Legacy

There are also two legacy bash scripts that generate map without sorting.
Unfortunately, the main smart algo does not differ much from it if you have crazy connected map tiles (hyperspace, I'm looking at you).
So if you don't care about sorting, you can use the much simpler bash scripts in this repo to generate graphviz file contents.
In this case, use:

```bash
./generate_graph.sh /path/to/mod/maps
```

## Example

[empyrean_campaign_default](./example/empyrean_campaign_default.png)

[empyrean_campaign_hyperspace](./example/empyrean_campaign_hyperspace.png)


## Prequisities

Install "graphviz" package.


## License

GPLv3+
