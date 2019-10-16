from kivy.app import App
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.utils import rgba
import csv
from functools import partial
Config.set('graphics', 'window_state', 'maximized')
from kivy.garden.mapview import MapView, MapMarker
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

load_count = 0
general_info_count = 0
general_info_dict = {}
favList = list()

# reading info from general info csv and storing in dictionary
with open('general-information-of-schools.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if general_info_count == 0:
            general_info_count += 1
        else:
            general_info_dict[row[0]] = [row[1], row[2], row[3], row[4], row[6], row[8], row[9], row[10], row[11],
                                         row[18], row[19], row[20], row[22], row[24], row[25], row[26], row[27],
                                         row[32], row[33], row[34]]


# 0[key]:school name 1[0]:website 2[1]:address 3[2]:postal code 4[3]:telephone 6[4]:Fax 8[5]:email 9[6]:mrt 10[7]:bus
# 11[8]:principal 18[9]:vision 19[10]:mission 20[11]:philosophy 22[12]:region 24[13]:school type 25[14]:school nature
# 26[15]:session type 27[16]:education level 32[17]:mother tongue1 33[18]:mother tongue2 34[19]:mother tongue3


class RootWidget(AnchorLayout):
    def on_enter(self):
        m1 = MapMarker(lon=103.8198, lat=1.3521)
        self.guimap.add_marker(m1)

    def on_load(self):
        global load_count
        if load_count == 0:
            self.scroll_view_load()
            load_count += 1

    def scroll_view_load(self):
        results_count = 0
        self.menu_scroll.clear_widgets()
        gridlayout = GridLayout(cols=1, spacing=20, size_hint_y=None)
        gridlayout.bind(minimum_height=gridlayout.setter('height'))
        for key, value in sorted(general_info_dict.iteritems()):
            if value[16] == self.level_spinner.text and value[12] == self.region_spinner.text:
                #filter by school level AND school region
                box = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=-3)
                btn_school = Button(text=key)
                btn_school.disabled = True
                btn_school.disabled_color = rgba('#000000')
                btn_details = Button(text='View Details', on_release=partial(self.view_details_popup, key))
                btn_view = Button(text='Show on map')
                box.add_widget(btn_school)
                box.add_widget(btn_details)
                box.add_widget(btn_view)
                gridlayout.add_widget(box)
                results_count += 1
        self.lbl_results_count.text = str(results_count) + ' schools match your criteria'
        self.menu_scroll.add_widget(gridlayout)

    def view_details_popup(self, key, x):
        popup = Popup(title=key, size_hint=(0.5, 0.8))
        btnFavv = Button(text='test', on_release=partial(self.addToFavorites, key))
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
                                     + '[size=20]' + '[b]' + 'CONTACT' + '[/b]' + '[/size]' + '\n' + '\n'
                                     + 'Email' + '\n'
                                     + general_info_dict[key][5] + '\n' + '\n'
                                     + 'Address' + '\n'
                                     + general_info_dict[key][1] + ' (' + general_info_dict[key][2] + ')' + '\n' + '\n'
                                     + 'Telephone / Fax' + '\n'
                                     + general_info_dict[key][3] + ' / ' + general_info_dict[key][4]+'\n'+'\n'+'\n'+'\n'
                                     + '[size=20]' + '[b]' + 'GETTING THERE' + '[/b]' + '[/size]' + '\n' + '\n'
                                     + 'Nearest MRT' + '\n'
                                     + general_info_dict[key][6] + '\n' + '\n'
                                     + 'Bus Services' + '\n'
                                     + general_info_dict[key][7]
                                , markup=True, line_height=1.5, padding=(50, 50))
        #lbl_school_info.bind(size=partial(self.details_popup_widget_sizing, lbl_school_info))
        scroll_view = ScrollView(scroll_wheel_distance=80, scroll_type=['bars', 'content'], bar_width=10)
        scroll_view.add_widget(lbl_school_info)

        box = BoxLayout()
        box.add_widget(scroll_view)
        box.add_widget(btnFavv)

        popup.add_widget(box)
        popup.open()

    def addToFavorites(self, key, x):
        favList.append(general_info_dict[key])

    def details_popup_widget_sizing(self, label, *args):
        label.text_size = (label.width, None)
        label.height = label.texture_size[1]
        label.valign = 'top'

    def cca_popup(self):
        popup = Popup(title='CCAs',
                      content=Label(text='Hello world'),
                      size_hint=(None, None), size=(400, 400))
        popup.open()


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
