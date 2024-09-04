import io
import os
import requests
from datetime import datetime, timedelta
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from sentinelhub.constants import CRS
from sentinelhub.geometry import BBox
from sentinelhub.geo_utils import bbox_to_dimensions

def get_image(cloud_coverage, sampling_date, coords):
    """
    Retrieves Sentinel-2 imagery from Sentinel Hub API.

    Args:
        cloud_coverage (int): Maximum cloud coverage percentage.
        sampling_date (str): The date of the image in YYYY-MM-DD format.
        coords (tuple): Bounding box coordinates (lon_min, lat_min, lon_max, lat_max).

    Returns:
        io.BytesIO: Image data as a BytesIO object if successful, None otherwise.
    """
    
    # Compute date range
    sampling_date_from = datetime.strptime(sampling_date, "%Y-%m-%d") - timedelta(days=10) # ten days behind the sampling date
    sampling_date_from = sampling_date_from.strftime("%Y-%m-%d")
    sampling_date_to = sampling_date

    # Define bounding box and image size
    bbox = BBox(bbox=coords, crs=CRS.WGS84)
    resolution = 20
    size = bbox_to_dimensions(bbox, resolution=resolution)

    # Get OAuth2 token
    client_id = os.getenv("SENTINEL_CLIENT_ID")
    client_secret = os.getenv("SENTINEL_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("Client and Secret IDs must be set in environment variables.")

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(
        token_url="https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        client_secret=client_secret,
        include_client_id=True
    )

    # Define the evalscript
    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12"],
                units: "REFLECTANCE"
            }],
            output: {
                bands: 10,
                sampleType: "FLOAT32"
            },
            mosaicking: "SIMPLE"
        };
    }

    function evaluatePixel(sample) {
        return [sample.B02,
                sample.B03,
                sample.B04,
                sample.B05,
                sample.B06,
                sample.B07,
                sample.B08,
                sample.B8A,
                sample.B11,
                sample.B12];
    }
    """

    # Prepare the request
    request = {
        "input": {
            "bounds": {
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
                "bbox": coords
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "mosaickingOrder": "leastCC", # lowest cloud cover image available
                        "maxCloudCoverage": cloud_coverage,
                        "timeRange": {
                            "from": f"{sampling_date_from}T00:00:00Z",
                            "to": f"{sampling_date_to}T23:59:00Z",
                        }
                    },
                }
            ],
        },
        "output": {
            "width": size[0],
            "height": size[1],
            "responses": [
                {
                    "identifier": "default",
                    "format": {"type": "image/tiff"},
                }
            ],
        },
        "evalscript": evalscript,
    }

    url = "https://sh.dataspace.copernicus.eu/api/v1/process"
    
    try:
        response = oauth.post(url, json=request)
        response.raise_for_status()

        img = io.BytesIO(response.content)
        return img

    except requests.RequestException as e:
        print(f"Request failed: {e}")