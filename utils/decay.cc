#include <TLorentzVector.h>
#include <TVector3.h>
#include <TF1.h>
#include <TRandom.h>
#include <iostream>
#include <utility>
#include <cmath>

#include "decay.h"

// use global TF1s. Otherwise, the overhead of re-computing integrals every time is verrrry slow
TF1 *PDF_LOGQ2_VDM = 0;
TF1 *PDF_LOGQ2_NONVDM = 0;

std::pair<TLorentzVector,TLorentzVector>
Do2BodyDecay(TLorentzVector p4_mother, double m1, double m2, double cosTheta, double phi){
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
        std::cout << "ERROR: illegal 2-body decay! m1 + m2 > M (" << m1 << ", " << m2 << ", " << p4_mother.M() << ")\n";
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
DoDalitz(TLorentzVector p4_mother, double me, double mX, bool useVDM){
    // Dalitz decay of the form P -> e+e-X (e can be electron, but doesn't have to be)
    // returns a 3-tuple of four-momenta pX, pe+, pe-
    // useVDM controls the type of form factor to use

    double mP = p4_mother.M();
    
    if(2*me + mX > mP){
        std::cout << "ERROR: illegal Dalitz decay! 2*me + mX > mP" << std::endl;
        throw std::exception();        
    }    
    
    // pdf of q^2 = m(e+e-)^2
    
    TF1 *pdf_q2;
    if(useVDM){
        if(PDF_LOGQ2_VDM == 0){
            PDF_LOGQ2_VDM = new TF1("logq2_pdf", DGDLOGQ2_VDM, log(2*me*2*me), log((mP-mX)*(mP-mX)));
            PDF_LOGQ2_VDM->SetParameter(0, mP-mX); // max q2
            PDF_LOGQ2_VDM->SetParameter(1, mP+mX);
            PDF_LOGQ2_VDM->SetParameter(2, 2*me);  // min q2
            PDF_LOGQ2_VDM->SetParameter(3, 0.7755); // mass of rho, part of the form factor F(q^2)
            PDF_LOGQ2_VDM->SetParameter(4, 0.1462); // width of rho, part of the form factor F(q^2)
            PDF_LOGQ2_VDM->SetNpx(1000);
        }
        pdf_q2 = PDF_LOGQ2_VDM;
    }else{
        if(PDF_LOGQ2_NONVDM == 0){
            PDF_LOGQ2_NONVDM = new TF1("logq2", DGDLOGQ2_NONVDM, log(2*me*2*me), log((mP-mX)*(mP-mX)));
            PDF_LOGQ2_NONVDM->SetParameter(0, mP-mX);
            PDF_LOGQ2_NONVDM->SetParameter(1, mP+mX);
            PDF_LOGQ2_NONVDM->SetParameter(2, 2*me);
            PDF_LOGQ2_NONVDM->SetParameter(3, 0.03); // "a" of the form factor F(q^2) = 1 + 0.03*q^2/mpi^2
            PDF_LOGQ2_NONVDM->SetParameter(4, 0.1350); // "mpi" of the form factor F(q^2) = 1 + 0.03*q^2/mpi^2
            PDF_LOGQ2_NONVDM->SetNpx(1000);
        }
        pdf_q2 = PDF_LOGQ2_NONVDM;
    }

    double q2 = exp(pdf_q2->GetRandom());

    // do the P -> X gstar decay. cos(theta) is uniform here
    TLorentzVector pX, pgstar;
    std::tie(pX, pgstar) = Do2BodyDecay(p4_mother, mX, sqrt(q2));

    // want to generate cost(theta) according to PDF:
    //     dN/dcos(theta) = 1 + cos^2(theta) + 4*me^2/q^2*sin^2(theta)
    // But TF1s are slowwwwww. So numerically solve for CDF(cos(theta)) = R,
    // where R is a random number between 0,1
    double R =  gRandom->Uniform(0,1);
    double cosTheta = newton(4*me*me/q2, R);

    TLorentzVector pe1, pe2;
    std::tie(pe1, pe2) = Do2BodyDecay(pgstar, me, me, cosTheta);

    return std::make_tuple(pX,pe1,pe2);

}

void decay_test(){
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


double pdf_ct(double ct, double a){
    // pdf of cos(theta), where a = 4*me^2/q^2, normalized to unit area
    return 3./(4.*(2+a)) * ((1-a)*ct*ct + (1+a));
}
double cdf_ct(double ct, double a){
    // this is the integral of above, from -1 to ct
    return 3./(4.*(2+a)) * ((1-a)*ct*ct*ct/3. + (1+a)*ct + 2./3.*(2+a));
}
double newton(double a, double R, double guess, double tol){
    double x = guess;
    double xold = guess+tol+1;
    while(fabs(x-xold) > tol){
        xold = x;
        x = x - (cdf_ct(x,a) - R) / pdf_ct(x,a);
    }
    return x;
}
