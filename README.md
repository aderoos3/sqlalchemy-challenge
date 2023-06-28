# sqlalchemy-challenge
##Analysis of Hawaii vacation

For this assignment, I started with a ipynb file, a sqlite database, app.py and two csv files for weather information in Hawaii. I started with the normal SQLAlchemy things, I created an engine to connectt to the database and I used automap_base to find my tables (keys) and save them for reference. Then I linked to a session. 

This is where the actual analysis started. I started by finding the most recent date in the csv file and then the date from 12 months before. I did a query for the precipitation and date data and then loaded it into a DataFrame. From I sorted it all by date and then plotted the results to show the inches of precipitation over time. I also got summary stats with the describe() function. 

Next I did some station analysis. I found the total number of stations in the other csv file and did a query to find the most active session in order. I calculated the minimum, maximum, and average temperatures for the most active station. I graphed the temperature observations over 12 months in a histogram. 

The second part was to create a site using HTML with all the data gathered from the first queries. I started with the usual set-up to get a flask and database connection for my site. Then I made a homepage with all the available routes. I made a route for each route shown on the homepage. I started with a precipitation analysis and made it into a dictionary, jsonified it and it was on the site. I did something similar for the stations. I made a list of the temperature observations of the most active station over 12 months. That was a combination of some of the analysis from earlier. I made a route to show the minimum, maximum, and average temperature for all dates before a specific start date and another route for those same things for between a start and end date. 
