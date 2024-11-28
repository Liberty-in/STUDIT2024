import os
import shutil
import requests
from flask import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'csv'}
work_dataset = 'train_data.pkl'
work_model = 'model1'
info_text = 'Version 1 by Dvukraeva Olga RTU MIREA'
help_text ='Доступные методы:<> success() - загрузка данных на сервер<> prepare() - предобработка данных и сохранение в новый файл в сжатом формате<> print_list_datasets() - вывод доступных датасетов<> print_list_models() - вывод доступынх моделей<> predict() - осуществление предсказаний для рабочего датасета с использованием рабочей модели<> setd() - установка рабочего датасета<> setm() - установка рабочей модели<> print_info() - вывести информацию об API'
@app.route('/')
def main():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    f = request.files['file']
    f.save("uploads/" + f.filename + ".csv")
    print(f.filename)
    return f.filename + ' успешно загружен'

def ln_x(x):
    return np.log(x)


def prepare_data(df):
    df['feature_1'] = df['feature_1'].apply(ln_x)
    scaler = MinMaxScaler()
    scaler.fit(df[['feature_2', 'feature_3']])
    df[['feature_2', 'feature_3']] = scaler.transform(df[['feature_2', 'feature_3']])
    return df

@app.route('/prepare',  methods=['POST'])
def prepare():
    name = request.json['dataset']
    df = prepare_data(pd.read_csv('uploads/' + name))
    df.to_pickle('uploads/datasets/' + name.split(".")[0] + '.pkl')
    os.unlink('uploads/' + name)
    return str(os.path.getsize('uploads/datasets/' + name.split(".")[0] + '.pkl') / 1000) +' Кбайт занимает полученный датасет'

@app.route('/request_data', methods=["GET"])
def print_list_datasets():
    return os.listdir('uploads/datasets')

@app.route('/request_model')
def print_list_models():
    return os.listdir('uploads/models')

@app.route('/help')
def print_help():
    return help_text.split('<>')

@app.route('/info')
def print_info():
    return info_text

@app.route('/predict')
def predict():
    try:
        df = pd.read_pickle('uploads/work/data/' + os.listdir('uploads/work/data')[0])
    except:
        return 'Не выбран рабочий датасет'
    from_file = CatBoostClassifier()
    try:
        from_file.load_model('uploads/work/model/' + os.listdir('uploads/work/model')[0], format='cbm')
    except:
        return 'Не выбрана рабочая иодель'
    preds = from_file.predict(df)
    return np.squeeze(preds).tolist()

@app.route('/setd',  methods=['POST'])
def setd():
    c_dataset = request.json['dataset']
    for filename in os.listdir('uploads/work/data'):
        file_path = 'uploads/work/data/' + filename
        os.unlink(file_path)
    shutil.copy(
        'uploads/datasets/' + c_dataset,
        'uploads/work/data'
    )
    return ' - текущий рабочий датасет'

@app.route('/setm',  methods=['POST'])
def setm():
    c_model = request.json['model']
    for filename in os.listdir('uploads/work/model'):
        file_path = 'uploads/work/model/' + filename
        os.unlink(file_path)
    shutil.copy(
        'uploads/models/' + c_model,
        'uploads/work/model'
    )
    return 'текущая модель'


@app.route('/column',  methods=['POST', 'GET'])
def column():
    #i = request.json['index']
    df = pd.read_pickle('uploads/work/data/' + os.listdir('uploads/work/data')[0])
    df_x = df['feature_1']
    return df_x.tolist()


if __name__ == '__main__':
    app.run(debug=True)