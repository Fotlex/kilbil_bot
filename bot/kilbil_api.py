import aiohttp

from config import config
    

async def search_client(phone_num):
    async with aiohttp.ClientSession() as session:
        payload = {
            "search_mode": 0,
            "search_value": phone_num,
        }
        try:
            async with session.post(f"{config.KILBIL_URL}/load/searchclient?h={config.API_KEY}", json=payload) as response:
                return await response.json()
        except Exception as e:
            print(f'При запросе поиска клиента возникла ошибка - {e}')
            
            
async def create_client(phone_num, last_name, first_name, surname, mail, birth_date):
    async with aiohttp.ClientSession() as session:
        payload = {
            "client_id": None,
            "phone": phone_num,
            "first_name": first_name,
            "middle_name": surname,
            "last_name": last_name,
            "birth_date": birth_date,
            "email": mail,
        }
        try:
            async with session.post(f"{config.KILBIL_URL}/load/addclient?h={config.API_KEY}", json=payload) as response:
                response.raise_for_status() 
                return await response.json()
        except Exception as e:
            print(f'При запросе создания клиента возникла ошибка - {e}')
            
        
async def get_ballance_info(client_id):
    async with aiohttp.ClientSession() as session:
        payload = {
            "client_id": client_id,
        }
        try:
            async with session.post(f"{config.KILBIL_URL}/load/getclientfullbalance?h={config.API_KEY}", json=payload) as response:
                response.raise_for_status() 
                return await response.json()
        except Exception as e:
            print(f'При запросе баланса клиента возникла ошибка - {e}')
            
            
async def get_operation_history(client_id):
    async with aiohttp.ClientSession() as session:
        payload = {
            "client_id": client_id,
        }
        try:
            async with session.post(f"{config.KILBIL_URL}/load/getmovesbyclient?h={config.API_KEY}", json=payload) as response:
                response.raise_for_status() 
                return await response.json()
        except Exception as e:
            print(f'При запросе операций клиента возникла ошибка - {e}')
            
            
async def get_wallet_card(client_id, outer_systems_interface_type = 5):
    async with aiohttp.ClientSession() as session:
        payload = {
            "client_id": client_id,
            "outer_systems_interface_type": outer_systems_interface_type,
        }
        try:
            async with session.post(f"{config.KILBIL_URL}/load/getconfirmationcode?h={config.API_KEY}", json=payload) as response:
                response.raise_for_status() 
                return await response.json()
        except Exception as e:
            print(f'При запросе карты клиента возникла ошибка - {e}')