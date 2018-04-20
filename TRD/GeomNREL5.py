# -*- coding: latin-1 -*-
# Générer la géométrie pour un modèle RDM
# Nous prenons la géométrie décrite dans "Definition of a 5-MW Reference Wind Turbine for
# Offshore System Development"

# Auteur: Hao BAI
# Date de création: 27/10/2017

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
import math

#------------------------------------------------------------------------
#                              	   GEOMETRIE
#------------------------------------------------------------------------
# Repère globale
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# ======================== POINTS ========================
TowerHt  = 87.6 # Height of tower above ground level [onshore] or MSL [offshore] (meters)
HtFract = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
Elevation = [i * TowerHt for i in HtFract]

NacCMxn  =  1.9 # Downwind distance from the tower-top to the nacelle CM (meters)
NacCMyn  =  0.0 # Lateral  distance from the tower-top to the nacelle CM (meters)
NacCMzn  =  1.75 # Vertical distance from the tower-top to the nacelle CM (meters)

Twr2Shft =  1.96256 # Vertical distance from the tower-top to the rotor shaft (meters)
ShftTilt = -5.0 # Rotor shaft tilt angle (degrees)
OverHang = -5.0191 # Distance from yaw axis to rotor apex [3 blades] (meters)
HubCM    =  0.0 # Distance from rotor apex to hub mass [positive downwind] (meters)

TipRad   = 63.0 # The distance from the rotor apex to the blade tip (meters)
HubRad   =  1.5 # The distance from the rotor apex to the blade root (meters)
PreCone  = -2.5 # Blade 1, 2 and 3 cone angle (degrees)
BldCM = 20.475 # Distance from the blade root to the blade CM (meters)
BldAngle = 120.0 # The angle between 2 blades (degrees)

# ======================== POINTS ========================
# Tower
list_tower = []
for elem in Elevation:
    node = geompy.MakeVertex(0., 0., elem)
    list_tower.append(node)

# Nacelle
nacCM = geompy.MakeVertex(NacCMxn, NacCMyn, TowerHt+NacCMzn)

# Shaft
shft = geompy.MakeVertex(0., 0., TowerHt+Twr2Shft)

# Rotor apex
apexXs = OverHang*cos(radians(ShftTilt))
apexYs = 0.0
apexZs = TowerHt + Twr2Shft + OverHang*sin(radians(ShftTilt))
# apex = geompy.MakeVertex(apexXs, apexYs, apexZs)

# Hub
if HubCM != 0.0:    
    hubCMxh = apexXs + HubCM*cos(radians(ShftTilt))
    hubCMyh = apexYs
    hubCMzh = apexZs + HubCM*sin(radians(ShftTilt))
    hubCM = geompy.MakeVertex(hubCMxh, hubCMyh, hubCMzh)
else:
    hubCM = geompy.MakeVertex(apexXs, apexYs, apexZs)

# Rotor axis
rotorAxis = geompy.MakeVector(shft, hubCM)
geompy.addToStudy(rotorAxis, "rotorAxis")

# Blade 1
bldCMXc1 = apexXs - (HubRad+BldCM)*sin(radians(PreCone))
bldCMYc1 = apexYs
bldCMZc1 = apexZs + (HubRad+BldCM)*cos(radians(PreCone))
bldCM1 = geompy.MakeVertex(bldCMXc1, bldCMYc1, bldCMZc1)

bldRootXc1 = apexXs + HubRad*sin(radians(PreCone))
bldRootYc1 = apexYs
bldRootZc1 = apexZs + HubRad*cos(radians(PreCone))
bldRoot1 = geompy.MakeVertex(bldRootXc1, bldRootYc1, bldRootZc1)

# Blade 2
bldCM2 = geompy.MakeRotation(bldCM1, rotorAxis, radians(-BldAngle))
geompy.addToStudy(bldCM2, "bldCM2")

bldRoot2 = geompy.MakeRotation(bldRoot1, rotorAxis, radians(-BldAngle))
geompy.addToStudy(bldRoot2, "bldRoot2")

