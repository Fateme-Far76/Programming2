# Importing necessary libraries
import ssl
import time
import os
import multiprocessing as mp
from Bio import Entrez

# Avoid SSL error
ssl._create_default_https_context = ssl._create_unverified_context

# Set the email and NCBI API Key for Entrez. 

# The way you have setup these tests results in a lot of duplicate code.
# You could have abstracted away all these duplication and still perform the 
# same tests.

Entrez.email = 'f.rakhshanifar@st.hanze.nl'
Entrez.api_key = '3fb661596ffc24f9f2fa5ae75f8ae8b76709'


def retrieve_and_save_article(article_id):
    ''' 
    Function to retrieve an article from PubMed Central (PMC) and save it into a file. 
    This function fetches the article in XML format and writes it to a file named as {article_id}.txt. 
    
    Args:
        article_id (str): The id of the article to be fetched from PMC.

    Raises:
        Exception: If an error occurs during the retrieval and saving process.
    '''
    try:
        # Pause for a second to respect NCBI's rate limit of requests per second.
        time.sleep(1)

        # Retrieve the article from PMC using the provided article id.
        handle = Entrez.efetch(db="pmc", id=article_id, rettype="full", retmode="xml", api_key=Entrez.api_key)

        # Write the retrieved article content to a file.
        with open(f"{article_id}.txt", 'w') as file:
            file.write(handle.read().decode('utf-8'))
    except Exception as e:
        print(f"Error occurred with article {article_id}: {e}")


def parallel_download_articles(pubmed_id):
    ''' 
    Function to download the first ten articles citing a given pubmed id in parallel.
    This function finds the first ten articles that cite the given pubmed id and downloads them in parallel using multiprocessing.
    It also calculates and prints the time taken for the downloading process.
    
    Args:
        pubmed_id (str): The PubMed id of the article to find the citing articles for.

    '''
    try:
        # Fetch the list of articles that cite the given pubmed id.
        file = Entrez.elink(dbfrom="pubmed", db="pmc", LinkName="pubmed_pmc_refs", id=pubmed_id, api_key=Entrez.api_key)

        # Read the fetched results and convert the article ids to strings.
        results = Entrez.read(file)
        references = [str(link["Id"]) for link in results[0]["LinkSetDb"][0]["Link"]]

        # Measure the time taken for downloading the first ten articles in parallel.
        start_time = time.time()

        # Create a multiprocessing pool and download the first ten articles in parallel.
        with mp.Pool(10) as pool:
            pool.map(retrieve_and_save_article, references[:10])

        # Print the execution time.
        print(f"Execution time: {time.time() - start_time} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")


def run_program():
    '''
    The main function to run the program.

    This function sets the pubmed id, prints a processing message, and calls the function to download the articles in parallel.
    '''
    pubmed_id = "30049270"
    print(f"Processing article {pubmed_id}...")
    parallel_download_articles(pubmed_id)


if __name__ == "__main__": 
    run_program()
