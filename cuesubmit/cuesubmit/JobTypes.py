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

from builtins import object
from cuesubmit.ui import SettingsWidgets
from cuesubmit import Constants


class JobTypes(object):
    """Base Job Types available in the UI.
    Plugin apps can subclass this to change out the mapping
    to enable customized settings widgets.
    """

    ARNOLD = 'Arnold'
    BLENDER = 'Blender'
    MAYA = 'Maya'
    NUKE = 'Nuke'
    SHELL = 'Shell'

    SETTINGS_MAP = {
        ARNOLD: SettingsWidgets.BaseArnoldSettings,
        BLENDER: SettingsWidgets.BaseBlenderSettings,
        MAYA: SettingsWidgets.BaseMayaSettings,
        NUKE: SettingsWidgets.BaseNukeSettings,
        SHELL: SettingsWidgets.ShellSettings,
    }

    DEFAULT_CORES_MAP = {
        ARNOLD: Constants.DEFAULT_MIN_CORES_ARNOLD,
        BLENDER: Constants.DEFAULT_MIN_CORES_BLENDER,
        MAYA: Constants.DEFAULT_MIN_CORES_MAYA,
        NUKE: Constants.DEFAULT_MIN_CORES_NUKE,
        SHELL: Constants.DEFAULT_MIN_CORES,
    }

    DEFAULT_CHUNK_MAP = {
        ARNOLD: Constants.DEFAULT_CHUNK_ARNOLD,
        BLENDER: Constants.DEFAULT_CHUNK_BLENDER,
        MAYA: Constants.DEFAULT_CHUNK_MAYA,
        NUKE: Constants.DEFAULT_CHUNK_NUKE,
        SHELL: Constants.DEFAULT_CHUNK,
    }

    DEFAULT_SERVICE_MAP = {
        ARNOLD: Constants.DEFAULT_SERVICE_ARNOLD,
        BLENDER: Constants.DEFAULT_SERVICE_BLENDER,
        MAYA: Constants.DEFAULT_SERVICE_MAYA,
        NUKE: Constants.DEFAULT_SERVICE_NUKE,
        SHELL: Constants.DEFAULT_SERVICE_SHELL,
    }

    def __init__(self):
        pass

    @classmethod
    def build(cls, jobType, *args, **kwargs):
        """Factory method for creating a settings widget."""
        return cls.SETTINGS_MAP[jobType](*args, **kwargs)

    @classmethod
    def types(cls):
        """return a list of types available."""
        return [cls.SHELL, cls.MAYA, cls.NUKE, cls.BLENDER, cls.ARNOLD]
