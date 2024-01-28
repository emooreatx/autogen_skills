# Ensure the code is robust and has no hardcoded values outside of the test declaration
import base64
import requests
import os

def encode_image_to_data_uri(image_path):
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"

def construct_payload(api_key, image_data_uri, prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt_messages = [
        {
            "role": "user",
            "content": prompt
        },
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
        "max_tokens": 4096,
    }
    return params, headers

def send_message(payload, headers):
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as http_err:
        return None, f"HTTP error occurred: {http_err}"
    except Exception as err:
        return None, f"An error occurred: {err}"

def multimodal_vision_describe(image_path, prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set.")
    image_data_uri = encode_image_to_data_uri(image_path)
    payload, headers = construct_payload(api_key, image_data_uri, prompt)
    response, error = send_message(payload, headers)
    if error:
        return None, error
    if response and "choices" in response:
        return response["choices"], None
    else:
        return None, "No choices in the response or an error occurred."

# Entry point for testing
if __name__ == '__main__':
    test_image_path = '/home/emoore/github_autogen_fullpage.png'
    test_prompt = 'Please provide a detailed description of the following image, and please try hard.'
    test_description, test_error = multimodal_vision_describe(test_image_path, test_prompt)
    if test_error:
        print(test_error)
    else:
        for choice in test_description:
            print(choice)
