// File: src/RunAction.cc
#include "RunAction.hh"
#include "G4Run.hh"
#include <iostream>

RunAction::RunAction() {}
RunAction::~RunAction() {
    if (neutronLog.is_open()) neutronLog.close();
}

void RunAction::BeginOfRunAction(const G4Run*) {
    neutronLog.open("neutron_output.csv");
    neutronLog << "Energy(MeV),Theta(deg),Phi(deg)\n";
}

void RunAction::EndOfRunAction(const G4Run*) {
    neutronLog.close();
}

std::ofstream& RunAction::GetNeutronLog() {
    return neutronLog;
}
