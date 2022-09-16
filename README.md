![workflow](https://github.com/rbs-18/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# foodgram project

Grocery assistant

## DESCRIPTION

On this service, users can publish recipes, subscribe to publications of other users,
add their favorite recipes to the "Favorites" list, and before going to the store,
download a summary list of products needed to prepare one or more selected dishes

## ENDPOINTS
### USERS
- #### GETTING LIST OF USERS

 `api/users/` `GET`

-- *Permissions*

All

-- *Parameters*

- page - number of page
- limit - nums of notes

-- *Responses*

200

- #### REGISTRATION OF NEW USER

 `api/users/` `POST`

```json
{
  "email": "vpupkin@yandex.ru", (required)
  "username": "vasya.pupkin", (required)
  "first_name": "Вася", (required)
  "last_name": "Пупкин", (required)
  "password": "Qwerty123" (required)
}
```
-- *Permissions*

All

-- *Responses*

201, 400

 #### GETING USER

 `api/users/{id}` `GET`

-- *Permissions*

All

-- *Responses*

200, 401, 404

- #### SHOWING CERTAIN USER

 `api/users/me/` `GET`

-- *Permissions*

Authintificated users

-- *Responses*

200, 401

- #### CHANGING PASSWORD

 `api/users/set_password/` `POST`

```json
{
  "new_password": "string", (required)
  "current_password": "string" (required)
}
```

-- *Permissions*

Authintificated users

-- *Responses*

204, 400, 401

- #### GETTING TOKEN

 `api/auth/token/login/` `POST`

```json
{
  "password": "string", (required)
  "email": "string" (required)
}
```

-- *Permissions*

Registred users

-- *Responses*

201

- #### DELETING TOKEN

 `api/auth/token/logout/` `POST`

-- *Permissions*

Authintificated users

-- *Responses*

204, 401

--------------------------------------------------------------------------------------


### SUBSCRIPTION
- #### GET ALL USERS IN SUBSCRIPTIONS

 `api/users/subscriptions/` `GET`

 ```json
{
    "id": 0,           (required)
    "name": "string",  (required)
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",             (required)
    "cooking_time": 1  (required)
}
```

-- *Parameters*

- page - number of page
- limit - nums of notes
- recipes_limit - amount of recipes in field recipes

-- *Permissions*

Authintificated users

-- *Responses*

200, 401

- #### SUBSCRIBE ON USER

 `api/users/{id}/subscribe/` `POST`

-- *Parameters*

- recipes_limit - amount of recipes in field recipes

-- *Permissions*

Authintificated users

-- *Responses*

201, 400, 401, 404

- #### DELETE RECIPE FROM SUBSCRIPTIONS

 `api/users/{id}/subscribe/` `DELETE`

-- *Permissions*

Authintificated users

-- *Responses*

204, 400, 401, 404

--------------------------------------------------------------------------------------

### TAGS
- #### GETTING LIST OF TAGS

 `api/tags/` `GET`

-- *Permissions*

All

-- *Responses*

200


 #### GETING TAG

 `api/tags/{id}` `GET`

-- *Permissions*

All

-- *Responses*

200, 404

--------------------------------------------------------------------------------------

### RECIPES
- #### GETTING LIST OF RECIPES

 `api/recipes/` `GET`

-- *Permissions*

All

-- *Parameters*

- page - number of page
- limit - nums of notes
- is_favorited (0 or 1) - show only recipe in favorite
- is_in_shopping_cart (0 or 1) - show only recipe in shopping list
- author - show only recipe with id author
- tags - show only recipe with tags (slug)

-- *Responses*

200

- #### CREATING OF NEW RECIPE

 `api/recipes/` `POST`

```json
{
    "ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
      ],               (required)
    "tags": [
        1,
        2
    ],                 (required)
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",    (required)
    "name": "string",  (required)
    "text": "string",  (required)
    "cooking_time": 1  (required)
}
```
-- *Permissions*

Authintificated users

-- *Responses*

201, 400, 401, 404

 #### GETING RECIPE

 `api/recipes/{id}` `GET`

-- *Permissions*

All

-- *Responses*

200

- #### UPDATING OF RECIPE

 `api/recipes/{id}/` `PATCH`

```json
{
    "ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
      ],               (required)
    "tags": [
        1,
        2
    ],                 (required)
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",    (required)
    "name": "string",  (required)
    "text": "string",  (required)
    "cooking_time": 1  (required)
}
```
-- *Permissions*

Author of recipe

-- *Responses*

200, 400, 401, 403, 404

- #### DELETING OF RECIPE

 `api/recipes/{id}/` `DELETE`

-- *Permissions*

Author of recipe

-- *Responses*

204, 401, 401, 403, 404

--------------------------------------------------------------------------------------

### SHOPPING CART
- #### DOWNLOAD LIST INGREDIENTS OF RECIPE IN SHOPPING CART

 `api/recipes/download_shopping_cart/` `GET`

-- *Permissions*

Authintificated users

-- *Responses*

200, 401

- #### CREATING OF NEW ITEM OF SHOPPING CART

 `api/recipes/{id}/shopping_cart/` `POST`

```json
{
    "id": 0,           (required)
    "name": "string",  (required)
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",             (required)
    "cooking_time": 1  (required)
}
```
-- *Permissions*

Authintificated users

-- *Responses*

201, 400, 401

 - #### DELETE ITEM OF SHOPPING CART

 `api/recipes/{id}/shopping_cart/` `DELETE`

-- *Permissions*

Authintificated users

-- *Responses*

204, 400, 401

--------------------------------------------------------------------------------------

### FAVORITE
- #### ADD RECIPE TO FAVORITE

 `api/recipes/{id}/favorite/` `POST`

 ```json
{
    "id": 0,           (required)
    "name": "string",  (required)
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",             (required)
    "cooking_time": 1  (required)
}
```

-- *Permissions*

Authintificated users

-- *Responses*

201, 400, 401

- #### DELETE RECIPE FROM FAVORITE

 `api/recipes/{id}/favorite/` `DELETE`

-- *Permissions*

Authintificated users

-- *Responses*

204, 400, 401

--------------------------------------------------------------------------------------

### INGREDIENTS
- #### GETTING LIST OF INGREDIENTS

 `api/ingredients/` `GET`

 -- *Parameters*

- name - searching by field name

-- *Permissions*

All

-- *Responses*

200


 #### GETING INGREDIENT

 `api/ingredients/{id}` `GET`

-- *Permissions*

All

-- *Responses*

200

## DOCUMENTATION AVAILIBLE AFTER LAUNCH:
- None


## TECHNOLOGY

- Python 3.8
- Django
- Django Rest Framework 3.12
- Docker


## DATABASE

- None


## HOW TO START PROJECT
None

# AUTHORS
*_Kozhevnikov Aleksei_*
