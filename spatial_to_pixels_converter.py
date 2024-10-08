def coordinates_to_pixels(dataframe, raster):
    """
    Converts geographical coordinates (longitude, latitude) to pixels indexes in a raster image.

    Args:
        dataframe (pd.DataFrame): DataFrame containing "Longitude" and "Latitude" columns.
        raster (rasterio.DatasetReader): Rasterio dataset object for the raster image.

    Returns:
        pd.DataFrame: Original DataFrame with an additional "PixelsIndexes" column containing raster image-related pixels indexes.
    """

    if not {"Longitude", "Latitude"}.issubset(dataframe.columns):
        raise ValueError("Dataframe must contain 'Longitude' and 'Latitude' columns.")

    def convert_to_pixel(row):
        return raster.index(row["Longitude"], row["Latitude"])

    dataframe["PixelsIndexes"] = dataframe.apply(lambda row: convert_to_pixel(row), axis = 1)
    
    return dataframe