import numpy as np

class SimilarityMetrics:   
    def __init__(self, query, data):
        self._query = query
        self._data = data 

    def absolute_difference(self):
        axis_batch_size = tuple(range(1, len(self._data.shape)))
        return np.sum(np.abs(self._data - self._query), axis = axis_batch_size)
    
    def mean_square_difference(self):
        axis_batch_size = tuple(range(1, len(self._data.shape)))
        return np.sqrt(np.sum((self._query - self._data) ** 2, axis=axis_batch_size))
    
    def cosine_similarity(self):
        axis_batch_size = tuple(range(1, len(self._data.shape)))
        query_norm = np.sqrt(np.sum(self._query**2)) 
        data_norm = np.sqrt(np.sum(self._data**2, axis=axis_batch_size))
        return np.sum(self._data * self._query, axis=axis_batch_size) / (query_norm * data_norm + np.finfo(float).eps)
    
    def correlation_coefficient(self):
        axis_batch_size = tuple(range(1, len(self._data.shape)))
        query_mean = self._query - np.mean(self._query)
        data_mean = self._data - np.mean(self._data, axis=axis_batch_size, keepdims=True)
        query_norm = np.sqrt(np.sum(query_mean**2)) 
        data_norm = np.sqrt(np.sum(data_mean**2, axis=axis_batch_size))
        return np.sum(data_mean * query_mean, axis=axis_batch_size) / (query_norm * data_norm + np.finfo(float).eps)