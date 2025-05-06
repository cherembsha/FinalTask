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
