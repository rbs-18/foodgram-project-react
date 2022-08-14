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

-

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

Authintificated users

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
