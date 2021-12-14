import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def loss_curves(df_stats):
    # Use plot styling from seaborn.
    sns.set(style='darkgrid')

    # Increase the plot size and font size.
    sns.set(font_scale=1.5)
    plt.rcParams["figure.figsize"] = (12,6)

    # Plot the learning curve.
    plt.plot(df_stats['Training Loss'], 'b-o', label="Training")
    plt.plot(df_stats['Valid. Loss'], 'g-o', label="Validation")

    # Label the plot.
    plt.title("Training & Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.xticks([0, 1, 2, 3])
    plt.yticks([0, 0.5, 1.0, 1.5])

    plt.show()

def plot_loss_csvs(csvs):
    training = pd.DataFrame()
    validation = pd.DataFrame()
    for i, csv in enumerate(csvs):
        df = pd.read_csv(csv)
        print(df.head())
        print(df.columns)
        training[str(i)] = df["training"]
        validation[str(i)] = df[" validation"]
    
    training['mean'] = training.mean(axis=1)
    validation['mean'] = validation.mean(axis=1)
    stats = pd.DataFrame()
    stats["Training Loss"] = training["mean"]
    stats["Valid. Loss"] = validation["mean"]
    
    print(training)
    print(validation)

    loss_curves(stats)

if __name__=='__main__':
    plot_loss_csvs(["/Users/kavery/Downloads/loss/decoder1_loss.csv", \
                    "/Users/kavery/Downloads/loss/decoder2_loss.csv", \
                    "/Users/kavery/Downloads/loss/decoder3_loss.csv", \
                    "/Users/kavery/Downloads/loss/decoder4_loss.csv", \
                    "/Users/kavery/Downloads/loss/decoder5_loss.csv" ])

    plot_loss_csvs(["/Users/kavery/Downloads/loss/prefix1_loss.csv", \
                    "/Users/kavery/Downloads/loss/prefix2_loss.csv", \
                    "/Users/kavery/Downloads/loss/prefix3_loss.csv", \
                    "/Users/kavery/Downloads/loss/prefix4_loss.csv", \
                    "/Users/kavery/Downloads/loss/prefix5_loss.csv" ])