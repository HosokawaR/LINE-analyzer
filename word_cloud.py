import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_wordcloud(frequencies, font, width=1000, height=600):
    wordcloud = WordCloud(background_color='white', font_path=font,
                          width=width, height=height)
    plt.figure(figsize=(width / 50, height / 50))
    plt.imshow(wordcloud.generate_from_frequencies(frequencies))
    plt.axis('off')
    plt.show()


from janome.analyzer import Analyzer
from janome.tokenfilter import ExtractAttributeFilter
from janome.tokenfilter import POSStopFilter

from janome.tokenfilter import POSKeepFilter


def get_words(string, keep_pos=None):
    filters = []
    if keep_pos is None:
        filters.append(POSStopFilter(['記号']))  # 記号を除外
    else:
        filters.append(POSKeepFilter(keep_pos))  # 指定品詞を抽出
    filters.append(ExtractAttributeFilter('surface'))
    a = Analyzer(token_filters=filters)  # 後処理を指定
    return list(a.analyze(string))


import matplotlib.font_manager as fm
from matplotlib import rcParams

japanese_font_candidates = ['Hiragino Maru Gothic Pro', 'Yu Gothic',
                            'Arial Unicode MS', 'Meirio', 'Takao',
                            'IPAexGothic', 'IPAPGothic', 'VL PGothic',
                            'Noto Sans CJK JP']


def get_japanese_fonts(candidates=japanese_font_candidates):
    fonts = []
    for f in fm.findSystemFonts():
        p = fm.FontProperties(fname=f)
        try:
            n = p.get_name()
            if n in candidates:
                fonts.append(f)
        except RuntimeError:
            pass
    # サンプルデータアーカイブに含まれているIPAexフォントを追加
    fonts.append('conversation_files/ipaexg.ttf')
    return fonts


def configure_fonts_for_japanese(fonts=japanese_font_candidates):
    if hasattr(fm.fontManager, 'addfont'):
        fm.fontManager.addfont('font/ipaexg.ttf')
    else:
        ipa_font_files = fm.findSystemFonts(fontpaths='font')
        ipa_font_list = fm.createFontList(ipa_font_files)
        fm.fontManager.ttflist.extend(ipa_font_list)
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = fonts


from collections import Counter


def word_cloud(string):
    words = get_words(string, keep_pos=['名詞'])
    count = Counter(words)
    font = get_japanese_fonts()[0]
    create_wordcloud(count, font)
