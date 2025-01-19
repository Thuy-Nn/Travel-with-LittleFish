def iso8601_to_minutes(iso_time):
    hours = 0
    minutes = 0

    # Check if the string starts with 'PT' (ISO 8601 duration format)
    if iso_time.startswith('PT'):
        # Remove the 'PT' prefix
        duration = iso_time[2:]

        # Split into hours and minutes
        if 'H' in duration:
            hours_part, duration = duration.split('H')
            hours = int(hours_part)

        if 'M' in duration:
            minutes_part = duration.replace('M', '')
            minutes = int(minutes_part)

    # Convert to total minutes
    total_minutes = hours * 60 + minutes
    return total_minutes


if __name__ == '__main__':
    d = 'PT1H50M'
    print(iso8601_to_minutes(d))