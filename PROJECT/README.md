# YOUR PROJECT TITLE
A Web-site For MSMEs
#### Video Demo:  <[URL HERE](https://youtu.be/RbO1uHldGdA?si=zc7p3uiBwixdBWHr)>
#### Description:
For my final project I decided to make a web-application for MSMEs[Micro Small and Medium-sized Enterprises]. What i have created is a generalised version which can be customized as per the needs of various businesses. My application aims at digitizing a lot of work that business owners handle manually, in addition to providing an easy to use portal for customers to order products and track them.
# Languages and Frameworks Used:
Flask, html, css, javascript, sqlite, chatgpt3.5(For help in Front-end)
# Files Used
Let,s go through each file of the project and discusss the functionalities.  
# app.py
Let,s go through the important functions:
1) order()
It allows users to order products and fill in other important details that the owner would need in order to deliver the product. The products selected along with their quantity, time of order etc. are sfurther stored in the database.

2) owner_dashboard()
Allows owner to view opending orders, pending deliveries, pending payments and make changes to their order status. It also allows the owner to send back a bill to the customer whuch can be further accepted or rejected by the customer.

3) login()
In addition to logging in customers to their accounts, it also enables owners to be logged in to their dashboard with the use of specific usernames.

4) customer_dashboard()
This feature, makes it possible for customers to view the orders they have placed, track their orders that are to be delivered and to acceot or reject the price set by the owners for their orders.

5)TBD()
Mover orders from pending section to "TO BE DELIVERED" section once the owner sees that the payment is done.

# index.html
It is the home page of the website that is availble for the users to view. Contains a lot of information about the business. 

# customer_dashboard.html
Contains three different sections, namely- pending orders, pending deliveries, accepted orders. Allows the user to track the status of their orders and either accept or reject the bill sent by the owner.

# dashboard.html
Contains three different sections, namely- pending orders, pending deliveries, pending payments. Allows the owner to track the status of their orders and either accept or reject orders and send back the bills to customers.

# order.html
Allows users to order products by slecting items, their units and inputting other important informations. Additionally equipped with a search bar made using javascript to help customers navigate through products.

# helpers.py 
I've used two functions from this file that I had previously used in my finance webpage in my cs50 assignment namely- apology and @login required.

# Features that I've thought of implementing in future
Right now, there's no payment interface. The reason for this is that MSMEs normally  deal with their payments in various ways. So, depending on that, this feature can be added as per the needs of the business owner.