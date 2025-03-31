#Testing the API endpoints using unittest and requests library

import datetime
import unittest, requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import subprocess
import os
import shutil
from fastapi import HTTPException
from fastapi.responses import FileResponse



MONGO_URI = "mongodb://root:example@localhost:27017/autoStock?authSource=admin"
DATABASE_NAME = "autoStock"
DATABASE_COLLECTION = "itemList"

class getAllProductsTestCase(unittest.TestCase):
    def test_enpointAllProduct(self):
        url = 'http://localhost:5000/getAllProducts'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class getProductByIDTestCase(unittest.TestCase):
    def test_enpointGetSingleProduct(self):
        url = 'http://localhost:5000/getSingleProduct?prodID=AUTO001'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class addNewProductTestCase(unittest.TestCase):
    def test_enpointAddNewProduct(self):
        url = 'http://localhost:5000/addNewProduct?prodID=AUTO050&name=TestProduct&price=99.99&quantity=40&description=TESTUNITTESTING'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class deleteProductTestCase(unittest.TestCase):
    def test_enpointDeleteProduct(self):
        url = 'http://localhost:5000/deleteProduct?prodID=AUTO002'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class startsWithTestCase(unittest.TestCase):
    def test_enpointStartsWith(self):
        url = 'http://localhost:5000/startsWith?letter=T'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class paginateTestCase(unittest.TestCase):
    def test_enpointPaginate(self):
        url = 'http://localhost:5000/paginate?prodStartID=AUTO001&prodEndID=AUTO010'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class convertTestCase(unittest.TestCase):
    def test_enpointConvert(self):
        url = 'http://localhost:5000/convert?prodID=AUTO007'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

#generate a pdf file of test results
class PDFTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f"Test {test} passed\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"Test {test} failed\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"Test {test} encountered an error\n")

# Custom Test Runner to Generate PDF
def tests_and_generate_pdf():
    # Create a string stream to capture the test results
    stream = io.StringIO()
    # Create a custom test runner that uses the PDFTestResult class
    runner = unittest.TextTestRunner(stream=stream, verbosity=2,)
    # Load all test cases from the current module
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = runner.run(suite)
    
    test_output = stream.getvalue()
    
    # Generate PDF report
    pdf_filename = "WS-UnitTest_Result.pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 750, "Panitan Sripoom B00148508 - Web Services Assignment")
    pdf.drawString(150, 730, "Unit Test for APIs Endpoints")
    
    # Draw the test results
    #starting position for writing the results
    y_position = 700
    for line in test_output.split("\n"):
        if y_position < 50:  # Start new page if needed
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = 750
        pdf.drawString(50, y_position, line) # start to write the results from each test case
        y_position -= 20

    pdf.save()
    print(f"Test results saved in {pdf_filename}")


def dump_database():
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    backup_dir = f"database_dump{timestamp}"
    zip_file = f"mongo_backup.zip{timestamp}"

    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    try:
        # Run mongodump
        result = subprocess.run(
            ["mongodump", "--uri", MONGO_URI, "--collection","itemList","--out", backup_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Mongodump Output:", result.stdout)
        print("Mongodump Error (if any):", result.stderr)

        # Zip the backup directory
        shutil.make_archive("itemList_backup", "zip", backup_dir)

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {e.stderr}")

    return FileResponse(zip_file, filename="database-${date}.zip", media_type="application/zip")

if __name__ == '__main__':
    tests_and_generate_pdf()
    dump_database()