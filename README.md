# We-Byte

## Description
For sharing code related to dDliveries 3 and on, for SWE.

## Prerequisites
- Python 3.x installed on your system.
- Git installed on your system.

## Installation and Usage

### Clone the Repository
1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command:

    ```
    git clone https://github.com/CSCI3356-Spring2024/We-Byte.git
    ```
(or use SSH)

### Set Up Virtual Environment
1. Navigate to the project directory.
2. Create a virtual environment by running:

    ```
    python -m venv env
    ```
   
3. Activate the virtual environment:
   
    - On Windows:
    ```
    .\env\Scripts\activate
    ```
   
    - On macOS and Linux:
    ```
    source env/bin/activate
    ```
4. Make sure to add env to .gitignore
   
### Install Dependencies
1. Ensure you are in the project directory with the `requirements.txt` file.
2. Install the required dependencies by running:

    ```
    pip install -r requirements.txt
    ```

### Run the Development Server
1. Start the development server by running:

    ```
    python manage.py runserver
    ```

2. Open a web browser and navigate to `http://127.0.0.1:8000/admin` to access your Django application database. Login using username: cfe and password: 1234

3. Student and advisor models have been added to loginuservalidation/models.py

