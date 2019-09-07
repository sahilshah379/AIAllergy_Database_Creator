import selenium
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

HEADERS = {'user-agent': ('Chrome/45.0.2454.101 Safari/537.36'), 'referer': 'https://www.food2fork.com/api'}

url_search = 'https://www.food2fork.com/api/search'
url_get = 'https://www.food2fork.com/api/get'

def getRecipeID(recipe_name, api_key):
	str.lower(recipe_name)
	recipe_array = recipe_name.split(' ')
	recipe_name = recipe_array[0]
	for i in range(1, len(recipe_array)):
		recipe_name = recipe_name + '%20'
		recipe_name = recipe_name + recipe_array[i]

	recipe_id_array = []
	for page in range(1):
		url_recipe_search = url_search + '?key=' + api_key + '&q=' + recipe_name + '&page=' + str(page+1)
		search_request = requests.get(url_recipe_search, headers = HEADERS)

		search_text = search_request.text
		search_start_key = '"recipe_id": "'
		search_end_key = '"'
		search_array = search_text.split(search_start_key)
		for i in range(1, len(search_array)):
			recipe_id = search_array[i].split(search_end_key)[0]
			recipe_id_array.append(recipe_id)


	print('\n'.join(map(str, recipe_id_array)))
	print(len(recipe_id_array))

def getIngredients(recipe_name, api_key):
	recipes = []
	recipe_id_array = getRecipeID(recipe_name, api_key)

	for recipe_id in recipe_id_array:
		url_ingredients_get = url_get + '?key=' + api_key + '&rId=' + recipe_id
		get_request = requests.get(url_ingredients_get, headers = HEADERS)

		get_text = get_request.text
		get_start_key = '"ingredients": ['
		get_end_key = '], '
		get_ingredients_list = get_text.split(get_start_key)[1].split(get_end_key)[0] + ' '
		get_ingredients_list = get_ingredients_list.replace(',', '')
		recipe_ingredients_list = get_ingredients_list.split('" ')
		recipe_ingredients_list = map(lambda foo: foo.replace('"', ''), recipe_ingredients_list)
		recipe_data = []
		recipe_data.append(recipe_id)
		recipe_data.append(recipe_ingredients_list)
		recipes.append(recipe_data)

def getAPIKey():
	email = getEmail()

	options = Options()
	# options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)

	driver.get('https://www.food2fork.com/default/user/register')
	first_name_element = driver.find_element_by_name('first_name')
	first_name_element.send_keys('Pennapps')
	last_name_element = driver.find_element_by_name('last_name')
	last_name_element.send_keys('Nibbas')
	email_element = driver.find_element_by_name('email')
	email_element.send_keys(email)
	password_element = driver.find_element_by_name('password')
	password_element.send_keys('weneedmoremoney')
	password_two_element = driver.find_element_by_name('password_two')
	password_two_element.send_keys('weneedmoremoney')
	driver.find_element_by_class_name("g-recaptcha").click()
	driver.find_element_by_xpath('//*[@id="submit_record__row"]/td[2]/input').click()

	if driver.current_url == 'https://www.food2fork.com/default/user/register#':
		recaptcha = input('Recaptcha')
	driver.find_element_by_xpath('//*[@id="submit_record__row"]/td[2]/input').click()
	driver.get('https://www.food2fork.com/user/api')
	api_key_element = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/span')

	api_key = api_key_element.text
	driver.quit()
	return api_key

def getEmail():
	emailText = requests.get('http://generator.email').text
	email = emailText.split('id="email_ch_text">')[1].split('</span></b><p>')[0]
	return email

def main():
	category = 'Cookie'
	api_key = getAPIKey()
	print(api_key)
	getIngredients(category, api_key)

if __name__ == '__main__':
    main()