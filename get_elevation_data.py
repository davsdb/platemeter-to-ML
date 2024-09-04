import requests
import time

def get_elevation(dataframe):
    """
    Retrieves elevation data for each location in the dataframe using an external API.

    Args:
        dataframe (pd.DataFrame): DataFrame containing 'Longitude' and 'Latitude' columns.

    Returns:
        pd.DataFrame: DataFrame with an additional 'Elevation' column.
    """
    elevation_list = []

    for _, row in dataframe.iterrows():
        lon, lat = row["Longitude"], row["Latitude"]
        url = f"https://api.opentopodata.org/v1/eudem25m?locations={lat},{lon}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            elevation = data["results"][0]["elevation"]
            elevation_list.append(elevation)
        
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            elevation_list.append(None)
        
        time.sleep(1)  # rate limit handling

    dataframe["Elevation"] = elevation_list
    return dataframe