import csv
import re

# 讲数据保存为brat格式
def save_to_brat(s, type, substring, filename,i):
    start_position = s.find(substring)
    end_position = start_position + len(substring)
    with open(filename, 'a', encoding='utf-8') as f:
        line = f"T{i}\t{type} {start_position} {end_position}\t{substring}\n"
        f.write(line)

output_path = './test_result_data/result2__glm4.csv'
title_path = './test_result_data/dataname.csv'

j = 1

# 求name表长度
with open(title_path, 'r') as file:
    csv_reader = csv.reader(file)
    row_count = sum(1 for row in csv_reader)

# 读取LLM的输出csv
with open(output_path, 'r') as file1:
    csv_reader = csv.reader(file1)

    next(csv_reader)  # 跳过第一行

    # 读取剩余行的数据
    for row in csv_reader:
        output = row[0]      # output接收LLM输出

        words_to_remove = ["药品名称：", "副作用：", "{", "}"]

        for word in words_to_remove:
            output = output.replace(word, "")

        segments = re.split(r"，", output)

        if len(segments) == 2:
            segment1 = segments[0].strip()
            segment2 = segments[1].strip()
            # print("第一段文字:", segment1)
            # print("第二段文字:", segment2)

        segments1 = segment1.split("、")
        segments2 = segment2.split("、")

        with open(title_path, 'r') as file2:
            csv_reader = csv.reader(file2)

            # 跳过第一行（标题行）
            for _ in range(j):
                next(csv_reader)

            j = j + 1

            # 从第二行开始读取第二列的数据
            for row in csv_reader:
                title = row[1]  # 第二列的数据（索引为1）

                # 读取原文内容
                with open('test_result_data/test_result2/' + title + '.txt', 'r', encoding='utf-8') as file3:
                    content = file3.read()
                    #print(content)

                    i = 0

                    for segment in segments1:
                        i = i + 1
                        save_to_brat(content, "DRUG", segment, title + ".ann", i)
                        # print(segment.strip())

                    for segment in segments2:
                        i = i + 1
                        save_to_brat(content, "DISORDER", segment, title + ".ann", i)
                        # print(segment.strip())
                break