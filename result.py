import os
import sys
import matplotlib.pyplot as plt

difference_path = "output/difference"
threshold = None

def extract_num(filename):
	return int(filename[4:-4])

def plot_difference():
	differences = []
	
	for filename in sorted(os.listdir(difference_path), key = extract_num):
		with open(difference_path + '/' + filename, "r") as file:
			difference = file.read().strip()
			differences.append(float(difference))

	iterations = len(differences)+1

	plt.plot(range(2, iterations + 1), differences, marker = 'o', linestyle = '-')
	plt.axhline(y = threshold, color = 'r', linestyle = 'dashed', label = "threshold")
	plt.xticks(range(2, iterations + 1))

	plt.xlabel("Iteration")
	plt.ylabel("Difference")
	plt.title("Converging Difference")
	plt.legend()
	
	plt.savefig("results/convergence.png")	
	plt.close()


if __name__ == '__main__':
    threshold = float(sys.argv[1])
    plot_difference()
