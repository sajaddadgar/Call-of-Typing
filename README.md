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

`/reset_password`

then to recover the user password, `POST` on this URL:

`/reset_password`

body of this request must contain these props:

1. email

After `POST` this request, a message will be sent to input email that user can recover its password

### Logout 
To log out, do `POST` on this URL:

`/accounts/logout`

### Profile

To open profile's page, `GET` on this URL:

`/accounts/profile`

In this page, the user can see its information such as:

* username
* first name
* last name
* email
* position in the text typing ranking
* position in the song typing ranking
* best score in text typing
* best score in song typing
* total score in text typing
* total score in song typing

##### Change Name
To change first name and last name, `POST` on this URL:

`/accounts/edit`

body of this request must contain these props:

1. firstName
2. lastName

##### Change Password
To change first name and last name, `POST` on this URL:

`/accounts/changepassword`

body of this request must contain these props:

1. oldpass
2. newpass
3. confirmpass

##### Change Profile Image
To profile's image, `POST` on this URL:

`/accounts/change_image`

body of this request must contain these props:

1. file

##### Add Text
To add text for text typing, `POST` on this URL:

`/type/create`

body of this request must contain these props:

1. content

### Ranking 
To see all of the rankings, do `GET` on this URL:

`/ranking`

In this page, the user can see different rankings such as:

* text typing ranking
* song typing ranking
* group text typing ranking
* group song typing ranking

### Text Typing 
To start a text typing, do `GET` on this URL:

`/type/normal`

In this page, the user can type the specified text and get a score based on this formula:
<kbd>WPM * wordcount</kbd>

**WPM: Word Per Minute**
**WordCount: Number of word in the text**

### Song Typing 
To Typing a Song , do `GET` on this URL:

`/type/song/mode`

**Mode 1: Random Song**
In this case, the system selects a song at random and the Spotify and Soundcloud links of the song are given to the user.

To start a song typing in this mode, do `POST` on this URL:

`/type/song/random`

**Mode 2: Search Song**
In this case, the user can search a song in Spotify and Soundcloud and start typing.

To start a song typing in this mode , do `POST` on this URL:

`/type/song/mode`

In the both case, the user can type the lyric of song and get a score based on:
<kbd>LCS algorithm on lyric and text which user type</kbd>

**LCS: Longest Common Subsequence**

### Group Typing 
To start a group typing, do `GET` on this URL:

`/type/group/Mygroups`

##### Create a Group
To create a group, do `POST` on this URL:

`/type/group/create`

body of this request must contain these props:

1. name

##### Join the Group
To join the group, do `POST` on this URL:

`/type/group/join`

body of this request must contain these props:

1. name

##### Enter Group 
To enter a group, do `GET` on this URL:

`/type/group/{group_id}`

`{group_id}` is the id of the group.

##### Add Member to Group (just for admin of group) 
To add member to a group, do `POST` on this URL:

`/type/group/add_member/{group_id}`

`{group_id}` is the id of the group.

body of this request must contain these props:

1. member

##### Delete Group
To delete a group, do `GET` on this URL:

`/type/group/delete/{group_id}`

`{group_id}` is the id of the group.

##### Add Text for Text Typing in Group
To add text in group, do `POST` on this URL:

`/type/group/group_add_text/{group_id}`

`{group_id}` is the id of the group.

body of this request must contain these props:

1. content

##### Text Typing in group
To start text typing in group, do `GET` on this URL:

`/type/group/group_normal_type/{group_id}`

`{group_id}` is the id of the group.

**Just like simple text typing**

##### Song Typing in group
To start song typing in group, do `GET` on this URL:

`/type/group/song/mode/{group_id}`

`{group_id}` is the id of the group.

**Just like simple text typing**
