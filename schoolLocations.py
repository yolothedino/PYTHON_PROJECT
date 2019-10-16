import pandas as pd
from geopy.distance import geodesic

# importing CSV files
sch_data = pd.read_csv('general-information-of-schools.csv', usecols=['school_name', 'postal_code', 'zone_code',
                                                                      'mainlevel_code'])
cords_data = pd.read_csv("geonames-coordinates.csv", usecols=['postal_code', 'Latitude', 'Longitude'])
cca_data = pd.read_csv("co-curricular-activities-ccas.csv", usecols=['school_name', 'cca_grouping_desc',
                                                                 'cca_generic_name'])
subjects_data = pd.read_csv("subjects-offered.csv", usecols=['school_name', 'subject_desc'])

# joining some columns and rows together
# cca_data_grouped = cca_data.groupby(['school_name', 'cca_grouping_desc'])['cca_generic_name'].apply(', '.join).reset_index()
# cca_data_all = cca_data_grouped.groupby(['school_name'])['cca_generic_name'].apply(', '.join).reset_index()
# cca_data_groups = cca_data_grouped.groupby(['school_name'])['cca_grouping_desc'].apply(', '.join).reset_index()
# subjects_data = subjects_data.groupby(['school_name'])['subject_desc'].apply(', '.join).reset_index()

# combining data to main data
sch_data = sch_data.merge(cords_data, on="postal_code", how='left').fillna(0)  # adds coordinates to main data
# sch_data = sch_data.merge(subjects_data, on="school_name", how='left').fillna(0)  # adds subjects to main data
# sch_data = sch_data.merge(cca_data_groups, on="school_name", how='left').fillna(0)  # adds cca groups to main data
# sch_data = sch_data.merge(cca_data_all, on="school_name", how='left').fillna(0)  # adds actual ccas to main data


def cords_from_name(*sch_name):
    """
    Getting coordinates with school name
    Used only for postal codes in Singapore
    Returns tuple(s) in the form of (latitude, longitude)
    """
    cords = []
    for i in sch_name:
        for j in i: #dont ask me why but it only works in a double loop
            index_no = sch_data[sch_data['school_name'] == j].index.item()
            lat = sch_data.loc[index_no, "Latitude"]
            lon = sch_data.loc[index_no, "Longitude"]
            cord_tuple = (float(lat),float(lon))
            cords.append(cord_tuple)
    return cords


def cords_from_postal(p_code):
    """
    Getting coordinates with postal code
    Used for only postal codes in Singapore
    Returns a list in the form of [longitude, latitude]
    """
    index_no = cords_data[cords_data['postal_code'] == p_code].index.item()
    lat = cords_data.loc[index_no, "Latitude"]
    lon = cords_data.loc[index_no, "Longitude"]
    return [float(lat), float(lon)]

def distance_calc(p_code_start, p_code_end):
    """
    Returns distance from home
    Takes in start and end postal codes
    """
    start = cords_from_postal(p_code_start)
    end = cords_from_postal(p_code_end)
    distance = geodesic(start, end).km
    return distance

def distance_calc_all(start_code):
    """
    Updates main dataframe with distance to all schools as new column
    """
    closest_up = start_code
    closest_down = start_code
    while start_code not in list(cords_data['postal_code']): #uses next closest available postal code
        closest_up += 1
        closest_down -= 1
        if closest_up in list(cords_data['postal_code']):
            start_code = closest_up
        elif closest_down in list(cords_data['postal_code']):
            start_code = closest_down
    print start_code
    distances_postal_codes = list(sch_data['postal_code'].values)
    distances = []
    for i in distances_postal_codes:
        distances.append(distance_calc(start_code, int(i)))
    sch_data['distances']=distances


def filter_distance(max_distance):
    """
    based on max_distance (in km), calculate schools that are within radius
    returns sorted values in (dataframe, list of schools, list of distances)
    """
    is_max_dis = sch_data['distances'] <= max_distance
    filtered_data = sch_data[is_max_dis].sort_values('distances')
    filtered_data = filtered_data.reset_index(drop=True)
    return filtered_data, list(filtered_data['school_name']), list(filtered_data.round(2)['distances'])


all_cords = cords_from_name(sch_data['school_name'])
