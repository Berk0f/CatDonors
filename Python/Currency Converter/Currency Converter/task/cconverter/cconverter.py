import requests
currency_code = input().lower()
url = f'http://www.floatrates.com/daily/{currency_code}.json'
r = requests.get(url).json()
dict_currencies = {}
if currency_code != 'usd':
	dict_currencies['usd'] = float(r['usd']['rate'])
if currency_code != 'eur':
	dict_currencies['eur'] = float(r['eur']['rate'])
while True:
	received_code = input().lower()
	if received_code == '':
		break
	amount = int(input())
	print('Checking the cache...')
	received_rate = float(r[received_code]['rate'])
	if received_code in dict_currencies.keys():
		print('Oh! It is in the cache!')
	else:
		print('Sorry, but it is not in the cache!')
		dict_currencies[received_code] = received_rate
	result = round(amount * received_rate, 2)
	print(f'You received {result} {received_code.upper()}.')