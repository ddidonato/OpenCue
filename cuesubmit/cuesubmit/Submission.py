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
from outline import Outline, cuerun
from outline.modules.shell import Shell

from cuesubmit import Constants
from cuesubmit import JobTypes
from cuesubmit import Util

import fileseq
import uuid
import os


def buildMayaCmd(layerData):
    """From a layer, build a Maya Render command."""
    mayaFile = layerData.cmd.get('mayaFile')
    mayaProject = layerData.cmd.get('mayaProject')
    if not mayaFile:
        raise ValueError('No Maya File provided. Cannot submit job.')
    renderCommand = '{renderCmd} -r file -s {frameToken} -e {frameToken}'.format(
        renderCmd=Constants.MAYA_RENDER_CMD, frameToken=Constants.FRAME_TOKEN)
    if 'camera' in layerData.cmd:
        # If launched within maya, select a camera
        camera = layerData.cmd.get('camera')
        if not camera:
            raise ValueError('No camera selected. Cannot submit job.')
        renderCommand += ' -cam {}'.format(camera)
    if mayaProject:
        renderCommand += ' -proj \'{}\''.format(mayaProject)
    renderCommand += ' {}'.format(mayaFile)
    return renderCommand


def buildNukeCmd(layerData):
    """From a layer, build a Nuke Render command."""
    writeNodes = layerData.cmd.get('writeNodes')
    nukeFile = layerData.cmd.get('nukeFile')
    if not nukeFile:
        raise ValueError('No Nuke file provided. Cannot submit job.')
    renderCommand = '{renderCmd} -F {frameToken} '.format(
        renderCmd=Constants.NUKE_RENDER_CMD, frameToken=Constants.FRAME_TOKEN)
    if writeNodes:
        renderCommand += '-X {} '.format(writeNodes)
    renderCommand += '-x {}'.format(nukeFile)
    return renderCommand

def buildBlenderCmd(layerData):
    """From a layer, build a Blender render command."""
    blenderFile = layerData.cmd.get('blenderFile')
    outputPath = layerData.cmd.get('outputPath')
    outputFormat = layerData.cmd.get('outputFormat')
    if not blenderFile:
        raise ValueError('No Blender file provided. Cannot submit job.')
    
    renderCommand = '{renderCmd} -b -noaudio {blenderFile}'.format(
        renderCmd=Constants.BLENDER_RENDER_CMD, blenderFile=blenderFile)
    if outputPath:
        renderCommand += ' -o {}'.format(outputPath)
    if outputFormat:
        renderCommand += ' -F {}'.format(outputFormat)
    # The render frame must come after the scene and output
    renderCommand += ' -f {frameToken}'.format(frameToken=Constants.FRAME_TOKEN)
    return renderCommand


def buildArnoldCmd(layerData):
    """From a layer, build a Maya Render command."""
    arnold_file = layerData.cmd.get('arnoldFile')
    render_folder = layerData.cmd.get('renderFolder')
    render_file = layerData.cmd.get('renderFile')
    render_file_type = layerData.cmd.get('renderFileType')
    errors = ""
    if not arnold_file:
        errors += 'Invalid arnold file\n'
    if render_folder and not render_file:
        errors += 'Invalid render file\n'
    if errors:
        raise ValueError(errors)
    input_file_sequence = arnold_file
    output_file_sequence = None
    if render_folder and render_file:
        if not render_file_type:
            raise ValueError("Invalid render file type")
        output_file = render_file
        if not render_file.lower().endswith(".{}".format(render_file_type)):
            output_file += ".{}".format(render_file_type)
        output_file_sequence = fileseq.FileSequence(output_file)
        if not output_file_sequence:
            raise Exception('Output filename must be in image sequence format')
        if not output_file_sequence.zfill() == input_file_sequence.zfill():
            raise ValueError('Frame padding number of render file must match arnold file')

    render_command = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/hfs18.0/dsolib;"

    padding_length = input_file_sequence.zfill()
    input_file = input_file_sequence.format(template='{dirname}{basename}$currentFrame{extension}')
    render_command += 'currentFrame=$(printf "%0{0}d" "#IFRAME#");'.format(padding_length)
    render_command += '{renderCmd} -i "{inFile}"'.format(
        renderCmd=Constants.config.get('ARNOLD_RENDER_CMD', 'kick'),
        inFile=input_file,
    )

    final_path = None
    output_path = None
    if output_file_sequence:
        temp_file_name = "{0}_$currentFrame.{1}".format(uuid.uuid4().hex, render_file_type)
        output_file_name = output_file_sequence.format(template='{basename}$currentFrame{extension}')
        output_path = os.path.join(render_folder, temp_file_name)
        final_path = os.path.join(render_folder, output_file_name)
        render_command += ' -o "{0}"'.format(output_path)
    if render_file_type:
        render_command += ' -of {0}'.format(render_file_type)
    render_command += ' -v 4 -nstdin -dw -dp;'
    if final_path:
        render_command += 'mv "{0}" "{1}";'.format(output_path, final_path)
    return render_command


