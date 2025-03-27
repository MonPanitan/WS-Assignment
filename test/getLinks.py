import unittest, requests

#
class getAllProductsTestCase(unittest.TestCase):
    def test_enpointAllProduct(self):
        url = 'http://localhost:5000/getAllProducts'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class getProductByIDTestCase(unittest.TestCase):
    def test_enpointGetSingleProduct(self):
        url = 'http://localhost:5000/getSingleProduct/AUTO001'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class addNewProductTestCase(unittest.TestCase):
    def test_enpointAddNewProduct(self):
        url = 'http://localhost:5000/addNewProduct/AUTO)11,Test Product,10.99,100,This is a test product'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class deleteProductTestCase(unittest.TestCase):
    def test_enpointDeleteProduct(self):
        url = 'http://localhost:5000/deleteProduct/AUTO002'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class startsWithTestCase(unittest.TestCase):
    def test_enpointStartsWith(self):
        url = 'http://localhost:5000/startsWith/T'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class paginateTestCase(unittest.TestCase):
    def test_enpointPaginate(self):
        url = 'http://localhost:5000/paginate/1,10'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)

class convertTestCase(unittest.TestCase):
    def test_enpointConvert(self):
        url = 'http://localhost:5000/convert/AUTO007'

        #Making a GET request to the API endpoint
        response = requests.get(url)

        #Asserting the response status code
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()