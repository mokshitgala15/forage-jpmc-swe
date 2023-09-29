################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server requests
N = 500

def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    """ ------------- Update this function ------------- """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    
    # Calculate the stock price as the average of bid_price and ask_price
    price = (bid_price + ask_price) / 2.0
    
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    """ ------------- Update this function ------------- """
    # Handle the case where price_b could be zero (avoid division by zero)
    if price_b == 0:
        ratio = "N/A"  # Handle as "Not Available" or any other appropriate value
    else:
        ratio = price_a / price_b
    return ratio

# Main
if __name__ == "__main__":
    # Initialize a dictionary to store stock prices
    prices = {
        'ABC': None,
        'DEF': None
    }

    # Query the price once every N seconds.
    for _ in iter(range(N)):
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())

        """ ----------- Update to get the ratio --------------- """
        # Initialize variables for calculating the ratio
        price_A = None
        price_B = None

        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))
            
            # Store the prices for stock A (ABC) and stock B (DEF)
            if stock == 'ABC':
                price_A = price
            elif stock == 'DEF':
                price_B = price

        # Print prices for debugging
        print("Price A (ABC):", price_A)
        print("Price B (DEF):", price_B)

        # Calculate and print the ratio, even if one price is None
        if price_A is not None and price_B is not None:
            ratio = getRatio(price_A, price_B)
            print("Ratio %s" % ratio)
        else:
            print("Unable to calculate ratio due to missing prices.")

        # Store the stock prices in the dictionary
        prices['ABC'] = price_A
        prices['DEF'] = price_B

    # Print the final stock prices
    print("Final Stock Prices:")
    for stock, price in prices.items():
        print("%s: %s" % (stock, price))
