import pandas as pd
import numpy as np
import nltk
import pickle
df= pd.read_excel(r"dataset\masters\New Masters Dataset.xlsx")
df.style.format({'Percentage': "{:.1f}"})
print(df.nunique())
df.info()
df.isnull().sum()
df.isnull().sum()
cols = ['Post_Graduation']+['Graduation']+ ['Graduation_Stream']+['Percentage']+['Applicant_Id']+['Interests']
df1 =df[cols]
df1["text"] = df1["Graduation"].map(str)+" "+ df1["Graduation_Stream"] +" "+df1["Interests"]
df1.info()

#initializing tfidf vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_jobid = tfidf_vectorizer.fit_transform((df1['text']).values.astype('U')) #fitting and transforming the vector
tfidf_jobid
cols2 = ['Applicant_Id']+ ['Post_Graduation']+['Percentage']+['text']
df_final =df1[cols2]

with open (r'pickle\masters\dataset-masters.pickle', 'wb') as ptr:
  pickle.dump(df_final, ptr)

with open (r'pickle\masters\vector-masters.pickle', 'wb') as ptr1:
  pickle.dump(tfidf_vectorizer, ptr1)

with open (r'pickle\masters\recommendation-master.pickle', 'wb') as ptr2:
  pickle.dump(tfidf_jobid, ptr2)


#Sort and create text files for dropdown menu of streamlit
lst = [x for xs in df1['Graduation'] for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')]))

with open(r'data\masters\grad_masters.txt', 'w') as gradtxt:
  gradtxt.write(','.join(finalList))

lst = [x for xs in df1['Interests'] for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')]))

with open(r'data\masters\interest_master.txt', 'w') as interesttxt:
  interesttxt.write(','.join(finalList))

lst = [x for xs in df1['Graduation_Stream'].astype(str) for x in xs.split(';')]
finalList = sorted(set([x.title().strip() for xs in lst for x in xs.split(',')]))

with open(r'data\masters\gradstreammaster.txt', 'w') as grad_stream:
  grad_stream.write(','.join(finalList))




