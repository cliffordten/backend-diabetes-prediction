import pickle
import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')

class Predictor:

    def __init__(self, pregnancies, glucose, blood_pressure, skin_thickness, insulin, BMI, DPF, age):
        self.pregnancies = pregnancies
        self.glucose = glucose
        self.blood_pressure = blood_pressure
        self.skin_thickness = skin_thickness
        self.insulin = insulin
        self.BMI = BMI
        self.DPF = DPF
        self.age = age

    def predict(self):

        dataset=pd.read_csv('prediction/diabetes.csv')

        Q1=dataset.quantile(0.25)
        Q3=dataset.quantile(0.75)
        IQR=Q3-Q1

        dataset_out = dataset[~((dataset < (Q1 - 1.5 * IQR)) |(dataset > (Q3 + 1.5 * IQR))).any(axis=1)]

        X=dataset_out.drop(columns=['Outcome'])
        y=dataset_out['Outcome']

        #Splitting train test data 80 20 ratio
        train_X,test_X,train_y,test_y=train_test_split(X,y,test_size=0.2)

        clf=RandomForestClassifier()
        clf.fit(train_X,train_y)

        test_s = np.array([self.pregnancies,self.glucose,self.blood_pressure,self.skin_thickness,self.insulin,self.BMI,self.DPF, self.DPF]).reshape(1, -1)

        pickle.dump(clf, open('model.pkl','wb'))
        model = pickle.load(open('model.pkl', 'rb'))

        prediction = model.predict(test_s)

        result = prediction[0]

        return result

    def save_to_file(self, result):
        test_s = [self.pregnancies,self.glucose,self.blood_pressure, self.skin_thickness, self.insulin, self.BMI, self.DPF, self.age, result]
        print(test_s)
        with open("prediction/diabetes.csv", "a") as file:
            wr = csv.writer(file, dialect='excel')
            wr.writerow(test_s)
            return "success"

        return "error"