This project was created for my Python Belt Exam at Coding Dojo.
Author: Joshua Wren
Creation August 24, 2020

If you run these files locally, you will need to install Django (pip install Django).
This project showcases a login/registration page accessible by client and makes changes to the server database through POST requests.
You can register a new user or login with a current one. These forms will be checked through validators through a class manager.
The password registered will be hashed with a salt using the `bcrypt()` function.
Once access is granted, you will be able to add a quote with an associated author (also checked through a validator).
Users can see all quotes posted by another user, add their own quotes, like or dislike a quote, or delete their own quotes. 
Users can also update their own account info (just name and email at this time).
Styling was primarily completed using Bootstrap. I did not have time during the exam to focus on making a static CSS page... maybe that will be added later.
Users can like comments which increases the count of likes on a comment which is visible to all users. By clicking it again, it will take away the like from before.

I will continue to perfect my Django/Python skills. Next goal is to learn how to get some functionality improvements from AJAX.
