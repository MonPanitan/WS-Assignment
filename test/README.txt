API Endpoints:

Endpoint: /
  Method: GET

Endpoint: /getSingleProduct
  Method: GET
  Parameters:
    - prodID (query): No description

Endpoint: /getAllProducts
  Method: GET

Endpoint: /addNewProduct
  Method: GET
  Parameters:
    - prodID (query): No description
    - name (query): No description
    - price (query): No description
    - quantity (query): No description
    - description (query): No description

Endpoint: /deleteProduct
  Method: GET
  Parameters:
    - prodID (query): No description

Endpoint: /startsWith
  Method: GET
  Parameters:
    - letter (query): No description

Endpoint: /paginate
  Method: GET
  Parameters:
    - prodStartID (query): No description
    - prodEndID (query): No description

Endpoint: /convert
  Method: GET
  Parameters:
    - prodID (query): No description


For full API documentation, visit: http://localhost:5000/docs
