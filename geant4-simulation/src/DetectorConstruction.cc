// File: src/DetectorConstruction.cc
#include "DetectorConstruction.hh"
#include "G4Material.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"

DetectorConstruction::DetectorConstruction() {}
DetectorConstruction::~DetectorConstruction() {}

G4VPhysicalVolume* DetectorConstruction::Construct() {
    G4NistManager* nist = G4NistManager::Instance();

    G4Material* worldMat = nist->FindOrBuildMaterial("G4_AIR");
    G4Material* tungsten = nist->FindOrBuildMaterial("G4_W");

    G4double worldSize = 1.0 * m;
    G4Box* solidWorld = new G4Box("World", worldSize, worldSize, worldSize);
    G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld, worldMat, "World");
    G4VPhysicalVolume* physWorld = new G4PVPlacement(0, {}, logicWorld, "World", nullptr, false, 0);

    G4double radius = 7.5 * cm;
    G4double height = 60 * cm;
    G4Tubs* solidTarget = new G4Tubs("Target", 0, radius, height / 2.0, 0, 360 * deg);
    logicTarget = new G4LogicalVolume(solidTarget, tungsten, "Target");

    new G4PVPlacement(0, G4ThreeVector(0, 0, 0), logicTarget, "Target", logicWorld, false, 0);

    logicTarget->SetVisAttributes(G4VisAttributes::GetInvisible());

    return physWorld;
}
