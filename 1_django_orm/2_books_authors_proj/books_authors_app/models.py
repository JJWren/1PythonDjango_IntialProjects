from django.db import models
# regex import:
import re
import bcrypt


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


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title']) == 0:
            errors["title"] = "Book title should be at least 1 character"
        if len(postData['desc']) == 0:
            errors["desc"] = "Book description should be at least 1 character"

        print("*-* *-* *-* *-* *-*")
        print("in the book_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors


class AuthorManager(models.Manager):
    def author_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) == 0:
            errors["first_name_req"] = "Author first name should be at least 1 character"
        if len(postData['last_name']) == 0:
            errors["last_name_req"] = "Author last name should be at least 1 character"
        if len(postData['notes']) == 0:
            errors["notes_req"] = "Author notes should be at least 1 character"

        print("*-* *-* *-* *-* *-*")
        print("in the book_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors


class Book(models.Model):
    # id - is implicit when creating models
    title = models.CharField(max_length=255)
    desc = models.TextField("")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __str__(self):
        return f"\nID: {self.id} Title: {self.title}"


class Author(models.Model):
    # id - is implicit when creating models
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    notes = models.TextField("")
    books = models.ManyToManyField(Book, related_name="authors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

    def __str__(self):
        return f"\nID: {self.id} Name: {self.first_name} {self.last_name}"
