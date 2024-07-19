# We-Byte

## Description
Below is a walkthrough of the application, since it is not accessible to non-bc users or anyone without access to the Boston College Course Info API. The main focus of the design choices was to make the application fit seamlessly into existing Boston College application platforms. 

First, users will be prompted to login using Google SSO with their Boston College Credentials.

<img width="1440" alt="EagleApps Login" src="https://github.com/user-attachments/assets/65fdba58-0e1d-4688-b7e4-f8ab90e93b9c">

Next, if they are a new user, they will be prompted to fill out the following information. They will not be able to continue without finishing the required fields.

<img width="1440" alt="EagleApps Year Select" src="https://github.com/user-attachments/assets/ec4b20f9-c817-4f57-bbaf-689d7cd3eb63">

<img width="1440" alt="EagleApps Major Select" src="https://github.com/user-attachments/assets/0e97bf51-1dc1-42ef-8492-d69f3bf59104">

If they are a returning user, they will instead be brought to the landing page. If they already have courses in their plan, they will see their credit progress. The progress bar is based on courses actually taken.

<img width="1440" alt="EagleApps Progress" src="https://github.com/user-attachments/assets/fa0c9bc8-5e20-4f9b-a3f9-39eea7fbba46">

If they click on "Build Plan" on the menu above, they will be brought to the view of their plan. Students can have up to 3 plans to alternate between, and will receive suggestions for courses not yet taken based on their major. Additionally, they can add credits from AP classes, to account for requirements that can be fulfilled prior to starting college. The menu has been cut off from the screenshot to show the entire plan view.

<img width="1440" alt="EagleApps Plan View Student" src="https://github.com/user-attachments/assets/b03a60ff-9288-44b3-9fe3-1f7e482ca3d4">

Next, if the user navigates to "Search Courses", they will be able to find courses by department. In future work on this progress, it would be helpful to implement a fully-functional free-text search, though that was out of the scope of this project.

<img width="1440" alt="EagleApps Course Search" src="https://github.com/user-attachments/assets/57681286-dc6d-4e5f-a685-707060bf6f05">

Students can add a desired course to thier plan by specifying what year and semester they'd like to include it in.

<img width="1440" alt="EagleApps Add Course" src="https://github.com/user-attachments/assets/742c18a8-3649-4835-8170-4f4adfc3f46e">

If a user is an advisor, they will have student's associated to their account in the database. They will be able to see these students' plans and toggle through them on their "Plan View" page (the selected student's plan is empty). Information about what courses the student needs was not included in the MVP from the advisor's page as they should have that info already, but this should be included in future iterations.

<img width="942" alt="EagleApps Plan View" src="https://github.com/user-attachments/assets/7daae440-f5f2-4eaa-907a-386173fe793f">

If a user is an administartor and would like a department-view, they will be able to see how many students have a class in their plan by semester and year, so that the University can estimate how many seats they will need for that course.

<img width="1440" alt="EagleApps Dept View" src="https://github.com/user-attachments/assets/3f9eb041-4270-4cb1-bbbe-24ab7302507f">


## Prerequisites
- Python 3.x installed on your system.
- Git installed on your system.

## Installation and Usage
*** Since the Boston College Course Info API is not deployed, much of the code which utilized API calls will not work (anything related to course searching or course information). Feel free to connect your own API, or use a JSON file!
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

3. Student and advisor models have been added to loginuservalidation/models.py. You will need to add your email to the advisor or administrator section to access those views, otherwise your account will default to student upon first login.

