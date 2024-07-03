import pandas as pd
import matplotlib.pyplot as plt


def main():
    plot_jedi_info()
    plot_knight_info()


def plot_jedi_info():
    jedi_data = pd.read_csv("../Test_knight.csv")

    plt.clf()
    plt.scatter(jedi_data["Empowered"],
                jedi_data["Stims"], alpha=0.4, color='green')
    plt.xlabel("Empowered")
    plt.ylabel("Stims")
    plt.legend(["Knight"])
    plt.show()

    plt.clf()
    plt.scatter(jedi_data["Push"], jedi_data["Deflection"],
                alpha=0.4, color='green')
    plt.xlabel("Push")
    plt.ylabel("Deflection")
    plt.legend(["Knight"])

    plt.ylim(0.007, 0.082)
    plt.xlim(0.3, 3.9)

    plt.show()


def plot_knight_info():
    knight_data = pd.read_csv("../Train_knight.csv")

    plt.clf()
    jedi_knight_data = knight_data[knight_data["knight"] == "Jedi"]
    sith_knight_data = knight_data[knight_data["knight"] == "Sith"]
    plt.scatter(jedi_knight_data["Empowered"],
                jedi_knight_data["Stims"], alpha=0.4, color='blue', label="Jedi")
    plt.scatter(sith_knight_data["Empowered"],
                sith_knight_data["Stims"], alpha=0.4, color='red', label="Sith")
    plt.xlabel("Empowered")
    plt.ylabel("Stims")
    plt.legend()
    plt.show()

    plt.clf()
    plt.scatter(jedi_knight_data["Push"],
                jedi_knight_data["Deflection"], alpha=0.4, color='blue', label="Jedi")
    plt.scatter(sith_knight_data["Push"],
                sith_knight_data["Deflection"], alpha=0.4, color='red', label="Sith")
    plt.xlabel("Push")
    plt.ylabel("Deflection")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
