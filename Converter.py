from pycbrf.toolbox import ExchangeRates # импортируем библиотеку

rates = ExchangeRates('2024-02-18') # задаем дату, за которую хотим получить данные
result = rates['USD']
print(result.value)
print(result)

result = rates['KRW']
if result.par == 1:
    print(f'{result.par} Рубль равен {result.value}')
else:
    print(f'{result.par} Рублей равно {result.value} {result.name}')
print(result)

