import appdaemon.plugins.hass.hassapi as hass
import datetime

class Termostaty(hass.Hass):

  def initialize(self):
    time = datetime.time(0, 0, 0) #potrzebne w run_minutely
    #self.run_minutely(self.run_minutely_c, time)
    #self.listen_state(self.wlacz, "input_select")
    self.run_minutely(self.wlacz_2, time)

  #def wlacz_2 (self, kwargs):
  #  self.log("=========== ODPALAM ==============")

  #def wlacz (self, entity, attribute, old, new, kwargs): #tak powinna wygladac definicja funkcji odpalana za pomoca listen_state
  def wlacz_2 (self, kwargs):
    self.log("=========== ODPALAM ==============")
    #self.log(self.get_state("input_boolean.testowy_boolean")) #ok
    #self.log(self.get_state("input_datetime.czas_salon_rano")) #ok

    #start = datetime.datetime.strptime(self.get_state("input_datetime.czas_salon_rano"), '%H:%M:%S').time() #ok
    #today = datetime.date.today() #ok
    #start = datetime.datetime.combine(today, start) #ok
    #self.log(self.args["tryb"]) #ok
    czas_rano = self.get_state(self.args["czas_rano"])
    czas_praca = self.get_state(self.args["czas_praca"])
    czas_dzien = self.get_state(self.args["czas_dzien"])
    czas_noc = self.get_state(self.args["czas_noc"])
    temp_rano = int(float(self.get_state(self.args["temp_rano"])))
    temp_praca = int(float(self.get_state(self.args["temp_praca"])))
    temp_dzien = int(float(self.get_state(self.args["temp_dzien"])))
    temp_noc = int(float(self.get_state(self.args["temp_noc"])))
    okno = self.get_state(self.args["okno"])
    tryb = self.get_state(self.args["tryb"])
    termostat = self.args["termostat"]
    termostat_setpoint = self.args["termostat_setpoint"]
    temp_min = self.args["temp_min"]
    temp_max = self.args["temp_max"]
    self.log("===== atrybut ======")
    #atrybut = self.get_state("climate.eurotronic_eur_stellaz_wall_radiator_thermostat_valve_control_comfort_setpoint_2", attribute="temperature")
    #atrybut = self.get_state(termostat_setpoint, attribute = "temperature")
    #self.log(atrybut)
    self.call_service("climate/set_temperature", entity_id = "climate/danfoss_z_thermostat_heating_1", temperature = "19")

    self.ustaw_temperature(czas_rano, czas_praca, czas_dzien, czas_noc, temp_rano, temp_praca, temp_dzien, temp_noc, okno, tryb, termostat, termostat_setpoint, temp_min, temp_max)

    #today = datetime.date.today()

    #self.log(datetime.datetime.strptime(self.get_state("input_datetime.czas_salon_rano"), '%H:%M:%S'))
  def godzina_na_date (self, tekst):
    dzisiaj = datetime.date.today()
    godzina = datetime.datetime.strptime(tekst, '%H:%M:%S').time()
    return datetime.datetime.combine(dzisiaj, godzina)

  def czy_weekend (self):
    if datetime.date.today().weekday() > 4:
      self.log(datetime.date.today().weekday())
      return True
    else:
      self.log(datetime.date.today().weekday())
      return False


  def ustaw_temperature(self, czas_rano, czas_praca, czas_dzien, czas_noc, temp_rano, temp_praca, temp_dzien, temp_noc, okno, tryb, termostat, termostat_setpoint, temp_min, temp_max):
    #self.log(self.godzina_na_date(czas_noc)) #ok
    #self.log(datetime.datetime.now().replace(microsecond=0)) #ok
    if (datetime.date.today().weekday() > 4) and (tryb == "Auto"):
      tryb = "Weekend"
    else:
      pass

    if tryb == "Wyłączone" or okno == "on":
      temperatura = temp_min
      self.log(tryb + okno + " czas " + czas_noc)
      #self.set_state(self.args["termostat"], state = min) #ok
    elif tryb == "Auto":
      self.log(tryb)
      if self.now_is_between(czas_noc, czas_rano):
        temperatura = temp_noc
        self.log("teraz jest noc")
      elif self.now_is_between(czas_rano, czas_praca):
        temperatura = temp_rano
      elif self.now_is_between(czas_praca, czas_dzien):
        temperatura = temp_praca
      elif self.now_is_between(czas_dzien, czas_noc):
        temperatura = temp_dzien
      else:
        temperatura = 18
    elif tryb == "Weekend":
      self.log(tryb)
      if self.now_is_between(czas_noc, czas_rano):
        temperatura = temp_noc
        self.log("teraz jest noc")
      elif self.now_is_between(czas_rano, czas_praca):
        temperatura = temp_rano
      elif self.now_is_between(czas_praca, czas_dzien):
        temperatura = temp_dzien
      elif self.now_is_between(czas_dzien, czas_noc):
        temperatura = temp_dzien
      else:
        temperatura = 18
    elif tryb == "Manual":
      self.log(tryb)
      #tutaj chyba nie trzeba nic robić, po prostu nie będziemy zmieniac temperatury skryptem, a zostanie reczne ustawienie termostatu. Ewentualnie ustawienie temperatury z termostatu - do zakombinowania jak podłączymy z-wave
      #temperatura = self.get_state(termostat)
    elif tryb == "Out":
      self.log(tryb)
      temperatura = temp_noc
    elif tryb == "Max":
      self.log(tryb)
      temperatura = temp_max

    #self.log("get_state: " + int(float(self.get_state(termostat))) + " temperaturra: " + temperatura)
    self.log(self.get_state(termostat))
    self.log(temperatura)
    if (int(self.get_state(termostat_setpoint, attribute = "temperature")) != temperatura) and (tryb != "Manual"):
      self.log("Ustawiam temperaturę na: " + str(temperatura))
      self.set_state(termostat_setpoint, attributes = {"temperature": temperatura})
      #self.call_service("climate.set_temperature", entity_id = "climate.danfoss_z_thermostat_heating_1", temperature = "19")
    
    #if self.czy_weekend():
    #  self.log("weekend")
    #else:
    #  self.log("tyrka - nie weekend")