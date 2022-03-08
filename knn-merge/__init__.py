import azure.functions as func
import json, urllib.parse

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = req.params.get('data')
    decoded_distances = urllib.parse.unquote(data).strip().split('\n')
    result = []
    for d in decoded_distances:
        json_object = json.loads(d)
        for dist in json_object["distances"]:
            result.append(dist)
    result.sort()
    return json.dumps({'distances':result[:5]})