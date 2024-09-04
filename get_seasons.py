from datetime import datetime

def get_season(date):
    """
    Determine the season of the year for a given date.
    
    Args:
        date (datetime): The date to determine the season for.
    
    Returns:
        str or None: The season name ('spring', 'summer', 'autumn', or 'winter') or None if not determined.
    """

    year = date.year
    
    seasons = {
        "spring" : (
            datetime(year, 3, 21),
            datetime(year, 6, 20)
        ),
        "summer" : (
            datetime(year, 6, 21),
            datetime(year, 9, 22)
        ),
        "autumn" : (
            datetime(year, 9, 23),
            datetime(year, 12, 20)
        )
    }

    for season, (start, end) in seasons.items():
        if start <= date <= end:
            return season
    
    if date >= datetime(year, 12, 21) or date <= datetime(year, 3, 20):
        return "winter"
    
    return None