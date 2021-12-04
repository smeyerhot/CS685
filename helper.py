import datetime
from rouge_score import rouge_scorer

def format_time(elapsed):
    return str(datetime.timedelta(seconds=int(round((elapsed)))))

def rouge(predicted, ground):
    scorer = rouge_scorer.RougeScorer(['rougeL', 'rougeLsum'], use_stemmer=True)
    return scorer.score(predicted, ground)

if __name__=='__main__':
    score = rouge("I have a dry cough. Could I have COVID-19?In brief:   Fever, dry cough, headache, body aches.   If you have access to testing you can do that.   Would you like to video or text chat with me?", 
        "Perhaps. If you have access to testing, you should do that.")
    print(score)