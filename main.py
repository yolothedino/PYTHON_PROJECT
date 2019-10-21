from kivy.app import App
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.utils import rgba
import csv
import os
from functools import partial

Config.set('graphics', 'window_state', 'maximized')
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
import schoolLocations as locPin
import pandas

load_count = 0
general_info_count = 0
general_info_dict = {}
favorites_dict = {}
cca_offeredAll = {}
ccaList = list()
nearSchool_dict = {}
ccas = locPin.sch_ccas
cords = locPin.sch_data_dict        # Next three lines is for map markers
map_layer = False
marker_layer = MarkerMapLayer()
predict_count = 0
imported_file = ''
after_import_status = False
error_msg = ''


def predict_count_reset(x):
    global predict_count
    predict_count = 0


dropdown = DropDown(on_dismiss=predict_count_reset)

isViewingFavorites = False

# reading info from general info csv and storing in dictionary
with open('general-information-of-schools.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if general_info_count == 0:
            general_info_count += 1
        else:
            general_info_dict[row[0]] = [row[1], row[2], row[3], row[4], row[6], row[8], row[9], row[10], row[11],
                                         row[18], row[19], row[20], row[22], row[24], row[25], row[26], row[27],
                                         row[32], row[33], row[34], 0.0, 'is_near', 'ccas']
# updating main dict with CCAs [22]
for i in general_info_dict:
    if i in ccas:
        general_info_dict[i][22] = ccas[i][0]
    else:
        general_info_dict[i][22] = ["Missing CCAs"]

# below codes adds all CCAs from a school to a school/cca dictionary
recordcnt = 0
filename = "co-curricular-activities-ccas.csv"
infile = open(filename, "r")
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file)
    for data in csv_reader:
        if data[0] != 'school_name':  # ignores the header row
            recordcnt += 1
            if data[0] in cca_offeredAll.keys():  # Checking if the School is inside the Dictionary Already
                cca_offeredAll[data[0]].append(data[3])  # If yes, append the new CCA to the List
            else:
                cca_offeredAll[data[0]] = [data[3]]  # If not, create a new Key and assign the CCA as a List to it

            if data[3] not in ccaList:  # check if CCA exist in list of all CCAs
                ccaList.append(data[3])  # if it doesn't exist yet, add to it. if it exists, then ignore.

infile.close


# now, dictionary  of every CCA offered by each school is populated
# and list of every single CCA is also made

def update_distances():
    # updating main dict with distances [20] and whether is_near [21]
    for i in general_info_dict:
        if i in cords:
            general_info_dict[i][20] = cords[i][3]
            general_info_dict[i][21] = cords[i][4]
        else:
            general_info_dict[i][20] = 0.0
            general_info_dict[i][21] = False
def reset_distances():
    # resets distances of schools in main dict
    for i in general_info_dict:
        general_info_dict[i][20] = 0.0
        general_info_dict[i][21] = False

# 0[key]:school name 1[0]:website 2[1]:address 3[2]:postal code 4[3]:telephone 6[4]:Fax 8[5]:email 9[6]:mrt 10[7]:bus
# 11[8]:principal 18[9]:vision 19[10]:mission 20[11]:philosophy 22[12]:region 24[13]:school type 25[14]:school nature
# 26[15]:session type 27[16]:education level 32[17]:mother tongue1 33[18]:mother tongue2 34[19]:mother tongue3
# [20]:distances [21]:is_near [22]:CCAs

# classes used for file picker


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)

# /classes used for file picker


