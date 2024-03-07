from openai import OpenAI
import httpx

client = OpenAI(
    base_url="https://api.xty.app/v1", 
    api_key="sk-vQIOfXZ8olru1QPIDe068f3fE637418a9aDf4a495147E9Af",
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                    "type": "image_url",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                },
            ],
        }
    ]
)

print(response)