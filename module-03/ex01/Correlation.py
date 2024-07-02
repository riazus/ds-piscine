import pandas as pd
import scipy.stats as stats


def main():
	df_plt = pd.read_csv('../Train_knight.csv')
	df_plt['knight'] = df_plt['knight'].map({'Jedi': 1, 'Sith': 0})
	
	correlations = {}
	for column in df_plt.columns:
		correlation, p_value = stats.pointbiserialr(df_plt['knight'], df_plt[column])
		correlations[column] = correlation
	
	sorted_correlations = dict(sorted(correlations.items(), key=lambda item: item[1], reverse=True))
	print(sorted_correlations)


if __name__ == '__main__':
	main()
