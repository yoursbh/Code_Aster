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
#------------------------------------------------------------------------
#                              	   GEOMETRIE
#------------------------------------------------------------------------
# Le mât est composé par plusiers parties:
# Mât =   Tour (de 0,00m à 87,6m)
#		+ 

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
BldAngle = 120.0 # The angle between 2 blades (degrees)

# ======================== POINTS ========================
# Tower
list_tower = []
for elem in Elevation:
    node = geompy.MakeVertex(0., 0., elem)
    list_tower.append(node)

# Nacelle
nacelleCM = geompy.MakeVertex(NacCMxn, NacCMyn, TowerHt+NacCMzn)

# Shaft and Rotor apex
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

# Blade 1
bldTipXc1 = apexXs + TipRad*sin(radians(PreCone))
bldTipYc1 = apexYs
bldTipZc1 = apexZs + TipRad*cos(radians(PreCone))
bldTip1 = geompy.MakeVertex(bldTipXc1, bldTipYc1, bldTipZc1)

bldRootXc1 = apexXs + HubRad*sin(radians(PreCone))
bldRootYc1 = apexYs
bldRootZc1 = apexZs + HubRad*cos(radians(PreCone))
bldRoot1 = geompy.MakeVertex(bldRootXc1, bldRootYc1, bldRootZc1)

# Blade 2
bldTipXc2 = apexXs + TipRad*sin(radians(PreCone))
bldTipYc2 = apexYs + TipRad*sin(radians(-BldAngle))
bldTipZc2 = apexZs - TipRad*cos(radians(PreCone))
bldTip2 = geompy.MakeVertex(bldTipXc2, bldTipYc2, bldTipZc2)

bldRootXc2 = apexXs + HubRad*sin(radians(PreCone))
bldRootYc2 = apexYs + HubRad*sin(radians(-BldAngle))
bldRootZc2 = apexZs - HubRad*cos(radians(PreCone))
bldRoot2 = geompy.MakeVertex(bldRootXc2, bldRootYc2, bldRootZc2)

# Blade 3
bldTipXc3 = apexXs + TipRad*sin(radians(PreCone))
bldTipYc3 = apexYs + TipRad*sin(radians(BldAngle))
bldTipZc3 = apexZs - TipRad*cos(radians(PreCone))
bldTip3 = geompy.MakeVertex(bldTipXc3, bldTipYc3, bldTipZc3)

bldRootXc3 = apexXs + HubRad*sin(radians(PreCone))
bldRootYc3 = apexYs + HubRad*sin(radians(BldAngle))
bldRootZc3 = apexZs - HubRad*cos(radians(PreCone))
bldRoot3 = geompy.MakeVertex(bldRootXc3, bldRootYc3, bldRootZc3)


# ======================== LIGNES ========================
# +++ Tower
tower = geompy.MakePolyline(list_tower, False) # Créer une liger fermée si 'True'
id_tower = geompy.addToStudy(tower, "Tower")
# gg.createAndDisplayGO(id_tower)

# +++ Hub C.M.
id_hubCM = geompy.addToStudy(hubCM, "HubCM")
# gg.createAndDisplayGO(id_hubCM)

# +++ Blade 1
bld1 = geompy.MakePolyline([bldRoot1, bldTip1], False)
id_bld1 = geompy.addToStudy(bld1, "Blade1")
# gg.createAndDisplayGO(id_bld1)
# +++ Blade 2
bld2 = geompy.MakePolyline([bldRoot2, bldTip2], False)
id_bld2 = geompy.addToStudy(bld2, "Blade2")
# gg.createAndDisplayGO(id_bld2)
# +++ Blade 3
bld3 = geompy.MakePolyline([bldRoot3, bldTip3], False)
id_bld3 = geompy.addToStudy(bld3, "Blade3")
# gg.createAndDisplayGO(id_bld3)

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
vertexIDs = geompy.SubShapeAllIDs(bld1, geompy.ShapeType["VERTEX"])
        
Groupe_BldRoot1 = geompy.CreateGroup(bld1, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldRoot1, [vertexIDs[0]])
geompy.addToStudyInFather(bld1, Groupe_BldRoot1, 'Groupe_BldRoot1')

Groupe_BldTip1 = geompy.CreateGroup(bld1, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldTip1, [vertexIDs[-1]])
geompy.addToStudyInFather(bld1, Groupe_BldTip1, 'Groupe_BldTip1')

# |-- Blade 2
vertexIDs = geompy.SubShapeAllIDs(bld2, geompy.ShapeType["VERTEX"])
        
Groupe_BldRoot2 = geompy.CreateGroup(bld2, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldRoot2, [vertexIDs[0]])
geompy.addToStudyInFather(bld2, Groupe_BldRoot2, 'Groupe_BldRoot2')

Groupe_BldTip2 = geompy.CreateGroup(bld2, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldTip2, [vertexIDs[-1]])
geompy.addToStudyInFather(bld2, Groupe_BldTip2, 'Groupe_BldTip2')

