import boto3
import json
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Set the model ID for Claude 3.5 Haiku.
model_id = "anthropic.claude-3-5-haiku-20241022-v1:0"

# Define the prompt for the model.
prompt = "Can you covert this to SQL? How many blue shirts do we have left in stock"

# Format the request payload using the model's native structure.
native_request = {
    "modelId": "anthropic.claude-3-5-haiku-20241022-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "top_k": 250,
            "temperature": 1,
            "top_p": 0.999,
            "messages": [{"role": "user", "content": prompt}],
        }
    ),
}
# Invoke the model with the request.
try:
    response = client.invoke_model(**native_request)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    print(model_response)
except ClientError as e:
    print(f"ClientError: {e}")
except Exception as e:
    print(f"Error: {e}")
