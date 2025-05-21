#  Email Campaign Manager

This is a Django-based application that allows you to manage email campaigns and send them to a list of subscribers. It includes features for:

- Campaign creation
- Subscriber management
- Email dispatch
- Unsubscribe handling



## 🚀 How to Run the Project (Step by Step)




### 1. ✅ Activate the Virtual Environment

Activate your Python virtual environment based on your operating system.

  .venv/Scripts/activate




### 2. 🖥️ Run the Django Development Server 

Start the server to access the application locally:

   cd email_campaign_project

   python manage.py runserver

Default URL: http://127.0.0.1:8000/




### 3. 🔐 Access the Admin Panel

Go to the Django admin panel:

http://127.0.0.1:8000/admin/

Log in using your superuser credentials

Create a new Email Campaign

Provide subject, preview text, article URL, HTML and plain text content, and the publish date




### 4. ➕ Add Subscriber(s)

On the homepage, click the “Add Subscriber” button

Enter a valid email address

The subscriber will now receive emails for future campaigns




### 5. 🚫 Unsubscribe 

From the homepage, click the “Unsubscribe” button

Enter a subscriber's email address

That user will be removed from the mailing list




### 6. 📤 Send Campaigns (Final Step)

After you've added campaigns and subscribers:

Stop the Django server by pressing:

   CTRL + C

Run the custom management command to send emails:

  python manage.py send_daily_campaigns


This command will:

Send all due campaigns to active subscribers
Log all success or failure messages
Mark campaigns as "sent" after processing




### ✅ Summary of Commands

Task	                                         Command/URL
Activate venv (Windows)	                    venv\Scripts\activate
Activate venv (Linux/macOS)              	source venv/bin/activate
Start server                            	python manage.py runserver
Admin panel	                                http://127.0.0.1:8000/admin/
Stop server                              	CTRL + C
Send campaigns	                            python manage.py send_daily_campaigns





