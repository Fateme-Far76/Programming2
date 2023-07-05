import asyncio
import aiohttp
import json

class NetworkDataFetcher:
    '''This class provides the methods to fetch data from a server'''

    def __init__(self, base_url):
        '''Initializes the NetworkDataFetcher with the base URL of the data server'''
        self.base_url = base_url

    async def fetch_data(self, endpoint, data_processing_callback):
        '''Fetches data from the provided endpoint, processes it using the callback function'''

        # Determines the full URL based on the base URL and the endpoint
        url = endpoint if endpoint.startswith('http') else self.base_url + '/' + endpoint

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f"Fetching data from {url}: {response.status}")
                if response.status == 200:
                    raw_data = await response.text()
                    print(f"Data received: {raw_data[:100]}...")
                    processed_data = json.loads(raw_data)
                    return data_processing_callback(processed_data)
                else:
                    print(f"Error fetching data from {url}: {response.status} {await response.text()}")
                    return None

def calculate_yearly_average(data):
    '''Calculates the average temperature for each month in the given year's data'''

    averages = {month: sum(temperatures.values()) / len(temperatures) for month, temperatures in data.items() if month != 'Year'}

    return {'Average Temperature': averages}


def calculate_monthly_average(data):
    '''Calculates the average temperature for each month in the given data'''

    averages = {month: sum(temperatures.values()) / len(temperatures) for month, temperatures in data.items() if month != 'Year'}

    return {'Average Temperature': averages}


async def main():
    '''This is the main method. It initializes the data fetcher and fetches data from different endpoints.'''

    data_fetcher = NetworkDataFetcher("http://localhost:8080/data")
    fetch_tasks = [
        data_fetcher.fetch_data("all", calculate_yearly_average),
        data_fetcher.fetch_data("1991", calculate_monthly_average),
        data_fetcher.fetch_data("http://localhost:8080/data/1991-2000", calculate_monthly_average)
    ]
    
    # Wait for all fetch tasks to complete
    results = await asyncio.gather(*fetch_tasks)

    # Print the results
    for result in results:
        print("Result:" if result else "No result returned for a task", result)

if __name__ == "__main__":
    asyncio.run(main())
