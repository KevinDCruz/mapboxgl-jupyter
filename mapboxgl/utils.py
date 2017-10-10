import geojson

def df_to_geojson(df, properties=None, lat='lat', lon='lon', precision=None):
    """Serialize a Pandas dataframe to a geojson format Python dictionary
    """
    lat = df[lat]
    lon = df[lon]
    if precision:
        lat = lat.round(precision)
        lon = lon.round(precision)

    if properties is None: # allow empty properties list
        properties = list(df.columns)

    features = []
    for idx, row in df.iterrows():
        f = geojson.Feature(geometry=geojson.Point((lon[idx],lat[idx])),
                            properties={prop: row[prop] for prop in properties})
        features.append(f)
    fc = geojson.FeatureCollection(features)
    return fc

def scale_between(minval, maxval, numStops):
    """ Scale a min and max value to equal interval domain with 
        numStops discrete values
    """

    scale = []

    if numStops < 2:
        return [minval, maxval]
    elif maxval < minval:
        raise ValueError()
    else:
        domain = maxval - minval
        interval = domain/numStops
        for i in range(numStops):
            scale.append(round(minval + interval*i, 2))
        return scale


def create_radius_stops(breaks, min_radius, max_radius):
    """Convert a data breaks into a radius ramp
    """
    num_breaks = len(breaks)
    radius_breaks = scale_between(min_radius, max_radius, num_breaks)
    stops = []

    for i, b in enumerate(breaks):
        stops.append([b, radius_breaks[i]])
    return stops