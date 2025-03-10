import boto3
import botocore.config
import json
from datetime import datetime

def blog_generate_using_bedrock(blogtopic: str) -> str:
    # For Nova, the prompt should be placed inside the "messages" list, under "content".
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"Write a 200-word blog on the topic: {blogtopic}"
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 1000
        }
    }

    try:
        bedrock = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",
            config=botocore.config.Config(
                read_timeout=300,
                retries={'max_attempts': 3}
            )
        )

        response = bedrock.invoke_model(
            modelId="amazon.nova-lite-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        response_content = response['body'].read()
        response_data = json.loads(response_content)

        if (
            "output" in response_data
            and "message" in response_data["output"]
            and "content" in response_data["output"]["message"]
            and len(response_data["output"]["message"]["content"]) > 0
        ):
            # Grab the first result
            first_result = response_data["output"]["message"]["content"][0]
            # Navigate to the text
            generated_text = first_result["text"]
            print(generated_text)
            return generated_text
        else:
            print("No results found in response.")
            return ""

    except Exception as e:
        print(f"Error generating the blog: {e}")
        return ""

def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Blog text saved to s3")
    except Exception as e:
        print("Error when saving the blog to s3:", e)

def lambda_handler(event, context):
    event = json.loads(event['body'])
    blogtopic = event['blog_topic']

    generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

    if generate_blog:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'awsbedrock96'
        save_blog_details_s3(s3_key, s3_bucket, generate_blog)
    else:
        print("No blog was generated")

    return {
        'statusCode': 200,
        'body': json.dumps('Blog Generation is completed')
    }
