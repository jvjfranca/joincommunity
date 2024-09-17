import boto3
import pytest
import requests
class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = "joincommunity"

        if stack_name is None:
            raise ValueError('Stack name is required')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "ApiUrl"]

        if not api_outputs:
            raise KeyError(f"API not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

    def test_post_participant(self, api_gateway_url):
        """ Call the API Gateway endpoint to post a participant """
        url = f"{api_gateway_url}/participant"
        data = {
            "participantId": "1",
            "name": "John Doe",
            "email": "johndoe@joincommunity.com.br",
        }
        response = requests.post(url, json=data)
        assert response.status_code == 201


    def test_get_participant(self, api_gateway_url):
        """ Call the API Gateway endpoint to get a participant """
        url = f"{api_gateway_url}/participant/1"
        response = requests.get(url)
        assert response.status_code == 200
