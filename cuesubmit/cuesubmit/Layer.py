#  Copyright Contributors to the OpenCue Project
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


from builtins import str
from builtins import object

from cuesubmit import Constants, JobTypes

class DependType(object):
    """Types of Dependencies available in the UI."""

    Null = ''
    Layer = 'Layer'
    Frame = 'Frame'


class LayerData(object):
    """Data object for storing settings about the Layer."""

    def __init__(self):
        self.name = Constants.DEFAULT_LAYER_PREFIX
        self.layerType = Constants.DEFAULT_LAYER_TYPE
        self.cmd = {}
        self.layerRange = ''
        self.chunk = 1
        self.cores = 1
        self.env = {}
        self.services = []
        self.limits = []
        self.applicationVersion = None
        self.applicationVersions = None
        self.renderCommands = None
        self.dependType = DependType.Null
        self.dependsOn = None
        self.populateDefaultValues()

    def populateDefaultValues(self):
        if self.layerType in Constants.LAYER_TYPE_SETTINGS:
            settings_to_use = Constants.LAYER_TYPE_SETTINGS[self.layerType]
        else:
            settings_to_use = Constants.LAYER_TYPE_SETTINGS["DEFAULT"]
        self.chunk = settings_to_use.get("CHUNK", 1)
        self.cores = settings_to_use.get("MIN_CORES", 1)
        self.renderCommands = settings_to_use.get("RENDER_CMD", {"default": None})
        self.applicationVersions = list(self.renderCommands.keys())
        self.applicationVersion = self.applicationVersions[0]
        self.services = settings_to_use.get("SERVICES", [])

    def __str__(self):
        return str(self.toDict())

    def getRenderCommand(self):
        return self.renderCommands[self.applicationVersion]

    def toDict(self):
        """Return a dictionary from the attributes."""
        return {
            'name': self.name,
            'layerType': self.layerType,
            'cmd': self.cmd,
            'layerRange': self.layerRange,
            'chunk': self.chunk,
            'cores': self.cores,
            'applicationVersion': self.applicationVersion,
            'env': self.env,
            'services': self.services,
            'limits': self.limits,
            'dependType': self.dependType,
            'dependsOn': self.dependsOn
        }

    @staticmethod
    def buildFactory(name=None, layerType=None, cmd=None, layerRange=None, chunk=None, cores=None,
                     applicationVersion=None, env=None, services=None, limits=None, dependType=None, dependsOn=None):
        """Build a new LayerData object with the given settings."""
        layerData = LayerData()
        layerData.update(name, layerType, cmd, layerRange, chunk, cores, applicationVersion,
                         env, services, limits, dependType, dependsOn)
        return layerData

    def update(self, name=None, layerType=None, cmd=None, layerRange=None, chunk=None, cores=None,
               applicationVersion=None, env=None, services=None, limits=None, dependType=None, dependsOn=None):
        """Update this Layer with the provided settings."""
        if name is not None:
            self.name = name
        if cmd is not None:
            self.cmd = cmd
        if layerRange is not None:
            self.layerRange = layerRange
        if chunk is not None:
            self.chunk = chunk
        if cores is not None:
            self.cores = cores
        if applicationVersion is not None and len(applicationVersion) > 0:
            self.applicationVersion = applicationVersion[0]
        if env is not None:
            self.env = env
        if services is not None:
            self.services = services
        if limits is not None:
            self.limits = limits
        if dependType is not None:
            self.dependType = dependType
        if dependsOn is not None:
            self.dependsOn = dependsOn
        if layerType is not None:
            layer_type_old = self.layerType
            self.layerType = layerType
            if layer_type_old != self.layerType:
                self.populateDefaultValues()
