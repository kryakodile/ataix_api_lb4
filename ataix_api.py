import requests

BASE_URL = "https://api.ataix.kz/"
responce=requests.get('https://api.ataix.kz/')
print("Ответ сервера: ",responce.status_code)

def get_currencies():  #список валют
    responce=requests.get(f"{BASE_URL}api/currencies")
    data=responce.json()
    print("Список всех валют:"+ "\n".join(item["symbol"] for item in data["result"]))
    counts = len(data['result'])
    print(f"Общее кол-во валют:", counts)

def get_symbols():  #торговые пары
    response = requests.get(f"{BASE_URL}api/symbols")
    data = response.json()
    print("Все торговые пары:\n" + "\n".join(item["symbol"] for item in data["result"]))
    count = len(data['result'])
    print(f"Общее кол-во торговых пар:", count)

def get_prices():  #цена монет и токенов
    response = requests.get(f"{BASE_URL}api/prices")
    data = response.json()
    print("Цены всех монет и токенов:")
    if data["status"]:
        for coin in data["result"]:
            print(f"{coin['symbol']}: {coin['last']}")
    else:
        print("Ошибка: статус API = false")
  
#вызываем все функции
get_currencies()
print("\n")
get_symbols()
print("\n")
get_prices()
