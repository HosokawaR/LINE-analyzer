import csv
import MeCab
import pandas

print("LINE解析プログラムです。")
print("解析メニューを選んでください。")
print('''
    'word': 単語の使用頻度を解析します。
    'user_by_balloon': 吹き出し単位で、最も発言しているユーザーを解析します。
    'user_by_letters': 文字数単位で、最も発言しているユーザーを解析します。
''')

PATH = 'chat_csv/mierda_20200618.csv'


history = []

with open(PATH, encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        history.append(row)


def word():
    t = MeCab.Tagger()
    print(t.parse("こんにちはみなさん。はじめまして"))

menu = input("解析メニューを選択: ")

if menu == 'word':
    word()
elif menu == 'user_by_balloon':
    pass
elif menu == 'user_by_letters':
    pass