# filename: send_image_to_gpt4v.py
import base64
import requests
import os

# Function to encode the image to base64
def encode_image_to_data_uri(image_path):
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"

# Function to construct the payload
def construct_payload(api_key, image_data_uri):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": image_data_uri
                }
            ],
        },
    ]

    params = {
        "model": "gpt-4-vision-preview",
        "messages": prompt_messages,
        "max_tokens": 500,
    }
    
    return params, headers

# Function to send the message
def send_message(payload, headers):
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Main function to run the script
def main():
    # Read the OpenAI API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set.")
    
    # Image path
    image_path = "test_image.png"
    
    # Encode image to data URI
    image_data_uri = encode_image_to_data_uri(image_path)
    
    # Construct the payload
    payload, headers = construct_payload(api_key, image_data_uri)
    
    # Send the message and get the response
    response = send_message(payload, headers)
    
    # Output the "choices" part of the response to the console
    if response and "choices" in response:
        for choice in response["choices"]:
            print(choice)
    else:
        print("No choices in the response or an error occurred.")

if __name__ == "__main__":
    main()
