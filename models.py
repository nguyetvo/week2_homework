import sqlite3
from collections import deque
from bs4 import BeautifulSoup
import requests

TIKI = "https://tiki.vn/"

conn = sqlite3.connect('ti_ki.db')
cur = conn.cursor()

#  tạo bảng categories 
def create_categories_table():
    query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INT, 
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        cur.execute(query)
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)



# tạo bảng sản phẩm 
def create_product_table():
    query = """
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INT,
            product_id TEXT, 
            price TEXT,
            category TEXT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        cur.execute(query)
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

#  func lấy tất cả data, ví dụ : select_all('product')
def select_all(name):
    a = cur.execute(f'SELECT * FROM {name};').fetchall()
    return a
#  func xóa tất cả data
def delete_all(name):
    a = cur.execute(f'DELETE FROM {name};')
    return a

# OOP

class Category:
    def __init__(self, cat_id, name, url, parent_id):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id

    def __repr__(self):
        return "ID: {}, Name: {}, URL: {}, Parent_id: {}".format(self.cat_id, self.name, self.url, self.parent_id)

# commit lưu đc file
    def save_into_db(self):
        query = """
            INSERT INTO categories (name, url, parent_id)
            VALUES (?, ?, ?);
        """
        val = (self.name, self.url, self.parent_id)
        try:
            cur.execute(query,val)
            self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

class Product:
    def __init__(self, cat_id, name, url, parent_id, product_id, price, category_name):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id
        self.product_id = product_id
        self.price = price
        self.category_name = category_name

    def __repr__(self):
        return "ID: {}, Name: {}, URL: {}, Parent_id: {}, Product_id: {},Price: {}, Category_name: {}".format(self.cat_id, self.name, self.url, self.parent_id, self.product_id, self.price,self.category_name)

# commit lưu đc file
    def save_into_db(self):
        query = """
            INSERT INTO product (name, url, parent_id, product_id, price, category)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        val = (self.name, self.url, self.parent_id, self.product_id, self.price, self.category_name)
        try:
            cur.execute(query,val)
            self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

def get_url(url):
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, 'html.parser')
        return response
    except Exception as err:
        print('ERROR BY REQUEST:', err)

def get_main_categories(save_db=False):
    soup = get_url(TIKI)

    result = []
    for a in soup.findAll('a', {'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        cat_id = None
        name = a.find('span', {'class':'text'}).text
        url = a['href']
        parent_id = None

        cat = Category(cat_id, name, url, parent_id)
        if save_db:
            cat.save_into_db()
        result.append(cat)
    return result

# print(get_main_categories(save_db=True))
''' - still not work
def get_main_categories(save_db=False):
    # Run Parser on Tiki
    s = parse(TIKI_URL)
    
    # Initialize an empty list of category 
    category_list = []

    # Scrape through the navigator bar on Tiki homepage
    for i in s.findAll('a',{'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        # new category has no id
        cat_id = None
        
        # Get the category name
        name = i.find('span',{'class':'text'}).text 
        
        # Get the url value
        url = i['href'] + "&page=1"
        
        # main categories has no parent
        parent_id = None
        
        # Add category and url values to list
        cat = Category(None, name, url, parent_id)
        if save_db:
            cat.save_into_db()
        category_list.append(cat)
        
    return category_list
    #main_categories = get_main_categories(save_db=True)

def get_sub_categories(category, save_db=False):
    name = category.name
    url = category.url
    sub_categories = []

    try:
        div_containers = parse(url).find_all('div', attrs={"class": "list-group-item is-child"})
        for div in div_containers:
            sub_id = None
            sub_name = div.a.text
            sub_url = 'https://tiki.vn' + div.a.get('href')
            sub_parent_id = category.cat_id
            
            cat = Category(sub_id, sub_name, sub_url, sub_parent_id)
            if save_db:
                cat.save_into_db()
            if cat.cat_id is not None:
                sub_categories.append(cat)
    except Exception as err:
        print(f'ERROR: {err}')
    
    return sub_categories

def get_all_categories(main_categories):
    queue = deque(main_categories)
    count = 0
    
    while queue:
        parent_cat = queue.popleft()
        sub_list = get_sub_categories(parent_cat, save_db=True)
        queue.extend(sub_list)
        
        # sub_list is empty, which mean the parent_cat has no sub-categories
        if not sub_list:
            count+=1
            if count % 100 == 0:
                print(f'{count} number of deepest nodes')
'''
                
def get_product(category, save_db=False):
    name = category.name
    url = category.url
    parent_id = category.parent_id
    result = []
   
    try:
    #for sub_page in main_page:
        #page = load_web(sub_page[1])
        soup = get_url(url)
        div_containers = soup.findAll('div', {'class':"product-item"}, limit=500)

        for div in div_containers:
            proid = None
            pro_name = div['data-title']
            pro_url = div.a['href']
            pro_parent_id = parent_id
            pro_id = div['data-seller-product-id']
            pro_price = div['data-price']
            pro_cat_name = name
                
            pro = Product(proid,pro_name,pro_url,pro_parent_id,pro_id, pro_price,pro_cat_name)
            
            if save_db:
                pro.save_into_db()
            result.append(pro)

    except Exception as err:
        print('ERROR BY GET SUB CATEGORIES:', err)

    return result


#main_categories = get_main_categories(save_db=True)
# tạo bảng chạy
#get_main_categories(save_db=True) 
#data 16 cái categories
#get_main_categories(save_db=False)
# rồi chạy vòng for:
#for sp in get_main_categories(save_db=False):
#    get_product(sp,save_db=True)
# select xem thành phẩm

#get_main_categories (save_db=True)
#print(select_all('categories'))

#create_categories_table()
#create_product_table()
# delete_all('categories')
#a = Product(1,"ggg","dfdfd",12,"12252","2222","1111")
#a.save_into_db()
#print(select_all('product'))
# delete_all('product')
# get_main_categories(save_db=True)
