import time
import streamlit as st
import pandas as pd
import pickle
import requests 
from streamlit_lottie import st_lottie 

userData=pd.DataFrame(columns = ['Graduation','Graduation_Stream','Percentage','Technical/BusinessSkills','Interests','Administrartive_Skills','text'])

with open('./data/job/grad.txt', 'r') as file:
    grad = file.read().split(',')
with open('./data/job/gradstream.txt', 'r') as file:
    stream = file.read().split(',')
with open('./data/job/skills.txt', 'r') as file:
    skill = file.read().split(',')
with open('./data/job/interest.txt', 'r') as file:
    interest = file.read().split(',')
with open('./data/job/adminskills.txt', 'r') as file:
    adminskill = file.read().split(',')

with open('./data/masters/grad_masters.txt', 'r') as file:
    grad_master = file.read().split(',')
with open('./data/masters/gradstreammaster.txt', 'r') as file:
    gradstreammaster = file.read().split(',')
with open('./data/masters/interest_master.txt', 'r') as file:
    interest_master = file.read().split(',')

st.set_page_config(page_title= "Career Path Reccomendation System" , layout = "wide")

def load_lottieurl(url):
  retries = 1
  success = False
  while not success:
    try:
        r = requests.get(url)
        success = True
        if r.status_code != 200:
          return None
        return r.json()
    except Exception as e:
        wait = retries * 30;
        time.sleep(wait)
        retries += 1


lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_o6spyjnc.json")

with st.container():
    left_column , right_column = st.columns(2)
    with left_column:
     st.title ("Career Recommendation Engine")
     st.subheader("Hi there :wave:")
     st.write("When you are not sure of what type of job you want or what you want to do next with your career, You can use our system to get recommendations according to your intrests and skillset. Our system can also help you to get recommendations for master's courses.")
    with right_column:
      st_lottie(lottie_coding, height=250, key="coding")

st.write("Before we proceed, let us get to know you better...")
st.write("---")
choice = st.radio('Choose your path', ['Job', 'Masters'])
if choice == 'Job':
  with open ('./pickle/job/dataset.pickle', 'rb') as ptr:
    df_final = pickle.load(ptr)

  with open ('./pickle/job/recommendation.pickle', 'rb') as ptr1:
    tfidf_jobid = pickle.load(ptr1)

  with open ('./pickle/job/vector.pickle', 'rb') as ptr2:
    vector = pickle.load(ptr2)

  def get_job_recommendation(userData, df_final):
    userData.at[0, 'text']=userData.iloc[0]["Graduation"]+" "+ userData.iloc[0]["Graduation_Stream"] +" "+userData.iloc[0]["Percentage"] +" "+ " ".join(userData.iloc[0]["Technical/BusinessSkills"])+ " ".join(userData.iloc[0]["Administrartive_Skills"])+" "+" ".join(userData.iloc[0]["Interests"])
    from sklearn.metrics.pairwise import cosine_similarity
    user_tfidf = vector.transform((userData['text']))
    cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x),tfidf_jobid)
    output2 = list(cos_similarity_tfidf)
    top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]
    recommendation = pd.DataFrame(columns = ['Job_Type'])
    rowNum = 0
    for i in top:
        recommendation.at[rowNum, 'Job_Type'] = df_final['Job_Roles'][i]
        rowNum += 1
    return recommendation

  with st.container():
      
      left_column, mid_col , right_column = st.columns([2.8, .5, 2])
      with left_column:
        userData.at[0,'Graduation']  = st.selectbox('Select your graduation degree', grad)

        userData.at[0,'Graduation_Stream'] = st.selectbox('Select your graduation stream', stream)

        userData.at[0,'Percentage'] = st.text_input('Enter your graduation percentage')

        userData.at[0,'Technical/BusinessSkills'] = st.multiselect("Select your Technical/Business skills", skill)

        userData.at[0,'Administrartive_Skills'] = st.multiselect("Select your administrative skills", adminskill)

        userData.at[0,'Interests'] =  st.multiselect("Select your interests", interest)
      st.write("##")
      if st.button('Get job recommendation'):
        with right_column:
            with st.spinner('Wait for it...'):
              st.write("Here are your top ten job recommendations")
              recommendations = get_job_recommendation(userData, df_final)
              for i in recommendations['Job_Type']:
                st.markdown('- **'+i.strip()+'**')
else:
  
  with open ('./pickle/masters/dataset-masters.pickle', 'rb') as ptr:
    df_final_master = pickle.load(ptr)

  with open ('./pickle/masters/recommendation-master.pickle', 'rb') as ptr1:
    tfidf_jobid_master = pickle.load(ptr1)

  with open ('./pickle/masters/vector-masters.pickle', 'rb') as ptr2:
    vector_master = pickle.load(ptr2)

  def get_masters_recommendation(userData, df_final):
    userData.at[0, 'text']=userData.iloc[0]["Graduation"]+" "+ userData.iloc[0]["Graduation_Stream"]+" "+userData.iloc[0]["Percentage"] +" " +" ".join(userData.iloc[0]["Interests"])
    from sklearn.metrics.pairwise import cosine_similarity
    user_tfidf = vector_master.transform((userData['text']))
    cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x),tfidf_jobid_master)
    output2 = list(cos_similarity_tfidf)
    top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]
    recommendation = pd.DataFrame(columns = ['masters_type'])
    rowNum = 0
    for i in top:
        recommendation.at[rowNum, 'masters_type'] = df_final_master['Post_Graduation'][i]
        rowNum += 1
    return recommendation

  with st.container():
      
      left_column, mid_col , right_column = st.columns([2.8, .5, 2])
      with left_column:
        userData.at[0,'Graduation']  = st.selectbox('Select your graduation degree', grad_master)

        userData.at[0,'Graduation_Stream'] = st.selectbox('Select your graduation stream', gradstreammaster)

        userData.at[0,'Percentage'] = st.text_input('Enter your graduation percentage')

        userData.at[0,'Technical/BusinessSkills'] = st.multiselect("Select your skills", skill)

        userData.at[0,'Interests'] =  st.multiselect("Select your interests", interest_master)
      st.write("##")
      if st.button('Get masters recommendation'):
        with right_column:
            with st.spinner('Wait for it...'):
              st.write("Here are your top ten masters recommendations")
              recommendations = get_masters_recommendation(userData, df_final_master)
              for i in recommendations['masters_type']:
                st.markdown('- **'+i.strip()+'**')