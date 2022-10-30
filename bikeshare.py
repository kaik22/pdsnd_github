#Importing the libraries required
import time
import numpy as np
import pandas as pd
import inquirer as iq

#Variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

WEEKDAYS = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday' ]

DAYS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


#Functions required for the process
def city_input():
    """
    Call for a infinite loop that ask the user for the city he/she wants to query
    Return:
    str - city
    """
    while True: #When successfully input the city the loop will end
        try:
            city = str(input("Which city would you like to see data from? \n").lower())
            if city in CITY_DATA:
                return city
                break
            else: #In case input is wrong
                print("Apologies,{} is not a valid city".format(city))
                #Ask the user if he/she wants to continue
                #Call to function that elavorates the question 
                continue_q = continue_query() 
                #Exit if user do es not want to continue
                if continue_q == "no":
                    print('See you soon, have a nice day!')
                    break
                else: #Keep trying to get user city input
                    continue
        except Exception:
            # The cycle will go on until validation
            print("Wrong value, please try again")
        
def continue_query():
    """
    Call for making the question to see if the user wants to continue
    Return:
    (str) - yes/no response
    """  
    #Question to be made and options  
    want_continue = [
        iq.List('y/n',
                        message="Do you want to continue?",
                        choices=['yes', 'no'],
                    ),
    ]           
    print('-'*50)
    continue_query = iq.prompt(want_continue)
    return continue_query['y/n']


def time_filter_input():
    """
    Call for getting if the user wants to apply any type of filter on the data
    Return:
    Response to question
    str - 'Yes, I want to filter by month'
    str - 'Yes, I want to to filter by a specifc day'
    str - 'Yes, I want to filter by a specific weekday'
    str - 'No'
    """
    #Question to be made and options
    what_time_filter = [
        iq.List('time_filter',
                                 message="Would you like to see data for an specific month or day?",
                                 choices=['Yes, I want to filter by month', 
                                          'Yes, I want to to filter by a specifc day',
                                          'Yes, I want to filter by a specific weekday',
                                          'No'],
                        ),
        ]           
    print('-'*50)
    time_filter = iq.prompt(what_time_filter)    
    return time_filter['time_filter']

def month_input():
    """
    Call for getting the month the user wants to filter by
    Return:
    str - month
    """
    #Question to be made and options, options comming from MONTHS variable defined at the beginning
    what_month = [
        iq.List('month_filter',
                                message="By which month do you want to filter by?",
                                choices = MONTHS,
                    ),
        ]           
    print('-'*50)
    month_filter = iq.prompt(what_month)    
    return month_filter['month_filter']
    
def day_input():
    """
    Call for getting the day the user wants to filter by
    Return:
    str - day 
    """
    #Question to be made and options, options comming from DAYS variable defined at the beginning
    what_day = [
        iq.List('day_filter',
                                message="By which day do you want to filter by?",
                                choices = DAYS,
                    ),
        ]           
    print('-'*50)
    day_filter = iq.prompt(what_day)    
    return day_filter['day_filter']      

def weekday_input():
    """
    Call for getting the weekday the user wants to filter by
    Return:
    str - weekday  
    """
    #Question to be made and options, options comming from WEEKDAYS variable defined at the beginning
    what_weekday = [
        iq.List('weekday_filter',
                                message="By which weekday do you want to filter by?",
                                choices = WEEKDAYS,
                    ),
        ]           
    print('-'*50)
    weekday_filter = iq.prompt(what_weekday)    
    return weekday_filter['weekday_filter']     

   
#LOAD DATA
def load_data(city, month ='all', day='all', weekday='all'):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - day of the month, or "all" to apply no day filter
        (str) weekday - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month, month and day or weekday
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month, day of week, hour and day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Start hour'] = df['Start Time'].dt.hour
    df['day']= df['Start Time'].dt.day
 
    # extract hour from End Time to create new column
    df['End hour'] = df['End Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if weekday != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == weekday.title()]
        
    # filter by day  if applicable
    if day != 'all':
        # filter by day to create the new dataframe
        df = df[ df['day'] == day]  
          
    return df

def wantindividualdata():
    """
    Call for making the question to see if the user want to see individual trip data
    Return:
    (str) - yes/no
    """     
    #Question to be made and options  
    ind_trip = [
        iq.List('y/n',
                        message="Would you like to view individual trip data?",
                        choices=['yes', 'no'],
                    ),
    ]           
    ind_trip = iq.prompt(ind_trip)
    print('-'*50)
    return ind_trip['y/n']   

def time_stats(df, month='all', weekday='all'):
    """Function to calculate and display statistics on the most frequent times of travel.
    Args:
    (df): Data frame to work with.
    Returns: None
    """
    print('-'*50)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    #Unless the data is already filter by month
    if month == 'all':
        most_common_month = df['month'].value_counts().idxmax()
        most_common_month = MONTHS[int(most_common_month)-1]
        print("The most common month is: {}".format(most_common_month))

    #Display the most common day of week
    #Unless the data is already filter by weekday
    if weekday == 'all':
        most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
        print("The most common day of week is: {}".format(most_common_day_of_week))

    #Display the most common start hour

    most_common_start_hour = df['Start hour'].value_counts().idxmax()
    print("The most common start hour is: {}".format(most_common_start_hour))
    
    #Display the most common emd hour
    
    most_common_end_hour = df['End hour'].value_counts().idxmax()
    print("The most common end hour is: {}".format(most_common_end_hour))

    #Display time it took to calculate it
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*50)

