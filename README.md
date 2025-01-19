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
1. **Trust the Self-Signed Certificate**
To avoid the ERR_CERT_AUTHORITY_INVALID error, you need to trust the self-signed certificate on your local machine.

On Windows:
Open the localhost.crt file.
Click on "Install Certificate".
Choose "Local Machine" and click "Next".
Select "Place all certificates in the following store" and browse to "Trusted Root Certification Authorities".
Click "Next" and then "Finish".
On macOS:
Open the localhost.crt file.
Add it to the keychain.
Open Keychain Access, find the certificate, and set it to "Always Trust".
On Linux:
Copy the localhost.crt file to /usr/local/share/ca-certificates/.
Run sudo update-ca-certificates.

2. **Access the application:**
    Open your web browser and go to `https://localhost:8001`.
   

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
