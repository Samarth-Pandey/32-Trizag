import pickle
with open("dataset.pickle","rb") as file_handle:
    retrieved_data = pickle.load(file_handle)
    print(retrieved_data)