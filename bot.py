import robin_stocks as r
import pyotp
import pprint
import secrets
import smtplib
from time import sleep
from email.message import EmailMessage

#Robinhood Login
try:
    login = r.login(secrets.RH_User, secrets.RH_Pass, mfa_code=totp)
except:
    login = r.login(secrets.RH_User, secrets.RH_Pass)

# For Text Notifications
def email_alert(body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['to'] = to

    user = secrets.email
    msg['from'] = user
    password = secrets.password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

amount = 40000 # Quanity you want to buy

# There are three options after you buy. The price increases, the price decreases, or the price stays the same.
def main():
    pur_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Get's market price for what I'm about to buy at
    r.order_buy_crypto_limit('DOGE', amount, pur_price) # Buys
    target_price = (pur_price * .03) + pur_price # Set's a variable for your target price (Up _%)
    stop_loss = ((pur_price * (.06 * -1)) + pur_price) # Set's a variable for your stop loss (Down _%)
    while True:
        mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Updated market price
        if mark_price >= target_price: # If price increases
            r.order_sell_crypto_limit('DOGE', amount, mark_price)
            print("Profits Taken")
            email_alert("Profits Taken", secrets.phone_number)
            profit_buy_back()

        elif mark_price <= stop_loss: # If price decreases
            r.order_sell_crypto_limit('DOGE', amount, mark_price)
            print("Stop Loss Triggered")
            email_alert("Stop Loss Triggered", secrets.phone_number)
            loss_buy_back()

        else: # If price stays the same
            print("In the main function")
            print("Current Market Price: " + str(mark_price))
            print("Target Price: " + str(target_price))
            print("Percentage Change: " + str(((mark_price - pur_price) / pur_price) * 100))
            sleep(300)

def profit_buy_back():
    sale_price = float(r.get_crypto_quote('DOGE').get("mark_price", ""))
    new_target_price = ((sale_price * .03) + sale_price)
    new_stop_loss = ((sale_price * (.06 * -1)) + sale_price)
    while True:
        new_mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Updated market price
        if new_mark_price >= new_target_price:
            r.export_completed_crypto_orders(".", "Export from profit buy back function, profit going back to main")
            email_alert("Profit taken, profit going back to main", secrets.phone_number)
            main()
        elif new_mark_price <= new_stop_loss:
            r.export_completed_crypto_orders(".", "Export from profit buy back function, loss going back to main")
            email_alert("Profit taken, loss going back to main", secrets.phone_number)
            main()
        else: # No change, continue loop
            print("In the profit function")
            print("Current Market Price: " + str(new_mark_price))
            print("Target Price: " + str(new_target_price))
            print("Percentage Change: " + str(((new_mark_price - sale_price) / sale_price) * 100))
            sleep(300)

def loss_buy_back():
    sale_price = float(r.get_crypto_quote('DOGE').get("mark_price", ""))
    new_target_price = ((sale_price * .06) + sale_price)
    new_stop_loss = ((sale_price * (.03 * -1)) + sale_price)
    while True:
        new_mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Updated market price
        if new_mark_price >= new_target_price:
            r.export_completed_crypto_orders(".", "Export from loss buy back function, profit, going back to main")
            email_alert("Profit taken, profit going back to main", secrets.phone_number)
            main()
        elif new_mark_price <= new_stop_loss:
            r.export_completed_crypto_orders(".", "Export from loss buy back function, loss, going back to main")
            email_alert("Profit taken, loss going back to main", secrets.phone_number)
            main()
        else: # No change, continue loop
            print("In the loss function")
            print("Current Market Price: " + str(new_mark_price))
            print("Target Price: " + str(new_target_price))
            print("Percentage Change: " + str(((new_mark_price - sale_price) / sale_price) * 100))
            sleep(300)

main() # The big red button

