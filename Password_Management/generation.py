import random 
import string

def save_password_to_file(password, filename):
    with open(filename, 'a') as file:
        file.write('Password: ' + password + '\n')

def generate_password(length):
    if length < 8:
        raise ValueError("Password should be at least 8")

    lower = string.ascii_lowercase    
    upper = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation

    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(special)
    ]

    all_characters = lower + upper + digits + special
    password += random.choices(all_characters, k=length-4)

    random.shuffle(password)

    return ''.join(password)

try:
    length = int(input("Enter the desired password length: "))
    password = generate_password(length)
    print("Generated password:", password)

    filename = input("Enter the filename to save the password: ")
    save_password_to_file(password, filename)
    print(f"Password save to filename")
except ValueError as ve:
    print("Error:", ve)