import pandas as pd
import matplotlib.pyplot as plt


def standardize_test_knight():
    data = pd.read_csv("../Test_knight.csv")
    mean = data.mean()
    std = data.std()
    standardized_data = (data - mean) / std
    plt.scatter(standardized_data["Empowered"],
                standardized_data["Stims"], alpha=0.4,
                color='green')

    plt.show()

    print(standardized_data)


def standardize_train_knight():
    raw_data = pd.read_csv("../Train_knight.csv")
    data = raw_data.drop(columns=["knight"])
    mean = data.mean()
    std = data.std()
    lol = (data - mean) / std

    standardized_data = lol.join(raw_data["knight"])

    jedi_knight_data = standardized_data[standardized_data["knight"] == "Jedi"]
    sith_knight_data = standardized_data[standardized_data["knight"] == "Sith"]
    plt.scatter(jedi_knight_data["Empowered"],
                jedi_knight_data["Stims"], alpha=0.4,
                color='blue', label="Jedi")
    plt.scatter(sith_knight_data["Empowered"],
                sith_knight_data["Stims"], alpha=0.4,
                color='red', label="Sith")
    plt.xlabel("Empowered")
    plt.ylabel("Stims")
    plt.legend(loc='upper left')

    plt.ylim(-1.99, 4.8)
    plt.xlim(-1.99, 2.99)

    plt.show()

    print(standardized_data)


def main():
    standardize_test_knight()
    standardize_train_knight()


if __name__ == "__main__":
    main()
