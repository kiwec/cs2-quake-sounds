# WARNING: Claude-generated, expect bugs!

from ctypes import *
import array
import os
import platform
import sys

if platform.system() == 'Windows':
    bass_lib = 'bass.dll'
    bassloud_lib = 'bassloud.dll'
elif platform.system() == 'Darwin':
    bass_lib = 'libbass.dylib'
    bassloud_lib = 'libbassloud.dylib'
else:
    bass_lib = 'libbass.so'
    bassloud_lib = 'libbassloud.so'

bass = CDLL(os.path.join(os.getcwd(), bass_lib))
bassloud = CDLL(os.path.join(os.getcwd(), bassloud_lib))

# Define function prototypes for correct type handling
bass.BASS_ChannelGetLength.restype = c_uint64
bass.BASS_ChannelGetPosition.restype = c_uint64
bass.BASS_ChannelBytes2Seconds.restype = c_double
bass.BASS_StreamCreateFile.restype = c_ulong
bass.BASS_SampleLoad.restype = c_ulong
bass.BASS_SampleGetChannel.restype = c_ulong
bassloud.BASS_Loudness_Start.restype = c_ulong

# Error codes
BASS_OK = 0
BASS_ERROR_MEM = 1
BASS_ERROR_FILEOPEN = 2
BASS_ERROR_DRIVER = 3
BASS_ERROR_HANDLE = 5
BASS_ERROR_FORMAT = 6
BASS_ERROR_POSITION = 7
BASS_ERROR_INIT = 8
BASS_ERROR_ALREADY = 14
BASS_ERROR_NOCHAN = 18
BASS_ERROR_ILLTYPE = 19
BASS_ERROR_ILLPARAM = 20
BASS_ERROR_DEVICE = 23
BASS_ERROR_NOPLAY = 24
BASS_ERROR_FREQ = 25
BASS_ERROR_UNKNOWN = -1

# Loudness flags
BASS_LOUDNESS_CURRENT = 0
BASS_LOUDNESS_INTEGRATED = 1
BASS_LOUDNESS_RANGE = 2
BASS_LOUDNESS_PEAK = 4
BASS_LOUDNESS_TRUEPEAK = 8
BASS_LOUDNESS_AUTOFREE = 0x8000

# Random flags
BASS_ATTRIB_VOL = 2
BASS_UNICODE = 0x80000000
BASS_STREAM_DECODE = 0x200000

# Device setup flags
BASS_DEVICE_8BITS = 1
BASS_DEVICE_MONO = 2
BASS_DEVICE_3D = 4

# Music flags
BASS_MUSIC_RAMP = 1
BASS_MUSIC_RAMPS = 2
BASS_MUSIC_LOOP = 4
BASS_MUSIC_FT2MOD = 16
BASS_MUSIC_PT1MOD = 32
BASS_MUSIC_POSRESET = 256

# Sample flags
BASS_SAMPLE_8BITS = 1
BASS_SAMPLE_FLOAT = 256
BASS_SAMPLE_MONO = 2
BASS_SAMPLE_LOOP = 4
BASS_SAMPLE_3D = 8
BASS_SAMPLE_SOFTWARE = 16
BASS_SAMPLE_OVER_VOL = 65536
BASS_SAMPLE_OVER_POS = 131072
BASS_SAMPLE_OVER_DIST = 196608

def Init(device=-1, freq=44100, flags=0, win=0, clsid=None):
    """Initialize BASS audio output device"""
    result = bass.BASS_Init(device, freq, flags, win, clsid)
    return result != 0

def PluginLoad(filename):
    if platform.system() == 'Windows':
        filename += '.dll'
    elif platform.system() == 'Darwin':
        filename += '.dylib'
    else:
        filename += '.so'

    filepath = os.path.join(os.getcwd(), filename)
    handle = bass.BASS_PluginLoad(filepath.encode(), c_ulong(0))
    return handle != 0

def Free():
    """Free all resources used by BASS"""
    return bass.BASS_Free() != 0

def SetDevice(id):
    return bass.BASS_SetDevice(id)

def GetVersion():
    """Get the BASS version"""
    return bass.BASS_GetVersion()

def ErrorGetCode():
    """Get the error code for the most recent error"""
    return bass.BASS_ErrorGetCode()

