## About

`generate_graph` is a tool that constructs a graph image from a well structured flare_game mod. It does so by traversing maps and extracting relevant "map connections".

It is kinda "untyped", relying on regular expressions, yet it works just fine on the empyrean campaign (and probably others).

## Usage

```bash
data_dir="/path/to/mod/" graphviz_prefix="./prefix.dot" ./generate_graph.py | dot -Tsvg > output.svg
```

## Example

[empyrean_campaign_default.svg](./example/empyrean_campaign_default.svg)

[empyrean_campaign_hyperspace.svg](./empyrean_campaign_hyperspace.svg)


## Prequisities

Install "graphviz" package.


## License

GPLv3+
