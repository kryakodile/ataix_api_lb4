import json
import requests
import time

API_KEY = "&&&"
API_BASE = "https://api.ataix.kz/api/orders"
ORDERS_FILE = "orders_data.json"

def load_orders():
    with open(ORDERS_FILE, "r") as file:
        return json.load(file)

def save_orders(orders):
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)

def get_order_info(order_id):
    url = f"{API_BASE}/{order_id}"
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }
    response = requests.get(url, headers=headers, timeout=20)
    if response.status_code == 200:
        return response.json().get("result", {})
    else:
        print(f" Ошибка получения ордера {order_id}: {response.status_code}")
        return {}

def calculate_profit(buy_order, sell_order):
    buy_total = float(buy_order.get("cumQuoteQuantity", 0))
    buy_comm = float(buy_order.get("cumCommission", 0))
    sell_total = float(sell_order.get("cumQuoteQuantity", 0))
    sell_comm = float(sell_order.get("cumCommission", 0))

    net_profit = sell_total - sell_comm - (buy_total + buy_comm)
    percent = (net_profit / (buy_total + buy_comm)) * 100 if (buy_total + buy_comm) != 0 else 0
    return round(net_profit, 6), round(percent, 2)

def process_orders():
    orders = load_orders()
    new_orders = []

    for order in orders:
        if order["status"].lower() != "new":
            continue

        order_id = order["orderID"]
        print(f" Проверка ордера {order_id}...")

        order_data = get_order_info(order_id)
        status = order_data.get("status")

        if status == "filled":
            print(f" Ордер {order_id} выполнен. Рассчитываем доход...")

            order["status"] = "filled"
            order["cumQuoteQuantity"] = order_data.get("cumQuoteQuantity")
            order["cumCommission"] = order_data.get("cumCommission")

            related_buy = next((
                o for o in orders
                if o.get("symbol") == order.get("symbol")
                and o.get("status") == "filled"
                and o.get("side") == "buy"
            ), None)

            if related_buy:
                net_profit, percent = calculate_profit(related_buy, order)
                order["net_profit_usdt"] = net_profit
                order["profit_percent"] = percent
                print(f" Доход по ордеру {order_id}: {net_profit} USDT ({percent}%)")
            else:
                print(" Нет информации о связанном ордере на покупку")

        time.sleep(1)

    save_orders(orders)
    print("Обработка завершена. Обновления сохранены в orders_data.json")

if __name__ == "__main__":
    process_orders()
