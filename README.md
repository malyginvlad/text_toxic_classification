# Text toxic classification

Небольшой проект по определению токсичности текста.

На этапе предварительной обработки я извлек подмножество "токсичных" слов из словаря, удалил наиболее встречающиеся не информативные слова, написал регулярные выражения для выделения токсичных слов. Была выбрана модель Tfidf + LogReg с наибольшим точностью по roc_auc.

К сожалению, не все удалось попробовать и протестировать.


Данные: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge

## Запуск проекта
1. `pip install requirements` - установка зависимостей
2. `python app.py` - запуск сервера flask

## Проверка работы
1. Проект запустится по адресу http://127.0.0.1:5000/, можно на него зайти и вписать текст вручную
2. Также можно протестировать запустив в соседнем терминале `python test.py`

## Структура
* `data/` - данные для обучения
* `models/` - сохраненные модели
* `notebooks/` - jupyter notebooks
* `templates/` - шаблоны отображения фронта
* `utils/` - утилиты

## TODO
- [ ] Добавить файл для дообучения моделей
- [ ] Добавить модели на основе word2vec, gru, bert
- [ ] Добавить телеграмм бота
