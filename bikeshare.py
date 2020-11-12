import time
import pandas as pd
import numpy as np

CITY_DATA   = { 'chicago': 'chicago.csv',
                'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
active_months=['january','february','march','april','may','june','all']
active_days  =['monday','tuesday','wednesday','thursday','friday',
              'saturday','sunday','all']
active_cities=['chicago','new york city','washington']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze0
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('Enter city name (You can choose from chicago, new york city, washington: ').lower()
        if city in active_cities:
            
            break
        else:
            print('Invalid input {}, please try again'.format(city))
    

    #get user input for month (all, january, february, ... , june)
    while True:
        month=input('Enter month name: ').lower()
        if month in active_months:
            print('Thank you for your input')
            break
        else:
            print('Invalid input {}, please try again.'.format(month))
    

    #get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Enter day of week: ').lower()
        if day in active_days:
            print('Thank you for you input, one moment.')
            break
        else:
            print('{} is not a valid input, please try again.'.format(day))
     

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
    df=pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #extract month and day of week from Start Time to create new column
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
    # filter by month to create new dataframe
    if month !='all':
        # using the index of valids months list to get corresponding month name
        month=active_months.index(month)+1
        
        #filter by month to create new dataframe
        df=df[df['month']==month]
     # filter by day 
    if day !='all':
        # filter by day of week to create new dataframe
        df=df[df['day_of_week']==day.title()]
     # returns final dataframe     
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    common_month=df['month'].mode()[0]
    month_name=active_months[common_month-1].title()
    print('Most common month was {}'.format(month_name))

    #display the most common day of week
    common_day_name=df['day_of_week'].mode()[0]
    print('Most common day of the week was {}'.format(common_day_name))

    #display the most common start hour
    df['Start Hour']=df['Start Time'].dt.hour
    common_hour=df['Start Hour'].mode()[0]
    print('Most common start hour was {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    print('Most common start station was {}'.format(df['Start Station'].mode()[0]))

    #display most commonly used end station

    print('Most common end station was {}'.format(df['End Station'].mode()[0]))
    #display most frequent combination of start station and end station trip
    popular_trips=df.groupby(['Start Station','End Station'])['Start Time'].count()
    sorted_trips=popular_trips.sort_values(ascending=False,axis=0)
    print('The most common combination of Start and Stop stations are:{} and {}'.format(sorted_trips.index[0][0],sorted_trips.index[0][1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print('The total travel time is {}'.format(df['Trip Duration'].sum()))

    #display mean travel time
    print('The mean travel time is {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('The counts of uder types is {}'.format(df['User Type'].value_counts()))

    #Display counts of gender
    if 'Gender' in df:
        
        print('The counts of gender is {}'.format(df['Gender'].value_counts()))
    else:
        print('Gender data not available for given data')

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Earliest birth year is {}'.format(df['Birth Year'].min()))
        print('Most recent birth year is {}'.format(df['Birth Year'].max()))
        print('Most common birth year is {}'.format(df['Birth Year'].mode()[0]))
    else:
        print('Birth Year does not exist in given data')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data=input('Would you like to see the first 5 rows of data, Enter yes to view and no to cancel:  \n').lower()
        start_loc=0
        end_loc=5
        while(view_data=='yes'):
            print(df.iloc[start_loc:end_loc])
            start_loc+=5
            end_loc+=5
            view_display=input('Would you like to see the next 5 rows of data? Enter yes or no:  \n').lower()
            if view_display=='yes':
                continue
            else:
                print('Thank you')
                break
            

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()



