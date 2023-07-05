import dask.dataframe as dd
import dask.array as da
import numpy as np 

import dask.dataframe as dd

def load_dataframe(file_path):
    """
    Loads a Dask DataFrame from a CSV file.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        df (dask.dataframe.DataFrame): The loaded Dask DataFrame.
    """
    df = dd.read_csv(file_path, delimiter="\t")
    return df


if __name__ == '__main__': 
    
    # Load the DataFrame
    file_path = '/data/dataprocessing/interproscan/all_bacilli.tsv'
    df = load_dataframe(file_path)
        
    # How many distinct protein annotations are found in the dataset?
    distinct_protein_annotations = df['IPR022291'].nunique().compute()
    print("Number of distinct protein annotations:", distinct_protein_annotations)

    # How many annotations does a protein have on average?
    average_annotations_for_protein = df.groupby('gi|29898682|gb|AAP11954.1|')['IPR022291'].count().mean().compute()
    print("Average number of annotations per protein:", average_annotations_for_protein)

    # What is the most common GO Term found?
    most_frequent_go_term = df['TIGRFAM'].mode().compute()
    print("Most common GO Term:", most_frequent_go_term)

    # What is the average size of an InterPRO feature found in the dataset?
    average_size_of_interpro_feature = df['547'].mean().compute()
    print("Average size of InterPRO feature:", average_size_of_interpro_feature)

    # What is the top 10 most common InterPRO features?
    top_10_frequent_interpro_features = df['TIGR03882'].value_counts().nlargest(10).compute()
    print("Top 10 most common InterPRO features:")
    print(top_10_frequent_interpro_features)

    # If you select InterPRO features that are almost the same size (within 90-100%) as the protein itself, what is the top 10 then?
    protein_length = df['92d1264e347e149248231cb9b649388c'].astype(str)
    protein_length = dd.to_numeric(protein_length, errors='coerce')
    protein_length = protein_length[protein_length.notnull()]  # Filter out non-numeric values
    selected_features = df[(protein_length.notnull()) & (df['547'] >= protein_length * 0.9) & (df['547'] <= protein_length * 1.0)]['TIGR03882']
    top_10_frequent_selected_features = selected_features.value_counts().nlargest(10).compute()
    print("Top 10 most common selected InterPRO features:")
    print(top_10_frequent_selected_features)

    # If you look at those features which also have textual annotation, what is the top 10 most common word found in that annotation?
    features_with_text = df[df['TIGR03882'].notnull()]['cyclo_dehyd_2: bacteriocin biosynthesis cyclodehydratase domain']
    top_10_common_words_in_text = features_with_text.str.split().explode().value_counts().nlargest(10).compute()
    print("Top 10 most common words in annotation:")
    print(top_10_common_words_in_text)

    # And the top 10 least common?
    features_with_text = df[df['TIGR03882'].notnull()]['cyclo_dehyd_2: bacteriocin biosynthesis cyclodehydratase domain']
    top_10_least_common_words_in_text = features_with_text.str.split().explode().value_counts().tail(10) 
    print("Top 10 least common words in annotation:")
    print(top_10_least_common_words_in_text)

    # What is the coefficient of correlation between the size of the protein and the number of features found?
    protein_feature_correlation = da.correlate(protein_length.to_dask_array(lengths=True), df['TIGR03882'].to_dask_array(lengths=True), dtype=np.float64).compute()
    print("Correlation coefficient between protein size and number of features:", protein_feature_correlation)
