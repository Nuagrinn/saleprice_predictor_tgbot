### Telegram bot to predict the prices of secondary apartment in Moscow

### Results briefly:
1. XBGBoost-Regressor 
2. Trained on 44 000 ads from CIAN.ru
3. RMSE: 23848052 RMSPE: 16.48 R2: 0.92

* Contains:
    1. Data parsing
    2. Data processing and model training
    3. Telegram Bot
    
### 1. map_request_parser:

The parser is based on the CIAN map query algorithm. 
The request contains the coordinates of the vertices of the box.
All ads out of the box are returned upon request.

*PointRectangleClasses.py* - from small squares returning no more than 300 ads, 
a grid is generated that covers the whole of Moscow.

*async_map_request* - makes an asynchronous request for a map across all generated squares. 
Return coordinates and links to ads.

*async_announcement_parser* -makes asynchronous requests for links for each declaration and 
returns all data on them. Data is saved to csv-file.

*crutch* - function to exclude an error from aiohttp on Windows.

### 2. j-note
*Cian_SalePricePrediction_ML* - Data preprocessing, model training. Saving model
and pipeline 

### 3. tg_bot

*prediction_handlers* - main handlers for messages in bot. Take buttons from *buttons.py*.
Starting with *app.py*.

*ml_functions* - main functions to handle user's data. Also handle it with additional 
functions from *additional_ml_functions.py*. 

*.env* - gitingored file. Need to be created and filled up with bot_token, gmaps_token and
admin's tg-ID

