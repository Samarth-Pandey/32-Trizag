import streamlit as st
import time
import json


with st.container():
    left_column , right_column = st.columns(2)
    with left_column:
     st.title ("Career Recommendation Engine")
     st.subheader("Hi there :wave:")
     st.write("Most of the students afetr completing 10th , 12th or degree are confused about their carrer , which dgree to persue or whether to go for higher eductaion or not . So basically there are multiple thing going on in the mind of students , here is our project that can help students in choosing an appropriate path in thier career")
  
st.write("Before we proceed, let us get to know you better...")
st.write("---")
choice = st.radio('Choose your path', ['Job', 'Masters'])


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



#loading the url for animation
lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_and4mptz.json")