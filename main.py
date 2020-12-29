import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
# from decorator import decorator
from matplotlib.font_manager import FontProperties

from parse_conversation_history import parse
from private_settings import unique_users

# 日本語フォント設定
font_path = "/usr/share/fonts/truetype/migmix/migu-1p-regular.ttf"
font_prop = FontProperties(fname=font_path)
matplotlib.rcParams["font.family"] = font_prop.get_name()


def conv_time_to_linear(time):
    hours, min = time.split(':')
    return int(hours) + int(min) / 60


def analyze_talk_frequency_by_user_and_time(df):
    fig, ax = plt.subplots()
    df['linear_time'] = df['time'].apply(conv_time_to_linear)
    sns.histplot(data=df, x='linear_time', hue='user', multiple="stack")
    plt.title(f'2020年の時間ごとの発言回数 n={df.shape[0]}')
    plt.xlabel('時間（時）')
    ax.set_xticks(np.arange(0, 25, 3))
    # ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F'])
    plt.ylabel('回数（回）')
    plt.show()


def analyze_talk_frequency_by_user_and_month(df):
    fig, ax = plt.subplots()
    s = df.groupby(['month', 'user'])['contents'].count()
    df2 = pd.DataFrame(s)
    sns.lineplot(data=df2, x='month', y='contents', hue='user')
    plt.title(f'2020年の月ごとの発言回数 n={df.shape[0]}')
    plt.xlabel('月（月）')
    ax.set_xticks(np.arange(1, 13, 1))
    plt.ylabel('回数（回）')
    plt.show()


def analyze_word_count_by_user_and_month(df):
    pass


def show_users(df):
    print('ユーザ一覧を表示')
    print('重複するユーザはprivate_settings.pyに記録して下さい。')
    print(df['user'].unique().tolist())


def make_users_unique(df):
    for key_name, every_name in unique_users.items():
        df = df.replace({'user': {name: key_name for name in every_name}})
    show_users(df)
    return df


def main():
    df = parse('mierda_by_chikayama')

    mode = 3
    if mode == 1:
        show_users(df)
    else:
        df = make_users_unique(df)
        df = df[df['year'] == 2020]
        if mode == 2:
            analyze_talk_frequency_by_user_and_time(df)
        if mode == 3:
            analyze_talk_frequency_by_user_and_month(df)


if __name__ == '__main__':
    main()

## おもしろそうな相関
# 発言数の推移
# 最頻単語
# 今年の漢字
# メンション
# 発言文字数
# 語彙力が少ない人（語数 / 全体）
