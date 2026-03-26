import json
import math


def lambda_handler(event, context):
    result = sum(math.sqrt(i) for i in range(1000))
    return {
        'statusCode': 200,
        'body': json.dumps({
            'result': result,
            'message': 'ok'
        })
    }
