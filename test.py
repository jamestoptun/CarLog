import os

# Get the absolute paths of both files
signup_path = os.path.abspath("signup.py")
mainpage_path = os.path.abspath("mainpage.py")

# Check if the directory paths of both files are the same
if os.path.dirname(signup_path) == os.path.dirname(mainpage_path):
    print("Both files are in the same directory.")
else:
    print("The files are in different directories.")
