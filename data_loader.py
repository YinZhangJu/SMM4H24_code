import os
import pandas as pd
import csv

dataname = []

data_path = './SMM4H_2024_Task_2_test'

# 遍历文件夹中的所有文件
def Data_namecon(data_path): 
    for filename in os.listdir(data_path):
        if filename.endswith('.txt'):
            # file_path = os.path.join(data_path, filename)
            # df = pd.read_csv(file_path, delimiter='\t')  # 假设是tab分隔的文本文件
            # datas.append([df.columns[0]])
            filename = filename.replace(".txt", "")
            dataname.append(filename)

Data_namecon(data_path)

# '''
# de_path = './SMM4H_2024_Task_2_train_dev/dev/de_dev'
# fr_path = './SMM4H_2024_Task_2_train_dev/train/fr_few_shot'
# ja_path = './SMM4H_2024_Task_2_train_dev/dev/ja_dev'
#
# # 列表来存储数据框
# inputresult = []
#
# Data_namecon(de_path,inputresult)
# Data_namecon(fr_path,inputresult)
# Data_namecon(ja_path,inputresult)
# '''


dataname = pd.DataFrame(dataname)
dataname.columns = ['Name']
dataname.to_csv("./test_result_data/dataname.csv")

# df.to_csv('Datas.csv',index=0)