#Function to calculate station related statistics
def station_stats(df):
    """Function to calculate and display statistics on the most popular stations and trip.
    Args:
    (df): Data frame to work with.
    Returns: None
    """

    print('\nCalculating The Most Popular Stations and Trip Combinations...\n')
    start_time = time.time()

    #Mode method to find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print("The most commonly station used for starting the trip is: {}".format(common_start_station))

    #Mode method to find the most common end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly station used for ending the trip is: {}".format(common_end_station))
    
    #str.cat to combine two columsn in the df and creation of new column 'Start Combination'
    df['Station Combination'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    
    #Mode method on new column to find  the most common combination
    combo = df['Station Combination'].mode()[0]
    print("\nThe most frequent combination of trips is: {}".format(combo))
    
    #Display time it took to calculate it
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """Function to calculate and display statistics on the average trip duration.
    Args:
    (df): Data frame to work with.
    Returns: None
    """
    print('\nCalculating Average Trip Duration...\n')
    start_time = time.time()

    #Mean method to find the average trip duration
    average_duration = round(df['Trip Duration'].mean())
    
    #Find the average duration in minutes and seconds format
    min, sec = divmod(average_duration, 60)
    print("The average trip duration is {} minutes and {} seconds.".format(min,sec))
    
    #Display time it took to calculate it
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*50)

def user_stats(df):
    """Function to calculate and display statistics on bikeshare users.
        Args:
    (df): Data frame to work with.
    Returns: None
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Value_counts method to find the total users by type 
    #They are then displayed by their types
    user_type = df['User Type'].value_counts()

    print("The types of users by number are shown below:\n")
    print(user_type)

    #Value_counts method to find the total users by gender
    #Try clause is implemented to display the number of users by Gender, since the Gender has NaNs
    try:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are shown below:\n")
        print(gender)
    except:
        print("\nThere is no 'Gender' column in this set of data.")

    #Try clause is implemented to display Birth stats, since the Birth Year column has NaNs
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe oldest user was born in: {}".format(oldest))
        print("The youngest user was born in: {}".format(youngest))
        print("The most common year of birth: {}".format(common_year))
    except:
        print("There are no birth year details in this set of data.")
        
    #Display time it took to calculate it
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*50)


def display_data(df):
    """Function to individual trip data if user wants to.
    Args:
    (df): Data frame to work with.
    Returns: None
    """
    #Get number or rows
    row_length = df.shape[0]
    ind_trip = 'yes' #variable that determines if user want to see individual trip data
    counter = 0
    #Creation of new df with the original columns in the csv
    df2=df[["Start Time", 'End Time', 'Trip Duration',
       'Start Station', 'End Station', 'User Type']]
    #Iteration from 0 to the number of rows in steps of 5 rows
    while ind_trip == 'yes':
        print('-'*50)
        #Call to ask question to user
        ind_trip = wantindividualdata()
        if ind_trip == 'no': #exit in case user does not want to see more data
            break
        elif ind_trip == "yes" and row_length > (counter+5): #check if we are close to the end of the data
             print(df2[counter:counter+5])
             counter += 5     
        else: 
            print(df[counter:]) 
            print("This were the last records")
            break
 

#Main function to call all the previous functions
def main():
    #Welcome message
    print("Let's explore some US bikeshare data. We currently have data for Chicago, New York, or Washington")
    print('-'*50)
    while True:
        #Call function to get the city request 
        city = city_input()   
        #Call function to get if user want to filter the date by time
        time_filter = time_filter_input()
        #Depending on the response we ask the month or month and day
        if time_filter == 'Yes, I want to filter by month':
            month = month_input()
            #Call for loading the DataFrame
            df=load_data(city,month)
            #Call for getting the time statistic
            #This call is included in this if, since the arguments depend on the time filter
            time_stats(df,month)
        elif time_filter == "Yes, I want to to filter by a specifc day":
            month = month_input()
            day = day_input()
            #Call for loading the DataFrame
            df=load_data(city,month,day)
            #Call for getting the time statistic
            #This call is included in this if, since the arguments depend on the time filter
            time_stats(df,month,day)  
        elif time_filter == "Yes, I want to filter by a specific weekday":
            month = 'all'
            day = "all"
            weekday=weekday_input()
            #Call for loading the DataFrame
            df=load_data(city,month,day,weekday)
            #Call for getting the time statistic
            #This call is included in this if, since the arguments depend on the time filter
            time_stats(df,month,weekday)
        else:
            #Call for loading the DataFrame
            df=load_data(city)
            #Call for getting the time statistic
            #This call is included in this if, since the arguments depend on the time filter
            time_stats(df)
                
        #Calls to the rest of the stats functions
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #Call to see if the user want to see individual trip data and if so, so it.
        display_data(df)
        
        #Ask the user if he/she wants to continue
        continue_q = continue_query()
        #Exit if user do es not want to continue
        if continue_q == "no":
            print('See you soon, have a nice day! \n')
            break
        else:
            continue 
   

if __name__ == "__main__":
	main()

