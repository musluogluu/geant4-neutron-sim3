// File: src/SteppingAction.cc
#include "SteppingAction.hh"
#include "RunAction.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4SystemOfUnits.hh"
#include "G4EventManager.hh"
#include "G4RunManager.hh"
#include "G4ParticleDefinition.hh"
#include "G4ParticleTypes.hh"
#include <fstream>
#include <cmath>

SteppingAction::SteppingAction() {}
SteppingAction::~SteppingAction() {}

void SteppingAction::UserSteppingAction(const G4Step* step) {
    auto track = step->GetTrack();
    if (track->GetTrackStatus() == fStopAndKill &&
        track->GetDefinition() == G4Neutron::Definition() &&
        track->GetStepLength() > 0) {

        auto runAction = static_cast<RunAction*>(
            G4RunManager::GetRunManager()->GetUserRunAction());

        G4ThreeVector momDir = track->GetMomentumDirection();
        G4double energy = track->GetKineticEnergy() / MeV;

        G4double theta = momDir.theta() * 180. / CLHEP::pi;
        G4double phi = momDir.phi() * 180. / CLHEP::pi;

        runAction->GetNeutronLog() << energy << "," << theta << "," << phi << "\n";
    }
}
