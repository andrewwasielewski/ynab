import json
import requests
from collections import defaultdict

# api-endpoint
url_base = 'https://api.youneedabudget.com/v1/budgets/'

f_budget = open("budget_id.key", "r")
budget_id = f_budget.read()
url_month = '{0}{1}/months/2022-03-01'.format(url_base, budget_id)
url_categories = '{0}{1}/categories'.format(url_base, budget_id)

f_token = open("access_token.key", "r")
token = f_token.read()

headers = {'Authorization': 'Bearer {0}'.format(token)}
  
# sending get request and saving the response as response object
r = requests.get(url = url_month, headers = headers)
result = r.json()['data']

r = requests.get(url = url_categories, headers = headers)
categories_ids = r.json()['data']['category_groups']

# f = open('month2.json')
# result = json.load(f)['data']['month']

# f = open('categories.json')
# categories_ids = json.load(f)['data']['category_groups']

flow = defaultdict(list)
monthly_income_name = 'Monthly Income'

print(result)
for entry in result['month']['categories']:
    flow[entry['category_group_id']].append([entry['name'],round(entry['activity']/-1000)])

budget_groups = dict()
for group in categories_ids:
	 budget_groups[group['id']] = group['name']
		
print ('My [{0}] {1}'.format(result['month']['income']/1000, monthly_income_name))

excluded = ['Internal Master Category', 'Credit Card Payments', 'Hidden Categories']

# print groups
for group, categories in flow.items():
	group_sum = 0
	for c in categories:
		group_sum = group_sum + c[1]
	if budget_groups[group] not in excluded: 
		print('{0} [{1}] {2}'.format(monthly_income_name, group_sum, budget_groups[group]))

# print categories		
for group, categories in flow.items():
	for c in categories:
		if budget_groups[group] not in excluded:
			print('{0} [{1}] {2}'.format(budget_groups[group], c[1], c[0]))
	
