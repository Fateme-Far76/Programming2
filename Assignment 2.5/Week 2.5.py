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
    # You should have called the variable `ddf`, to make clear that it is a Dask dataframe.
    df = dd.read_csv(file_path, delimiter="\t", dtype=str, header=None, names=list(str(range(15))))
    return df


if __name__ == '__main__': 
    
    # Load the DataFrame
    file_path = '/data/dataprocessing/interproscan/all_bacilli.tsv'
    df = load_dataframe(file_path)
        
    # How many distinct protein annotations are found in the dataset?
    distinct_protein_annotations = df['11'].nunique().compute(num_worker=16)
    print("Number of distinct protein annotations:", distinct_protein_annotations)

    # How many annotations does a protein have on average?
    average_annotations_for_protein = df.groupby('0')['IPR022291'].count().mean().compute(num_worker=16)
    print("Average number of annotations per protein:", average_annotations_for_protein)

    # What is the most common GO Term found?
    go_terms = df['0'].str.split('|').explode(num_worker=16)
    most_frequent_go_term = go_terms.value_counts().nlargest(1).compute().index[0] 
    print("Most common GO Term:", most_frequent_go_term)

    # What is the average size of an InterPRO feature found in the dataset?
    df['FeatureSize'] = df['7'].astype(int) - df['6'].astype(int)
    average_size_of_interpro_feature = df['FeatureSize'].mean().compute(num_worker=16)
    print("Average size of InterPRO feature:", average_size_of_interpro_feature)

    # What is the top 10 most common InterPRO features?
    top_10_frequent_interpro_features = df['1'].value_counts().nlargest(10).compute(num_worker=16)
    print("Top 10 most common InterPRO features:", top_10_frequent_interpro_features) 

    # If you select InterPRO features that are almost the same size (within 90-100%) as the protein itself, what is the top 10 then?
    protein_length = df['2'].astype(int) 
    selected_features = df[abs(df['FeatureSize'] - protein_length) / protein_length <= 0.9] 
    top_10_frequent_selected_features = selected_features['1'].value_counts().nlargest(10).compute(num_worker=16)
    print("Top 10 most common selected InterPRO features:", top_10_frequent_selected_features) 

    # If you look at those features which also have textual annotation, what is the top 10 most common word found in that annotation?
    features_with_text = df[df['4'].notnull()]['5']
    top_10_common_words_in_text = features_with_text.str.split().explode().value_counts().nlargest(10).compute(num_worker=16)
    print("Top 10 most common words in annotation:", top_10_common_words_in_text) 

    # And the top 10 least common?
    features_with_text = df[df['4'].notnull()]['5']
    top_10_least_common_words_in_text = features_with_text.str.split().explode().value_counts().tail(10) 
    print("Top 10 least common words in annotation:", top_10_least_common_words_in_text) 
    
    # What is the coefficient of correlation between the size of the protein and the number of features found? 
    coefficient_of_correlation = df['2'].astype(int).corr(df['7'].astype(int) - df['6'].astype(int)) 
    protein_feature_correlation = coefficient_of_correlation.compute(num_worker=16)
    print("Correlation coefficient between protein size and number of features:", protein_feature_correlation)
