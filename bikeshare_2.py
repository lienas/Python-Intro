import time
import pandas as pd


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """Ask user to specify a city, month, and day."""
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("Enter city name (chicago, new york city, washington): ")
    while city not in CITY_DATA:
        city = input("Invalid city: ")

    month = input("Enter month name (all, january, february, ... , june): ")
    months = ['all', 'january', 'february', 'march', 'april',
              'may', 'june']
    while month not in months:
        month = input("Invalid month: ")

    day = input("Enter day of week (all, monday, tuesday, ... , sunday): ")
    days = ['all', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    while day not in days:
        day = input("Invalid day: ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for city and filter by month and day."""
    df = pd.read_csv(CITY_DATA[city])

    start_time = pd.to_datetime(df['Start Time'])
    df['month'] = start_time.dt.month_name().str.lower()
    df['day_of_week'] = start_time.dt.day_name().str.lower()
    df['hour'] = start_time.dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Display statistics on most frequent times of travel."""
    print('\nCalculating Most Frequent Times of Travel...\n')
    start_time = time.time()

    print(f'Most common month: {df["month"].mode()[0]}')
    print(f'Most common day: {df["day_of_week"].mode()[0]}')
    print(f'Most common hour: {df["hour"].mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display statistics on most popular stations and trip."""
    print('\nCalculating Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most common start station:',
          df['Start Station'].mode()[0])
    print('Most common end station:',
          df['End Station'].mode()[0])

    combo = df.groupby(['Start Station',
                        'End Station']).size().idxmax()
    print('Most common start/end combination:', combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total = df['Trip Duration'].sum()
    d = int(total // 86400)
    h = int((total % 86400) // 3600)
    m = int((total % 3600) // 60)
    s = int(total % 60)
    print(f'Total: {d}d {h}h {m}m {s}s')

    mean = df['Trip Duration'].mean()
    d = int(mean // 86400)
    h = int((mean % 86400) // 3600)
    m = int((mean % 3600) // 60)
    s = int(mean % 60)
    print(f'Mean: {d}d {h}h {m}m {s}s')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(f'User types:\n{user_types}')
    print('-'*40)

    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(f'Gender:\n{gender}')
        print('-'*40)
    else:
        print('Gender data not available')

    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])

        print('Birth year stats')
        print('-'*20)
        print(f'Earliest: {earliest}')
        print(f'Most recent: {recent}')
        print(f'Most common: {common}')
    else:
        print('Birth year data not available')

    print('-'*40)

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

        restart = input('\nRestart? Enter yes/no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
