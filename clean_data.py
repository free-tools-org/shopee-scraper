import pandas as pd
import re

def clean_data(df):
    _df = df.dropna(axis=0, how='any')
    _df = _df.drop_duplicates(subset=['ชื่อสินค้า'], keep='first')
    _df = _df.drop_duplicates(subset=['ราคาปัจจุบัน'], keep='first')

    _df['ยอดขาย'] = _df['ยอดขาย'].str.replace('ขายแล้ว ', '')
    _df['ยอดขาย'] = _df['ยอดขาย'].str.replace(' ชิ้น', '')
    _df['จำนวนขาย'] = _df['ยอดขาย'].replace(r'([^\d\.]+)', '', regex=True)

    # change จำนวนขาย to float
    _df['จำนวนขาย'] = _df['จำนวนขาย'].astype(float)

    _df['ตัวคูณ'] = _df['ยอดขาย'].replace(r'([\d\.]+)', '', regex=True)

    # คำนวณจากตัวคูณ
    neural_units = [
      {
        "name": "พัน",
        "multiplier": 1_000
      },
      {
        "name": "หมื่น",
        "multiplier": 10_000
      },
      {
        "name": "แสน",
        "multiplier": 100_000
      },
      {
        "name": "ล้าน",
        "multiplier": 1_000_000
      }
    ]
    for i, unit in enumerate(neural_units):
      _df.loc[_df['ตัวคูณ'] == unit['name'],'จำนวนขาย'] = _df['จำนวนขาย'] * unit['multiplier']

    _df = _df.drop(columns=['ตัวคูณ'])
    _df.loc['ราคา'] = _df['ราคา'].replace(r'[^\d\.\s]', '', regex=True)
    _df.loc[_df['ราคา'] == _df['ราคาปัจจุบัน'], 'โปรโมชั่น'] = "NO"
    _df.loc[_df['ราคา'] != _df['ราคาปัจจุบัน'], 'โปรโมชั่น'] = "YES"
    return _df

if __name__ == "__main__":
  df = pd.read_excel("product_list.xlsx")
  df = clean_data(df)
  df.to_excel("cleaned_product_list.xlsx", index=False)