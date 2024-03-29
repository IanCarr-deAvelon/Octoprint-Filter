# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import logging

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import logging

class FilterPlugin(octoprint.plugin.SettingsPlugin,
                   octoprint.plugin.AssetPlugin,
                   octoprint.plugin.TemplatePlugin):

        def __init__(self):
            self.ian_debug=False
            self.log="/home/pi/.octoprint/logs/filter.log"

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
        __plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

        def handle_gcode_queuing(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
            if self.ian_debug:
                logger = logging.getLogger("filter")
                logger.setLevel(logging.INFO)
                fh = logging.FileHandler(self.log)
                fh.setLevel(logging.INFO)
                logger.addHandler(fh)
        
            if not gcode is None:
                if gcode in ("M0","M106"):
                    if self.ian_debug:
                        logger.info("IAN remove pause or fan")
                    return (None,)
            
                if gcode in ("G28"):
                    if self.ian_debug:
                        logger.info("IAN Home command")
                    if 'Z' in cmd:
                        if self.ian_debug:
                            logger.info("IAN Z home command. Add recover leveling")
                        return [(cmd, cmd_type),    # 2-tuple, command & command type
                               ("M420 S1","IAN get leveling back") ]                       
            
            
def __plugin_load__():
    global __plugin_implementation__
    global __plugin_hooks__

    debug=True
    if debug: 
        log="/home/pi/.octoprint/logs/filter.log"
        logger = logging.getLogger("filter")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        logger.info("IAN loading")

    plugin =  FilterPlugin()

    __plugin_implementation__ = plugin


    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.handle_gcode_queuing
       }
    if debug:
        logger.info("IAN loaded")
 

