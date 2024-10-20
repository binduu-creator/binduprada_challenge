import re

# Function to validate the credit card number
def validate_credit_card(card_number):
    # expression to match the credit card format
    pattern = r"^[456]\d{3}(-?\d{4}){3}$"
    
    # checking the credit card matches the format
    if not re.match(pattern, card_number):
        return "Invalid"
    
    # Check if the card contains 4 or more consecutive repeated digits
    card_number_clean = card_number.replace("-", "")
    if re.search(r"(\d)\1{3,}", card_number_clean):
        return "Invalid
    
    

# Input the number of card numbers to check
n = int(input("Enter the number of credit cards: "))

# Iterate through each card number and check validity
for _ in range(n):
    card_number = input().strip()
    print(validate_credit_card(card_number))
