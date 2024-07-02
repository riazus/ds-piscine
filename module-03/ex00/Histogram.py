import pandas as pd
import matplotlib.pyplot as plt


def main():
	df = pd.read_csv('../Test_knight.csv')
	for column in df.columns:
		df[column].plot(kind='hist')
		plt.title(column)
		plt.show()


if __name__ == '__main__':
	main()
