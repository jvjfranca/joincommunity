import json
from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JoinCommunityParticipants')

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        participant_id: str = event['pathParameters']['participantId']
        response = table.get_item(
            Key={
                'participantId': participant_id
            }
        )
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps(f'Participant {participant_id} not found')
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'Error': f'An unexpected error occurred: {str(e)}'})
        }