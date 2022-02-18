# Crypto-portfolio
Tracking my crypto portfolio using Binance API
This program is designed to track my crypto portfolio.
Calculate my current balance and present it as a dataframe. 
The app gets all my order history for all different coin pairs, cleans and filters the information and creates a balance sheet using pandas.
The API only allows recieving orders for a specified pair, I needed to manually extract the pairs I traded in the past and then loop through them to get all my orders.

This app is a great base for future features to be added like monitoring different trade strategies etc.
