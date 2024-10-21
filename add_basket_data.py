import aiohttp
API_URL_Add_basket = 'https://emirmagalov13.pythonanywhere.com/api/add_basket/'
API_URL_Put_basket = 'https://emirmagalov13.pythonanywhere.com/api/update_basket/'
API_URL_Get_basket = 'https://emirmagalov13.pythonanywhere.com/api/get_basket/'
API_URL_Userbasketprod='https://emirmagalov13.pythonanywhere.com/api/userbasket/'
API_URL_Plusminus = 'https://emirmagalov13.pythonanywhere.com/api/plusminus/'
async def add_basket(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_Add_basket, json=data) as response:
            if response.status == 201:

                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status}, {error_message}")
                return None


async def get_basket(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL_Get_basket}{user_id}/") as response:
            if response.status == 200:

                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status}, {error_message}")
                return None

async def update_basket(user_id, data):
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{API_URL_Put_basket}{user_id}/", json=data) as response:
            if response.status == 200:

                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status}, {error_message}")
                return None
async def del_basket(user_id, data):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL_Put_basket}{user_id}/", json=data) as response:
            if response.status == 200:

                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status}, {error_message}")
                return None
async def plusminus_basket(user_id,data):
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{API_URL_Plusminus}{user_id}/", json=data) as response:
            if response.status == 200:

                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status}, {error_message}")
                return None


async def userbasketprod(ids):
    url = API_URL_Userbasketprod
    params = {'id': ids}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                products = await response.json()
                return products
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None