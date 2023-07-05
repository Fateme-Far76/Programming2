import ssl
from Bio import Entrez
from time import sleep, time

# Avoid SSL error
ssl._create_default_https_context = ssl._create_unverified_context

# Set email and NCBI API Key
Entrez.email = 'f.rakhshanifar@st.hanze.nl'
Entrez.api_key = '3fb661596ffc24f9f2fa5ae75f8ae8b76709'

def fetch_article_and_save(article_id):
    ''' 
    Retrieve an article from PMC (PubMed Central) and save it to a file.

    Args:
        article_id (str): The ID of the article to retrieve and save.
    '''
    sleep(1) 
    try:
        handle = Entrez.efetch(db="pmc", id=article_id, rettype="full", retmode="text", api_key=Entrez.api_key)
        with open(f"{article_id}.txt", 'w') as out_file:
            out_file.write(handle.read())
    except Exception as ex:
        print(f"Error occurred with article {article_id}: {ex}")


def retrieve_and_save_articles(pubmed_id):
    ''' 
    Retrieves and saves the first ten articles citing the provided PubMed ID.

    Args:
        pubmed_id (str): The PubMed ID of the article.

    Raises:
        Exception: If an error occurs during the retrieval and saving process.
    '''
    try:
        file = Entrez.elink(dbfrom="pubmed", db="pmc", LinkName="pubmed_pmc_refs", id=pubmed_id, api_key=Entrez.api_key)
        results = Entrez.read(file)
        references = [str(link["Id"]) for link in results[0]["LinkSetDb"][0]["Link"]]  # Convert to strings

        # Download and save the first ten articles sequentially
        start_time = time()
        for article_id in references[:10]:
            fetch_article_and_save(article_id)
        print(f"Execution time: {time() - start_time} seconds")

    except Exception as ex:
        print(f"An error occurred: {ex}")


def run_program():
    ''' 
    Runs the program by retrieving and saving articles based on a PubMed ID.
    '''
    pubmed_id = "30049270"
    print(f"Processing article {pubmed_id}...")
    retrieve_and_save_articles(pubmed_id)


if __name__ == "__main__":
    run_program()
