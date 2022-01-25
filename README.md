# **TPW: Practical Work 2**



## Group #2

| Element       | NMEC   |
| ------------- | ------ |
| Tomé Carvalho | 97939  |
| Dinis Lei     | 98452  |
| Afonso Campos | 100055 |



## Django REST API

### Windows Instructions (PowerShell)

**Virtual Environment Creation and Activation**

In the repository's root directory, create the venv:

`python -m venv venv`

Obtain permission to run the venv activation script:

`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted`

Activate the venv:

`.\venv\Scripts\activate`

Install the requirements

`pip install -r requirements.txt`

**Application Execution**

Run the application

`python .\manage.py runserver`



### API Endpoints

Note: All of the following endpoints are prefixed by `ws/`.

| Endpoint                    |                                                              |
| --------------------------- | ------------------------------------------------------------ |
| `token-auth`                | **POST**: Returns an authentication token if provided with correct credentials (username and password). |
| `signup`                    | **POST**: Creates a new user, receiving username and password. |
| `dashboard`                 | **GET**: Gets the products, excluding the user's own, if logged in; allows filtering and sorting: group, category, upper price, lower price, order. |
| `my-products`               | **GET**: Gets the user's products; allows filtering: group, category, upper price, lower price. **POST**: Adds a new product. *Requires login.* |
| `products/<int:i>`          | **GET**: Gets the information of the product with ID `i`.    |
| `groups`                    | **GET**: Gets the list of product groups.                    |
| `cart`                      | **DELETE**: Deletes a product's instances from the user's cart. **GET**: Gets the product instances that the user's cart is composed of. **POST**: Adds instances of a product to the cart. *Requires login.* |
| `cart/checkout`             | **POST**: Purchases the items in the user's cart. *Requires login.* |
| `history/purchases`         | **GET**: Gets the product instances related to the user's previous purchases. *Requires login.* |
| `history/sales`             | **GET**: Gets the product instances related to the user's previous sales. *Requires login.* |
| `add-product-stock`         | **POST**: Increases the stock of a user's product. *Requires login.* |
| `add-product-img`           | **POST**: Adds an image to a user's product. *Requires login.* |
| `add-product-group`         | **POST**: Adds a group to a user's product. *Requires login.* |
| `toggle-product-visibility` | **POST**: Toggles the visibility of a product. *Requires login as an administrator.* |
| `superuser`                 | **GET**: Returns whether logged user is superuser. *Requires login* |
