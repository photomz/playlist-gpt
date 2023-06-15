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

# Example usage
if __name__ == '__main__':
		image_url = 'https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzODczMzh8MHwxfHNlYXJjaHwxfHxmaXNofGVufDF8fHx8MTY4Njg2OTI4M3ww&ixlib=rb-4.0.3&q=80&w=400'
		try:
				base64_image_data = get_base64_encoded_image(image_url)
				print(base64_image_data)
		except ValueError as e:
				print(str(e))
