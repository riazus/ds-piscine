import pandas as pd
import matplotlib.pyplot as plt


def main():
	df_plt = pd.read_csv('../Test_knight.csv')
	for column in df_plt.columns:
		df_plt[column].plot(kind='hist')
		plt.title(column)
		plt.show()
	df_graph = pd.read_csv('../Train_knight.csv')
	jedi_data = df_graph[df_graph['knight'] == 'Jedi']
	sith_data = df_graph[df_graph['knight'] == 'Sith']
	
	for column in df_graph.columns:
		plt.hist(jedi_data[column], alpha=0.5, label='Jedi')
		plt.hist(sith_data[column], alpha=0.5, label='Sith')
		plt.title(column)
		plt.legend()
		plt.show()


if __name__ == '__main__':
	main()
