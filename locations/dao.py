import time
import random
from datetime import datetime, timedelta
from typing import List
from benchmark import timing


@timing
def get_current_dislocation() -> List:
    """
    Формирование текущей дислокации вагонов. 
    Получаем список вагонов и их дату прибытия.
    Каждый вагон может быть привязан к одной и той же накладной!
    Для того, чтобы получить предсказанную дату прибытия, необходимо вызывать сервис 'get_predicted_dates'
    """
    locations = []
    arrivale_dates = [None, None, None, datetime.now() - timedelta(days=3),
                      datetime.now()]
    time.sleep(2)

    for i in range(0, 20000):
        arrivale_date = random.choice(arrivale_dates)
        location = {
            "wagon": random.randint(10000, 90000),
            "invoice": f"{random.randint(1, 30000)}__HASH__",
            "arrivale_date": arrivale_date.strftime(
                "%d.%m.%Y") if arrivale_date else None,
        }
        locations.append(location)
    return locations


@timing
def get_predicted_date_by_invoices(invoices: List) -> List:
    """
    На вход необходимо передать список из уникальных накладных. 
    По каждой накладной будет сформировано время прибытия
    """
    time.sleep(1)
    predicted_results = []
    for invoice in invoices:
        predicted_date = datetime.now() + timedelta(days=random.randint(1, 5))
        data = {
            "invoice": invoice,
            "predicted_date": predicted_date.strftime("%d.%m.%Y")
        }
        predicted_results.append(data)

    return predicted_results


def get_no_date_invoices_from_locations(locations):
    invoices = [
        location.get('invoice') for location in locations
        if location.get('arrivale_date') is None
    ]
    return invoices


def find_new_date_for_invoice(location, predicted_date):
    for element in predicted_date:
        if element.get('invoice') == location.get('invoice'):
            new_date = element.get('predicted_date')
            predicted_date.remove(element)
            return new_date


@timing
def api_call():
    """
    В качестве ответа должен выдаваться повагонный список из сервиса get_current_dislocation 
    с обновленной датой прибытия вагона из сервиса get_predicted_dates
    только по вагоном, у которых она отсутствует
    """
    locations = get_current_dislocation()

    invoices = get_no_date_invoices_from_locations(locations)
    predicted_date = get_predicted_date_by_invoices(invoices)

    for location in locations:
        if location.get('arrivale_date') is None:
            new_date = find_new_date_for_invoice(location, predicted_date)
            location.update({'arrivale_date': new_date})
    return locations


if __name__ == '__main__':
    api_call()
