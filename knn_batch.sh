#!/bin/bash
#url='http://localhost:7071/api/knn?id=0&batch_number=0&batch_size='$1'&total_mini_batches=0'
url='https://knn-serverless.azurewebsites.net/api/knn?code=b5BaGjBshHgTVYNzueo1ZDrJEwNGQLvpG6DjfIDa8KJVp0CnDi1aBw==&id=0&batch_number=0&batch_size='$1'&total_mini_batches=0'
var=`curl -G $url`