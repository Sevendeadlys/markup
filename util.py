#coding=utf-8


def lines(f):
    for line in f:
        yield line
    yield '\n'


def blocks(f):
    block = []
    for line in lines(f):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []