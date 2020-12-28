import enum
import re

import pandas as pd
from tqdm import tqdm


class Action(enum.Enum):
    SEND_MESSAGE = enum.auto()
    DEL_MSG_BY_SOMEONE = enum.auto()
    DEL_MSG_BY_USER = enum.auto()
    CHANGE_GROUP_NAME = enum.auto()
    CHANGE_GROUP_IMG = enum.auto()
    FINISH_GROUP_CALL = enum.auto()


def parse(filename):
    """
    ラインの会話データをパースしてdf形式で返還する。
    :param filename: <str> conversation_filesの中に入っている会話履歴のファイル名
    :return: <df>
    """

    read_path = 'conversation_files/' + filename
    with open(read_path) as f:
        lines = f.read().splitlines()
        df = pd.DataFrame(columns=['year', 'month', 'day', 'date', 'time', 'user', 'action', 'contents'])
        for i, line in enumerate(tqdm(lines, desc="　　パース中")):
            if i == 0:
                title = line
                continue

            if i <= 2:
                continue

            # 日付から始まる場合
            if m := re.match(r'(\d{4})/(\d{1,2})/(\d{1,2})\((.)\)', line):
                year, month, day, date = m.groups()

            # 時刻から始まる場合
            elif re.match(r'[0-9]{2}:[0-9]{2}', line):
                msg = line.split('\t')
                time = msg[0]
                if msg[1] == 'メッセージの送信を取り消しました':
                    user = None
                    action = Action.DEL_MSG_BY_SOMEONE
                    contents = None

                elif m := re.match(r'(.*?)がメッセージの送信を取り消しました', msg[1]):
                    user = m.group()
                    action = Action.DEL_MSG_BY_USER
                    contents = None

                elif m := re.match(r'(.*?)がグループ名を(.*?)に変更しました。', msg[1]):
                    user, contents = m.groups()
                    action = Action.CHANGE_GROUP_NAME

                elif m := re.match(r'(.*?)がグループのプロフィール画像を変更しました。', msg[1]):
                    user = m.group()
                    action = Action.CHANGE_GROUP_IMG
                    contents = None

                elif msg[1] == 'グループ通話が終了しました。':
                    user = None
                    action = Action.FINISH_GROUP_CALL
                    contents = None

                else:
                    time, user, contents = msg
                    action = Action.SEND_MESSAGE

                row = pd.Series([year, month, day, date, time, user, action, contents], index=df.columns)
                df = df.append(row, ignore_index=True)

            # 空行ではない場合コメントの改行を示すので前回の発言に\nを噛ませて結合する
            elif line != '':
                contents += '\n' + line
                df.iloc[-1, 7] = contents

            # 空行は無視する

        return df
