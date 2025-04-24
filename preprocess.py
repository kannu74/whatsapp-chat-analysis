import re
import pandas as pd

def preprocess(data):
    # Define regex pattern for WhatsApp chat format
    pattern = r"(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}\s?[APM\u202F\u00A0]{2,3}) - ([^:]+): (.*)"

    # Find all matches
    matches = re.findall(pattern, data)
    
    # Convert matches into a DataFrame with correct column names
    df = pd.DataFrame(matches, columns=["Date", "Time", "Sender", "Message"])

    # Combine Date & Time into a single DateTime column
    df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%m/%d/%y %I:%M %p")

    # Reorder and drop old Date & Time columns
    df = df[["DateTime", "Sender", "Message"]]

    # Convert DateTime to 24-hour format
    df["DateTime"] = df["DateTime"].dt.strftime("%Y-%m-%d %H:%M") 

    # Convert DateTime back to datetime type
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%Y-%m-%d %H:%M")

    # Extracting date & time components
    df['year'] = df['DateTime'].dt.year
    df['month'] = df['DateTime'].dt.month_name()
    df['day'] = df['DateTime'].dt.day
    df['hour'] = df['DateTime'].dt.hour
    df['minute'] = df['DateTime'].dt.minute
    df['month_num'] = df['DateTime'].dt.month
    df['date'] = df['DateTime'].dt.date
    df['day_name'] = df['DateTime'].dt.day_name()
    
    # Create a period column in 24-hour format
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-{0}")
        elif hour == 0:
            period.append(f"{0}-{hour + 1}")
        else:
            period.append(f"{hour}-{hour + 1}")
    df['period'] = period
    
    return df