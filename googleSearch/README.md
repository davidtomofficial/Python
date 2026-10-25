# Google Search example

> Historical educational example. See the [repository overview](../README.md) for context and validation limits.

This learning script reads a query, prints results from `googlesearch-python`, and
waits 3–10 seconds before accepting the next query. It skips blank input and exits
cleanly on `exit()` or end of input.

From the repository root, after completing the [setup](../README.md):

```sh
python googleSearch/googleSearch.py
```

You can also read queries from a file with one query per line:

```sh
python googleSearch/googleSearch.py < googleSearch/randomSearchTerms.txt
```

Each nonblank line triggers a real network search. The package scrapes search
results and is not Google's official search API; spacing requests does not
guarantee compliance with service limits or availability.

Importing the script does not prompt or submit searches. Call `main()` or run it as
a script to start the interactive loop.

## Contributing

See the repository-local [contribution guide](../CONTRIBUTING.md) for reporting issues and submitting focused pull requests while preserving the educational context.

## Authors

* **David Tom** - *Initial Work* - [davidtomofficial](https://github.com/davidtomofficial)

See this repository's [commit history](https://github.com/davidtomofficial/Python/commits/main/) for recorded changes. Additional authors and course-provided material remain credited in their respective files.

## License

The notice in [googleSearch.py](googleSearch.py) permits GNU GPL version 3 or any later version. See the [repository licensing notes](../README.md#license) for the existing repository-level statement and pending documentation clarification.

## Acknowledgements

* A big thanks to any and all contributors, no matter how big or small the contribution it all helps.
