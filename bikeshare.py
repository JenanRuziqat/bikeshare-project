import pandas as pd

# City data
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.
    Returns validated inputs.
    """
    print("Hello! Let's explore bike-sharing data.\n")

    # Choose city
    while True:
        city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Error! Please select one of the listed cities.")

    # Choose month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input(
            "Choose a month (January, February, ..., June) or 'all' for all months: "
        ).strip().lower()
        if month in months:
            break
        else:
            print("Error! Choose a correct month.")

    # Choose day
    days = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input(
            "Choose a day (Monday, ..., Sunday) or 'all' for all days: "
        ).strip().lower()
        if day in days:
            break
        else:
            print("Error! Choose a correct day.")

    return city, month, day


def load_data(city, month, day):
    """Load data for the specified city and filter by month and day."""
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, and hour for analysis
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':
        month_index = ['january', 'february', 'march',
                       'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df

def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print("\n--- Popular Times of Travel ---")
    print("Most common month:", df['month'].mode()[0])
    print("Most common day:", df['day_of_week'].mode()[0])
    print("Most common hour:", df['hour'].mode()[0])
    print("-------------------------------")  # Added separator for clarity

def station_stats(df):
    """Display statistics on the most popular stations and trips."""
    print("\n--- Station Statistics ---")
    print("Most common start station:", df['Start Station'].mode()[0])
    print("Most common end station:", df['End Station'].mode()[0])

    # Renamed variable for clarity
    most_common_trip = (df['Start Station'] + " → " + df['End Station']).mode()[0]
    print("Most common trip:", most_common_trip)


def trip_duration_stats(df):
    """Display statistics on total and average trip duration."""
    print("\n--- Trip Duration Statistics ---")
    print("Total trip duration (seconds):", df['Trip Duration'].sum())
    print("Average trip duration (seconds):", df['Trip Duration'].mean())


def user_stats(df, city):
    """Display statistics on bikeshare users."""
    print("\n--- User Statistics ---")
    print("User types:\n", df['User Type'].value_counts())

    if city in ['chicago', 'new york city']:
        if 'Gender' in df.columns:
            print("\nGender counts:\n", df['Gender'].value_counts())

        if 'Birth Year' in df.columns:
            print("Oldest birth year:", int(df['Birth Year'].min()))
            print("Most recent birth year:", int(df['Birth Year'].max()))
            print("Most common birth year:", int(df['Birth Year'].mode()[0]))


def display_raw_data(df):
    """Display raw data in increments of 5 rows upon request."""
    index = 0
    while True:
        show = input("\nDo you want to see 5 rows of raw data? (yes/no): ").lower()
        if show != 'yes':
            break

        print(df.iloc[index:index + 5])
        index += 5

        if index >= len(df):
            print("No more data to display.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input("\nDo you want to restart? (yes/no): ").lower()
        if restart != 'yes':
            print("Thank you for using Bikeshare!")
            break


if __name__ == "__main__":
    main()