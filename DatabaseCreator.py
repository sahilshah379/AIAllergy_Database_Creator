from os import path
import requests
import math
import time
import csv
import re


app_id = 'e56fe635'
app_key = '24f4c6849e34004f0b6348ca81addee0'

url = 'http://api.edamam.com/search'
HEADERS = {'user-agent': ('Chrome/45.0.2454.101 Safari/537.36'), 'referer': url}

results_per_category = 1000

def getIngredients(category):
	category_url_format = formatCategory(category)

	all_the_ingredients_omg_lol = []

	for page in range(1, math.ceil(results_per_category/100.0)+1):
		time.sleep(12)
		url_category = url + '?q=' + category_url_format + '&app_id=' + app_id + '&app_key=' + app_key + '&from=' + str((100*page)-100) + '&to=' + str(100*page)
		request = requests.get(url_category, headers = HEADERS)

		recipes_text = request.text

		ingredients_start_key = '"ingredientLines" : [ '
		ingredients_end_key = ' ],'
		ingredients_array = recipes_text.split(ingredients_start_key)
		for i in range(1, len(ingredients_array)):
			ingredients = ingredients_array[i].split(ingredients_end_key)[0]
			ingredients.replace(',','')
			all_the_ingredients_omg_lol.append(ingredients)

		if '"more" : false' in recipes_text:
			if page == 1:
				addToMissing(category)
			break


	addToCSV(category, all_the_ingredients_omg_lol)

	# print('\n'.join(map(str, all_the_ingredients_omg_lol)))
	# print(len(all_the_ingredients_omg_lol))

def addToCSV(category, ingredients_array):
	csvText = ingredients_array
	csvText.insert(0, category)

	with open('recipe.csv', mode='a') as recipe_file:
		recipe_writer = csv.writer(recipe_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		recipe_writer.writerow(csvText)

def addToMissing(category):
	missing_file = open('missing.txt', 'a')
	missing_file.write(category)
	missing_file.write('\n')
	missing_file.close()

def formatCategory(category_name):
	category_array = category_name.split('_')
	category_name = category_array[0]
	for i in range(1, len(category_array)):
		category_name = category_name + '%20'
		category_name = category_name + category_array[i]
	return category_name

def readCategories():
	category_file = open('categories.txt', 'r')
	contents = category_file.read()
	categories = contents.split('\n')
	return categories

def main():
	categories = readCategories()
	# print(len(categories)) ----- 418 categories
	for i in range(len(categories)):
		print(i+1)
		getIngredients(categories[i])

if __name__ == '__main__':
    main()