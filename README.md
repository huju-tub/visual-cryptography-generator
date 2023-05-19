# Visual Cryptography Generator
A Visual Cryptography Generator that takes text as input and encrypts it using a (2,2) visual cryptography scheme.


## Installation

1. Clone the repository:

``git clone https://github.com/your-username/project-name.git``


2. Navigate to the project directory:

`cd project-name`


3. Create a virtual environment (optional but recommended):

`python -m venv venv`


4. Activate the virtual environment:  

On Unix-based systems:

`source venv/bin/activate`


On Windows:

`venv\Scripts\activate`

5. Install the required packages using `pip` and the `requirements.txt` file:

`pip install -r requirements.txt`


This will install all the necessary dependencies for the project.

## Usage

To run the main file of the project, execute the following command:

`python main.py <text> <private_key>`

Replace <text> with the text you want to encrypt and <private_key> with the name of the private key file (e.g., secret_1.png). The private key file should be saved in the private_keys/ directory and must be in PNG format.

For example, to encrypt the word "hello" using the private key file secret_1.png, you would run:

`python main.py hello secret_1.png`
