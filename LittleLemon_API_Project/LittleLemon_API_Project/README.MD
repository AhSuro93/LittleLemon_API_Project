Commented Out [rest_framework.authentication.SessionAuthentication'] In Settings.py


[Rubric_Question]
`Four Questions Have Missing URL Info`
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
<Number13 Test if customers can browse all categories:

<Make a GET API call to this endpoint 
<http://127.0.0.1/api/categories       ← Wrong URL(Missing :8000)      *Heres the correct one...  http://127.0.0.1:8000/api/categories      
 <with a customer token

<Are the categories visible to customers?     
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

<Number 14 Test if customers can browse all menu items:

<Make a GET API call to this endpoint 
<http://127.0.0.1/api/menu-items       ← Wrong URL(Missing :8000)      *Heres the correct one..  http://127.0.0.1:8000/api/menu-items
 <with a customer token

<Are the menu items visible to customers?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

<Number20 Test if customers can place orders:

<Make a POST call to this endpoint 
<http://127.0.0.1:8000/api/cart/orders       ← Wrong URL(Missing :8000)      *Heres the correct one.. http://127.0.0.1:8000/api/orders
 <with a customer token. Add only the date field with valid data in the REQUEST body. Here is a sample date – 2022-11-16.

<Can customers successfully place an order?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

<Number21 Customers can view their own orders:

<Make a GET call to this endpoint 
<http://127.0.0.1:8000/api/cart/orders       ← Wrong URL(Missing :8000)      *Heres the correct one.. http://127.0.0.1:8000/api/orders
 <with a customer token. 

<Can customers browse their own orders? 



# Users

#### SuperUser
- **Username:** admin
    
- **Password:** password

[Token] : 996aefe4e1c57f5c8a3389f7b6dc8687e3ab9abf

_______
#### Manager
- **Username:** Adrian 
    
- **Email:** adrian@littlelemon.com
    
- **Password:** lemon@adr!

[Token] : 
545206b6f1342b56b38b29b3e30b04d525a78c0c
_______
#### DeliveryCrew
http://127.0.0.1:8000/auth/users/ To create the rest

- **Username:** Mario
    
- **Email:** mario@littlelemon.com
    
- **Password:** lemon@mar!

[Token] :
10cc3f13ef488386d1e4bbf3376ace14d01118f3

_______
#### Customer NO TOKEN
Don't Add Token This One Is A Customer
- **Username:** Sana
    
- **Email:** sana@littlelemon.com
    
- **Password:** lemon@san!

[Token] : 

_______
#### Customer 2 TOKEN 
Add Token To This Customer
Token Created At http://127.0.0.1:8000/auth/token/login
- **Username:** Emily
    
- **Email:** emily@littlelemon.com
    
- **Password:** lemon@em!

[Token] : fc45c0c9d8f939b8c3eb31fcd3e42cebffa136a0


_______

#### User For Deleting Manager Role 
Add Token To This Customer
Token Created At http://127.0.0.1:8000/auth/token/login
- **Username:** DeleteTwo
    
- **Email:** delete2@littlelemon.com
    
- **Password:** lemon@de2!

[Token] : 


_______

#### User For Deleting Delivery-Crew?
Add Token To This Customer
Token Created At http://127.0.0.1:8000/auth/token/login
- **Username:** Delete
    
- **Email:** delete1@littlelemon.com
    
- **Password:** lemon@de1!

[Token] : 