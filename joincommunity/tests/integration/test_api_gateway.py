import boto3
import pytest
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

class TestApiGateway:
    @pytest.fixture(scope="class")
    def api_gateway_url(self):
        """Get the API Gateway URL from Cloudformation Stack outputs"""
        logger.info("Setting up API Gateway URL...")
        stack_name = "joincommunity"
        if stack_name is None:
            raise ValueError('Stack name is required')
        
        client = boto3.client("cloudformation")
        try:
            logger.info(f"Describing stack: {stack_name}")
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            error_msg = f"Cannot find stack {stack_name}. Please make sure a stack with the name '{stack_name}' exists"
            logger.error(error_msg)
            raise Exception(error_msg) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "ApiUrl"]
        if not api_outputs:
            error_msg = f"API not found in stack {stack_name}"
            logger.error(error_msg)
            raise KeyError(error_msg)
        
        api_url = api_outputs[0]["OutputValue"]
        logger.info(f"API Gateway URL: {api_url}")
        return api_url

    def test_post_participant(self, api_gateway_url):
        """Call the API Gateway endpoint to post a participant"""
        logger.info("Testing POST /participant endpoint")
        url = f"{api_gateway_url}/participant"
        data = {
            "participantId": "1",
            "name": "John Doe",
            "email": "johndoe@joincommunity.com.br",
        }
        logger.info(f"Sending POST request to {url}")
        logger.info(f"Request data: {data}")
        
        response = requests.post(url, json=data)
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        
        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        logger.info("POST /participant test passed")

    def test_get_participant(self, api_gateway_url):
        """Call the API Gateway endpoint to get a participant"""
        logger.info("Testing GET /participant/1 endpoint")
        url = f"{api_gateway_url}/participant/1"
        logger.info(f"Sending GET request to {url}")
        
        response = requests.get(url)
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        logger.info("GET /participant/1 test passed")