# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class FilterPlugin(octoprint.plugin.SettingsPlugin,
                   octoprint.plugin.AssetPlugin,
                   octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/filter.js"],
			css=["css/filter.css"],
			less=["less/filter.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			filter=dict(
				displayName="Filter Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="IanCarr-deAvelon",
				repo="OctoPrint-Filter",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/IanCarr-deAvelon/OctoPrint-Filter/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Filter Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#IAN
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3
IAN_DEBUG=True

def handle_gcode_sent(comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    if gcode in ("M106"):
        if IAN_DEBUG:
            import logging
            logging.getLogger(__name__).info("We removed a fan command to the printer!")
        return (None,)

    if gcode in ("M0"):
        if IAN_DEBUG:
            import logging
            logging.getLogger(__name__).info("We removed a pause command to the printer!")
        return (None,)

def handle_gcode_queuing(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None *args, **kwargs):
    if gcode in ("G28"):
        if IAN_DEBUG:
            import logging
            logging.getLogger(__name__).info("We recovered bed leveling after a home Z command to the printer!")
        return

    return [("M105", "temperature_poll"),    # 2-tuple, command & command type
            ("M110",),                       # 1-tuple, just the command
            "M117 echo foo: {}".format(cmd)] # string, just the command

__plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.queuing": rewrite_foo
}


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = FilterPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
                "octoprint.comm.protocol.gcode.sent": handle_gcode_sent
	}

