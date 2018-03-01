## About

`generate_graph` is a tool that constructs a graph image from a well structured flare_game mod. It does so by traversing maps and extracting relevant "map connections".

It is kinda "untyped", relying on regular expressions, yet it works just fine on the empyrean campaign (and probably others).

## Usage

```bash
data_dir="/path/to/mod/" graphviz_prefix="./prefix.dot" ./generate_graph.py | dot -Tsvg > output.svg
```

There are also two legacy bash scripts that generate map without sorting.
Unfortunately, the main smart algo does not differ much from it if you have crazy connected map tiles (hyperspace, I'm looking at you).
So if you don't care about sorting, you can use the much simpler bash scripts in this repo to generate graphviz file contents.
In this case, use:

```bash
./generate_graph.sh /path/to/mod/maps
```

## Example

[empyrean_campaign_default.svg](./example/empyrean_campaign_default.svg)

[empyrean_campaign_hyperspace.svg](./empyrean_campaign_hyperspace.svg)


## Prequisities

Install "graphviz" package.


## License

GPLv3+
