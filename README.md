# CS685-Project

## How To Run the Notebooks

Our suggestion for running the code in this repository is to use google drive for desktop https://www.google.com/drive/download/ and enable streaming. You can then open your google drive folder in terminal and clone this repo. At this point you can then go to google drive in browser and open any of the notebooks by double clicking on them.  You will now need to download the file med_dialogue_sample.pickle from the following  https://drive.google.com/drive/folders/1mvsW-300yjhgwLZHSDDpEVWapx74l0Hb and place it in the project directory. You can now start running any of the notebooks via the Run All command. Near the top will be a cell that changes directory in your google drive. We stored our project in /UMass/CS685 but you can update this to whatever you choose.


## Evaluation instructions
We will hand-evaluate the model on how well it answered the question and how fluent the answers were. 

| Question Answering  |  |
| -------- | -------- | 
| 5 | The question is generally answered.  | 
| 4 | The answer is somewhat related to the question and COVID-19/respiratory illness, and it makes logical sense.  | 
| 3 | The answer is not related to the question, but it is about COVID-19/respiratory illness and makes logical sense. OR It answers the question and makes sense but gives bad advice. | 
| 2 | The answer is somewhat related to the question or COVID-19/respiratory illness, but it does not make logical sense.  | 
| 1 | The answer is unrelated to the question and does not make logical sense.  | 

Examples: 

Question: I have a dry cough. Could I have COVID-19?
Answer: Perhaps. If you have access to testing you can do that. Would you like to video or text chat with me?
Rating: 5 (answers the question)

Question: I have a dry cough. Could I have COVID-19?
Answer: If you have access to testing you can do that.
Rating: 4 (doesn't quite answer the question but makes a reasonable suggestion; is nearly a 5)

Question: I have a dry cough. Could I have COVID-19?
Answer: I woke up with a cough and fever. I haven't had contact with anyone with COVID-19 could I have COVID-19 could I have COVID-19 could I have COVID-19 ... 
Rating: 3 (not related to the question but related to COVID-19; thinks it's a patient but makes sense)

Question: I have a dry cough. Could I have COVID-19?
Answer: COVID-19 is an infectious disease cause by SARS-CoV-2.
Rating: 3 (not related to the question but related to COVID-19; makes sense)

Question: I have a dry cough. Could I have COVID-19?
Answer: No, of course not. It's just a cold.
Rating: 3 (answers the question but gives bad advice)

Question: I have a dry cough. Could I have COVID-19?
Answer: Cough respiratory COVID respiratory disease testing testing testing testing ...
Rating: 2 (clearly related to COVID-19, but does not make any sense)

Question: I have a dry cough. Could I have COVID-19?
Answer: In brief: your daughter has COVID because of asthma she got from a polar bear
Rating: 2 (clearly related to COVID-19, but does not make sense, though it is more fluent than the above example)

Question: I have a dry cough. Could I have COVID-19?
Answer: pandas pandas pandas bears bears polar polar polar ...
Rating: 1 (unrelated to the question or COVID and doesn't make sense)


| Fluency  |  |
| -------- | -------- | 
| 5 | flawless English  | 
| 4 | good English  | 
| 3 | non-native English  | 
| 2 | disfluent English  | 
| 1 | incomprehensible  | 

Examples: 

Question: I have a dry cough. Could I have COVID-19?
Answer: Perhaps. If you have access to testing, you can do that. Would you like to video or text chat with me?
Rating: 5 

Question: I have a dry cough. Could I have COVID-19?
Answer: Perhaps. If testing access is there, that can be done by you. Video or text chat with me?
Rating: 4 

Question: I have a dry cough. Could I have COVID-19?
Answer: Perhaps. If testing is present for access there where you are, that can be done by you. Video or text chat
Rating: 3

Question: I have a dry cough. Could I have COVID-19?
Answer: Perhaps do testing do testing if as present or if as accessible.  text chat?.,
Rating: 2

Question: I have a dry cough. Could I have COVID-19?
Answer: video text testing present testing video video video ...
Rating: 1 
