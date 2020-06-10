import time
import sys
import pandas as pd
import numpy as np

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city_list = ['chicago','new york city', 'washington']
    month_list = ['january','february','march','april','may','june','july','august','september','october','november','december','none']
    day_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','none']
    try: #probably need to move this try statement to be on each while loop instead to catch its keyboard interupt clause but I am running this in Jupyter and can't seem to use ctrl-C and thus couldn't trouble shoot it
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        while False == any(ele == city for ele in city_list): # determines if input is in the list of cities
            city = input('Invalid input, please enter one of the three cities to investigate: Chicago, New York City, or Washington:\n').lower()
        month = input('Would you like to filter by month? Please state the month you would like to explore or \"none\" to look at all months.\n').lower()
        while False == any(ele == month for ele in month_list): # determines if input is in the list of months
            month = input('Invalid input, please enter one of the months of the year or \"none\" to investigate all months:\n').lower()
        day = input('Would you like to filter by day? Please state the day you would like to explore or \"none\" to look at all days.\n').lower()
        while False == any(ele == day for ele in day_list): # determines if input is in the list of days
            day = input('Invalid input, please enter one of the days of the week or none to investigate all days:\n').lower()
        return city, month, day
    except KeyboardInterrupt:
        sys.exit()
    except:
        print('Invalid input, please try again. Remember to respond to each question with the name of the city, month, day, or none if applicable.')

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
    # gets the numberical equivalent of the months and days of the week to filter data
    month_list = {'january':1, 'february':2,'march':3,'april':4,'may':5,'june':6,'none':-1}
    day_list = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6,'none':-1}
    city = city.replace(' ','_') +'.csv'
    month_num = month_list.get(month)
    day_num = day_list.get(day)
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time']) # converts time to the proper object
    df['Month'] = df['Start Time'].dt.month # Gets the month of the timestamp
    df['Day of the Week'] = df['Start Time'].dt.dayofweek # Gets the day of the week, 0-6 is Monday to Sunday
    df['Hour'] = df['Start Time'].dt.hour # Gets the hours of the day
    if month_num != -1: # filters data for months
        df = df[df['Month'] == month_num]
    if day_num != -1: # filters data for days
        df = df[df['Day of the Week'] == day_num]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # lists to convert days and months into their corresponding names
    months = ['January','February','March','April','May','June']
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    # display the most common month
    month = df['Month'].mode()
    month = months[month.values[0]-1] # converts number to word
    print('The most common month of travel is: {}'.format(str(month)))

    # display the most common day of week
    day = df['Day of the Week'].mode()
    day = days[day.values[0]] # converts number to word
    print('The most common day of travel is: {}'.format(str(day)))

    # display the most common start hour, "military time" 0 - 24 hours
    hour = df['Hour'].mode()
    print('The most common hour of travel is: {}'.format(str(hour.values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()
    print('The most commonly used start station is: {}'.format(str(start_station.values[0])))

    # display most commonly used end station
    end_station = df['End Station'].mode()
    print('The most commonly used end station is: {}'.format(str(end_station.values[0])))

    # display most frequent combination of start station and end station trip
    df['Both Stations'] = df['Start Station'] + '*' + df['End Station']
    route = df['Both Stations'].mode()
    stations = route.values[0].split('*')
    print('The most common route are... Starting Station: {} ---> Ending Station: {}'.format(stations[0],stations[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time, rounding and displaying time in years for clarity
    print('The total travel time of all trips is: {} seconds or {} years'.format(df['Trip Duration'].sum(),(df['Trip Duration'].sum()/3600/24/365).round(2))) # converted into years because all other time points were a bit large

    # display mean travel time, rounding and displaying time in minutes for clarity
    print('The average travel time of all trips is: {} seconds or {} minutes'.format(round(df['Trip Duration'].mean(),2), round(df['Trip Duration'].mean()/60,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    customers = df.groupby(['User Type'])['End Station'].count().values[0]
    subs = df.groupby(['User Type'])['End Station'].count().values[1]
    print('There are {} customers and {} subscribers'.format(customers,subs))

    # Display counts of gender, note there is no gender category in washington.csv
    try:
        females = df.groupby(['Gender'])['End Station'].count().values[0]
        males = df.groupby(['Gender'])['End Station'].count().values[1]
        print('There are {} male subscribers and {} female subscribers'.format(males, females))
    except: # catching washington files
        print('Something went wrong, gender data could not be obtained. If Washington is the subject of this query, there is no gender data available.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min()) # casting as a int for rounding purposes
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode().values[0])
        print('The oldest customer was born in {}'.format(earliest))
        print('The youngest customer was born in {}'.format(recent))
        print('The most common birth year is {}'.format(common))
    except: # catching washington files
        print('Something went wrong, birth year data could not be obtained. If Washington is the subject of this query, there is no birth year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # Prompts the user if they want to see a subset of the raw data and prints it out upon request. The user will be prompted until they decline.
    # The first five rows of the dataframe are printed on the first prompt, followed by the next 5 rows and so on.
    # Also returns the derived data, such as month, day of the week, station combinations... I saw no reason to omit it

    acceptable_responses = ['yes','no'] # list of acceptable responses to the following question
    first_prompt = input('Would you like to see a subset of the raw data? Please answer yes or no.\n').lower()
    while False == any(ele == first_prompt for ele in acceptable_responses):
        # Catches any user input that is not yes or no
        first_prompt = input('Invalid input, please state yes if you want to see a subset of the raw data and no if you do not.\n').lower()

    while first_prompt == 'yes' and df.shape[0] > 4:
        # First condition checks to see if they want to see more data subsets
        # Second condition checks to see if the data frame has 5 rows of data to display using the head() function and to remove via drop. I have not actually tried to see if this would throw an error but I imagine it would.



        # Printing the first 5 rows of the data frame as well as some spacers for clarity. Probably could manually print instead of using head() for better format but its not necessary
        print('-'*40)
        print(df.head())
        print('-'*40)

        # Dropping the first five rows and reseting the index so that future drops still work
        # There are two resets since filtering the data by month and/or day results in a index that has varying step sizes since the index reflected the original unflitered data.
        # This could have been done before the print for consistency, but since the index was somewhat arbitrary already I didn't bother.
        # I feel like there should be a elegant way to call the first 5 rows of the data frame in the drop method but I'm not familiar with it.
        df.reset_index(drop=True,inplace=True) # This is redudent if the data is not filtered by month or day, a if statement might save on some processing power
        df = df.drop([0,1,2,3,4])
        df.reset_index(drop=True,inplace=True)

        # Determine if the user wants to see more raw data subsets
        first_prompt = input('Would you like to see a subset of the raw data? Please answer yes or no.\n').lower()
        while False == any(ele == first_prompt for ele in acceptable_responses):
            # Catches any user input that is not yes or no
            first_prompt = input('Invalid input, please state yes if you want to see a subset of the raw data and no if you do not.\n').lower()

def main():
    while True:
        # Runs until we break the loop

        # Gets the data frame parameters from the user
        city, month, day = get_filters()

        # Creates the data frame from parameters
        df = load_data(city, month, day)

        # Obtains time stats for the data frame
        time_stats(df)

        # Obtains station stats for the data frame
        station_stats(df)

        # Obtains trip duration stats for the data frame
        trip_duration_stats(df)

        # Obtains user stats for the data frame
        user_stats(df)

        # Prints out some raw data if the user desires it
        raw_data(df)

        # Determines if the user wants to make another query
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes': # This technically breaks on everything other than yes but w/e
            break

if __name__ == "__main__":
	main()
    
