#!/bin/bash
for i in {1..6}; do
    #url='http://localhost:7071/api/knn?id=0&batch_number='$i
    url='https://knn-serverless.azurewebsites.net/api/knn?code=b5BaGjBshHgTVYNzueo1ZDrJEwNGQLvpG6DjfIDa8KJVp0CnDi1aBw==&id=0&batch_number='$i
    ( curl -G $url; echo '' ) >> op.txt &
done
wait

payload=$(cat op.txt)
#url='http://localhost:7071/api/knn-merge'
url='https://knn-serverless.azurewebsites.net/api/knn-merge?code=8rEV8r48bygHoHAbZMKuv2rB3LuEDjM9F35oaUZG7TQwvFR3kVRGiQ=='
curl -G --data-urlencode "data=""$payload" $url