import pickle as pkl
import pandas as pd
with open("dataset.pickle", "rb") as f:
    object = pkl.load(f)
    
df = pd.DataFrame(object)
df.to_csv(r'file.csv')