# Blade 3
bldCM3 = geompy.MakeRotation(bldCM1, rotorAxis, radians(BldAngle))
geompy.addToStudy(bldCM3, "bldCM3")

bldRoot3 = geompy.MakeRotation(bldRoot1, rotorAxis, radians(BldAngle))
geompy.addToStudy(bldRoot3, "bldRoot3")

# ======================== LIGNES ========================
# +++ Tower
tower = geompy.MakePolyline(list_tower, False) # Créer une liger fermée si 'True'
id_tower = geompy.addToStudy(tower, "Tower")
# gg.createAndDisplayGO(id_tower)

# +++ Nacelle C.M. & Hub C.M.
id_nacCM = geompy.addToStudy(nacCM, "NacCM")
id_hubCM = geompy.addToStudy(hubCM, "HubCM")
# gg.createAndDisplayGO(id_hubCM)

# +++ Blade 1
id_bldCM1 = geompy.addToStudy(bldCM1, "BldCM1")
id_bldRoot1 = geompy.addToStudy(bldRoot1, "BldRoot1")
# +++ Blade 2
id_bldCM2 = geompy.addToStudy(bldCM2, "BldCM2")
id_bldRoot2 = geompy.addToStudy(bldRoot2, "BldRoot2")
# +++ Blade 3
id_bldCM3 = geompy.addToStudy(bldCM3, "BldCM3")
id_bldRoot3 = geompy.addToStudy(bldRoot3, "BldRoot3")

# ======================== GROUPES ========================
# +++ tower
# |-- Groupe des noeuds
vertexIDs = geompy.SubShapeAllIDs(tower, geompy.ShapeType["VERTEX"])

Groupe_TwrRoot = geompy.CreateGroup(tower, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_TwrRoot, [vertexIDs[0]])
geompy.addToStudyInFather(tower, Groupe_TwrRoot, 'Groupe_TwrRoot')

Groupe_TwrTip = geompy.CreateGroup(tower, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_TwrTip, [vertexIDs[-1]])
geompy.addToStudyInFather(tower, Groupe_TwrTip, 'Groupe_TwrTip')
# |-- Groupe des arrêtes
edgeIDs = geompy.SubShapeAllIDs(tower, geompy.ShapeType["EDGE"])

segments = []
i = 0
for edgeid in edgeIDs:
    i = i + 1
    temp = geompy.CreateGroup(tower, geompy.ShapeType["EDGE"])
    segments.append(temp)
    geompy.UnionIDs(temp, [edgeid])
    geompy.addToStudyInFather(tower, temp, 'Seg_'+str(i))

# +++ bld: Groupe des noeuds
# |-- Blade 1
# |-- Blade 2
# |-- Blade 3

# ======================== ASSEMBLAGE ========================
windplant = geompy.MakeCompound([tower, nacCM, hubCM, bldCM1, bldCM2, bldCM3])
id_windplant = geompy.addToStudy(windplant, "WindPlant")
gg.createAndDisplayGO(id_windplant)

# Récupérer les groupes précédement définies
list_windplant = [tower, Groupe_TwrRoot, Groupe_TwrTip] + segments + [nacCM, hubCM,
                  bldCM1, bldCM2, bldCM3]

geompy.RestoreGivenSubShapes(windplant, list_windplant, \
                             GEOM.FSM_GetInPlace, False, False)

# Ajouter des groupes pour définir la liaison rigide
vertexIDs = geompy.SubShapeAllIDs(windplant, geompy.ShapeType["VERTEX"])

Groupe_HubToBlade1 = geompy.CreateGroup(windplant, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_HubToBlade1, [vertexIDs[-4], vertexIDs[-3]])
geompy.addToStudyInFather( windplant, Groupe_HubToBlade1, 'Groupe_HubToBlade1')