# |-- Blade 3
vertexIDs = geompy.SubShapeAllIDs(bld3, geompy.ShapeType["VERTEX"])
        
Groupe_BldRoot3 = geompy.CreateGroup(bld3, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldRoot3, [vertexIDs[0]])
geompy.addToStudyInFather(bld3, Groupe_BldRoot3, 'Groupe_BldRoot3')

Groupe_BldTip3 = geompy.CreateGroup(bld3, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_BldTip3, [vertexIDs[-1]])
geompy.addToStudyInFather(bld3, Groupe_BldTip3, 'Groupe_BldTip3')


# ======================== ASSEMBLAGE ========================
windplant = geompy.MakeCompound([tower, hubCM, bld1, bld2, bld3])
id_windplant = geompy.addToStudy(windplant, "WindPlant")
gg.createAndDisplayGO(id_windplant)

# Récupérer les groupes précédement définies
list_windplant = [tower, Groupe_TwrRoot, Groupe_TwrTip] + segments + [hubCM, bld1,
                  Groupe_BldRoot1, Groupe_BldTip1, bld2, Groupe_BldRoot2, Groupe_BldTip2,
                  bld3, Groupe_BldRoot3, Groupe_BldTip3]

geompy.RestoreGivenSubShapes(windplant, list_windplant, \
                             GEOM.FSM_GetInPlace, False, False)

# Ajouter un groupe de rotor: réservé à définir la liaison rigide
vertexIDs = geompy.SubShapeAllIDs(windplant, geompy.ShapeType["VERTEX"])

Groupe_Rotor = geompy.CreateGroup(windplant, geompy.ShapeType["VERTEX"])
geompy.UnionIDs(Groupe_Rotor, [vertexIDs[-8], vertexIDs[-7], vertexIDs[-6], vertexIDs[-4],
                vertexIDs[-2]])
geompy.addToStudyInFather( windplant, Groupe_Rotor, 'Groupe_Rotor')

# Ajouiter un groupe de toutes les pâles
edgeIDs = geompy.SubShapeAllIDs(windplant, geompy.ShapeType["EDGE"])

Groupe_AllBlades = geompy.CreateGroup(windplant, geompy.ShapeType["EDGE"])
geompy.UnionIDs(Groupe_AllBlades, edgeIDs[-3:])
geompy.addToStudyInFather( windplant, Groupe_AllBlades, 'Groupe_AllBlades')


#------------------------------------------------------------------------
#                              	    MAILLAGE
#------------------------------------------------------------------------
# ======================== CONFIGURATION ========================
# Algorithme 1D
algo_1D = smesh.CreateHypothesis('Regular_1D')
smesh.SetName(algo_1D, 'Algorithme 1D_Wire Discretisation')

# Hypothèse 1D
hyp_1D = smesh.CreateHypothesis('LocalLength')
hyp_1D.SetLength(5) 
hyp_1D.SetPrecision(1e-7)
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
maillage.GroupOnGeom(hubCM, 'HubCM', SMESH.NODE)
maillage.GroupOnGeom(Groupe_BldRoot1, 'Groupe_BldRoot1', SMESH.NODE)
maillage.GroupOnGeom(Groupe_BldTip1, 'Groupe_BldTip1', SMESH.NODE)
maillage.GroupOnGeom(Groupe_BldRoot2, 'Groupe_BldRoot2', SMESH.NODE)
maillage.GroupOnGeom(Groupe_BldTip2, 'Groupe_BldTip2', SMESH.NODE)
maillage.GroupOnGeom(Groupe_BldRoot3, 'Groupe_BldRoot3', SMESH.NODE)
maillage.GroupOnGeom(Groupe_BldTip3, 'Groupe_BldTip3', SMESH.NODE)
maillage.GroupOnGeom(Groupe_Rotor, 'Groupe_Rotor', SMESH.NODE)

# Lignes
maillage.GroupOnGeom(tower, 'Tower', SMESH.EDGE)
maillage.GroupOnGeom(bld1, 'Blade1', SMESH.EDGE)
maillage.GroupOnGeom(bld2, 'Blade2', SMESH.EDGE)
maillage.GroupOnGeom(bld3, 'Blade3', SMESH.EDGE)
maillage.GroupOnGeom(Groupe_AllBlades, 'Groupe_AllBlades', SMESH.EDGE)
j = 0
for seg in segments:
    j = j + 1
    maillage.GroupOnGeom(seg, 'Seg_'+str(j), SMESH.EDGE)


# ======================== EXPORTATION ========================
maillage.ExportMED(r'./Eolien/Code_Aster/TRD/Maillage.mmed', False, SMESH.MED_V2_2, 1, 
                   None ,1)
print ('Mesh has been exported to ./Eolien/Code_Aster/TRD/Maillage.mmed')
