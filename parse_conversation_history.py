import os
import re
import csv

# 日付, 時間, 名前, 発言のcsvに変換


READ_PATH = 'conversation_files/mierda_20200618.txt'
RIGHT_PATH = 'chat_csv/mierda_20200618.csv'

print(os.getcwd())

with open(READ_PATH) as f:
    lines = f.readlines()

    new_lines = []
    date = 0

    for i, line in enumerate(lines):

        # LINEの会話履歴の最初の３行は無効
        if i <= 2:
            continue

        new_line = []

        # 日付から始まる場合
        if re.match(r"\d{4}/\d{1,2}/\d{1,2}", line):
            line = re.sub(r'\n', '', line)
            line = re.sub(r'\([月|火|水|木|金|土|日]\)', '', line)
            date = line

        # 時刻から始まる場合
        elif re.match(r"[0-9]+:[0-9][0-9]", line):
            line = re.sub('\n', '', line)

            new_line.append(date)
            new_line.append(line.split('\t')[0])
            new_line.append(line.split('\t')[1])
            new_line.append(line.split('\t')[2])
            new_lines.append(new_line)

        # 空行ではない場合
        # 前回の発言に\nを噛ませて結合する
        elif line != '\n':
            line = re.sub(r'\n', '', line)
            # print(line)
            new_lines[len(new_lines) - 1][3] += '\n' + line

with open(RIGHT_PATH, 'w', newline="") as f:
    writer = csv.writer(f)
    for i in new_lines:
        print(i)
        writer.writerow(i)
