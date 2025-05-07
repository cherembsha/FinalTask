# Модель определяет позитивную, нейтральную или негативную эмоцию содержит в себе текст.
# Группа: Касимов Тимерхан, Ломанн Влада

# Установка библиотек производится командами:
# pip install transformers sentencepiece
# pip install -q streamlit

import streamlit as st
from fastapi import FastAPI, Body
from transformers import pipeline
from pydantic import BaseModel

model = pipeline(model="seara/rubert-tiny2-russian-sentiment")


def Em_T_accuracy(inp):
    res = model(inp)
    acc = round(res[0]['score'] * 100, 2)
    return acc


def Em_T_label(inp):
    res = model(inp)
    lbl = res[0]['label']
    return lbl


def Em_T(to_api=False):
    st.header('Определить настроение по тексту')

    inp = st.text_input('Введите фразу, а я определю ваше настроение: ')

    if st.button('Старт'):
        result = model(inp)
        acc = round(result[0]['score'] * 100, 2)

        if result[0]['label'] == 'negative':
            st.error(f'Я уверена на {acc}%, что у вас ПЛОХОЕ настроение')
        elif result[0]['label'] == 'positive':
            st.success(f'Я уверена на {acc}%, что у вас ХОРОШЕЕ настроение')
        else:
            st.warning(f'Я уверена на {acc}%, что у вас НЕЙТРАЛЬНОЕ настроение')


if __name__ == "__main__":
    Em_T()

# Работа с API


class Item(BaseModel):
    text: str


app = FastAPI()


@app.get('/')
def root():
    return 'Я умею читать настроение по тексту'


@app.get('/how/')
def how():
    acc = Em_T_accuracy("Hello world!")

    return 'Например, я считаю, что фраза "Hello world!" позитивна на ' + str(acc) + '%'


@app.post('/predict/')
async def predict(data=Body()):
    text = data['text']

    acc = Em_T_accuracy(text)
    label = Em_T_label(text)

    if label == 'negative':
        label = 'ПЛОХОЕ'
    elif label == 'positive':
        label = 'ХОРОШЕЕ'
    else:
        label = 'НЕЙТРАЛЬНОЕ'

    return {'message': f'Я уверена на {acc}%, что у вас {label} настроение'}
