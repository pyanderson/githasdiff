#!/usr/bin/env python
import argparse
import json
import os
from subprocess import check_output
from fnmatch import fnmatch


def get_files():
    '''Get all changed files.'''
    cmd = ['git', 'diff', 'HEAD~', '--name-only']
    return [n for n in check_output(cmd).decode('utf-8').split('\n') if n]


def load_patterns(name, patterns_path='.githasdiff.json'):
    with open(patterns_path, 'r') as jfile:
        data = json.load(jfile)
    include = data.get(name, {}).get('include', []) + data.get('include', [])
    exclude = data.get(name, {}).get('exclude', []) + data.get('exclude', [])
    if len(include) == 0:
        include = ['*']
    return include, exclude


def has_diff(files, include, exclude):
    files = [n for n in files if not any(fnmatch(n, p) for p in exclude)]
    return any(fnmatch(n, p) for n in files for p in include)


def run(name, command='', patterns_path='.githasdiff.json'):
    files = get_files()
    try:
        include, exclude = load_patterns(name, patterns_path)
    except FileNotFoundError:
        include, exclude = [], []
    if has_diff(files, include, exclude):
        print('has diff!')
        if command:
            print('running command: ' + command)
            return os.system(command) >> 8
        return 0
    print('has not diff!')
    if command:
        return 0
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search for changes.')
    parser.add_argument('project')
    args, command = parser.parse_known_args()
    patterns_path = os.getenv('GITHASDIFF_FILE', '.githasdiff.json')
    exit(run(args.project, ' '.join(command), patterns_path))
