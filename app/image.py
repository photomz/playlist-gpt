import requests
import base64

def get_base64_encoded_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content

        # Ensure the image data size is within the maximum payload limit
        if len(image_data) > 256 * 1024:
            raise ValueError("Image size exceeds the maximum payload limit.")

        # Encode the image data in Base64
        base64_encoded_image = base64.b64encode(image_data).decode('utf-8')
        return base64_encoded_image

    raise ValueError("Failed to retrieve the image.")

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def replace_url_parameter(url, parameter, new_value):
    """
    Replace a parameter value in a URL query string with a new value.

    Args:
        url (str): The URL string.
        parameter (str): The parameter to replace.
        new_value (str): The new value for the parameter.

    Returns:
        str: The modified URL with the updated parameter value.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params[parameter] = [new_value]
    updated_query = urlencode(query_params, doseq=True)
    updated_url = urlunparse(parsed_url._replace(query=updated_query))
    return updated_url

# Example usage
if __name__ == '__main__':
    fullres_url = 'https://images.unsplash.com/photo-1461988320302-91bde64fc8e4?ixid=2yJhcHBfaWQiOjEyMDd9&&fm=jpg&w=400&fit=max'
    image_url = replace_url_parameter(fullres_url, 'w', '720')
    try:
        base64_image_data = get_base64_encoded_image(image_url)
        print(base64_image_data)
    except ValueError as e:
        print(str(e))
