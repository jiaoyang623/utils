import os

path_options = {
    '-p': lambda value: os.path.abspath(value),
    '-P': lambda value: os.path.dirname(os.path.abspath(value))
}


def get_path(opts):
    path = ''
    for op, value in opts:
        if op in path_options:
            path = path_options[op](value)
    return path
