from fileseq import FileSequence
import math


def formatPathsAsFileSequences(paths):
    file_sequences = getFileSequencesFromPaths(paths)
    result_paths = []
    for file_seq in file_sequences:
        file_seq_paths = list(file_seq)
        if len(file_seq_paths) == 1:
            result_paths.append(file_seq_paths[0])
        else:
            result_paths.append(formatFileSequenceAsRangePath(file_seq))
    result_paths.sort()
    return result_paths


def formatFileSequenceAsRangePath(file_seq):
    file_sequence_paths = list(file_seq)
    if len(file_sequence_paths) > 1:
        padding_number = file_seq.zfill()
        padding_str = '{{:0{}d}}'.format(padding_number)
        start_frame_str = padding_str.format(file_seq.start())
        end_frame_str = padding_str.format(file_seq.end())
        path_template = '{{dirname}}{{basename}}[{0}-{1}]{{extension}}'.format(start_frame_str, end_frame_str)
        return file_seq.format(template=path_template)
    elif len(file_sequence_paths) == 1:
        return file_sequence_paths[0]
    else:
        raise ValueError('No paths found in file sequence')


def getFileSequencesFromPaths(paths):
    file_sequences = []
    for file_seq in FileSequence.findSequencesInList(paths):
        for file_seq_consec in file_seq.split():
            file_sequences.append(file_seq_consec)
    return file_sequences

def sizeof_fmt(num, suffix='B'):
    if num:
        magnitude = int(math.floor(math.log(num, 1024)))
        val = num / math.pow(1024, magnitude)
        if magnitude > 7:
            return '{:.1f}{}{}'.format(val, 'Yi', suffix)
        return '{:3.1f}{}{}'.format(val, ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'][magnitude], suffix)
