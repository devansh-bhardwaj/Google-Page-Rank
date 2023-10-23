import sys

N = None

def final_mapper():
    for line in sys.stdin:
        line = line.strip()
        if line[0] == '#':
            continue

        if len(line.split()) == 1:
            print('\t%s' % line)
            continue

        node, val = line.split()
        
        try:
            score = int(val)
            print('%s\t1' % node)
            print('%s\t1' % val)
        except:
            print('%s\t%s' % (node[:-2], val))

def final_reducer():
    sum = None
    increment = None
    current_node = None
    current_score = None
  
    for line in sys.stdin:
        line = line.strip()
        if len(line.split()) == 1:
            sum = float(line)
            increment = (1 - sum) / N
            continue

        node, score = line.split()

        if current_node == node:
            if score != '1':
                current_score = float(score)
        else:
            if current_score is not None:
                print('%s\t%s' % (current_node, current_score))
                current_score = None
            elif current_node is not None:
                print('%s\t%s' % (current_node, increment))

            if score != '1':
                current_score = float(score)

            current_node = node

if __name__ == '__main__':
    stage = sys.argv[1]

    if len(sys.argv) > 2:
    	N = int(sys.argv[2])

    func = getattr(sys.modules[__name__], stage)
    func()
  
  