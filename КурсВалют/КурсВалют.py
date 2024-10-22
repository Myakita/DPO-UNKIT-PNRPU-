import requests
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

def get_currency_rate(start_date, end_date, currency_code='R01235'):
    url = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}&date_req2={end_date}&VAL_NM_RQ={currency_code}"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        dates = []
        rates = []
        for record in root.findall('Record'):
            date = record.attrib['Date']
            rate = float(record.find('Value').text.replace(',', '.'))
            nominal = int(record.find('Nominal').text)
            rates.append(rate / nominal)
            dates.append(date)
        return dates, rates
    else:
        print("Ошибка при загрузке данных")
        return [], []



start_date = "01/10/2023" 
end_date = "22/10/2023"

dates, rates = get_currency_rate(start_date, end_date)

df = pd.DataFrame({'Дата': pd.to_datetime(dates, format='%d.%m.%Y'), 'Курс': rates})
df.set_index('Дата', inplace=True)

plt.figure(figsize=(10, 5))
df['Курс'].plot()
plt.title(f'Курс USD к RUB с {start_date} по {end_date}')
plt.xlabel('Дата')
plt.ylabel('Курс (RUB)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
