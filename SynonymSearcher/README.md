##### D. Tom 11/2023
# SynonymSearcher: Article and Web Link Finder

> Historical learning project. See the [repository overview](../README.md), [contribution guide](../CONTRIBUTING.md), and [licensing notes](../README.md#license). The dated notebook remains the source of the original learning context; this README describes the revised behavior and its validation limits.

This Python learning project collects words from a prompt or CSV file, checks
spelling, looks up WordNet synonyms, and submits the resulting search queries.
The [Python script](SynonymSearcher.py) and [Jupyter notebook](SynonymSearcher.ipynb)
contain the same input, spelling, combination, and search functions.

## Setup

Complete the virtual-environment setup in the [repository README](../README.md),
then run these commands from the repository root:

```sh
python -m pip install -r requirements.txt
python -m nltk.downloader omw-1.4 wordnet verbnet
python SynonymSearcher/SynonymSearcher.py
```

The first two commands install dependencies and download NLTK data. The script
does not perform either action automatically. For the notebook, use a Jupyter
kernel with these dependencies and corpora installed, then run the cells in order.

Answer `n` to type words or `y` to supply a CSV filename. CSV cells are combined
into the input phrase; relative filenames resolve from the current directory.

## Query behavior

- If the spell checker has no correction, the original word is retained.
- Each word is included alongside its synonyms, including words with no synonyms.
- Duplicate options are removed and query order is deterministic.
- Empty input produces no searches.
- The default maximum is **100 combinations**. A larger expansion is rejected
  before combinations are materialized or any searches are submitted. Use fewer
  input words or a smaller synonym set when this happens. The helper function's
  `max_combinations` argument can be set explicitly by callers.

For `n` words with `k_i` distinct options each, the number of combinations is the
product `k_1 × k_2 × ... × k_n`. For example, two words with 11 options each produce
121 combinations and exceed the default limit. Constructing all query tuples
takes time and memory proportional to `n` times that product. Each combination
adds one search invocation; the package determines the number of HTTP requests.

The `googlesearch-python` package scrapes results; it is not Google's official
search API. Live service changes, missing corpora, network failures, and request
limits may interrupt a run. Review service terms before submitting queries.

## Validation

Run `python -m unittest discover -s tests -v` from the repository root. The tests
exercise script and notebook functions using fake language/search dependencies;
they do not download corpora or send live searches.

## Contributing and licensing

See the repository-local [contribution guide](../CONTRIBUTING.md), [author credits](../README.md#authors), and [licensing notes](../README.md#license). Existing file-specific notices and attribution are unchanged; local license documentation remains pending maintainer clarification.
