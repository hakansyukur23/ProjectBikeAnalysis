# Project Bike Sharing Analysis and Dashboard

Welcome to my project! This is a Streamlit dashboard that visualizes bike sharing data.
Bike-sharing systems are modernized bike rental services where the entire process, including membership, rental, and return, is automated. Users can conveniently rent bikes from one location and return them to another. With over 500 programs and 500,000 bicycles globally, these systems are gaining significant attention for their positive impact on traffic management, environmental sustainability, and public health.

## Defining Question
- What has been the trend in the number of bicycle users in 2012?
- Which season has the highest total trips for both casual and registered riders?
- What is the difference in bike rental patterns between member riders and casual riders during weekdays and weekends?
- What weather condition has the highest number of bicycle users according to the rental pattern?

## Insights and Findings

- Trend in the number of bicycle users in 2012: The number of bicycle users in 2012 showed fluctuations throughout the year, with clear seasonal trends. The peak months generally occurred in warmer seasons like spring and summer, while the number of rentals decreased during the colder months.

- Season with the highest total trips for both casual and registered riders: Fall (autumn) is the season with the highest total trips for both casual and registered riders, indicating a strong preference for bike rentals during this season.

- Difference in bike rental patterns between member riders and casual riders during weekdays and weekends: Member riders dominate bike rentals during weekdays, with a gradual decrease in trips after Tuesday, reaching the lowest point on Sundays. Casual riders have relatively low usage during weekdays, but their trips significantly increase over the weekend. In conclusion, member riders tend to rent bikes on weekdays, while casual riders prefer weekends.

- Weather condition with the highest number of bicycle users: Clear weather is the condition with the highest number of bicycle users, showing that good weather positively influences the number of bike rentals.

 ## Dashboard

  ![BikeSharing Dashboard](image/dashboard.jpg)


  
## How to Run the Dashboard Locally

Follow the steps below to run the dashboard on your local machine.

### 1. Install Dependencies

To install all the required libraries, open your terminal/command prompt/conda prompt, navigate to this project folder, and run the following command:

```bash
pip install -r requirements.txt
```
### 2. Run Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```
