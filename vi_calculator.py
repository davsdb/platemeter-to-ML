def compute_NDVI(row):
    """
    Computes the Normalized Difference Vegetation Index (NDVI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: NDVI value.
    """
    try:
        ndvi = (row["B08"] - row["B04"]) / (row["B08"] + row["B04"])
    except ZeroDivisionError:
        ndvi = float("nan")
    return ndvi

def compute_NDWI(row):
    """
    Computes the Normalized Difference Water Index (NDWI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: NDWI value.
    """
    try:
        ndwi = (row["B08"] - row["B11"]) / (row["B08"] + row["B11"])
    except ZeroDivisionError:
        ndwi = float("nan")
    return ndwi

def compute_EVI(row):
    """
    Computes the Enhanced Vegetation Index (EVI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: EVI value.
    """
    try:
        evi = 2.5 * (row["B08"] - row["B04"]) / ((row["B08"] + 6 * row["B04"] - 7.5 * row["B02"]) + 1)
    except ZeroDivisionError:
        evi = float("nan")
    return evi

def compute_GLI(row):
    """
    Computes the Green Leaf Index (GLI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: GLI value.
    """
    try:
        gli = (2 * row["B03"] - row["B04"] - row["B02"]) / (2 * row["B03"] + row["B04"] + row["B02"])
    except ZeroDivisionError:
        gli = float("nan")
    return gli

def compute_SAVI(row):
    """
    Computes the Soil Adjusted Vegetation Index (SAVI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: SAVI value.
    """
    try:
        savi = (row["B08"] - row["B04"]) / (row["B08"] + row["B04"] + 0.725) * (1 + 0.725)
    except ZeroDivisionError:
        savi = float("nan")
    return savi

def compute_GCI(row):
    """
    Computes the Green Chlorophyll Index (GCI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: GCI value.
    """
    try:
        gci = (row["B08"] / row["B03"]) - 1
    except ZeroDivisionError:
        gci = float("nan")
    return gci

def compute_RGR(row):
    """
    Computes the Red-Green Ratio (RGR).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: RGR value.
    """
    try:
        rgr = row["B04"] / row["B03"]
    except ZeroDivisionError:
        rgr = float("nan")
    return rgr

def compute_SIPI(row):
    """
    Computes the Soil-Adjusted Vegetation Index (SIPI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: SIPI value.
    """
    try:
        sipi = (row["B08"] - row["B02"]) / (row["B08"] - row["B04"])
    except ZeroDivisionError:
        sipi = float("nan")
    return sipi

def compute_ARVI(row):
    """
    Computes the Atmospherically Resistant Vegetation Index (ARVI).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: ARVI value.
    """
    try:
        arvi = (row["B8A"] - row["B04"] - 0.069 * (row["B04"] - row["B02"])) / (row["B8A"] + row["B04"] - 0.069 * (row["B04"] - row["B02"]))
    except ZeroDivisionError:
        arvi = float("nan")
    return arvi

def compute_NBR(row):
    """
    Computes the Normalized Burn Ratio (NBR).

    Args:
        row (pd.Series): Row of a dataframe containing the necessary band values.

    Returns:
        float: NBR value.
    """
    try:
        nbr = (row["B08"] - row["B12"]) / (row["B08"] + row["B12"])
    except ZeroDivisionError:
        nbr = float("nan")
    return nbr