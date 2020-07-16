import requests

def download_file_from_google_drive(id, destination):
    """
    Download a files from Google drive. The file has to shared and made viewable by everybody. The id of the
    file is the long list of random characters in the public link.

    Example: download_file_from_google_drive('1c8FPxYIdRNY8WmB8G4k7p_DSNrWwwfwfD','myfile.txt'
    
    """
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    