def StreamCreateFile(mem, file, offset=0, length=0, flags=0):
    """Create a sample stream from a file"""
    if platform.system() == "Windows":
        filepath = c_wchar_p(file)
        flags = flags | BASS_UNICODE
    else:
        filepath = file.encode()
    
    result = bass.BASS_StreamCreateFile(c_bool(mem), filepath, c_ulonglong(offset), c_ulonglong(length), c_ulong(flags))
    if result == 0:
        return None
    return result


def SampleLoad(mem, file, offset=0, length=0, max=1, flags=0):
    """Load a sample from a file"""
    if platform.system() == "Windows":
        filepath = c_wchar_p(file)
        flags = flags | BASS_UNICODE
    else:
        filepath = file.encode()
        
    result = bass.BASS_SampleLoad(c_bool(mem), filepath, c_ulonglong(offset), c_ulong(length), c_ulong(max), c_ulong(flags))
    if result == 0:
        return None
    return result

def SampleFree(handle):
    """Free a sample"""
    return bass.BASS_SampleFree(handle) != 0

def SampleGetChannel(handle):
    """Get a sample channel"""
    result = bass.BASS_SampleGetChannel(handle, BASS_SAMPLE_OVER_POS)
    if result == 0:
        return None
    return result

def ChannelPlay(handle, restart=True):
    """Start playback of a sample, stream, or music"""
    return bass.BASS_ChannelPlay(handle, c_bool(restart)) != 0

def ChannelStop(handle):
    """Stop playback of a sample, stream, or music"""
    return bass.BASS_ChannelStop(handle) != 0

def ChannelPause(handle):
    """Pause playback of a sample, stream, or music"""
    return bass.BASS_ChannelPause(handle) != 0

def ChannelSetPosition(handle, pos, mode=0):
    """Set the playback position of a sample, stream, or music"""
    return bass.BASS_ChannelSetPosition(handle, c_ulonglong(pos), mode) != 0

def ChannelGetPosition(handle, mode=0):
    """Get the playback position of a sample, stream, or music"""
    return bass.BASS_ChannelGetPosition(handle, mode)

def ChannelGetLength(handle, mode=0):
    """Get the playback length of a sample, stream, or music"""
    return bass.BASS_ChannelGetLength(handle, mode)

def ChannelBytes2Seconds(handle, pos):
    """Convert byte position to seconds"""
    return c_double(bass.BASS_ChannelBytes2Seconds(handle, pos)).value

def ChannelSeconds2Bytes(handle, pos):
    """Convert seconds to byte position"""
    return bass.BASS_ChannelSeconds2Bytes(handle, c_double(pos))

def ChannelSetAttribute(handle, attrib, value):
    """Set channel attributes"""
    return bass.BASS_ChannelSetAttribute(handle, attrib, c_float(value)) != 0

def ChannelGetAttribute(handle, attrib):
    """Get channel attributes"""
    value = c_float()
    if bass.BASS_ChannelGetAttribute(handle, attrib, byref(value)) != 0:
        return value.value
    return None

def StreamFree(handle):
    """Free a sample stream"""
    return bass.BASS_StreamFree(handle) != 0

def ChannelSetVolume(handle, volume):
    return bass.BASS_ChannelSetAttribute(handle, BASS_ATTRIB_VOL, c_float(volume)) != 0

def ChannelGetVolume(handle):
    volume = c_float()
    if bass.BASS_ChannelGetAttribute(handle, BASS_ATTRIB_VOL, byref(volume)) != 0:
        return volume.value
    return None

def LoudnessStart(decoder, flags=BASS_LOUDNESS_INTEGRATED):
    return bassloud.BASS_Loudness_Start(c_ulong(decoder), c_ulong(flags), c_int(0))

def LoudnessDecode(decoder):
    buf_size = 44100
    buf = array.array('f', [0] * (buf_size // 4))
    buffer_address = buf.buffer_info()[0]
    while bass.BASS_ChannelGetData(c_ulong(decoder), c_void_p(buffer_address), c_ulong(buf_size)) >= 0:
        pass

def LoudnessGetLevel(handle, mode=BASS_LOUDNESS_INTEGRATED):
    level = c_float()
    result = bassloud.BASS_Loudness_GetLevel(c_ulong(handle), c_ulong(mode), byref(level))
    if not result:
        print(f"Failed to call BASS_Loudness_GetLevel: error {ErrorGetCode()}")
        return -14.0 # TODO return -inf
    return level.value

def LoudnessStop(handle):
    return bassloud.BASS_Loudness_Stop(c_ulong(handle))

def ChannelFree(handle):
    return bass.BASS_ChannelFree(c_ulong(handle))
