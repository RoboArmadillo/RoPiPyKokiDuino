from ctypes import *
import os
from opencv_pytypes import IplImageType
import cv2

KOKI_MARKER_GRID_WIDTH = 10

### GLib structs ###

# GLib 'primitive' datatypes
class gchar_p(c_char_p): pass
class guint(c_uint): pass
class gpointer(c_void_p): pass


class GArray(Structure):
    "A glib GArray"
    _fields_ = [("data", gchar_p), ("len", guint)]


class GSList(Structure):
    "A glib GSList"
    pass
GSList._fields_ = [("data", gpointer), ("next", POINTER(GSList))]

class GPtrArray(Structure):
    "A glib GPtrArray"
    _fields_ = [("pdata", POINTER(gpointer)), ("len", guint)]


class Bearing(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]

    def __repr__(self):
        return "Bearing (x=%f, y=%f, z=%f)" % (self.x, self.y, self.z)


class Point2Di(Structure):
    _fields_ = [("x", c_uint16), ("y", c_uint16)]

    def __repr__(self):
        return "Point2Di (x=%d, y=%d)" % (self.x.value, self.y.value)


class Point2Df(Structure):
    _fields_ = [("x", c_float), ("y", c_float)]

    def __repr__(self):
        return "Point2Df (x=%f, y=%f)" % (self.x, self.y)


class Point3Df(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]

    def __repr__(self):
        return "Point3Df (x=%f, y=%f, z=%f)" % (self.x, self.y, self.z)


class MarkerVertex(Structure):
    _fields_ = [("image", Point2Df), ("world", Point3Df)]

    def __repr__(self):
        return "Marker Vertex (image = %s, world = %s)" % (self.image, self.world)


class MarkerRotation(Structure):

    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]

    def __repr__(self):
        return "MarkerRotation (x=%f, y=%f, z=%f)" % (self.x, self.y, self.z)


class Marker(Structure):
    _fields_ = [("code", c_uint8), ("image", Point2Df) ,("world", Point3Df),
                ("rotation_offset", c_float), ("rotation", MarkerRotation),
                ("bearing", Bearing), ("distance", c_float)]

    def __repr__(self):
        return "Marker (\n\tcode=%d,\n\tcentre = %s,\n\tbearing = %s,\n\tdistance=%f,\n\trotation = %s,\n\trotation_offset=%f,\n\tvertices = [\n\t\t%s,\n\t\t%s,\n\t\t%s,\n\t\t%s])" % (self.code, self.centre, self.bearing, self.distance, self.rotation, self.rotation_offset, self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3])


class ClipRegion(Structure):
    _fields_ = [("min", Point2Di), ("max", Point2Di), ("mass", c_uint16)]

    def __repr__(self):
        return "ClipRegion (mass=%d, min = %s, max = %s)" % (self.mass.value, self.min, self.max)


class Cell(Structure):
    _fields_ = [("sum", c_uint), ("num_pixels", c_uint16), ("val", c_uint8)]

    def __repr__(self):
        return "Cell (num_pixels=%d, sum=%d, val=%d)" % (self.num_pixels.value, self.sum, self.val.value)


Grid = (Cell * KOKI_MARKER_GRID_WIDTH) * KOKI_MARKER_GRID_WIDTH

def GridRepr(self):
    ret = "Grid:\n["
    for i in range(KOKI_MARKER_GRID_WIDTH):
        ret += "["
        for j in range(KOKI_MARKER_GRID_WIDTH):
            ret += "(%d, %d, %d),\t" % (self[i][j].num_pixels.value, self[i][j].sum, self[i][j].val.value)
        ret = ret[:-3]
        ret += "],\n "

    ret = ret[:-3]
    ret += "]"
    return ret

Grid.__repr__ = GridRepr


class CameraParams(Structure):
    _fields_ = [("principal_point", Point2Df), ("focal_length", Point2Df), ("size", Point2Di)]

    def __repr__(self):
        return "CameraParams (focal_length = %s, principal_point = %s, size = %s)" % (self.focal_length, self.principal_point, self.size)


class Quad(Structure):
    _fields_ = [("vertices", Point2Df * 4), ("links", POINTER(GSList) * 4)]

    def __repr__(self):
        return "Quad (links = [%s, %s, %s, %s], vertices = [%s, %s, %s, %s])" % (self.links[0], self.links[1], self.links[2], self.links[3], self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3])


class LabelledImage(Structure):
    _fields_ = [("data", POINTER(c_uint16)),  ("w", c_uint16), ("h", c_uint16),
                ("clips", POINTER(GArray)), ("aliases", POINTER(GArray))]

    def __repr__(self):
        return "LabelledImage (aliases = %s, clips = %s, data = %s, w=%s, h=%s)" % (self.aliases, self.clips, self.data, self.w, self.h)