def buildLayer(layerData, command, lastLayer=None):
    """Create a PyOutline Layer for the given layerData.
    @type layerData: ui.Layer.LayerData
    @param layerData: layer data from the ui
    @type command: str
    @param command: command to run
    @type lastLayer: outline.layer.Layer
    @param lastLayer: layer that this new layer should be dependent on if dependType is set.
    """
    if float(layerData.cores) >= 2:
        threadable = True
    else:
        threadable = False
    layer = Shell(layerData.name, command=command.split(), chunk=layerData.chunk,
                  threads=float(layerData.cores), range=str(layerData.layerRange),
                  threadable=threadable)
    if layerData.services:
        layer.set_service(layerData.services[0])
    if layerData.limits:
        layer.set_limits(layerData.limits)
    if layerData.dependType and lastLayer:
        if layerData.dependType == 'Layer':
            layer.depend_all(lastLayer)
        else:
            layer.depend_on(lastLayer)
    return layer


def buildMayaLayer(layerData, lastLayer):
    mayaCmd = buildMayaCmd(layerData)
    return buildLayer(layerData, mayaCmd, lastLayer)


def buildNukeLayer(layerData, lastLayer):
    nukeCmd = buildNukeCmd(layerData)
    return buildLayer(layerData, nukeCmd, lastLayer)


def buildBlenderLayer(layerData, lastLayer):
    blenderCmd = buildBlenderCmd(layerData)
    return buildLayer(layerData, blenderCmd, lastLayer)

def buildArnoldLayer(layerData, lastLayer):
    arnoldCmd = buildArnoldCmd(layerData)
    return buildLayer(layerData, arnoldCmd, lastLayer)

def buildShellLayer(layerData, lastLayer):
    return buildLayer(layerData, layerData.cmd['commandTextBox'], lastLayer)


def submitJob(jobData):
    """Submit the job using the PyOutline API."""
    outline = Outline(jobData['name'], shot=jobData['shot'], show=jobData['show'],
                      user=jobData['username'])
    lastLayer = None
    for layerData in jobData['layers']:
        if layerData.layerType == JobTypes.JobTypes.MAYA:
            layer = buildMayaLayer(layerData, lastLayer)
        elif layerData.layerType == JobTypes.JobTypes.SHELL:
            layer = buildShellLayer(layerData, lastLayer)
        elif layerData.layerType == JobTypes.JobTypes.NUKE:
            layer = buildNukeLayer(layerData, lastLayer)
        elif layerData.layerType == JobTypes.JobTypes.BLENDER:
            layer = buildBlenderLayer(layerData, lastLayer)
        elif layerData.layerType == JobTypes.JobTypes.ARNOLD:
            layer = buildArnoldLayer(layerData, lastLayer)
        else:
            raise ValueError('unrecognized layer type %s' % layerData.layerType)
        outline.add_layer(layer)
        lastLayer = layer
    if 'facility' in jobData:
        outline.set_facility(jobData['facility'])

    job = cuerun.launch(outline, use_pycuerun=False)
    show = Util.getShow(jobData['show'])
    show.getRootGroup().reparentJobs(job)
    return job
