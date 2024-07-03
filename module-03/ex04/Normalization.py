import pandas as pd
import matplotlib.pyplot as plt


def main():
	files = ["../Test_knight.csv", "../Train_knight.csv"]

	for file in files:
		raw_data = pd.read_csv(file)
		data = raw_data

		has_knight = False
		if "knight" in data.columns.values:
			has_knight = True
			data = data.drop(columns=["knight"])

		normalized_data = (data - data.min()) / (data.max() - data.min())

		plt.clf()
		if has_knight:
			normalized_data = normalized_data.join(raw_data["knight"])

			jedi_knight_data = normalized_data[normalized_data["knight"] == "Jedi"]
			sith_knight_data = normalized_data[normalized_data["knight"] == "Sith"]

			plt.scatter(jedi_knight_data["Push"],
						jedi_knight_data["Deflection"], alpha=0.4, color='blue', label='Jedi')
			plt.scatter(sith_knight_data["Push"],
						sith_knight_data["Deflection"], alpha=0.4, color='red', label='Sith')

			plt.xlabel('Push')
			plt.ylabel('Deflection')
			plt.legend()

			plt.show()
		else:
			plt.scatter(normalized_data['Empowered'],
						normalized_data['Stims'], alpha=0.4,
						color='green')
			plt.show()

		print(normalized_data)


if __name__ == '__main__':
	main()
