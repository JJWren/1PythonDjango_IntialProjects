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


class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['review']) < 10:
            errors['reviewreq'] = "LENGTH: Review must be at least 10 characters"

        print("*-* *-* *-* *-* *-*")
        print("in the book_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors


class Review(models.Model):
    # id - is implicit when creating models
    review = models.TextField("")
    # one to many relationship (one User can have many Reviews; one Review can only have one User)
    user = models.ForeignKey(
        User, related_name="review", on_delete=models.CASCADE)


class AuthorManager(models.Manager):
    def author_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['full_name']) < 3:
            errors["full_name_req"] = "Author first name should be at least 3 characters"

        print("*-* *-* *-* *-* *-*")
        print("in the book_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors


class Author(models.Model):
    # id - is implicit when creating models
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

    def __str__(self):
        return f"\nID: {self.id} Name: {self.first_name} {self.last_name}"


class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title']) == 0:
            errors["title"] = "Book title should be at least 1 character"
        if len(postData['review']) == 0:
            errors["review"] = "Book review should be at least 1 character"

        print("*-* *-* *-* *-* *-*")
        print("in the book_validator in models.py")
        print("errors")
        print("*-* *-* *-* *-* *-*")

        return errors


class Book(models.Model):
    # id - is implicit when creating models
    title = models.CharField(max_length=255)
    # many to many relationships - User can be connected to many Books; Book can have many Users
    users = models.ManyToManyField(User, related_name="books")
    reviews = models.ManyToManyField(Review, related_name="books")
    # one to many - Book can have one Author; Author can have many Books
    author = models.ForeignKey(
        Author, related_name="books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __str__(self):
        return f"\nID: {self.id} Title: {self.title}"
