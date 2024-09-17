import json
import unittest
from moto import mock_aws
import boto3

# Import the lambda function
from joincommunity.post.main import lambda_handler

@mock_aws
class TestAddParticipantLambdaHandler(unittest.TestCase):
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

    def test_lambda_handler_participant_added_successfully(self):
        """Test the lambda handler when a participant is added successfully."""
        event = {
            'body': json.dumps({
                'participantId': '12345',
                'name': 'John Doe',
                'email': 'john@example.com'
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 201)
        self.assertEqual(response['body'], json.dumps('Participant 12345 added successfully'))

        # Verify the item was added to the table
        item = self.table.get_item(Key={'participantId': '12345'})
        self.assertIn('Item', item)
        self.assertEqual(item['Item']['name'], 'John Doe')
        self.assertEqual(item['Item']['email'], 'john@example.com')

    def test_lambda_handler_missing_required_fields(self):
        """Test the lambda handler when required fields are missing."""
        event = {
            'body': json.dumps({
                'name': 'John Doe'
                # Missing participantId
            })
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['body'], json.dumps('Error: Missing required fields'))

if __name__ == '__main__':
    unittest.main()