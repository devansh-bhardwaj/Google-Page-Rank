import sys

N = None
initial_score = None

def degree_mapper():
    for line in sys.stdin:
        line = line.strip()

        if line[0] != '#':
            from_node = line.split()[0]
            print('%s\t1' % from_node)


def degree_reducer():
    current_node = None
    current_count = 0
    node = None

    for line in sys.stdin:
        line = line.strip()
        node, count = line.split()
        count = int(count)

        if current_node == node:
            current_count += count
        else:
            if current_node:
                print('%sa\t%s' % (current_node, current_count))
            current_count = count
            current_node = node

    if current_node == node:
        print('%sa\t%s' % (current_node, current_count))


def score_mapper():
    for line in sys.stdin:
        line = line.strip()

        if line[0] != '#':
            from_node, to_node = line.split()
            print('%s' % from_node)


def score_reducer():
    current_node = None
    node = None

    for line in sys.stdin:
        node = line.strip()

        if current_node == node:
            continue
        else:
            if current_node:
                print('%sb\t%s' % (current_node, initial_score))
            current_node = node

    if current_node == node:
        print('%sb\t%s' % (current_node, initial_score))


def edge_mapper():
    for line in sys.stdin:
        line = line.strip()

        if line[0] != '#':
            from_node, to_node = line.split()
            print('%s\t%s' % (from_node, to_node))


def edge_reducer():
    for line in sys.stdin:
        line = line.strip()
        from_node, to_node = line.split()
        print('%sc\t%s' % (from_node, to_node))


if __name__ == '__main__':
    stage = sys.argv[1]

    if len(sys.argv) > 2:
    	N = int(sys.argv[2])
    	initial_score = 1/N

    func = getattr(sys.modules[__name__], stage)
    func()

