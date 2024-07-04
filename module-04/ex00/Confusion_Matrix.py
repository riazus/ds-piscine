import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np


def calc_confusion_matrix(truth, pred):
	true_positive = 0
	true_negative = 0
	false_positive = 0
	false_negative = 0

	for i in range(len(truth)):
		if (pred[i] == "Jedi" and truth[i] == "Jedi"):
			true_positive += 1
		elif (pred[i] == "Sith" and truth[i] == "Sith"):
			true_negative += 1
		elif (pred[i] == "Jedi" and truth[i] == "Sith"):
			false_positive += 1
		elif (pred[i] == "Sith" and truth[i] == "Jedi"):
			false_negative += 1
	
	row1 = np.array([true_positive, false_negative])
	row2 = np.array([false_positive, true_negative])
	return np.array([row1, row2])


def main():
	def read_file(file_path):
		with open(file_path, "r") as file:
			return [line.strip() for line in file.readlines()]

	truth = read_file("../truth.txt")
	pred = read_file("../predictions.txt")

	res = calc_confusion_matrix(truth, pred)
	test = confusion_matrix(truth, pred, labels=["Jedi", "Sith"])

	print("Own is:", f"{res[0][0]} {res[0][1]}, {res[1][0]} {res[1][1]}")
	print("Original:", f"{test[0][0]} {test[0][1]}, {test[1][0]} {test[1][1]}")

	plt.figure(figsize=(10, 7))
	sns.heatmap(res, annot=True, fmt='d', cmap='Blues',
				xticklabels=["0", "1"], yticklabels=["1", "0"])
	plt.xlabel('Predicted labels')
	plt.ylabel('True labels')
	plt.show()


if __name__ == "__main__":
	main()
