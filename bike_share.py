import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_DATA = {'january': 1, 'february': 2,
               'march': 3, 'april': 4,
               'may': 5, 'june': 6,
               'all': None}

WEEK_DAYS = ['all', 'monday', 'tuesday',
              'wednesday', 'thursday',
              'friday', 'saturday',
              'sunday']  

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("would you like to see data for chicago, new york city or washington?\n").lower()
    while city not in CITY_DATA:
        print("\nthere\'s no data available for this city in the current time\n")
        city = input("\nWould you like to see data for chicago, new york city or washington?\n").lower()
  
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nplease type a month from january to june to filter data by,\n or type \"all\" to view data for all months\n").lower()
    if month.isdigit():
        month = int(month)
    while month not in MONTHS_DATA.keys() and month not in MONTHS_DATA.values():
        print("\nyour input must be from the range specified above.")
        month = input("\nplease type a month between january to june to filter the data by,\n or type all to view data for all months\n").lower() 
        if month.isdigit():
            month = int(month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nPlease type a day to filter the data by, or type \"all\" to view data for all the days\n").lower()
    while day not in WEEK_DAYS:
        print("\nInvalid input. Please try again in the accepted input format.")
        day = input("\nPlease type a day to filter the data by, or type \"all\" to view data for all the days\n")
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"]) 
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    print()
    if month != "all":
        if type(month) == str:
            month = MONTHS_DATA[month]
        df = df[df['month'] == month]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df["month"].mode()[0]
    print("most common month: {}".format(common_month))
    # TO DO: display the most common day of week
    common_day = df["day_of_week"].mode()[0]
    print("most common day of week: {}".format(common_day))
    # TO DO: display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print("most common start hour: {}".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df["Start Station"].mode()[0]
    print("most commonly used start station: {}".format(common_start))
    # TO DO: display most commonly used end station
    common_end = df["End Station"].mode()[0]
    print("most commonly used end station: {}".format(common_end)[0])

    # TO DO: display most frequent combination of start station and end station trip
    df["Start To End"] = df["Start Station"].str.cat(df["End Station"], sep=" to ")
    combination = df["Start To End"].mode()[0]
    print("most frequent combination of start station and end station trip: {}".format(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = df["Trip Duration"].sum()
    print("total travel time: {}".format(total))
    # TO DO: display mean travel time
    mean = df["Trip Duration"].mean()
    print("mean travel time: {}".format(mean))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df["User Type"].value_counts()
    print("counts of user types: {}".format(user_type))

    # TO DO: Display counts of gender
    try:
        gender =  df["gender"].value_counts()
        print("counts of gender: {}".format(gender))
    except:
        print("\nThere is no 'Gender' column in this file.")
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {}\n\nThe most recent year of birth: {}\n\nThe most common year of birth: {}".format(earliest, recent, common_year))
    except:
        print("There are no birth year in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    response = ["yes", "no"]
    user_res = ""
    count = 0
    while user_res not in response:
        user_res = input("would you like to view the row data?\"yes or no\"").lower()
        if user_res == "yes":
            print(df.head())
        elif user_res not in response:
            print("\nrestarting")

    while user_res == "yes":
        print("would you like to print more?")
        count += 5
        user_res = input().lower()
        if user_res == "yes":
            print(df[count:count+5])
        elif user_res != "yes":
            break
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
       
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
