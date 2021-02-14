from django.db import models
# regex import:
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        users_with_email = User.objects.filter(email=postData['email'])
        # validation if checks
        if len(postData['email']) == 0:
            errors['emailreq'] = "REQUIRED FIELD: Email"

            print("*-* *-* *-* *-* *-*")
            print("in the login_validator in models.py")
            print("errors")
            print("*-* *-* *-* *-* *-*")

        # Check if email is in database
        elif len(users_with_email) == 0:
            errors['email_doesnt_exist'] = "INVALID: Email not found"

            print("*-* *-* *-* *-* *-*")
            print("in the login_validator in models.py")
            print("errors")
            print("*-* *-* *-* *-* *-*")

        # Check if password matches email
        else:
            # compare database to email
            # users_with_email[0] is the object but not in a list
            user_to_check = users_with_email[0]
            if bcrypt.checkpw(postData['pw'].encode(), user_to_check.pw.encode()):
                print("Password matches - Success!")
            else:
                errors['password_doesnt_match'] = "INVALID: Password doesn't match"

        return errors

    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # validation if checks
        if len(postData['fname']) == 0:
            errors['fnamereq'] = "REQUIRED FIELD: First Name"
        if len(postData['lname']) == 0:
            errors['lnamereq'] = "REQUIRED FIELD: Last Name"
        if len(postData['email']) == 0:
            errors['emailreq'] = "REQUIRED FIELD: Email"
        # test whether a field matches the pattern
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "INVALID: Email"
        else:
            duplicate_email = User.objects.filter(email=postData['email'])
            if len(duplicate_email) > 0:
                errors['dupemail'] = "DUPLICATE: Email already in use"
        if len(postData['pw']) == 0:
            errors['pwreq'] = "REQUIRED FIELD: Password"
        elif len(postData['pw']) < 8:
            errors['pwreq'] = "LENGTH: Password must be at least 8 characters"
        if len(postData['cpw']) == 0:
            errors['cpwreq'] = "REQUIRED FIELD: Confirm Password"
        if postData['cpw'] != postData['pw']:
            errors['pwreq'] = "MISMATCH: Confirm Password must match Password"

        print("*-* *-* *-* *-* *-*")
        print("in the register_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors

    def update_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # validation if checks
        if len(postData['fname']) == 0:
            errors['fnamereq'] = "REQUIRED FIELD: First Name"
        if len(postData['lname']) == 0:
            errors['lnamereq'] = "REQUIRED FIELD: Last Name"
        if len(postData['email']) == 0:
            errors['emailreq'] = "REQUIRED FIELD: Email"
        # test whether a field matches the pattern
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "INVALID: Email"
        else:
            duplicate_email = User.objects.filter(email=postData['email'])
            if len(duplicate_email) > 0:
                errors['dupemail'] = "DUPLICATE: Email already in use"
        
        print("*-* *-* *-* *-* *-*")
        print("in the register_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"\nID: {self.id} Name: {self.fname} {self.lname}"


class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) == 0:
            errors['author'] = "REQUIRED FIELD: Author"
        # "Author: More than 3 characters"
        elif len(postData['author']) < 4:
            errors['author'] = "LENGTH: Author must contain at least 4 characters"

        if len(postData['quote']) == 0:
            errors['quote'] = "REQUIRED FIELD: Quote"
        #  "Quote: More than 10 characters"
        elif len(postData['quote']) < 11:
            errors['quote'] = "LENGTH: Quote must contain at least 11 characters"

        print("*-* *-* *-* *-* *-*")
        print("in the register_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors


class Quote(models.Model):
    # id - is implicit when creating models
    user = models.ForeignKey(
        User, related_name="quotes", on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    quote = models.TextField(max_length=4000)
    # comments have ManyToMany relationship with User via 'likes'
    # liked_quotes is how you access likes table from User class
    # likes is how you access likes table from Quote class
    likes = models.ManyToManyField(User, related_name="liked_quotes")
    # dislikes = models.ManyToManyField(User, related_name="disliked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __str__(self):
        return f"{self.fname} {self.lname}\n"