class Buffer(Structure):
    _fields_ = [("length", c_size_t), ("start", POINTER(c_uint8))]

    def __repr__(self):
        return "Buffer (length=%s, start = %s)" % (self.length, self.start)

class LoggerCallbacks(Structure):
    _fields_ = [ ("init", CFUNCTYPE(c_void_p) ),
                 ("log", CFUNCTYPE(c_char_p, c_void_p, c_void_p) ) ]


class Koki(Structure):
    _fields_ = [ ("logger", LoggerCallbacks),
                 ("logger_userdata", c_void_p) ]


WIDTH_FROM_CODE_FUNC = CFUNCTYPE(c_float, c_int)

def cv_ipl_p_extract(pyipl):
    "Extract the IplImage pointer from a PyObject wrapping an IplImage"

    p = cast( c_void_p( id(pyipl) ),
              POINTER( IplImageType ) )

    return p[0].a

class PyKoki:
    def __init__(self, libdir = "/usr/lib"):
        self._load_library(libdir)
        self._setup_library()

        # Create ourselves a context
        self.ctx = self.libkoki.koki_new()

    def __del__(self):
        self.libkoki.koki_destroy( self.ctx )

    def _load_library(self, directory):
        libkoki = None

        path = os.path.join(directory, "libkoki.so")

        if os.path.exists(path):
            libkoki = cdll.LoadLibrary(path)

        if libkoki == None:
            raise Exception("pykoki: libkoki.so not found")

        self.libkoki = libkoki

    def _setup_library(self):
        l = self.libkoki

        # koki_t* koki_new( void );
        l.koki_new.argtypes = []
        l.koki_new.restype = POINTER(Koki)

        # void koki_destroy( koki_t* koki );
        l.koki_destroy.argtypes = [ POINTER(Koki) ]

        # GPtrArray* koki_find_markers(IplImage *frame, float marker_width,
        #                              koki_camera_params_t *params)
        l.koki_find_markers.argtypes = [ POINTER(Koki), c_void_p, c_float, POINTER(CameraParams) ]
        l.koki_find_markers.restype = POINTER(GPtrArray)


        # GPtrArray* koki_find_markers_fp(IplImage *frame, float (*fp)(int),
        #                                 koki_camera_params_t *params)
        l.koki_find_markers_fp.argtypes = [ POINTER(Koki), c_void_p, WIDTH_FROM_CODE_FUNC, POINTER(CameraParams) ]
        l.koki_find_markers_fp.restype = POINTER(GPtrArray)

        # void koki_markers_free(GPtrArray *markers)
        l.koki_markers_free.argtypes = [POINTER(GPtrArray)]

        # void koki_image_free(IplImage *image)
        l.koki_image_free.argtypes = [c_void_p]

        ### crc12.h ###

        # uint16_t koki_crc12 (uint8_t input)
        l.koki_crc12.argtypes = [c_uint8]
        l.koki_crc12.restype = c_uint16


    def _make_copy(self, o):
        ret = type(o)()
        pointer(ret)[0] = o
        return ret

    def image_free(self, img):
        self.libkoki.koki_image_free(img)

    def find_markers(self, image, marker_width, params):
        if isinstance(image, cv2.cv.iplimage):
            image = cv_ipl_p_extract(image)

        markers = self.libkoki.koki_find_markers(self.ctx, image, marker_width, params)

        ret = []

        for i in range(markers.contents.len.value):
            # cast the pointer tp a marker pointer, and append to a list
            # of actual (dereferenced) markers
            marker = cast(markers.contents.pdata[i], POINTER(Marker)).contents
            ret.append(self._make_copy(marker))

        # free the markers -- we only need the Python list
        self.libkoki.koki_markers_free(markers)

        return ret

    def find_markers_fp(self, image, func, params):
        if isinstance(image, cv2.cv.iplimage):
            image = cv_ipl_p_extract(image)

        markers = self.libkoki.koki_find_markers_fp(self.ctx, image, WIDTH_FROM_CODE_FUNC(func), params)

        ret = []

        for i in range(markers.contents.len.value):
            # cast the pointer tp a marker pointer, and append to a list
            # of actual (dereferenced) markers
            marker = cast(markers.contents.pdata[i], POINTER(Marker)).contents
            ret.append(self._make_copy(marker))

        # free the markers -- we only need the Python list
        self.libkoki.koki_markers_free(markers)

        return ret

    def crc12(self, n):
        return self.libkoki.koki_crc12(n)
