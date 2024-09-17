import boto3
import pytest
import requests

class TestApiGateway:
    @pytest.fixture(scope="class")
    def api_gateway_url(self):
        """Get the API Gateway URL from Cloudformation Stack outputs"""
        pytest.helpers.info("Setting up API Gateway URL...")
        stack_name = "joincommunity"
        if stack_name is None:
            raise ValueError('Stack name is required')
        
        client = boto3.client("cloudformation")
        try:
            pytest.helpers.info(f"Describing stack: {stack_name}")
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            error_msg = f"Cannot find stack {stack_name}. Please make sure a stack with the name '{stack_name}' exists"
            pytest.helpers.error(error_msg)
            raise Exception(error_msg) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "ApiUrl"]
        if not api_outputs:
            error_msg = f"API not found in stack {stack_name}"
            pytest.helpers.error(error_msg)
            raise KeyError(error_msg)
        
        api_url = api_outputs[0]["OutputValue"]
        pytest.helpers.info(f"API Gateway URL: {api_url}")
        return api_url

    def test_post_participant(self, api_gateway_url):
        """Call the API Gateway endpoint to post a participant"""
        pytest.helpers.info("\nTesting POST /participant endpoint")
        url = f"{api_gateway_url}/participant"
        data = {
            "participantId": "1",
            "name": "John Doe",
            "email": "johndoe@joincommunity.com.br",
        }
        pytest.helpers.info(f"Sending POST request to {url}")
        pytest.helpers.info(f"Request data: {data}")
        
        response = requests.post(url, json=data)
        
        pytest.helpers.info(f"Response status code: {response.status_code}")
        pytest.helpers.info(f"Response body: {response.text}")
        
        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        pytest.helpers.info("POST /participant test passed")

    def test_get_participant(self, api_gateway_url):
        """Call the API Gateway endpoint to get a participant"""
        pytest.helpers.info("\nTesting GET /participant/1 endpoint")
        url = f"{api_gateway_url}/participant/1"
        pytest.helpers.info(f"Sending GET request to {url}")
        
        response = requests.get(url)
        
        pytest.helpers.info(f"Response status code: {response.status_code}")
        pytest.helpers.info(f"Response body: {response.text}")
        
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        pytest.helpers.info("GET /participant/1 test passed")