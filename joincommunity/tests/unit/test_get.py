import json
import unittest
from moto import mock_aws
import boto3


# Import the lambda function
from joincommunity.get.main import lambda_handler

@mock_aws
class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.create_table(
            TableName='JoinCommunityParticipants',
            KeySchema=[
                {'AttributeName': 'participantId', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'participantId', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        self.table.meta.client.get_waiter('table_exists').wait(TableName='JoinCommunityParticipants')

    def test_lambda_handler_participant_found(self):
        """Test the lambda handler when a participant is found."""
        participant_id = "12345"
        self.table.put_item(Item={'participantId': participant_id, 'name': 'John Doe'})
        event = {'pathParameters': {'participantId': participant_id}}

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['participantId'], participant_id)
        self.assertEqual(body['name'], 'John Doe')

    def test_lambda_handler_participant_not_found(self):
        """Test the lambda handler when a participant is not found."""
        participant_id = "non_existent"
        event = {'pathParameters': {'participantId': participant_id}}

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(response['body'], json.dumps(f'Participant {participant_id} not found'))

if __name__ == '__main__':
    unittest.main()