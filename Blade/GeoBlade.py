# -*- coding: latin-1 -*-
# Test the finit element simulation for the blade
# Nous prenons la géométrie décrite dans "Definition of a 5-MW Reference Wind Turbine for
# Offshore System Development"

# Auteur: Hao BAI
# Date de création: 16/04/2018

import sys, os
cwd = os.getcwd()

import salome # Initialisation SALOME
salome.salome_init()

import GEOM # Interface Python de module GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")

import SMESH, SALOMEDS # Interface Python de module MESH
from salome.smesh import smeshBuilder
smesh = smeshBuilder.New(salome.myStudy)
from salome.StdMeshers import StdMeshersBuilder

from math import sin, cos, radians
#------------------------------------------------------------------------
#                              	   GEOMETRIE
#------------------------------------------------------------------------
# Repère globale
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# ======================== POINTS ========================
TipRad   = 63.0 # The distance from the rotor apex to the blade tip (meters)
HubRad   =  1.5 # The distance from the rotor apex to the blade root (meters)

BlFract = [0.000E+00, 3.250E-03, 1.951E-02, 3.577E-02, 5.203E-02, 6.829E-02, 8.455E-02, 1.008E-01, 1.171E-01, 1.334E-01, 1.496E-01, 1.659E-01, 1.821E-01, 1.984E-01, 2.147E-01, 2.309E-01, 2.472E-01, 2.634E-01, 2.960E-01, 3.285E-01, 3.610E-01, 3.935E-01, 4.260E-01, 4.586E-01, 4.911E-01, 5.236E-01, 5.561E-01, 5.886E-01, 6.212E-01, 6.537E-01, 6.862E-01, 7.187E-01, 7.512E-01, 7.838E-01, 8.163E-01, 8.488E-01, 8.813E-01, 8.976E-01, 9.138E-01, 9.301E-01, 9.382E-01, 9.464E-01, 9.545E-01, 9.626E-01, 9.707E-01, 9.789E-01, 9.870E-01, 9.951E-01, 1.000E+00]
Radius = [ HubRad + i * (TipRad-HubRad) for i in BlFract]


# ======================== POINTS ========================
# Blade
list_blade = []
for elem in Radius:
    node = geompy.MakeVertex(0., 0., elem)
    list_blade.append(node)


# ======================== LIGNES ========================
# +++ Blade
blade = geompy.MakePolyline(list_blade, False) # Créer une liger fermée si 'True'
id_blade = geompy.addToStudy(blade, "Blade")
gg.createAndDisplayGO(id_blade)


# ======================== GROUPES ========================
# +++ blade
# |-- Groupe des noeuds
vertexIDs = geompy.SubShapeAllIDs(blade, geompy.ShapeType["VERTEX"])
        
Groupe_BldRoot = geompy.CreateGroup(blade, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldRoot, [vertexIDs[0]])
geompy.addToStudyInFather(blade, Groupe_BldRoot, 'Groupe_BldRoot')

Groupe_BldTip = geompy.CreateGroup(blade, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldTip, [vertexIDs[-1]])
geompy.addToStudyInFather(blade, Groupe_BldTip, 'Groupe_BldTip')
# |-- Groupe des arrêtes
edgeIDs = geompy.SubShapeAllIDs(blade, geompy.ShapeType["EDGE"])

segments = []
i = 0
for edgeid in edgeIDs:
    i = i + 1
    temp = geompy.CreateGroup(blade, geompy.ShapeType["EDGE"])
    segments.append(temp)
    geompy.UnionIDs(temp, [edgeid])
    geompy.addToStudyInFather(blade, temp, 'Seg_'+str(i))


#------------------------------------------------------------------------
#                              	    MAILLAGE
#------------------------------------------------------------------------
# ======================== CONFIGURATION ========================
# Algorithme 1D
algo_1D = smesh.CreateHypothesis('Regular_1D')
smesh.SetName(algo_1D, 'Algorithme 1D_Wire Discretisation')

# Hypothèse 1D
hyp_1D = smesh.CreateHypothesis('NumberOfSegments')
# hyp_1D.SetLength(1.0)
hyp_1D.SetNumberOfSegments(1)
smesh.SetName(hyp_1D, 'Nb. Segments_1')

# ======================== ATTRIBUTION ========================
# Définir le maillage
maillage = smesh.Mesh(blade)

# Associer les algoritmes et les hypothèses correspondants
maillage.AddHypothesis(algo_1D)
maillage.AddHypothesis(hyp_1D)

# ======================== CALCUL ========================
maillage.Compute()
smesh.SetName(maillage, 'Maillage')

# ======================== GROUPES ========================
# Noeuds
maillage.GroupOnGeom(Groupe_BldRoot, 'Groupe_BldRoot', SMESH.NODE)
maillage.GroupOnGeom(Groupe_BldTip, 'Groupe_BldTip', SMESH.NODE)


# Lignes
maillage.GroupOnGeom(blade, 'Blade', SMESH.EDGE)
j = 0
for seg in segments:
    j = j + 1
    maillage.GroupOnGeom(seg, 'Seg_'+str(j), SMESH.EDGE)


# ======================== EXPORTATION ========================
maillage.ExportMED(r'./Eolien/Code_Aster/Blade/Maillage.mmed', False, SMESH.MED_V2_2, 1, 
                   None ,1)
print ('Mesh has been exported to ./Eolien/Code_Aster/Blade/Maillage.mmed')
