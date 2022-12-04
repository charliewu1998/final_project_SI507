import requests
import json
import webbrowser

BASE_URL = 'https://api.yelp.com/v3/businesses/search'
key = 'RzCec0WbteIW21wIPqI7boaOgKzHtA8O1AOgFYOxKr25e25HIKArnYq8KIQ6PDIgkZ31YsTpxwoS11JC5w-rbK2EReJhLo__QbOIuZRBwKAKo5_pT93Hf0tG_7CFY3Yx'
headers = {'Authorization': 'Bearer %s' % key}
CACHE_FILENAME = "cache.json"

class Restaurant:
    
    def __init__(self, name = 'no name', is_closed = 'no info', url = 'no url', review_count = 'no review_count',
                 categories = 'no categories', cate_list = None, rating = 'no rating', price = 'no price', display_address = 'no address', 
                 display_phone = 'no display phone', distance = 'no distance', json = None):
        if json is None:
            self.name = name
            self.is_closed = is_closed
            self.url = url
            self.review_count = review_count
            self.categories = categories
            self.rating = rating
            self.price = price
            self.display_address = display_address
            self.display_phone = display_phone
            self.distance = distance
            self.cate_list = None
        else:
            try:
                self.name = json['name']
            except:
                self.name = ""
            try:
                self.is_closed = json['is_closed']
            except:
                self.is_closed = ""
            try:
                self.url = json['url']
            except:
                self.url = ""
            try:
                self.review_count = json['review_count']
            except:
                self.review_count = ""
            try:
                self.categories = json['categories']
                category_lst = []
                for i in self.categories:
                    category_lst.append(i['title'].lower())
                self.cate_list = category_lst              
            except:
                self.categories = None
                self.cate_list = []
            try:            
                self.rating = json['rating']
            except:
                self.rating = ""
            try:
                self.price = json['price']
            except:
                self.price = ""
            try:
                self.display_address = json['display_address']
            except:
                self.display_address = ""
            try:
                self.display_phone = json['display_phone']
            except:
                self.display_phone = ""
            try:
                self.distance = json['distance']/1609.344
            except:          
                self.distance = ""             

        
    def info(self):
        print(self.name)
        print('review count: ' + str(self.review_count))
        print('Rating: ' + str(self.rating))
        print('Price: ' + self.price)
        print('Address: ' + self.display_address)
        print('Contact: ' + self.display_phone)
        print('Distance: ' + str(self.distance) + ' miles')

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def get_user_location():
    location = input("Please enter your location, or enter 'exit' to quit: ")
    print("You entered " + str(location))
    if location == "exit":
        return "exit"
    else:
        user_input = {'location':location, 'term': 'restaurant', 'radius': 1000, 'limit': 30}
        return user_input 


def get_restaurant(url=BASE_URL, headers = headers, params = None):
    resp = requests.get(url,headers = headers,params = params)
    json_str = resp.text
    Results_Dictionary = json.loads(json_str)
    return Results_Dictionary['businesses']

def get_user_response():
    ans1 = input('What is your budget? Please enter $ ~ $$$$: ')
    ans2 = input('What specific category are you looking for? i.e. Indian, Burgers...: ').lower()
    ans3 = int(input('what is your ideal distance? Enter 1 for <= 5 milie, 2 for <= 10 mile, 3 for <= 20 mile: '))
    response = [ans1,ans2,ans3]
    return response 

def recommendation(rest_list,response):
    full_list = []
    for i in rest_list:
        restaurant = Restaurant(json=i)
        print(restaurant.cate_list)
        print(restaurant.price)
        print(restaurant.distance)
        print(response)
        if restaurant.price == response[0] and response[1] in restaurant.cate_list:
            if (response[2] == 1 and restaurant.distance < 5) or (response[2] == 2 and restaurant.distance < 10) or (response[2] == 3 and restaurant.distance < 20):
                full_list.append(restaurant)
    print(full_list)
    for i in range(len(full_list)):
        print(str(i) + " " + full_list[i].name)
    return full_list

if __name__ == "__main__":
    while True:
        user_input = get_user_location()
        if user_input == 'exit':
            print('bye')
            break
        else:
            cache = get_restaurant(BASE_URL, headers, user_input)
            save_cache(cache)
            output = open_cache()
            response = get_user_response()
            full_restaurant_list = recommendation(output,response)
            if full_restaurant_list == []:
                print('There is no restaurant satisfying your requirements.')
                break 
            else:
                num = int(input("Enter the number to know more info: "))
                print(full_restaurant_list[num].info())
                webbrowser.open(full_restaurant_list[num].url)







