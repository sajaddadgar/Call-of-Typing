# Call of Typing
![logo](https://gitlab.com/AUT_SE_98/se-project/-/raw/master/call_of_typing/static/img/b.png)
## User API

### Create Account
To create a new user, do `POST` on this URL:

`/accounts/register`

body of this request must contain these props:

1. first_name
2. last_name
3. email
4. username
5. password1
6. password2

The passwords must be hashed cause of security issues.


### Login 
To log in, do `POST` on this URL:

`/user/login`

body of this request must contain these props:

1. username
2. password

### Recover Password

To open recover's page, `POST` on this URL:

`/reset_password/`

then to recover the user password, `POST` on this URL:

`/reset_password/`

body of this request must contain these props:
1. email
