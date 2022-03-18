# -*- coding: utf-8 -*-
import re

from collections import Counter

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = stopwords.words('english')
custom_stopwords = ['article', 'page', 'wikipedia', 'talk', 'would', 'one', 'people', 'trump', 'get']
stop_words = set(stop_words + custom_stopwords)

stemmer = SnowballStemmer(language='english')
lemmatizer = WordNetLemmatizer()

dict_words = {
    "\'ll": " will",
    "\'ve": " have",
    "\'t": " not",
    "don\'t": "do not",
    "dont": "do not",
    "aren\'t": "are not",
    "won\'t": "will not",
    "wont": "will not",
    "can\'t": "cannot",
    "cant": "cannot",
    "shan\'t": "shall not",
    "shant": " shall not",
    "\'m": "am",
    "doesn\'t": "does not",
    "doesnt": "does not",
    "didn\'t": "did not",
    "didnt": "did not",
    "hasn\'t": "has not",
    "hasnt": "has not",
    "haven\'t": "have not",
    "havent": "have not",
    "wouldn\'t": "would not",
    "it\'s": "it is",
    "that\'s": "that is",
    "weren\'t": "were not",
    "werent": "were not",
    "u": "you"
}


def replace_toxic_words(text: str) -> str:
    """
    Выделение токсичные слов
    """
    text = re.sub(r'(fuckfuck)', 'fuck fuck ', text)
    text = re.sub(r'(f+)( *)([u|*|_]+)( *)([c|*|_]+)( *)(k)+', 'fuck', text)
    text = re.sub(r'(h+)(a+)(h+)(a+)', 'ha ha ', text)
    text = re.sub(r'(s+ *h+ *[i|!]+ *t+)', 'shit', text)
    text = re.sub(r'\b(n+)(i+)(g+)(a+)\b', 'nigga', text)
    text = re.sub(r'\b(n+)([i|!]+)(g+)(e+)(r+)\b', 'nigger', text)
    text = re.sub(r'\b(d+)(o+)(u+)(c+)(h+)(e+)( *)(b+)(a+)(g+)\b', 'douchebag', text)
    text = re.sub(r'([a|@][$|s][s|$])', 'ass', text)
    text = re.sub(r'(\bfuk\b)', 'fuck', text)

    return text


def replace_toxic_symbols(text: str) -> str:
    """ 
    Замена символов на буквы
    """
    text = re.sub("5", "s", text)
    text = re.sub("1", "i", text)
    text = re.sub("0", "o", text)
    text = re.sub("\*", "u", text)

    return text


def clean_text(text: str) -> str:
    """
    Удаление лишних спец символов и конструкций 
    """
    # Удалим все ссылки
    template = re.compile(r'https?://\S+|www\.\S+')
    text = re.sub(template, ' ', text)
    # теги удаления
    html_tag = '<.*>'
    text = re.sub(html_tag, ' ', text)

    # Оставляем только буквы
    text = re.sub(r"[^a-zA-Z ]+", ' ', text)

    # Удаляем слова размера меньше 3
    # text = re.sub(r'\b\w{,2}\b', ' ', text)

    # удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def remove_stopwords(text: str) -> str:
    """
    Удаление стоп-слов.
    """

    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)


def replace_words(text: str) -> str:
    """
    Замена слов по словарю
    """

    text = [dict_words.get(w, w) for w in text.split()]
    return ' '.join(text)


def replace_repetitions(text: str, vocab: Counter) -> str:
    """
    Заменим аааавто на авто, если есть такой в словаре
    """
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    text_rep = []
    for word in text.split():
        word_rep_1 = re.sub(pattern, r'\1', word)
        word_rep_2 = re.sub(pattern, r'\1\1', word)
        if vocab.get(word_rep_1, ''):
            text_rep.append(word_rep_1)
        elif vocab.get(word_rep_2, ''):
            text_rep.append(word_rep_2)
        else:
            text_rep.append(word)

    return ' '.join(text_rep)


def stemming(text: str) -> str:
    """
    Стемминг слов
    """
    text = [stemmer.stem(w) for w in text.split()]

    return ' '.join(text)


def lemmatization(text: str) -> str:
    """
    Стемминг слов
    """

    def get_wordnet_pos(word):
        """ Get Tag"""

        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    text = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text)]

    return ' '.join(text)


def preprocessing(text: str) -> str:
    """
    Pipeline обработки.
    """

    text = str(text).lower()
    text = replace_toxic_words(text)
    text = replace_toxic_symbols(text)
    text = replace_words(text)
    text = clean_text(text)
    text = remove_stopwords(text)
    text = stemming(text)
    #     text = lemmatization(text)

    return text


def trunc_text(text: str, max_len: int) -> str:
    """
    Обрежем текст до необходимой длины
    """
    if len(text) > max_len:
        right_border = text[:max_len + 1].rfind(' ')
        return text[:right_border]
    else:
        return text
