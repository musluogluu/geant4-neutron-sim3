// File: src/PrimaryGeneratorAction.cc
#include "PrimaryGeneratorAction.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"
#include "G4Event.hh"
#include "Randomize.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction() {
    fParticleGun = new G4ParticleGun(1);
    fEventCounter = 0;
    fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0., 0., 1.));
    fParticleGun->SetParticleEnergy(1.0 * GeV);
    fParticleGun->SetParticlePosition(G4ThreeVector(0., 0., -35.0 * cm));
}

PrimaryGeneratorAction::~PrimaryGeneratorAction() {
    delete fParticleGun;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent) {
    G4ParticleDefinition* particle;
    if (fEventCounter < 1000) {
        particle = G4ParticleTable::GetParticleTable()->FindParticle("proton");
    } else {
        particle = G4ParticleTable::GetParticleTable()->FindParticle("pi+");
    }
    fParticleGun->SetParticleDefinition(particle);
    fParticleGun->GeneratePrimaryVertex(anEvent);
    fEventCounter++;
}
