import aiohttp
API_URL_Prod = 'https://emirmagalov13.pythonanywhere.com/api/products/?subcategory='
API_URL_Categ = 'https://emirmagalov13.pythonanywhere.com/api/category/'
API_URL_Banner = 'https://emirmagalov13.pythonanywhere.com/api/banner/?name='
API_URL_Subcategory = 'https://emirmagalov13.pythonanywhere.com/api/subcategory/?id='
API_URL_OneProd = 'https://emirmagalov13.pythonanywhere.com/api/oneproduct/?id='

async def categ():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_Categ) as response:
            if response.status == 200:
                products = await response.json()
                result = []
                for product in products:
                    result.append(product)
                return result



            else:
                print("error")



async def product(subcategory):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_Prod}{subcategory}") as response:
            if response.status == 200:
                products = await response.json()
                result = []
                for product in products:
                    result.append(product)
                return result



            else:
                print("error")
async def one_product(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_OneProd}{id}") as response:
            if response.status == 200:
                products = await response.json()
                result = []
                for product in products:
                    result.append(product)
                return result



            else:
                print("error")
async def subcateg(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_Subcategory}{id}") as response:
            if response.status == 200:
                products = await response.json()
                result = []
                for product in products:
                    result.append(product)
                return result



            else:
                print("error")


async def banner(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_Banner}{name}") as response:
            if response.status == 200:
                products = await response.json()

                return products



            else:
                print("error")