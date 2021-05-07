import robin_stocks.robinhood as r
import pyotp
import pprint
import secrets
import smtplib
from time import sleep
from slack_sdk import WebClient


#Robinhood Login
try:
    login = r.login(secrets.RH_User, secrets.RH_Pass, mfa_code=totp)
except:
    login = r.login(secrets.RH_User, secrets.RH_Pass)

# For Slack Notifications
client = WebClient(secrets.SLACK_API_TOKEN)

amount = 3100 # Quanity you want to buy

def buy():
    r.order_sell_crypto_limit('DOGE', amount, mark_price)

def sell():
    r.order_sell_crypto_limit('DOGE', amount, mark_price)



# There are three options after you buy. The price increases, the price decreases, or the price stays the same.
def main():
    pur_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Get's market price at the current time and sets it as a variable
    r.order_buy_crypto_limit('DOGE', amount, pur_price) # Buys at market price
    target_price = (pur_price * .05) + pur_price # Set's a variable for your target price (Up _%)
    stop_loss = ((pur_price * (.10 * -1)) + pur_price) # Set's a variable for your stop loss (Down _%)
    while True:
        mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Updates market price
        if mark_price >= target_price: # If price increases
            buy()
            print("Profits Taken")
            client.chat_postMessage(channel='#alerts', text='Profits Taken')
            profit_buy_back()

        elif mark_price <= stop_loss: # If price decreases
            sell()
            print("Stop Loss Triggered")
            client.chat_postMessage(channel='#alerts', text='Stop Loss Triggered') # Sends slack message that it sold for a loss
            loss_buy_back()

        else: # If price stays the same
            print("In the main function")
            print("Current Market Price: " + str(mark_price))
            print("Target Price: " + str(target_price))
            print("Percentage Change: " + str(((mark_price - pur_price) / pur_price) * 100))
            sleep(15)

def profit_buy_back():
    sale_price = float(r.get_crypto_quote('DOGE').get("mark_price", ""))
    new_target_price = ((sale_price * .03) + sale_price) # Really need a trailing stop loss
    new_stop_loss = ((sale_price * (.06 * -1)) + sale_price)
    while True:
        new_mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Updated market price
        if new_mark_price >= new_target_price:
            r.export_completed_crypto_orders(".", "Export from profit buy back function, profit going back to main")
            client.chat_postMessage(channel='#alerts', text='Profit taken, profit going back to main')
            main()
        elif new_mark_price <= new_stop_loss:
            r.export_completed_crypto_orders(".", "Export from profit buy back function, loss going back to main")
            client.chat_postMessage(channel='#alerts', text='Profit taken, loss going back to main')
            main()
        else: # No change, continue loop
            print("In the profit function")
            print("Current Market Price: " + str(new_mark_price))
            print("Target Price: " + str(new_target_price))
            print("Percentage Change: " + str(((new_mark_price - sale_price) / sale_price) * 100))
            sleep(30)

def loss_buy_back():
    sale_price = float(r.get_crypto_quote('DOGE').get("mark_price", ""))
    new_target_price = ((sale_price * .04) + sale_price)
    new_stop_loss = ((sale_price * (.15 * -1)) + sale_price)
    while True:
        new_mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Updated market price
        if new_mark_price >= new_target_price:
            r.export_completed_crypto_orders(".", "Export from loss buy back function, profit, going back to main")
            client.chat_postMessage(channel='#alerts', text='Profit taken, profit going back to main')
            main()
        elif new_mark_price <= new_stop_loss:
            r.export_completed_crypto_orders(".", "Export from loss buy back function, loss, going back to main")
            client.chat_postMessage(channel='#alerts', text='Profit taken, loss going back to main')
            main()
        else: # No change, continue loop
            print("In the loss function")
            print("Current Market Price: " + str(new_mark_price))
            print("Target Price: " + str(new_target_price))
            print("Percentage Change: " + str(((new_mark_price - sale_price) / sale_price) * 100))
            sleep(30)

def price_alert():
    pur_price = float(r.get_crypto_quote('DOGE').get("mark_price", ""))
    while True:
        mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", "")) # Updates market price
        target_price = (pur_price * .03) + pur_price # Set's a variable for your target price (Up _%)
        stop_loss = ((pur_price * (.05 * -1)) + pur_price) # Set's a variable for your stop loss (Down _%)
        if mark_price >= target_price: # If price increases
            client.chat_postMessage(channel='#alerts', text=("Doge is up: " + str(((mark_price - pur_price) / pur_price) * 100)))
            break
        elif mark_price <= stop_loss: # If price decreases
            client.chat_postMessage(channel='#alerts', text=("Doge is on sale : " + str(((mark_price - pur_price) / pur_price) * 100))) # Sends slack message that it sold for a loss
            break
        else:
            sleep(30)

def price_alert_one():
    while True:
        mark_price = float(r.get_crypto_quote('DOGE').get("mark_price", ""))
        if mark_price >= 0.60:
            client.chat_postMessage(channel='#alerts', text=("DOGE is up, sell it!"))
            break
        else:
            sleep(30)

#main()
price_alert_one()