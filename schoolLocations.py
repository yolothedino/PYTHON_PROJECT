"""
Main dictionary can be accessed with:
sch_data_dict
Keys: School Names
[0]: Postal Code
[1]: Latitude
[2]: Longitude
[3]: Distance to input postal code (default 0)
[4]: Whether school is near (default True)
Call distance_calc_all(<postal code of home>) to update [3]
Call is_it_near(<max distance>) to update [4] (only after updating [3])
    is_it_near(<max distance)[0] returns list sorted school's distances
    is_it_near(<max distance)[1] returns list of schools sorted by their distances
"""
import pandas as pd
from geopy.distance import geodesic

# importing CSV files
sch_data = pd.read_csv('general-information-of-schools.csv', usecols=['school_name', 'postal_code', 'zone_code',
                                                                      'mainlevel_code'])
cords_data = pd.read_csv("geonames-coordinates.csv", usecols=['postal_code', 'Latitude', 'Longitude'])
cca_data = pd.read_csv("co-curricular-activities-ccas.csv", usecols=['school_name', 'cca_grouping_desc',
                                                                  'cca_generic_name'])

# joining some columns and rows together
cca_data = cca_data.groupby(['school_name'])['cca_generic_name'].apply(', '.join).reset_index()

# combining data to main data
sch_data = sch_data.merge(cords_data, on="postal_code", how='left').fillna(0)  # adds coordinates to main data

sch_data_dict = {}

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


def get_closest_pcode(pcode):
    """
    For when user's postal code is not in database, next closest available postal code is used
    """
    code = pcode
    closest_up = pcode
    closest_down = pcode
    while code not in list(cords_data['postal_code']):  # uses next closest available postal code
        closest_up += 1
        closest_down -= 1
        if closest_up in list(cords_data['postal_code']):
            code = closest_up
        elif closest_down in list(cords_data['postal_code']):
            code = closest_down
    if pcode != code:
        print '{} not found, used next closest available postal code: {}'.format(pcode, code)
    return code


def distance_calc_all(start_code):
    """
    Updates main dataframe with distance to all schools as new column
    """
    start_code = get_closest_pcode(start_code)
    for i in sch_data_dict:
        sch_data_dict[i][3] = round(geodesic(cords_from_postal(start_code),
                                             (sch_data_dict[i][1],sch_data_dict[i][2])).km, 2)


def is_it_near(max_distance):
    """
    Changes a boolean value of dictionary if to indicate if the school is
    near/far from a postal code based on a given maximum distance
    """
    sch_list = []
    dist_list = []
    if max_distance > 0:
        for i in sch_data_dict:
            if sch_data_dict[i][3] <= max_distance:
                sch_data_dict[i][4] = True
                sch_list.append(i)
                dist_list.append(sch_data_dict[i][3])
            elif sch_data_dict[i][3] > max_distance:
                sch_data_dict[i][4] = False
    elif max_distance == 0:
        for i in sch_data_dict:
            sch_data_dict[i][4] = False
    to_return = sort_two_lists_2gd(dist_list,sch_list)
    return to_return[0], to_return[1]

def sort_two_lists_2gd(values,names):
    counter = 0
    while counter < len(values)-1:
        counter = 0
        for i in range(len(values)-1):
            if values[i]>values[i+1]:
                temp1 = values[i]
                temp2 = values[i+1]
                tempa = names[i]
                tempb = names[i+1]
                values[i] = temp2
                values[i+1] = temp1
                names[i] = tempb
                names[i+1] = tempa
            else:
                counter += 1
    return values, names


#   Creating a dictionary with school name as key, with postal code and coordinates as values
sch_data_sch_name = sch_data['school_name'].to_list()
sch_data_pcode = sch_data['postal_code'].to_list()
sch_data_lat = sch_data['Latitude'].to_list()
sch_data_lon = sch_data['Longitude'].to_list()
for i in range(len(sch_data_sch_name)):
    sch_data_dict[sch_data_sch_name[i]] = [int(sch_data_pcode[i]), float(sch_data_lat[i]), float(sch_data_lon[i]),
                                           float(0),True]

#   Creating a dictionary with school name as key, with CCA generic names as list
sch_cca_names = cca_data['school_name'].to_list()
sch_cca_ccas = cca_data['cca_generic_name'].to_list()
sch_ccas = {}
for i in range(len(sch_cca_names)):
    sch_ccas[sch_cca_names[i]] = sch_cca_ccas[i].split(', ')
    for x in range(len(sch_ccas[sch_cca_names[i]])):
        if sch_ccas[sch_cca_names[i]][x] == 'MUSIC':
            sch_ccas[sch_cca_names[i]][x] = 'MUSIC, DRAMA & DANCE CLUB'
        elif sch_ccas[sch_cca_names[i]][x] == 'DRAMA & DANCE CLUB':
            sch_ccas[sch_cca_names[i]][x] = ''
    sch_ccas[sch_cca_names[i]] = [x for x in sch_ccas[sch_cca_names[i]] if not '']
