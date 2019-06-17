#include <Math/LorentzVector.h>
#include <Math/PtEtaPhiM4D.h>
#include <TLorentzVector.h>
#include <TVector3.h>

std::pair<TLorentzVector,TLorentzVector>
Do2BodyDecay(TLorentzVector p4_mother, double m1, double m2, double cosTheta=-999, double phi=-999);

std::tuple<TLorentzVector,TLorentzVector,TLorentzVector>
DoDalitz(TLorentzVector p4_mother, double me, double mX, bool useVDM=true);

template <class T>
TLorentzVector LVtoTLV(ROOT::Math::LorentzVector<T> p){
    return TLorentzVector(p.x(), p.y(), p.z(), p.t());
}

template <class T>
ROOT::Math::LorentzVector<T> TLVtoLV(TLorentzVector p){
    return ROOT::Math::LorentzVector<T>(p.Pt(), p.Eta(), p.Phi(), p.M());
}

// support also ROOT::Math::LorentzVector
template <class T>
std::pair<ROOT::Math::LorentzVector<T>, ROOT::Math::LorentzVector<T> >
Do2BodyDecay(ROOT::Math::LorentzVector<T> p4_mother, double m1, double m2, double cosTheta=-999, double phi=-999){
    TLorentzVector p1,p2;
    std::tie(p1,p2) = Do2BodyDecay(LVtoTLV(p4_mother), m1, m2, cosTheta, phi);
    ROOT::Math::LorentzVector<T> q1 = TLVtoLV<T>(p1);
    ROOT::Math::LorentzVector<T> q2 = TLVtoLV<T>(p2);
    // return std::pair<ROOT::Math::LorentzVector<T>, ROOT::Math::LorentzVector<T> >(q1, q2);
    return std::pair(q1, q2);
}

template <class T>
std::tuple<ROOT::Math::LorentzVector<T>, ROOT::Math::LorentzVector<T>, ROOT::Math::LorentzVector<T> >
DoDalitz(ROOT::Math::LorentzVector<T> p4_mother, double me, double mX, bool useVDM=true){
    TLorentzVector p1,p2,p3;
    std::tie(p1,p2,p3) = DoDalitz(LVtoTLV(p4_mother), me, mX, useVDM);
    ROOT::Math::LorentzVector<T> q1 = TLVtoLV<T>(p1);
    ROOT::Math::LorentzVector<T> q2 = TLVtoLV<T>(p2);
    ROOT::Math::LorentzVector<T> q3 = TLVtoLV<T>(p3);
    return std::make_tuple(q1, q2, q3);
}

