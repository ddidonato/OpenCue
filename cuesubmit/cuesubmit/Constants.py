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
import os

from cuesubmit import Config

config = Config.getConfigValues()

UP_KEY = 16777235
DOWN_KEY = 16777237
TAB_KEY = 16777217

UI_NAME = config.get('UI_NAME', 'OPENCUESUBMIT')
SUBMIT_APP_WINDOW_TITLE = config.get('SUBMIT_APP_WINDOW_TITLE', 'OpenCue Submit')

MAYA_RENDER_CMD = config.get('MAYA_RENDER_CMD', 'Render')
NUKE_RENDER_CMD = config.get('NUKE_RENDER_CMD', 'nuke')
BLENDER_RENDER_CMD = config.get('BLENDER_RENDER_CMD', 'blender')
FRAME_TOKEN = config.get('FRAME_TOKEN', '#IFRAME#')
DEFAULT_MIN_CORES = config.get('DEFAULT_MIN_CORES', 1)
DEFAULT_MIN_CORES_MAYA = config.get('DEFAULT_MIN_CORES_MAYA', DEFAULT_MIN_CORES)
DEFAULT_MIN_CORES_NUKE = config.get('DEFAULT_MIN_CORES_NUKE', DEFAULT_MIN_CORES)
DEFAULT_MIN_CORES_BLENDER = config.get('DEFAULT_MIN_CORES_BLENDER', DEFAULT_MIN_CORES)
DEFAULT_MIN_CORES_ARNOLD = config.get('DEFAULT_MIN_CORES_ARNOLD', DEFAULT_MIN_CORES)
DEFAULT_MIN_CORES_SHELL = config.get('DEFAULT_MIN_CORES_SHELL', DEFAULT_MIN_CORES)
DEFAULT_CHUNK = config.get('DEFAULT_CHUNK', 1)
DEFAULT_CHUNK_MAYA = config.get('DEFAULT_CHUNK_MAYA', DEFAULT_CHUNK)
DEFAULT_CHUNK_NUKE = config.get('DEFAULT_CHUNK_NUKE', DEFAULT_CHUNK)
DEFAULT_CHUNK_BLENDER = config.get('DEFAULT_CHUNK_BLENDER', DEFAULT_CHUNK)
DEFAULT_CHUNK_ARNOLD = config.get('DEFAULT_CHUNK_ARNOLD', DEFAULT_CHUNK)
DEFAULT_CHUNK_SHELL = config.get('DEFAULT_MIN_CORES_SHELL', DEFAULT_CHUNK)
DEFAULT_SERVICE_ARNOLD = config.get('DEFAULT_SERVICE_ARNOLD', None)
DEFAULT_SERVICE_BLENDER = config.get('DEFAULT_SERVICE_BLENDER', None)
DEFAULT_SERVICE_MAYA = config.get('DEFAULT_SERVICE_MAYA', None)
DEFAULT_SERVICE_NUKE = config.get('DEFAULT_SERVICE_NUKE', None)
DEFAULT_SERVICE_SHELL = config.get('DEFAULT_SERVICE_SHELL', None)

DEFAULT_LAYER_PREFIX = config.get('DEFAULT_LAYER_PREFIX', 'Layer')
DEFAULT_LAYER_TYPE = config.get('DEFAULT_LAYER_TYPE', 'Shell')

BLENDER_FORMATS = ['', 'AVIJPEG', 'AVIRAW', 'BMP', 'CINEON', 'DPX', 'EXR', 'HDR', 'IRIS', 'IRIZ',
                   'JP2', 'JPEG', 'MPEG', 'MULTILAYER', 'PNG', 'RAWTGA', 'TGA', 'TIFF']
BLENDER_OUTPUT_OPTIONS_URL = \
  'https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#render-options'

DIR_PATH = os.path.dirname(__file__)

# Dropdown label to specify the default Facility, i.e. let Cuebot decide.
DEFAULT_FACILITY_TEXT = '[Default]'
