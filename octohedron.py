from ctypes import *
from openctm import *
import polyhedra, blob

verts, faces = polyhedra.octohedron() 
pVerts = blob.make_blob(verts, c_float)
pFaces = blob.make_blob(faces, c_uint)
pNormals = POINTER(c_float)()
ctm = ctmNewContext(CTM_EXPORT)
ctmDefineMesh(ctm, pVerts, len(verts), pFaces, len(faces), pNormals)
ctmSave(ctm, "octohedron.ctm")
ctmFreeContext(ctm)
