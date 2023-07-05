from Bio import Entrez 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Step 1: provide the api key to the Entrez.email variable
Entrez.email = 'r.rakhshanifar@st.hanze.nl'

# Step 2: provide the search term and the database to search in
file = Entrez.elink(dbfrom="pubmed",
                    db="pmc",
                    LinkName="pubmed_pmc_refs",
                    id="30049270",
                    api_key='3fb661596ffc24f9f2fa5ae75f8ae8b76709')

# Step 3: read the results
results = Entrez.read(file)
print(results)
