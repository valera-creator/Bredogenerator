from flask import Flask, render_template
import random
from docx import Document

app = Flask(__name__)


def get_text():
    text = []
    keys = list(slov)  # список ключей
    maybe = random.choice(keys)  # первое слово
    text.append(maybe)
    n = random.randint(150, 300)
    for i in range(n + 30):  # для того чтобы учесть запятые и прочее ненужные элементы
        maybe = text[-1]  # обычное слово
        if maybe not in slov:
            while True:  # если нет ключа
                maybe = random.choice(slov[random.choice(keys)])
                if maybe in slov:
                    break
        word = random.choice(slov[maybe])
        text.append(word)  # список слов
    for i in range(len(text)):
        if text[i] in ",.!?:;":  # склейка знаков препенания
            text[i - 1] = text[i - 1] + text[i]
    correst_words = list(filter(lambda x: x[0].isalnum(), text))  # чистка от знаков
    correst_words[0] = correst_words[0].capitalize()  # предложение с большой буквы
    for i in range(len(correst_words) - 1):
        if correst_words[i][-1] == ".":
            correst_words[i + 1] = correst_words[i + 1].capitalize()
    correst_words = correst_words[0:n]
    if correst_words[-1][-1] in ",.!?:;":  # если в конце знак препенания, то удалить
        correst_words[-1] = correst_words[-1][0:-1]
    return " ".join(correst_words) + "..."


@app.route('/', methods=['GET', 'POST'])
def answer():
    text = get_text()
    return render_template('base.html', text=text)


if __name__ == '__main__':
    doc = Document("list_words.docx")
    words = []
    for paragraph in doc.paragraphs:
        words.append(paragraph.text)
    words = words[0]
    words = words[9:-1]
    words = words.split(", ")
    words = list(map(lambda x: x[1:-1], words))  # адекватное преобразование в список
    words = words[0:-1]
    slov = {}
    words = list(map(lambda x: x.lower(), words))  # к строчным
    for i in range(len(words)):  # в словарь
        if words[i] not in slov and words[i] != words[-1]:
            slov[words[i]] = []
        if words[i] != words[-1]:
            slov[words[i]].append(words[i + 1])
    app.run(debug=True)
