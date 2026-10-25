# Python Scripts

Historical Python learning projects and experiments by [David Tom](https://github.com/davidtomofficial), preserved for educational reference and portfolio review.

**Status: Historical educational examples.** This collection is separate from current David Tom Solutions (DTS) and David Tom Publishing (DTP) offerings. Focused behavior fixes have offline regression coverage; live search-service compatibility and the installed third-party dependencies have not been validated end to end.

The original `googleSearch.py` header names Python 3.6; the SynonymSearcher notebook records Python 3.11.3. These remain historical environment details, not a verified current compatibility range.

| Project | Purpose |
| --- | --- |
| [SynonymSearcher](SynonymSearcher/) | Generate keyword/synonym combinations and find a search result for each query. Includes a Python script and a Jupyter notebook. |
| [googleSearch](googleSearch/) | Read search queries interactively or from standard input and print results. |

## Getting started

Install Python 3, clone this repository, and create a virtual environment:

```sh
git clone https://github.com/davidtomofficial/Python.git
cd Python
python3 -m venv .venv
```

Activate it with `source .venv/bin/activate` on Linux/macOS or
`.venv\Scripts\Activate.ps1` in Windows PowerShell. Use `python` instead of
`python3` if that is the name of your Python 3 interpreter.

```sh
python -m pip install -r requirements.txt
python googleSearch/googleSearch.py
```

SynonymSearcher also needs local NLTK corpora. See its
[setup instructions](SynonymSearcher/README.md). Dependency installation and
corpus downloads are explicit setup steps; importing the scripts does not install
packages, download corpora, prompt for input, or submit searches.

Searches require an internet connection and depend on the external search service.
The `googlesearch-python` package scrapes search results; this project does not use
Google's official search API. Review the service's terms and limits before use.

## Tests

Run the offline behavior tests from this directory:

```sh
python -m unittest discover -s tests -v
```

Tests replace external search and language dependencies with deterministic fakes;
they do not make network requests or verify live search-service compatibility.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution process.

## Authors

* **David Tom** - *Initial Work* - [davidtomofficial](https://github.com/davidtomofficial)

See this repository's [commit history](https://github.com/davidtomofficial/Python/commits/main/) for recorded changes. Additional authors and course-provided material remain credited in their respective files.

## License

The existing licensing statement is retained:

> This project is licensed under the GNU General Public License Version 3.

Read the [GNU GPL version 3 text](https://www.gnu.org/licenses/gpl-3.0.html). This repository currently has no local `LICENSE` file. Earlier READMEs linked to a license in the separate GitHub profile repository; that file is not a project-local license.

The notice in [googleSearch/googleSearch.py](googleSearch/googleSearch.py) explicitly permits GPL version 3 or any later version. That file-specific grant is unchanged.

Existing file-specific notices and third-party attribution remain unchanged. The maintainer still needs to document the scope of the repository-level statement, confirm the version wording where file-specific notices do not already settle it, and add the appropriate local license text. This documentation update does not change existing licensing terms.

## Acknowledgements

* A big thanks to any and all contributors, no matter how big or small the contribution it all helps.
