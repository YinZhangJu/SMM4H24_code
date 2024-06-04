import os
import pandas as pd
import csv

dataname = []

data_path = './SMM4H_2024_Task_2_test'

# 遍历文件夹中的所有文件
def Data_namecon(data_path): 
    for filename in os.listdir(data_path):
        if filename.endswith('.txt'):
            filename = filename.replace(".txt", "")
            dataname.append(filename)

Data_namecon(data_path)

dataname = pd.DataFrame(dataname)
dataname.columns = ['Name']
dataname.to_csv("./test_result_data/dataname.csv")