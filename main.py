import rasterio
import pandas as pd
from datetime import datetime
from get_sentinel2_imgs import get_image
from spatial_to_pixels_converter import coordinates_to_pixels
from vi_calculator import *
from get_elevation_data import get_elevation
from get_seasons import get_season
import os
import warnings
warnings.filterwarnings("ignore")

def main():
    if not os.path.exists("input_files/input.csv"):
        raise FileNotFoundError("The CSV file 'input.csv' does not exist, quit...")

    print("Reading CSV file...")
    df_initial = pd.read_csv("input_files/input.csv")
    print("CSV file successfully read.\n")

    df_initial["ReadingDateTime"] = pd.to_datetime(df_initial["ReadingDateTime"], format = "%d/%m/%Y %H:%M:%S")
    df_initial["ReadingDate"] = df_initial["ReadingDateTime"].dt.strftime("%Y-%m-%d")

    b02, b03, b04, b05, b06 = [], [], [], [], []
    b07, b08, b8a, b11, b12 = [], [], [], [], []

    df_satellite = pd.DataFrame()

    for farm in df_initial["FarmName"].unique():
        df_farm = df_initial[df_initial["FarmName"] == farm]

        print(f"Retrieving images for farm {farm}, please wait...\n")

        try:
            print(f"Removing invalid coordinate values for farm {farm} (if any), please wait...")
            columns_to_check = ["Longitude", "Latitude"]
            df_farm = df_farm.loc[(df_farm[columns_to_check] > 0).all(axis = 1)]
            df_farm = df_farm.loc[(df_farm[columns_to_check] != None).all(axis = 1)]
            print("Done.\n")

            lng_min = round(df_farm["Longitude"].min(), 6)
            lng_max = round(df_farm["Longitude"].max(), 6)
            lat_min = round(df_farm["Latitude"].min(), 6)
            lat_max = round(df_farm["Latitude"].max(), 6)

        except (TypeError, AttributeError) as e:
            print(f"Error with coordinate data type: {e}, converting to float...")
            df_farm["Longitude"] = df_farm["Longitude"].str.replace(",", ".").astype(float)
            df_farm["Latitude"] = df_farm["Latitude"].str.replace(",", ".").astype(float)
            print("Done.\n")

            print(f"Removing invalid coordinate values for farm {farm} (if any), please wait...")
            columns_to_check = ["Longitude", "Latitude"]
            df_farm = df_farm.loc[(df_farm[columns_to_check] > 0).all(axis = 1)]
            df_farm = df_farm.loc[(df_farm[columns_to_check] != None).all(axis = 1)]
            print("Done.\n")

            lng_min = round(df_farm["Longitude"].min(), 6)
            lng_max = round(df_farm["Longitude"].max(), 6)
            lat_min = round(df_farm["Latitude"].min(), 6)
            lat_max = round(df_farm["Latitude"].max(), 6)

        coords = (
            lng_min - 0.000001,
            lat_min - 0.000001,
            lng_max + 0.000001,
            lat_max + 0.000001
        )

        for sampling_date in df_farm["ReadingDate"].unique():
            img = get_image(30, sampling_date, coords)

            with rasterio.open(img) as src:
                df_pixels_indexes = coordinates_to_pixels(
                    df_farm[df_farm["ReadingDate"] == sampling_date],
                    src
                )

                for band in range(1, 11):
                    band_data = src.read(band)
                    for pixel_index in df_pixels_indexes["PixelsIndexes"]:
                        if band == 1:
                            b02.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 2:
                            b03.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 3:
                            b04.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 4:
                            b05.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 5:
                            b06.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 6:
                            b07.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 7:
                            b08.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 8:
                            b8a.append(band_data[pixel_index[0], pixel_index[1]])
                        elif band == 9:
                            b11.append(band_data[pixel_index[0], pixel_index[1]])
                        else:
                            b12.append(band_data[pixel_index[0], pixel_index[1]])

            df_pixels_indexes["B02"] = b02
            df_pixels_indexes["B03"] = b03
            df_pixels_indexes["B04"] = b04
            df_pixels_indexes["B05"] = b05
            df_pixels_indexes["B06"] = b06
            df_pixels_indexes["B07"] = b07
            df_pixels_indexes["B08"] = b08
            df_pixels_indexes["B8A"] = b8a
            df_pixels_indexes["B11"] = b11
            df_pixels_indexes["B12"] = b12

            df_satellite = pd.concat([df_satellite, df_pixels_indexes], ignore_index = True)

            b02.clear()
            b03.clear()
            b04.clear()
            b05.clear()
            b06.clear()
            b07.clear()
            b08.clear()
            b8a.clear()
            b11.clear()
            b12.clear()

            print(f"Images for farm {farm} successfully retrieved!\n")

    print("Computing vegetation indexes in progress, please wait...")

    df_satellite["NDVI"] = df_satellite.apply(compute_NDVI, axis = 1)
    df_satellite["NDWI"] = df_satellite.apply(compute_NDWI, axis = 1)
    df_satellite["SAVI"] = df_satellite.apply(compute_SAVI, axis = 1)
    df_satellite["SIPI"] = df_satellite.apply(compute_SIPI, axis = 1)
    df_satellite["ARVI"] = df_satellite.apply(compute_ARVI, axis = 1)

    df_satellite["NBR"] = df_satellite.apply(compute_NBR, axis = 1)
    df_satellite["EVI"] = df_satellite.apply(compute_EVI, axis = 1)
    df_satellite["GLI"] = df_satellite.apply(compute_GLI, axis = 1)
    df_satellite["GCI"] = df_satellite.apply(compute_GCI, axis = 1)
    df_satellite["RGR"] = df_satellite.apply(compute_RGR, axis = 1)

    print("Done.\n")
    print("Retrieving elevation data, please wait...")

    df_complete = get_elevation(df_satellite)
    df_complete.drop(columns = "PixelsIndexes", inplace = True)

    print("Elevation data retrieved.\n")
    print("Determining seasons, please wait...")

    df_complete["ReadingDate"] = pd.to_datetime(df_complete["ReadingDate"], format = "%Y-%m-%d")
    df_complete["Season"] = df_complete["ReadingDate"].apply(get_season)

    print("Seasons determined.\n")

    try:
        os.mkdir("output_files")
        print("Folder 'output_files' successfully created")
        
    except FileExistsError:
        print("Folder 'output_files' already exists, skip...")

    os.chdir("output_files")

    df_complete = df_complete[
        [
            "FarmName",
            "ReadingDateTime",
            "ReadingDate",
            "Latitude",
            "Longitude",
            "B02",
            "B03",
            "B04",
            "B05",
            "B06",
            "B07",
            "B08",
            "B8A",
            "B11",
            "B12",
            "NDVI",
            "NDWI",
            "SAVI",
            "SIPI",
            "ARVI",
            "NBR",
            "EVI",
            "GLI",
            "GCI",
            "RGR",
            "Elevation",
            "Season",
            "AverageDM"
        ]
    ]

    timestamp = datetime.now().strftime("%Y-%m-%d")
    df_complete.to_csv(f"output_{timestamp}.csv", index = False)

    print("CSV file successfully saved, end!")

if __name__ == "__main__":
    main()