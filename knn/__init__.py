import azure.functions as func
import numpy as np
import requests, gzip, math, json

def fetch(url):
    compressed_data = requests.get(url).content
    data = np.frombuffer(gzip.decompress(compressed_data), dtype=np.uint8).copy()
    return data

def distance(a,b):
    m, n = a.shape
    dist = 0
    for i in range(m):
        for j in range(n):
            dist += (a[i,j]-b[i,j])*(a[i,j]-b[i,j])
    return math.sqrt(dist)

def distances(x, X, Y):
    result = []
    print(len(X), len(Y))
    for x_train, y in zip(X, Y):
        result.append((distance(x, x_train), y.item()))
    result.sort()
    return result

def kNN(i, batch_size, batch_number, total_mini_batches):
    X = fetch("http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz")[0x10:].reshape((-1, 28, 28))
    Y = fetch("http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz")[8:]
    X_test = fetch("http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz")[0x10:].reshape((-1, 28, 28))
    Y_test = fetch("http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz")[8:]
    results = []
    if batch_number == 0:
        results = distances(X_test[i], X[0:batch_size,], Y[0:batch_size,])[:5]
    else:
        mini_batch_size = int(batch_size/total_mini_batches)
        lower_bound = mini_batch_size*(batch_number-1)
        upper_bound = mini_batch_size*batch_number
        results = distances(X_test[i], X[lower_bound:upper_bound,], Y[lower_bound:upper_bound,])[:5]
    return json.dumps({'distances':results, 'ground_truth':Y_test[i].item()})

def main(req: func.HttpRequest) -> func.HttpResponse:
    id = int(req.params.get('id'))
    batch_number = int(req.params.get('batch_number'))
    batch_size = int(req.params.get('batch_size'))
    total_mini_batches = int(req.params.get('total_mini_batches'))
    return func.HttpResponse(kNN(id, batch_size, batch_number, total_mini_batches))
