# Automating-blog-content-generation

I used API Gateway to create API endpoints for users to interact with the application. These API endpoints trigger an AWS Lambda function that I created. Within this Lambda function, I invoked Amazon Bedrock's foundational Llama models using Boto3 (AWS's Python SDK, specifically designed for interacting with AWS services. After invoking the model, I stored the generated text responses into an Amazon S3 bucket directly from the Lambda function.

Challenges faced during implementation:

Provisioned Throughput Requirement:
Initially, when using the foundational Llama model on Amazon Bedrock, I encountered errors stating that the model required provisioned throughput, despite being labeled as serverless. This requirement was not explicitly indicated initially, necessitating a deeper investigation into provisioning needs.

Parsing Response Format:
After switching to Amazon’s foundational model 'Nova' due to the provisioning issue, I updated the request body and model ID accordingly. However, I lacked detailed knowledge of the response structure. To address this, I used Postman to send a POST request directly to the API endpoint and then examined the response structure captured in AWS CloudWatch logs. This allowed me to identify the correct response format and successfully parse the generated text.

Managing Boto3 Versions in Lambda:
The Lambda environment did not contain the latest version of the Boto3 SDK required for Bedrock interactions. Latest version of Boto3 SDK is required to include support for recently launched AWS services like Amazon Bedrock. To resolve this, I installed the latest version of Boto3 locally, zipped it within a folder named 'python', and then uploaded this zipped file as a Lambda Layer. This ensured that the Lambda function had access to the necessary SDK version.

Configuring Lambda Permissions:
Initially, the Lambda function was configured with only basic execution permissions, which prevented interaction with the Bedrock service. I resolved this by explicitly granting the Lambda function the IAM permission bedrock:invokeModel, enabling it to successfully invoke the foundational models.

By addressing these challenges—clarifying provisioning requirements, accurately parsing the response format, managing SDK dependencies, and setting appropriate permissions—I was able to successfully integrate foundational models with AWS Lambda and API Gateway.
