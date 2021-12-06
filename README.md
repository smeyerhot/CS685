# CS685-Project

## Evaluation instructions
We will hand-evaluate the model on how well it answered the question and how fluent the answers were. 

| Question Answering  | 
| -------- | -------- | 
| 5 | The question is generally answered.  | 
| 4 | The answer is somewhat related to the question and COVID-19, and it makes logical sense.  | 
| 3 | The answer is not related to the question, but it is about COVID-19 and makes logical sense.  | 
| 2 | The answer is somewhat related to the question or COVID-19, but it does not make logical sense.  | 
| 1 | The answer is unrelated to the question and does not make logical sense.  | 

Examples: 

Question: I have a dry cough. Could I have COVID-19?
Answer: Perhaps. If you have access to testing you can do that. Would you like to video or text chat with me?
Rating: 5 (answers the question)

Question: I have a dry cough. Could I have COVID-19?
Answer: Some symptoms of COVID-19 include fever, dry cough, headache, body aches.
Rating: 4 (doesn't quite answer the question but gives an answer related to the question)

Question: I have a dry cough. Could I have COVID-19?
Answer: I woke up with a cough and fever. I haven't had contact with anyone with COVID-19 could I have COVID-19 could I have COVID-19 could I have COVID-19 ... 
Rating: 3 (not related to the question but related to COVID-19; thinks it's a patient but makes sense)

Question: I have a dry cough. Could I have COVID-19?
Answer: Cough respiratory COVID respiratory disease testing do testing
Rating: 2 (clearly related to COVID-19, but does not make any sense)

Question: I have a dry cough. Could I have COVID-19?
Answer: ..
Rating: 1 (unrelated to the question or COVID and doesn't make sense)


| Fluency  | 
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
Answer: Perhaps do testing if as present or if as accessible.  text chat?.,
Rating: 2

Question: I have a dry cough. Could I have COVID-19?
Answer: video text testing present 
Rating: 1 
