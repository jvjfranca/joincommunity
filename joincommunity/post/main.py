import json
from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JoinCommunityParticipants')

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        body = json.loads(event['body'])
        participant_id: str = body['participantId']
        
        table.put_item(Item=body)
        
        return {
            'statusCode': 201,
            'body': json.dumps(f'Participant {participant_id} added successfully')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing required fields')
        }