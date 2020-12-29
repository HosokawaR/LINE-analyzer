import MeCab

# 取り出したい品詞
select_conditions = ['動詞', '形容詞', '名詞']

tagger = MeCab.Tagger('')
tagger.parse('')


def wakati_text(text):
    node = tagger.parseToNode(text)
    terms = []

    while node:
        # 単語
        term = node.surface
        # 品詞
        pos = node.feature.split(',')[0]
        if pos in select_conditions:
            terms.append(term)
        node = node.next

    return terms

