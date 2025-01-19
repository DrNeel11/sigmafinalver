# sigmafinalver

## Project Description
This project is a FastAPI application running in a Docker container.

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Steps

1. **Clone the repository:**
    ```sh
    git clone https://github.com/DrNeel11/sigmafinalver.git
    cd sigmafinalver
    ```

2. **Build the Docker image:**
    ```sh
    docker-compose build
    ```

3. **Start the Docker container:**
    ```sh
    docker-compose up
    ```

## Running the Application

1. **Access the application:**
    Open your web browser and go to `https://localhost:8001`.
2. **Trust the Self-Signed Certificate**:
    To avoid the `ERR_CERT_AUTHORITY_INVALID` error, you need to trust the self-signed certificate on your local machine.

    ### On Windows:
    1. Open the `localhost.crt` file.
    2. Click on "Install Certificate".
    3. Choose "Local Machine" and click "Next".
    4. Select "Place all certificates in the following store" and browse to "Trusted Root Certification Authorities".
    5. Click "Next" and then "Finish".

    ### On macOS:
    1. Open the `localhost.crt` file.
    2. Add it to the keychain.
    3. Open Keychain Access, find the certificate, and set it to "Always Trust".

    ### On Linux:
    1. Copy the `localhost.crt` file to `/usr/local/share/ca-certificates/`.
    2. Run `sudo update-ca-certificates`.
   

## Additional Information

- **Stopping the Docker container:**
    ```sh
    docker-compose down
    ```

- **Rebuilding the Docker image:**
    ```sh
    docker-compose build
    ```

## License
This project is licensed under the MIT License.
