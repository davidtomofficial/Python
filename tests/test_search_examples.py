"""Offline regression tests; third-party services are replaced with fakes."""

import ast
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


class FakeSpellChecker:
    def unknown(self, words):
        return set()

    def correction(self, word):
        return word


def dependency_fakes():
    spellchecker = types.ModuleType('spellchecker')
    spellchecker.SpellChecker = FakeSpellChecker
    corpus = types.ModuleType('nltk.corpus')
    corpus.wordnet = mock.Mock()
    corpus.verbnet = mock.Mock()
    nltk = types.ModuleType('nltk')
    nltk.corpus = corpus
    googlesearch = types.ModuleType('googlesearch')
    googlesearch.search = mock.Mock(side_effect=AssertionError('Unexpected search'))
    return {'spellchecker': spellchecker, 'nltk': nltk,
            'nltk.corpus': corpus, 'googlesearch': googlesearch}


def load_script(path):
    spec = importlib.util.spec_from_file_location('example_under_test', ROOT / path)
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict('sys.modules', dependency_fakes()), \
            mock.patch('builtins.input', side_effect=AssertionError('Import prompted')):
        spec.loader.exec_module(module)
    return module


def load_notebook():
    path = ROOT / 'SynonymSearcher/SynonymSearcher.ipynb'
    notebook = json.loads(path.read_text(encoding='utf-8'))
    module = types.ModuleType('notebook_under_test')
    with mock.patch.dict('sys.modules', dependency_fakes()), \
            mock.patch('builtins.input', side_effect=AssertionError('Definition prompted')):
        for cell in notebook['cells']:
            if cell['cell_type'] != 'code':
                continue
            tree = ast.parse(''.join(cell['source']))
            # The notebook calls main explicitly; test that entry point separately.
            tree.body = [node for node in tree.body if not (
                isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == 'main')]
            exec(compile(tree, str(path), 'exec'), module.__dict__)
    return module


class SynonymSearcherTests(unittest.TestCase):
    def setUp(self):
        self.variants = {
            'script': load_script('SynonymSearcher/SynonymSearcher.py'),
            'notebook': load_notebook(),
        }

    def test_definitions_do_not_search(self):
        for name, module in self.variants.items():
            with self.subTest(name=name):
                module.search.assert_not_called()

    def test_word_with_no_synonyms_is_retained(self):
        for name, module in self.variants.items():
            with self.subTest(name=name):
                self.assertEqual(module.get_all_combinations(['quuxword'], {'quuxword': []}),
                                 [('quuxword',)])

    def test_combinations_keep_originals_and_are_unique_and_ordered(self):
        for name, module in self.variants.items():
            with self.subTest(name=name):
                self.assertEqual(module.get_all_combinations(
                    ['cat', 'home'], {'cat': ['feline', 'feline'], 'home': []}),
                    [('cat', 'home'), ('feline', 'home')])

    def test_empty_input_has_no_combinations(self):
        for name, module in self.variants.items():
            with self.subTest(name=name):
                self.assertEqual(module.get_all_combinations([], {}), [])

    def test_unknown_spelling_without_correction_keeps_word(self):
        for name, module in self.variants.items():
            with self.subTest(name=name), \
                    mock.patch.object(module.spell, 'unknown', return_value={'zzqv'}), \
                    mock.patch.object(module.spell, 'correction', return_value=None):
                self.assertEqual(module.check_spelling(['zzqv']), ['zzqv'])

    def test_spelling_correction_is_used(self):
        for name, module in self.variants.items():
            with self.subTest(name=name), \
                    mock.patch.object(module.spell, 'unknown', return_value={'helo'}), \
                    mock.patch.object(module.spell, 'correction', return_value='hello'), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.check_spelling(['helo', 'world']), ['hello', 'world'])

    def test_large_expansion_is_rejected_before_materialization(self):
        for name, module in self.variants.items():
            with self.subTest(name=name), mock.patch.object(module.itertools, 'product') as product:
                with self.assertRaisesRegex(ValueError, 'limit: 100'):
                    module.get_all_combinations(['a', 'b'],
                                                {'a': [str(i) for i in range(10)],
                                                 'b': [str(i) for i in range(10)]})
                product.assert_not_called()

    def test_limit_boundary_and_invalid_limit(self):
        for name, module in self.variants.items():
            with self.subTest(name=name):
                self.assertEqual(len(module.get_all_combinations(['a'], {'a': ['b']}, 2)), 2)
                with self.assertRaises(ValueError):
                    module.get_all_combinations(['a'], {}, 0)

    def test_empty_main_does_not_search(self):
        for name, module in self.variants.items():
            with self.subTest(name=name), \
                    mock.patch.object(module, 'process_user_input', return_value=([], {})), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                module.main()
                module.search.assert_not_called()
                self.assertIn('No words supplied', output.getvalue())

    def test_over_limit_main_does_not_search(self):
        for name, module in self.variants.items():
            with self.subTest(name=name), \
                    mock.patch.object(module, 'process_user_input', return_value=(['a', 'b'], {})), \
                    mock.patch.object(module, 'search_wordnet', return_value=[str(i) for i in range(10)]), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                module.main()
                module.search.assert_not_called()
                self.assertIn('Too many search combinations', output.getvalue())

    def test_no_synonyms_still_searches_original_query(self):
        for name, module in self.variants.items():
            with self.subTest(name=name), \
                    mock.patch.object(module, 'process_user_input', return_value=(['puzzle'], {})), \
                    mock.patch.object(module, 'search_wordnet', return_value=[]), \
                    mock.patch.object(module, 'search', return_value=['https://example.com/']) as search, \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                module.main()
                search.assert_called_once_with('puzzle', num_results=1)
                self.assertIn('https://example.com/', output.getvalue())

    def test_csv_cells_are_collected_as_words(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'words.csv'
            path.write_text('craft,puzzle\n"word game",art\n', encoding='utf-8')
            for name, module in self.variants.items():
                with self.subTest(name=name):
                    words, _ = module.split_string(module.load_words_from_file(path))
                    self.assertEqual(words, ['craft', 'puzzle', 'word', 'game', 'art'])


class GoogleSearchTests(unittest.TestCase):
    def test_import_does_not_search(self):
        module = load_script('googleSearch/googleSearch.py')
        module.search.assert_not_called()

    def test_eof_exits_without_search(self):
        module = load_script('googleSearch/googleSearch.py')
        with mock.patch('builtins.input', side_effect=EOFError), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            module.main()
        module.search.assert_not_called()
        self.assertIn('Program terminating', output.getvalue())

    def test_blank_and_exit_input_do_not_search_or_sleep(self):
        module = load_script('googleSearch/googleSearch.py')
        with mock.patch('builtins.input', side_effect=['  ', ' exit() ']), \
                mock.patch.object(module.time, 'sleep') as sleep, \
                contextlib.redirect_stdout(io.StringIO()):
            module.main()
        module.search.assert_not_called()
        sleep.assert_not_called()

    def test_query_then_eof_prints_results_and_terminates(self):
        module = load_script('googleSearch/googleSearch.py')
        with mock.patch('builtins.input', side_effect=['  craft  ', EOFError]), \
                mock.patch.object(module, 'search', return_value=['result']) as search, \
                mock.patch.object(module.time, 'sleep') as sleep, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            module.main()
        search.assert_called_once_with('craft', advanced=True)
        sleep.assert_called_once()
        self.assertIn('result', output.getvalue())
        self.assertIn('Program terminating', output.getvalue())


if __name__ == '__main__':
    unittest.main()
