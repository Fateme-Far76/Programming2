import asyncio
import aiohttp
import json

class NetworkClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def fetch_data(self, endpoint, callback):
        url = self.base_url + endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    result = json.loads(data)
                    return callback(result)
                else:
                    return None
                
def calculate_average_year(data):
    temperatures = [entry["Yearly Average"] for entry in data]
    average_temperature = sum(temperatures) / len(temperatures)
    return {"Average Temperature": average_temperature}

def calculate_average_month(data):
    monthly_averages = {month: 0.0 for month in data[0].keys() if month != "Year"}
    count = 0
    for entry in data:
        for month in monthly_averages.keys():
            monthly_averages[month] += entry[month]
        count += 1
    
    for month in monthly_averages.keys():
        monthly_averages[month] /= count

    return monthly_averages


async def main():
    client = NetworkClient("http://localhost:8000/data")
    tasks = [
        client.fetch_data("all", calculate_average_year),
        client.fetch_data("1991", calculate_average_year),
        client.fetch_data("1991/2000", calculate_average_month) 
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        if result is not None:
            print(result)
        else:
            print("Error fetching data")

if __name__ == "__main__":
    asyncio.run(main())