class RootWidget(AnchorLayout):
    # variables used by file picker
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    # /variables used by file picker

    # functions used by file picker

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, x):
        # import file popup gui
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.5, 0.7))
        self._popup.open()

    def show_save(self, x):
        # save file popup gui
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.5, 0.7))
        self._popup.open()

    def load(self, path, filename):
        global isViewingFavorites
        global after_import_status
        global imported_file
        global error_msg
        if bool(filename):
            try:
                imported_file = os.path.join(path, filename[0])
                with open(imported_file) as csvfile:
                    load_reader = csv.reader(csvfile)
                    for row in load_reader:
                        favorites_dict[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                                  row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17],
                                                  row[18], row[19], row[20], row[21], row[22], row[23]]
                self.dismiss_popup()
                isViewingFavorites = False
                after_import_status = True
                self.import_popup.dismiss()
                self.viewFavoritesList()
            except IOError as msg:
                error_msg = msg
                self.error_popup()

    def save(self, path, filename):
        global imported_file
        global error_msg
        if bool(filename):
            try:
                filename += '.csv'
                imported_file = os.path.join(path, filename)
                save_csv = open(imported_file, 'w') # creates empty favourite.csv to save in
                save_csv.close()
                self.dismiss_popup()
                self.import_popup.dismiss()
            except IOError as msg:
                error_msg = msg
                self.error_popup()
    # /functions used by file picker

    def on_load(self):
        global load_count
        if load_count == 0:
            self.scroll_view_load()
            self.txtsearch.bind(text=self.on_text)
            load_count += 1

    def enableDistanceFilter(self):

        if self.pcode.disabled:
            # if distance filter is currently toggled off, clicking it will enable all relevant controls
            # and disable irrelevant controls
            self.pcode.disabled = False
            self.radius.disabled = False
            self.txtsearch.disabled = True
            self.txtsearch.text = ""
            self.btn_viewFav.disabled = True
        else:
            # if distance filter is currently toggled on, clicking it again will disable all relevant controls
            # and enable other controls
            # also resets distances to 0.0
            self.pcode.disabled = True
            self.radius.disabled = True
            self.pcode.text = ""
            self.radius.text = ""
            self.txtsearch.disabled = False
            self.btn_viewFav.disabled = False
            locPin.is_it_near(0)
            reset_distances()

    def on_text(self, instance, x):
        global predict_count
        dropdown.clear_widgets()
        if self.txtsearch.text != '':
            autosuggestschool = filter(lambda x: x.startswith(self.txtsearch.text.upper()), general_info_dict.keys())
            if len(autosuggestschool) > 0:
                for a in autosuggestschool:
                    btn = Button(text=a, size_hint_y=None, height=44)
                    btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                    dropdown.add_widget(btn)
                dropdown.bind(on_select=lambda instance, x: setattr(self.txtsearch, 'text', x))
                dropdown.bind(on_select=self.test)
                if predict_count == 0:
                    dropdown.open(instance)
                    predict_count += 1
        else:
            self.scroll_view_load()

    def test(self, x, y):
        self.scroll_view_load()

    def scroll_view_load(self):
        # Updates mapview maplayer each time function is called
        global map_layer
        global marker_layer
        if map_layer is True:
            marker_layer.unload()
        elif map_layer is False:
            self.guimap.add_layer(marker_layer)
            map_layer = True
        results_count = 0
        self.menu_scroll.clear_widgets()
        gridlayout = GridLayout(cols=1, spacing=20, size_hint_y=None)
        gridlayout.bind(minimum_height=gridlayout.setter('height'))
        # Updates widgets (textboxes, buttons, etc)
        # When distance filter is not active
        if not self.isnear.active:
            for key, value in sorted(general_info_dict.iteritems()):
                if (value[16] == self.level_spinner.text or self.level_spinner.text == 'ALL') and \
                        (value[12] == self.region_spinner.text or self.region_spinner.text == 'ALL') and \
                        key.find(self.txtsearch.text.upper()) is not -1:
                    # value[16] = school level (e.g primary, secondary, etc), value[12] = north/south/east/west,
                    # "key.find(self.txtsearch.text)" checks if the string search text is a substring of a school's
                    # name and returns -1 if false
                    # a school that fulfills all three parameters will stay in the filtered list
                    self.guimap.add_marker(MapMarker(lat=cords[key][1], lon=cords[key][2]))
                    box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=-3)
                    btn_school = Button(text=key)
                    btn_school.disabled = True
                    btn_school.disabled_color = rgba('#000000')
                    btn_distance = Button(text=str(general_info_dict[key][20]) + " km away")
                    btn_distance.disabled = True
                    btn_distance.disabled_color = rgba('#000000')
                    btn_details = Button(text='View Details', on_release=partial(self.view_details_popup, key))
                    btn_view = Button(text='Show on map', on_release=partial(self.showPinAndZoom, key))
                    box.add_widget(btn_school)
                    box.add_widget(btn_distance)
                    box.add_widget(btn_details)
                    box.add_widget(btn_view)
                    gridlayout.add_widget(box)
                    results_count += 1
        # When distance filter is active
        elif self.isnear.active:
            # same as previous if statement, but checks for more inputs
            if len(str(self.pcode.text)) == 6 and str(self.pcode.text).isdigit() is True:
                correct_code = locPin.get_closest_pcode(int(self.pcode.text))
                self.guimap.center_on(locPin.cords_from_postal(correct_code)[0],
                                      locPin.cords_from_postal(correct_code)[1])
                self.guimap.add_marker(MapMarker(lat=locPin.cords_from_postal(correct_code)[0],
                                                 lon=locPin.cords_from_postal(correct_code)[1]))
                locPin.distance_calc_all(int(self.pcode.text))
                if self.radius.text != "" and self.radius.text.isdigit() is True:
                    locPin.is_it_near((float(self.radius.text)))
                    update_distances()
                # mapview zoom based on maximum distance indicated
                if int(self.radius.text) < 3:
                    self.guimap.zoom = 15
                elif int(self.radius.text) < 5:
                    self.guimap.zoom = 14
                elif int(self.radius.text) < 8:
                    self.guimap.zoom = 13
                else:
                    self.guimap.zoom = 12
            # this loop is the same as the previous loop (when distance filter is not active)
            for key, value in sorted(general_info_dict.iteritems()):
                if (value[16] == self.level_spinner.text or self.level_spinner.text == 'ALL') and \
                        (value[12] == self.region_spinner.text or self.region_spinner.text == 'ALL') and \
                        value[21] == self.isnear.active:
                    # filter by school level AND school region
                    self.guimap.add_marker(MapMarker(lat=cords[key][1], lon=cords[key][2]))
                    box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=-3)
                    btn_school = Button(text=key)
                    btn_school.disabled = True
                    btn_school.disabled_color = rgba('#000000')
                    btn_distance = Button(text=str(general_info_dict[key][20]) + " km away")
                    btn_distance.disabled = True
                    btn_distance.disabled_color = rgba('#000000')
                    btn_details = Button(text='View Details', on_release=partial(self.view_details_popup, key))
                    btn_view = Button(text='Show on map', on_release=partial(self.showPinAndZoom, key))
                    box.add_widget(btn_school)
                    box.add_widget(btn_distance)
                    box.add_widget(btn_details)
                    box.add_widget(btn_view)
                    gridlayout.add_widget(box)
                    results_count += 1
        self.lbl_results_count.text = str(results_count) + ' schools match your criteria'
        self.menu_scroll.add_widget(gridlayout)

    def view_details_popup(self, key, x):
        popup = Popup(title=key, size_hint=(0.5, 0.8))
        if key in favorites_dict.keys():
            btnFavv = Button(
                text="Delete from Favourites",
                size_hint=(1, 0.1),
                on_release=partial(self.addToFavorites, key))
            btnFavv.bind(on_press=popup.dismiss)
        else:
            btnFavv = Button(
                text="Add to Favourites",
                size_hint=(1, 0.1),
                on_release=partial(self.addToFavorites, key))
            btnFavv.bind(on_press=popup.dismiss)
        ccaStrings = ""

        if key in cca_offeredAll.keys():
            for n in cca_offeredAll[key]:
                print n
                ccaStrings += n + ', '
        else:
            ccaStrings = "NO DATA AVAILABLE"

        lbl_school_info = Label(text='[size=40]' + '[b]' + key + '[/b]' + '[/size]' + '\n' + '\n'
                                     + '[size=20]' + '[b]' + 'GENERAL INFO' + '[/b]' + '[/size]' + '\n' + '\n'
                                     + 'Type of School' + '\n'
                                     + general_info_dict[key][12] + ' / ' + general_info_dict[key][13] + ' / ' +
                                     general_info_dict[key][14] + '\n' + '\n'
                                     + 'Mother Tongue' + '\n'
                                     + general_info_dict[key][17] + ' / ' + general_info_dict[key][18] + ' / ' +
                                     general_info_dict[key][19] + '\n' + '\n'
                                     + 'Principal' + '\n'
                                     + general_info_dict[key][8] + '\n' + '\n'
                                     + 'Vision' + '\n'
                                     + general_info_dict[key][9] + '\n' + '\n'
                                     + 'Mission' + '\n'
                                     + general_info_dict[key][10] + '\n' + '\n'
                                     + 'School Philosophy, Culture and Ethos' + '\n'
                                     + general_info_dict[key][11] + '\n' + '\n' + '\n' + '\n'
                                     + 'Co-Curricular Activities' + '\n'
                                     + ccaStrings + '\n' + '\n'
                                     # + cca_offeredAll[key] + '\n' + '\n'   #can't place list object into label
                                     + '[size=20]' + '[b]' + 'CONTACT' + '[/b]' + '[/size]' + '\n' + '\n'
                                     + 'Email' + '\n'
                                     + general_info_dict[key][5] + '\n' + '\n'
                                     + 'Address' + '\n'
                                     + general_info_dict[key][1] + ' (' + general_info_dict[key][2] + ')' + '\n' + '\n'
                                     + 'Telephone / Fax' + '\n'
                                     + general_info_dict[key][3] + ' / ' + general_info_dict[key][
                                         4] + '\n' + '\n' + '\n' + '\n'
                                     + '[size=20]' + '[b]' + 'GETTING THERE' + '[/b]' + '[/size]' + '\n' + '\n'
                                     + 'Nearest MRT' + '\n'
                                     + general_info_dict[key][6] + '\n' + '\n'
                                     + 'Bus Services' + '\n'
                                     + general_info_dict[key][7]
                                , markup=True, line_height=1.5, padding=(50, 50))
        lbl_school_info.bind(size=partial(self.details_popup_widget_sizing, lbl_school_info))
        scroll_view = ScrollView(scroll_wheel_distance=80, scroll_type=['bars', 'content'], bar_width=10)
        scroll_view.add_widget(lbl_school_info)

        box = BoxLayout(orientation='vertical', spacing=20)
        box.add_widget(scroll_view)
        box.add_widget(btnFavv)
        popup.add_widget(box)
        popup.open()

    def showPinAndZoom(self, key, x):
        self.guimap.center_on(cords[key][1], cords[key][2])
        self.guimap.zoom = 17

    def addToFavorites(self, key, x):
        global error_msg
        global imported_file
        if bool(imported_file) is False:
            self.viewFavoritesList()
        else:
            if key in favorites_dict.keys():
                try:
                    remove_csv = open(imported_file, 'w')
                    favorites_dict.pop(key, None)  # if already in list, remove
                    remove_csv.truncate()
                    # with open(imported_file, 'r+') as remove_file:
                    for key in favorites_dict.keys():
                        writer = csv.writer(remove_csv)
                        data = general_info_dict[key]
                        data.insert(0, key)
                        writer.writerow(data)
                    remove_csv.close()
                except IOError as msg:
                    error_msg = msg
                    self.error_popup()
            else:
                try:
                    with open(imported_file, 'a+') as myfile:
                        favorites_dict[key] = general_info_dict[key]  # adds the corresponding school to favorites list
                        wr = csv.writer(myfile)
                        data = general_info_dict[key]
                        data.insert(0, key)
                        wr.writerow(data)
                except IOError as msg:
                    error_msg = msg
                    self.error_popup()
            results_count = 0
            if isViewingFavorites is True:
                self.menu_scroll.clear_widgets()
                gridlayout = GridLayout(cols=1, spacing=20, size_hint_y=None)
                gridlayout.bind(minimum_height=gridlayout.setter('height'))
                for key, value in sorted(favorites_dict.iteritems()):
                    box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=-3)
                    btn_school = Button(text=key)
                    btn_school.disabled = True
                    btn_school.disabled_color = rgba('#000000')
                    btn_distance = Button(text=str(general_info_dict[key][20]) + " km away")
                    btn_distance.disabled = True
                    btn_distance.disabled_color = rgba('#000000')
                    btn_details = Button(text='View Details', on_release=partial(self.view_details_popup, key))
                    btn_view = Button(text='Show on map', on_release=partial(self.showPinAndZoom, key))
                    box.add_widget(btn_school)
                    box.add_widget(btn_distance)
                    box.add_widget(btn_details)
                    box.add_widget(btn_view)
                    gridlayout.add_widget(box)
                    results_count += 1
                self.lbl_results_count.text = str(results_count) + ' schools in your favorite list'
                self.menu_scroll.add_widget(gridlayout)

    def viewFavoritesList(self):
        global isViewingFavorites
        global imported_file
        if isViewingFavorites is False:
            isViewingFavorites = True
            self.disable_widgets()
            if bool(favorites_dict) is False and bool(imported_file) is False:
                # popup that asks user to import or create new when there is no favourites added
                self.import_popup = Popup(title='Favourites', size_hint=(0.4, 0.3), on_dismiss=self.dismiss_import_popup, id='fav_popup')
                root_box = BoxLayout(orientation='vertical')
                label = Label(text='No favourites found.' + '\n' + 'Click New to start a new list or Import to load '
                                                                   'from a previous save file ', halign='center',
                              line_height=1.5)
                box = BoxLayout(orientation='horizontal', spacing=20, padding=(20, 0, 20, 20))
                btn_new = Button(text='New', on_release=self.show_save)
                btn_import = Button(text='Import', on_release=self.show_load)
                box.add_widget(btn_new)
                box.add_widget(btn_import)
                root_box.add_widget(label)
                root_box.add_widget(box)
                self.import_popup.add_widget(root_box)
                self.import_popup.open()
            else:
                results_count = 0
                self.menu_scroll.clear_widgets()
                gridlayout = GridLayout(cols=1, spacing=20, size_hint_y=None)
                gridlayout.bind(minimum_height=gridlayout.setter('height'))
                for key, value in sorted(favorites_dict.iteritems()):
                    box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=-3)
                    btn_school = Button(text=key)
                    btn_school.disabled = True
                    btn_school.disabled_color = rgba('#000000')
                    btn_distance = Button(text=str(general_info_dict[key][20]) + " km away")
                    btn_distance.disabled = True
                    btn_distance.disabled_color = rgba('#000000')
                    btn_details = Button(text='View Details', on_release=partial(self.view_details_popup, key))
                    btn_view = Button(text='Show on map', on_release=partial(self.showPinAndZoom, key))
                    box.add_widget(btn_school)
                    box.add_widget(btn_distance)
                    box.add_widget(btn_details)
                    box.add_widget(btn_view)
                    gridlayout.add_widget(box)
                    results_count += 1
                self.lbl_results_count.text = str(results_count) + ' schools in your favorite list'
                self.menu_scroll.add_widget(gridlayout)
                self.btn_viewFav.text = 'Close Favourites'
        else:  # isViewingFavorites is True, meaning user is currently looking at favorites list
            isViewingFavorites = False
            self.btn_viewFav.text = 'View Favourites'
            self.enable_widgets()
            # reset list
            self.scroll_view_load()

    def dismiss_import_popup(self, x):
        global isViewingFavorites
        global after_import_status
        if isViewingFavorites == True and after_import_status == True:
            self.disable_widgets()
            after_import_status = False
        elif isViewingFavorites:
            isViewingFavorites = False
            self.enable_widgets()

    def enable_widgets(self):
        self.txtsearch.disabled = False
        self.pcode.disabled = True
        self.radius.disabled = True
        self.isnear.disabled = False
        self.level_spinner.disabled = False
        self.region_spinner.disabled = False

    def disable_widgets(self):
        self.txtsearch.disabled = True
        self.pcode.disabled = True
        self.radius.disabled = True
        self.isnear.disabled = True
        self.level_spinner.disabled = True
        self.region_spinner.disabled = True
        self.txtsearch.text = ''

    def details_popup_widget_sizing(self, label, *args):
        label.text_size = (label.width, None)
        label.height = label.texture_size[1]
        label.valign = 'top'

    def error_popup(self):
        global error_msg
        popup = Popup(title='Error',
                      content=Label(text=str(error_msg) + '\n' + 'Please make sure the stated file is not open.'),
                      size_hint=(0.3, 0.3))
        popup.open()


class MainApp(App):
    def build(self):
        return RootWidget()


Factory.register('RootWidget', cls=RootWidget)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

MainApp().run()
