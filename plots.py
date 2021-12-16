import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from helper import avgs_ci

def loss_curves(df_stats, names):
    # Use plot styling from seaborn.
    sns.set(style='darkgrid')

    # Increase the plot size and font size.
    sns.set(font_scale=1.5)
    plt.rcParams["figure.figsize"] = (12,6)

    # Plot the learning curve.
    plt.plot(df_stats['Training Loss'], 'b-o', label="Training")
    plt.plot(df_stats['Valid. Loss'], 'g-o', label="Validation")

    # Label the plot.
    plt.title(names + " - Training & Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.xticks([0, 1, 2, 3, 4])
    plt.yticks([0, 0.5, 1.0, 1.5])

    plt.show()

def rouge(df_list, rouge_type):
    all_dfs = pd.concat(df_list, axis=1)
    cols = [
        rouge_type+"_precision_base", rouge_type+"_precision_lm", rouge_type+"_precision_prefix_lm", rouge_type+"_precision_similarity",
        rouge_type+"_recall_base", rouge_type+"_recall_lm", rouge_type+"_recall_prefix_lm", rouge_type+"_recall_similarity",
        rouge_type+"_fmeasure_base", rouge_type+"_fmeasure_lm", rouge_type+"_fmeasure_prefix_lm", rouge_type+"_fmeasure_similarity"
    ]
    all_dfs = all_dfs[cols]
    print(all_dfs.head())

    reds = [rouge_type+"_precision_base", rouge_type+"_precision_lm", rouge_type+"_precision_prefix_lm", rouge_type+"_precision_similarity"]
    purples = [rouge_type+"_fmeasure_base", rouge_type+"_fmeasure_lm", rouge_type+"_fmeasure_prefix_lm", rouge_type+"_fmeasure_similarity"]
    sns.set_theme(style="darkgrid")
    plt.xticks(rotation=90)
    plt.ylim(0,0.50)
    plt.subplots_adjust(bottom=0.35)
    pal = {col: "r" if col in reds else "purple" if col in purples else "b" for col in all_dfs.columns}
    ax = sns.pointplot(data=all_dfs, join=False, ci=95, palette=pal)
    plt.show()

def plot_loss_csvs(csvs, names):
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

    loss_curves(stats, names)

if __name__=='__main__':
    # plot_loss_csvs(["/Users/kavery/Downloads/loss/decoder1_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/decoder2_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/decoder3_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/decoder4_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/decoder5_loss.csv" ], "Regular LM")

    # plot_loss_csvs(["/Users/kavery/Downloads/loss/prefix1_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix2_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix3_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix4_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix5_loss.csv" ], "Prefix LM")
    
    # plot_loss_csvs(["/Users/kavery/Downloads/loss/prefix1_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix2_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix3_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix4_loss.csv", \
    #                 "/Users/kavery/Downloads/loss/prefix5_loss.csv" ], "Similarity Model")

    csvs = ["/Users/kavery/Documents/rouge_baseline.csv",
    "/Users/kavery/Documents/rouge_decoder.csv",
    "/Users/kavery/Documents/rouge_prefix.csv",
    "/Users/kavery/Documents/rouge_similarity.csv"]

    df_list = []
    for csv in csvs:
        df = pd.read_csv(csv)
        df_list.append(df)

    df_list[0] = df_list[0].add_suffix('_base')
    df_list[1] = df_list[1].add_suffix('_lm')
    df_list[2] = df_list[2].add_suffix('_prefix_lm')
    df_list[3] = df_list[3].add_suffix('_similarity')

    rouge(df_list, "rougeL")
    rouge(df_list, "rouge1")
    rouge(df_list, "rouge2")