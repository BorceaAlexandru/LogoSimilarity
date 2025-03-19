import numpy as np
from networkx.algorithms.bipartite.cluster import clustering
from sklearn.cluster import AgglomerativeClustering
from services.extractor import compare_features

def compute_similarity_matrix(descriptors_list):
    n=len(descriptors_list)
    similarity_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1, n):
            similarity=compare_features(descriptors_list[i], descriptors_list[j])
            similarity_matrix[i,j]=similarity
            similarity_matrix[j,i]=similarity
    return similarity_matrix

def group_logos(descriptors_list, n_clusters=5):
    similarity_matrix=compute_similarity_matrix(descriptors_list)
    clustering=AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage='average')
    labels=clustering.fit_predict(similarity_matrix)
    return labels