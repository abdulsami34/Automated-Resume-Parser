# Resume Parser
Resume Parser is a web application that allows users to upload a resume in PDF format and extracts useful information such as name, contact number, email, skills, education, and experience from it. This information is then displayed on the web page for easy viewing.

## Features

- Upload a resume in PDF format
- Extracts key information from the resume
- Displays extracted information in a user-friendly format
- Light Mode / Dark Mode

## Requirements

- Python 3.x
- Flask
- PyPDF2 (or any other PDF parsing library)
- HTML, CSS (Bootstrap), and JavaScript (jQuery)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/abdulsami34/Automated-Resume-Parser
    cd Automated-Resume-Parser
    ```

2. Set up a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```sh
    flask run or python app.py
    ```

5. Open your browser and go to `http://127.0.0.1:5000` to view the application.

## Usage

1. On the main page, click on the "Upload Resume (PDF)" button and select a PDF file to upload.
2. Click the "Parse Resume" button.
3. The extracted information will be displayed below the form.

## Project Structure

- `appf.py`: The main Flask application file that handles the backend logic.
- `templates/index.html`: The HTML template for the web application's front end.
- `static/js/app.js`: The JavaScript file that handles the form submission and displays the extracted information.
