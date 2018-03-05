import appdaemon.plugins.hass.hassapi as hass

class Zwave(hass.Hass):

  def initialize(self):
    self.listen_state(self.wlacz, "input_boolean.testowy_boolean")

  def wlacz (self, entity, attribute, old, new, kwargs):
    #self.turn_on("light.dimmer_i_pir_mys_20_8_0")
    self.log("============== Uruchamiam test Z-WAVE ===============")
    self.call_service("light/toggle", entity_id = "light.dimmer_i_pir_mys_20_8_0")
    self.call_service("climate/set_temperature", entity_id = "climate.danfoss_z_thermostat_heating_1", temperature = "24") # DZIAŁA!!! :)