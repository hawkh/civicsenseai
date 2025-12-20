import requests

def test_multi_upload():
    url = "http://localhost:8000/api/v1/reports"
    # Send both files
    files = [
        ('image', ('test_image.jpg', open('test_image.jpg', 'rb'), 'image/jpeg')),
        ('audio', ('test_audio.webm', open('test_audio.webm', 'rb'), 'audio/webm'))
    ]
    data = {
        'source': 'test_script_multi',
        'description': 'Test multi upload'
    }

    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

        if response.status_code == 200:
            print("SUCCESS: Multi upload endpoint worked.")
        else:
            print("FAILURE: Endpoint returned error.")

    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_multi_upload()
