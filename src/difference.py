import sys

def diff_mapper():
    for line in sys.stdin:
        line = line.strip()
        node, score = line.split()
        print('%s\t%s\t1' % (node, score))

def diff_reducer():
    diff = 0
    prev = None
    flag = 0
  
    for line in sys.stdin:
        line = line.strip()
        if line == '_':
            continue
        score = line.split()[1]
        if flag == 0:
            prev = float(score)
            flag = 1
        else:
            diff += abs(prev - float(score))
            flag = 0

    print(diff)

if __name__ == '__main__':
    stage = sys.argv[1]
    func = getattr(sys.modules[__name__], stage)
    func()
   
