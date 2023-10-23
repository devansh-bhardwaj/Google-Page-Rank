import sys

N = None
beta = None

def combine_reducer():
    
    degree = 0
    score = 0
      
    for line in sys.stdin:

        line = line.strip()
        node, value = line.split()

        if node[-1] == 'a':
            degree = int(value)
            continue

        if node[-1] == 'b':
            score = float(value)
            continue

        increment = beta * (score / degree)

        print('%s\t%s' % (value, increment))

def add_mapper():

    sum = 0
  
    for line in sys.stdin:

        line = line.strip()
        node, increment = line.split()
        sum += float(increment)
        print('%s\t%s' % (node, increment))

    print('\t%s' % sum)

def add_reducer():

    current_node = None
    current_score = 0
    sum = None

    for line in sys.stdin:

        line = line.strip()

        if len(line.split()) == 1:
            sum = float(line)
            continue

        node, score = line.split()
        score = float(score)
  
        if current_node == node:
            current_score += score
        else:
            if current_node:
                current_score += (1 - sum) / N
                print ('%sb1\t%s' % (current_node, current_score))
            current_score = score
            current_node = node
  
    if current_node == node:
        current_score += (1 - sum) / N
        print ('%sb1\t%s' % (current_node, current_score))

    print('\t%s' % sum)

def score_reducer():

    current_node = None
    flag = 0
  
    for line in sys.stdin:

        line = line.strip()

        if len(line.split()) == 1:
            continue

        node, score = line.split()

        if node[-1] == '1' and flag == 0:
            continue

        if node[-1] == 'b' and flag == 0:
            current_node = node[:-1]
            flag = 1
            continue

        if node[-1] == '1' and flag == 1:
            if node[:-2] == current_node:
                print('%sb\t%s' % (current_node, score))
                flag = 0
                continue
            else:
                print('%sb\t0' % current_node)
                flag = 0
                continue

        if node[-1] == 'b' and flag == 1:
            print('%sb\t0' % current_node)
            current_node = node[:-1]

if __name__ == '__main__':

    stage = sys.argv[1]

    if len(sys.argv) > 2:
    	try:
    		N = int(sys.argv[2])
    	except:
    		beta = float(sys.argv[2])

    func = getattr(sys.modules[__name__], stage)
    func()

 
