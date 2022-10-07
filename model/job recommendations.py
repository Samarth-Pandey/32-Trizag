import pandas as pd
import numpy as np
import nltk
import pickle

df= pd.read_excel(r"dataset/job/JOBDATASET.xlsx")
df.head()
df.style.format({'Percentage': "{:.1f}"})
df.head()

df.isnull().sum()
cols = ['Job_Roles']+['Graduation']+ ['Graduation_Stream']+['Technical/Business_Skills']+['Percentage']+['Applicant_Id']+['Interests']+['Administrative_Skills']
df1 =df[cols]
df1["text"] = df1["Graduation"].map(str)+" "+ df1["Graduation_Stream"] +" "+ df1["Technical/Business_Skills"]+" "+df1["Interests"]+" "+df1["Administrative_Skills"]
#initializing tfidf vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

tfidf_jobid = tfidf_vectorizer.fit_transform((df1['text'])) #fitting and transforming the vector
tfidf_jobid

cols2 = ['Applicant_Id']+ ['Job_Roles']+['Percentage']+['text']
df_final =df1[cols2]

with open (r'pickle/job/dataset.pickle', 'wb') as ptr:
  pickle.dump(df_final, ptr)

with open (r'pickle/job/vector.pickle', 'wb') as ptr1:
  pickle.dump(tfidf_vectorizer, ptr1)

with open (r'pickle/job/recommendation.pickle', 'wb') as ptr2:
  pickle.dump(tfidf_jobid, ptr2)

#Sort and create text files for dropdown menu of streamlit
lst = [x for xs in df1['Interests'] for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')])) 

with open(r'data\job\interest.txt', 'w') as interesttxt:
  interesttxt.write(','.join(finalList))

lst = [x for xs in df1['Graduation'] for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')])) 

with open(r'data\job\grad.txt', 'w') as gradtxt:
  gradtxt.write(','.join(finalList))

lst = [x for xs in df1['Graduation_Stream'] for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')])) 

with open(r'data\job\gradstream.txt', 'w') as gradstream:
  gradstream.write(','.join(finalList))

lst = [x for xs in df1['Technical/Business_Skills'] for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')])) 

with open(r'data\job\skills.txt', 'w') as skills:
  skills.write(','.join(finalList))

lst = [x for xs in df1['Administrative_Skills'] for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')])) 

with open(r'data\job\adminskills.txt', 'w') as skills:
  skills.write(','.join(finalList))