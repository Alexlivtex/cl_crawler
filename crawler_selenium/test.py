import pickle
test_dic = {}
f = open("data_total.pickle", "rb")
test_dic = pickle.load(f)
print(len(test_dic))