Groupe_HubToBlade2 = geompy.CreateGroup(windplant, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_HubToBlade2, [vertexIDs[-4], vertexIDs[-2]])
geompy.addToStudyInFather( windplant, Groupe_HubToBlade2, 'Groupe_HubToBlade2')

Groupe_HubToBlade3 = geompy.CreateGroup(windplant, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_HubToBlade3, [vertexIDs[-4], vertexIDs[-1]])
geompy.addToStudyInFather( windplant, Groupe_HubToBlade3, 'Groupe_HubToBlade3')

Groupe_NacelleToHub = geompy.CreateGroup(windplant, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_NacelleToHub, [vertexIDs[-5], vertexIDs[-4]])
geompy.addToStudyInFather( windplant, Groupe_NacelleToHub, 'Groupe_NacelleToHub')

Groupe_TowerTipToNacelle = geompy.CreateGroup(windplant, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_TowerTipToNacelle, [vertexIDs[-6], vertexIDs[-5]])
geompy.addToStudyInFather( windplant, Groupe_TowerTipToNacelle, 'Groupe_TowerTipToNacelle')



#------------------------------------------------------------------------
#                              	    MAILLAGE
#------------------------------------------------------------------------
# ======================== CONFIGURATION ========================
# Algorithme 1D
algo_1D = smesh.CreateHypothesis('Regular_1D')
smesh.SetName(algo_1D, 'Algorithme 1D_Wire Discretisation')

# Hypothèse 1D
hyp_1D = smesh.CreateHypothesis('LocalLength')
hyp_1D.SetLength(0.1) 
hyp_1D.SetPrecision(1e-9)
smesh.SetName(hyp_1D, 'Local Length_1')

# ======================== ATTRIBUTION ========================
# Définir le maillage
maillage = smesh.Mesh(windplant)

# Associer les algoritmes et les hypothèses correspondants
maillage.AddHypothesis(algo_1D)
maillage.AddHypothesis(hyp_1D)

# ======================== CALCUL ========================
maillage.Compute()
smesh.SetName(maillage, 'Maillage')

# ======================== GROUPES ========================
# Noeuds
maillage.GroupOnGeom(Groupe_TwrRoot, 'Groupe_TwrRoot', SMESH.NODE)
maillage.GroupOnGeom(Groupe_TwrTip, 'Groupe_TwrTip', SMESH.NODE)
maillage.GroupOnGeom(nacCM, 'NacCM', SMESH.NODE)
maillage.GroupOnGeom(hubCM, 'HubCM', SMESH.NODE)
maillage.GroupOnGeom(bldCM1, 'BldCM1', SMESH.NODE)
maillage.GroupOnGeom(bldCM2, 'BldCM2', SMESH.NODE)
maillage.GroupOnGeom(bldCM3, 'BldCM3', SMESH.NODE)
maillage.GroupOnGeom(Groupe_HubToBlade1, 'Groupe_HubToBlade1', SMESH.NODE)
maillage.GroupOnGeom(Groupe_HubToBlade2, 'Groupe_HubToBlade2', SMESH.NODE)
maillage.GroupOnGeom(Groupe_HubToBlade3, 'Groupe_HubToBlade3', SMESH.NODE)
maillage.GroupOnGeom(Groupe_NacelleToHub, 'Groupe_NacelleToHub', SMESH.NODE)
maillage.GroupOnGeom(Groupe_TowerTipToNacelle, 'Groupe_TowerTipToNacelle', SMESH.NODE)

# Lignes
maillage.GroupOnGeom(tower, 'Tower', SMESH.EDGE)
j = 0
for seg in segments:
    j = j + 1
    maillage.GroupOnGeom(seg, 'Seg_'+str(j), SMESH.EDGE)

# ======================== EXPORTATION ========================
maillage.ExportMED(r'./Eolien/Code_Aster/TRD/NREL5.mmed', False, SMESH.MED_V2_2, 1, 
                   None ,1)
print ('Mesh has been exported to ./Eolien/Code_Aster/TRD/NREL5.mmed')
