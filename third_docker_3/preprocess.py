import pandas as pd
import category_encoders as ce

class DataPreprocessor:
    def __init__(self, dataset, train_dataset=pd.read_csv('./data/train.csv')):
        self.dataset = dataset
        self.train_dataset = train_dataset

    def cleaning(self):
        self.dataset['ethnicity'] = self.dataset['ethnicity'].str.replace('others', 'Others', regex=True).str.replace(r'?', 'Others', regex=True)
        self.dataset['relation'] = self.dataset['relation'].replace('?', 'Others')
        self.dataset['gender'] = self.dataset['gender'].map({'m':1, 'f':0})
        self.dataset['jaundice'] = self.dataset['jaundice'].map({'yes':1, 'no':0})
        self.dataset['used_app_before'] = self.dataset['used_app_before'].map({'yes':1, 'no':0})
        self.dataset['austim'] = self.dataset['austim'].map({'yes':1, 'no':0})
        data_contry_of_res = pd.DataFrame(self.train_dataset['contry_of_res'].value_counts())
        lis = list(data_contry_of_res[data_contry_of_res.contry_of_res > 10].index)
        self.dataset['contry_of_res'] = self.dataset['contry_of_res'].apply(lambda x: x if x in lis else 'Others')
        return self.dataset

    def encode_categorical(self):
        recode_col = ['ethnicity', 'contry_of_res', 'relation']
        ord_enc = ce.OrdinalEncoder(cols=recode_col).fit(self.train_dataset)
        self.dataset = ord_enc.transform(self.dataset)
        self.dataset.drop(['ID', 'age_desc'], axis=1, inplace=True)
        return self.dataset

    def preprocess_data(self):
        self.cleaning()
        self.dataset = self.encode_categorical()  
        return self.dataset
