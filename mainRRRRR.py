from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from kivy.garden.mapview import MapView, MapMarker
import schoolLocations as locPin


class RootWidget(AnchorLayout):
    def on_enter(self):
        cords = locPin.sch_data_dict
        if self.pcode.text == "" and self.radius.text == "" and self.txtsearch.text == "":
            for i in cords.keys():
                marker = MapMarker(lat=cords[i][1], lon=cords[i][2])
                self.guimap.add_marker(marker)
        if len(str(self.pcode.text)) == 6 and str(self.pcode.text).isdigit() is True:
            if self.radius.text != "":
                locPin.distance_calc_all(int(self.pcode.text))
                locPin.is_it_near((float(self.radius.text)))
                for i in cords.keys():
                    if cords[i][4] == True:
                        self.guimap.add_marker(MapMarker(lat=cords[i][1], lon=cords[i][2]))
                    # if cords[i][4] == False:
                    #    self.guimap.remove_marker(MapMarker(lat=cords[i][1], lon=cords[i][2]))
                self.guimap.center_on(locPin.cords_from_postal(int(self.pcode.text))[0],locPin.cords_from_postal(int(self.pcode.text))[1])
                if int(self.radius.text) < 3:
                    self.guimap.zoom = 15
                elif int(self.radius.text) < 5:
                    self.guimap.zoom = 14
                elif int(self.radius.text) < 8:
                    self.guimap.zoom = 13
                else:
                    self.guimap.zoom = 12
            #  self.guimap.remove_marker(cord_markers[i]) works here but not below?
        #for i in cord_markers.keys():
            # TRY THE REMOVE AND THEN REPOPULATE TECHNIQUE
            #self.guimap.remove_marker(cord_markers[i])
        #if len(str(self.txtsearch.text)) == 6 and str(self.txtsearch.text).isdigit() is True:
            # creates pins based on specified location and radius (put home postal code here)
            # NEED DIFFERENT TEXT BOX (side by side in a 2:1 ratio?)
            # ALSO A BUTTON TO CLEAR ALL PINS


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()