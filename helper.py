import datetime
# from rouge_score import rouge_scorer
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score

def format_time(elapsed):
    return str(datetime.timedelta(seconds=int(round((elapsed)))))

def rouge(predicted, ground):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)
    return scorer.score(predicted, ground)

def ci95(column):
    stddev = np.std(column) 
    sqrtn = np.sqrt(len(column))
    return 1.960*(stddev/sqrtn)

def avgs_ci(csv):
    df = pd.read_csv(csv)
    print("mean")
    print(df.mean(axis=0))
    print("95 percent confidence interval")
    print(df.apply(ci95,axis=0))

def avg_evals(csvs):
    question_list = []
    fluency_list = []

    for i, csvlist in enumerate(csvs):
        df1 = pd.read_csv(csvlist[0]) 
        df2 = pd.read_csv(csvlist[1]) 

        avg_question = (df1["question_score"] + df2["question_score"])/2
        avg_fluency = (df1["fluency_score"] + df2["fluency_score"])/2
        
        question_list.append(avg_question)
        fluency_list.append(avg_fluency)

    questions = pd.concat(question_list)
    fluency = pd.concat(fluency_list)

    print(questions.mean())
    print(fluency.mean())


def agreements(csvs):
    annotator1_list = []
    annotator2_list = []

    for i, csvlist in enumerate(csvs):
        df1 = pd.read_csv(csvlist[0]) 
        df2 = pd.read_csv(csvlist[1]) 

        annotator1_list.append(df1)
        annotator2_list.append(df2)

    annotator1 = pd.concat(annotator1_list)
    annotator2 = pd.concat(annotator2_list)

    print("question score")
    same = annotator1["question_score"].values==annotator2["question_score"].values
    raw_agreement = list(same).count(True) / len(annotator1["question_score"])
    # print(raw_agreement)

    cohens = cohen_kappa_score(annotator1["question_score"], annotator2["question_score"], weights="linear")
    print(cohens)

    print("fluency")
    same = annotator1["fluency_score"].values==annotator2["fluency_score"].values
    raw_agreement = list(same).count(True) / len(annotator1["fluency_score"])
    # print(raw_agreement)

    cohens = cohen_kappa_score(annotator1["fluency_score"], annotator2["fluency_score"], weights="linear")
    print(cohens)


if __name__=='__main__':
    # score = rouge("I have a dry cough. Could I have COVID-19?In brief:   Fever, dry cough, headache, body aches.   If you have access to testing you can do that.   Would you like to video or text chat with me?", 
    #     "Perhaps. If you have access to testing, you should do that.")
    # print(score)

    # avgs_ci("/Users/kavery/Documents/rouge_prefix.csv")

    avg_evals([["/Users/kavery/Downloads/processed_baselines/baseline1_kate.csv", 
                "/Users/kavery/Downloads/processed_baselines/baseline1_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline2_kate.csv", 
              "/Users/kavery/Downloads/processed_baselines/baseline2_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline3_kate.csv",
              "/Users/kavery/Downloads/processed_baselines/baseline3_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline4_kate.csv",
              "/Users/kavery/Downloads/processed_baselines/baseline4_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline5_kate.csv",
              "/Users/kavery/Downloads/processed_baselines/baseline5_teo.csv"]]
              )

    agreements([["/Users/kavery/Downloads/processed_baselines/baseline1_kate.csv", 
                "/Users/kavery/Downloads/processed_baselines/baseline1_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline2_kate.csv", 
              "/Users/kavery/Downloads/processed_baselines/baseline2_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline3_kate.csv",
              "/Users/kavery/Downloads/processed_baselines/baseline3_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline4_kate.csv",
              "/Users/kavery/Downloads/processed_baselines/baseline4_mina.csv"], \
              ["/Users/kavery/Downloads/processed_baselines/baseline5_kate.csv",
              "/Users/kavery/Downloads/processed_baselines/baseline5_teo.csv"]]
              )