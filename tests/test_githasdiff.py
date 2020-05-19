import unittest
from unittest.mock import patch

# local imports
from githasdiff import has_diff, load_patterns, run


class TestFunctions(unittest.TestCase):
    def test_load_patterns(self):
        include, exclude = load_patterns('project', 'tests/testdata/data.json')
        assert 'foo/*' in include
        assert '*.py' in include
        assert 'foo/tests/*' in exclude
        assert '*.md' in exclude
        assert '*.rst' in exclude

    def test_has_diff(self):
        include = ['foo/*']
        exclude = ['*.md', 'tests/*']
        assert has_diff(['foo/main.py'], include, exclude)
        assert has_diff(['foo/tests/test_foo.py'], include, exclude)
        assert not has_diff(['foo/READEME.md'], include, exclude)
        assert not has_diff(['tests/test_foo.py'], include, exclude)

    def test_run(self):
        with patch('githasdiff.get_files') as mock:
            mock.return_value = ['main.py']
            assert not run('project', patterns_path='tests/testdata/data.json')

    def test_run_with_command(self):
        with patch('githasdiff.get_files') as mock:
            mock.return_value = ['main.py']
            assert not run('project', 'ls', 'tests/testdata/data.json')
