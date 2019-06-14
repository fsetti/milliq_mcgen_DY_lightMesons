#include <TLorentzVector.h>
#include <TVector3.h>
#include <TF1.h>
#include <TRandom.h>
#include <iostream>
#include <utility>
#include <cmath>

std::pair<TLorentzVector,TLorentzVector>
Do2BodyDecay(TLorentzVector p4_mother, double m1, double m2, double cosTheta=-999, double phi=-999){
    // get four-momenta p1,p2 of 2 daughter particles in decay m -> d1 + d2
    // p4_mother is four momentum of mother particle
    // m1, m2 are masses of daughters d1 and d2
    // cosTheta is cos(theta) of d1 in the rest frame of the mother, 
    // measured w.r.t. original direction of mother
    // phi is phi in this system. 
    // If these are not provided, they are generated randomly in ranges (-1,1), (-pi,pi).
    // 
    // returns a pair of four-momenta p1,p2 of the daughters d1,d2

    if(m1+m2 > p4_mother.M()){
        std::cout << "ERROR: illegal 2-body decay! m1 + m2 > M" << std::endl;
        throw std::exception();
    }    
    
    TVector3 direction = p4_mother.BoostVector().Unit();
    TVector3 axis;
    double angle;
    // special handling for the case where mother p4 is already along z-direction
    if(direction.Px()==0.0 && direction.Py()==0.0){
        axis = TVector3(1,0,0);
        angle = direction.Pz() < 0 ? M_PI : 0.0;
    }else{
        axis = direction.Cross(TVector3(0,0,1));
        angle = acos(direction.Dot(TVector3(0,0,1)));
    }
            
    // rotate mother so it points along +z axis
    p4_mother.Rotate(angle, axis);

    // boost mother so that it is at rest
    TVector3 boost = p4_mother.BoostVector();
    p4_mother.Boost(-boost);

    // assign cosTheta/phi randomly if they weren't provided
    if(cosTheta < -998)
        cosTheta = gRandom->Uniform(-1, 1);
    if(phi < -998)
        phi = gRandom->Uniform(-M_PI, M_PI);

    double theta = acos(cosTheta);
    TVector3 dir_1 = TVector3(sin(theta)*cos(phi), sin(theta)*sin(phi), cosTheta);
    TVector3 dir_2 = -dir_1;

    double M = p4_mother.M();
    double E1 = (M*M + m1*m1 - m2*m2) / (2*M);
    double E2 = M - E1;
    double p1 = sqrt(E1*E1 - m1*m1);
    double p2 = sqrt(E2*E2 - m2*m2);

    TLorentzVector p4_1, p4_2;
    p4_1.SetPxPyPzE(p1*dir_1.x(), p1*dir_1.y(), p1*dir_1.z(), E1);
    p4_2.SetPxPyPzE(p2*dir_2.x(), p2*dir_2.y(), p2*dir_2.z(), E2);

    p4_1.Boost(boost);
    p4_2.Boost(boost);
    p4_1.Rotate(-angle, axis);
    p4_2.Rotate(-angle, axis);

    return std::pair<TLorentzVector,TLorentzVector> (p4_1, p4_2);
}

std::tuple<TLorentzVector,TLorentzVector,TLorentzVector>
DoDalitz(TLorentzVector p4_mother, double me, double mX, bool useVDM=true){
    // Dalitz decay of the form P -> e+e-X (e can be electron, but doesn't have to be)
    // returns a 3-tuple of four-momenta pX, pe+, pe-
    // useVDM controls the type of form factor to use

    double mP = p4_mother.M();
    
    if(2*me + mX > mP){
        std::cout << "ERROR: illegal Dalitz decay! 2*me + mX > mP" << std::endl;
        throw std::exception();        
    }    
    
    // pdf of q^2 = m(e+e-)^2
    
    TF1 pdf_q2;
    if(useVDM){
        pdf_q2 = TF1("logq2_pdf","((1+exp(x)/([0]*[1]))^2-([0]+[1])^2*exp(x)/([0]*[1])^2)^1.5 * (1+0.5*[2]^2/exp(x)) * sqrt(1-[2]^2/exp(x)) * ([3]^4+([3]*[4])^2)/(([3]^2-exp(x))^2+([3]*[4])^2)", log(2*me*2*me), log((mP-mX)*(mP-mX)));
        pdf_q2.SetParameter(0, mP-mX); // max q2
        pdf_q2.SetParameter(1, mP+mX);
        pdf_q2.SetParameter(2, 2*me);  // min q2
        pdf_q2.SetParameter(3, 0.7755); // mass of rho, part of the form factor F(q^2)
        pdf_q2.SetParameter(4, 0.1462); // width of rho, part of the form factor F(q^2)
    }else{
        pdf_q2 = TF1("logq2","((1+exp(x)/([0]*[1]))^2-([0]+[1])^2*exp(x)/([0]*[1])^2)^1.5 * (1+0.5*[2]^2/exp(x)) * sqrt(1-[2]^2/exp(x)) * (1+[3]*exp(x)/[0]^2)^2", log(2*me*2*me), log((mP-mX)*(mP-mX)));
        pdf_q2.SetParameter(0, mP-mX);
        pdf_q2.SetParameter(1, mP+mX);
        pdf_q2.SetParameter(2, 2*me);
        pdf_q2.SetParameter(3, 0.03); // part of the form factor F(q^2) = 1 + 0.03*q^2/mP^2
    }
    pdf_q2.SetNpx(1000);

    double q2 = exp(pdf_q2.GetRandom());

    // do the P -> X gstar decay. cos(theta) is uniform here
    TLorentzVector pX, pgstar;
    std::tie(pX, pgstar) = Do2BodyDecay(p4_mother, mX, sqrt(q2));

    // pdf of cos(theta) in the gstar -> e+e- decay
    TF1 pdf_ct = TF1("pdf_ct", "1 + x^2 + [0]^2/[1]*(1-x^2)", -1, 1);
    pdf_ct.SetParameter(0, 2*me);
    pdf_ct.SetParameter(1, q2);
    pdf_ct.SetNpx(1000);

    double cosTheta = pdf_ct.GetRandom();

    TLorentzVector pe1, pe2;
    std::tie(pe1, pe2) = Do2BodyDecay(pgstar, me, me, cosTheta);

    return std::make_tuple(pX,pe1,pe2);

}

void decayMQ(){
    gRandom->SetSeed(1);
    TLorentzVector p4_pi0, p4_1, p4_2, pX, pe1, pe2;

    std::cout << "\nTest 2-body decay (pi0 -> gg):\n";
    p4_pi0.SetPtEtaPhiM(20.0, 0.68, 1.32, 0.139);
    std::tie(p4_1, p4_2) = Do2BodyDecay(p4_pi0, 0, 0);
    std::cout << "  pi0: "; p4_pi0.Print();
    std::cout << "   g1: "; p4_1.Print();
    std::cout << "   g2: "; p4_2.Print();
    std::cout << "g1+g2: "; (p4_1+p4_2).Print();

    std::cout << "\nTest Dalitz decay (pi0 -> e+e-g)\n";
    std::tie(pX, pe1, pe2) = DoDalitz(p4_pi0, 0.000511, 0);
    std::cout << "  pi0: "; p4_pi0.Print();
    std::cout << "    g: "; pX.Print();
    std::cout << "   e+: "; pe1.Print();
    std::cout << "   e-: "; pe2.Print();
    std::cout << "ge+e-: "; (pX+pe1+pe2).Print();

}


