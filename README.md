# challenge_backend
**challenge_backend** is a Python application which implements the assignment as defined in ["Challenge_Backend_South_African_Numbers_.pdf"](docs/Challenge_Backend_South_African_Numbers_.pdf)


## Minimum requirements 
python 3.8.1

fastapi==0.61.0  
numpy==1.19.1  
pandas==1.1.0  
pydantic==1.6.1  
python-dateutil==2.8.1  
pytz==2020.1  
six==1.15.0  
starlette==0.13.6

## Usage
Open terminal and install the necessary packages by running:

```
pip install
```

Then start the application by running:
```
uvicorn main:app
```

For running the tests, do:
```
pytest
```

Go to http://127.0.0.1:8000/docs to consult the interactive documentation.

## Features
The application allow the an user to check if a number is a valid South African mobile phone number, based on the 
following assumptions:
- a valid number must contains 11 digits; and
- a valid number must begin with 27.

If a number contains 10 or 9 digits, the application will try to suggest a correction by adding the prefix 27, e.g. 
**7**234567890 --> **27**345678901. 

By sending a GET request to the endpoint '*/*', a html form shall be provided to the user. By sending the form with a 
number, the application will confirm if the number is corrected, or not. If not correct, the user shall be notified on 
the reasons for which the number is not correct, and the possible correction.

The user may upload a csv file with a POST request to the endpoint '*/upload-file*' (parameter: file). The response shall 
be a json file, dividing the numbers in three categories: '**accepted**', '**corrected**', '**rejected**'.

Example of **accepted** number:
```
{
    "id_": 103426000,
    "number": "27718159078",
    "status": "accepted",
    "suggested_correction": null,
    "annotation": null
},
```

Example of **corrected** number:
```
{
    "id_": 103300640,
    "number": "730276061",
    "status": "corrected",
    "suggested_correction": "27730276061",
    "annotation": "Correction: missing 27 prefix"
},
```

Example of **rejected** number:
```
{
    "id_": 103343262,
    "number": "6478342944",
    "status": "rejected",
    "suggested_correction": null,
    "annotation": "Rejection: the number does not contain 11 digits; the number prefix is not 27."
},
```

### Implementation notes ###
For the implementation, the following assumption has been made:
- the client uploaded file is indeed a csv file, without missing data; and
- the application will reject a csv file without columns name 'id' and 'sms_phone' number.

The parsing of the csv file is done with **pandas** library. For the purpose of this application the standard csv module
might has been sufficient; however it is somehow awkward to work with uploaded files by using this module.

As required by the assignment, a temporary file is created by [main.py](main.py) during the execution of the 
application.