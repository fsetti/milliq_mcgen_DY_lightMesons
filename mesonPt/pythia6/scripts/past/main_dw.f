      PROGRAM MAIN_DW

C******************************************************************

C...All real arithmetic in double precision.
      IMPLICIT DOUBLE PRECISION(A-H, O-Z)
C...Three Pythia functions return integers, so need declaring.
      INTEGER PYK,PYCHGE,PYCOMP

C...EXTERNAL statement links PYDATA on most machines.
      EXTERNAL PYDATA

C...Commonblocks.
C...The event record.
      COMMON/PYJETS/N,NPAD,K(4000,5),P(4000,5),V(4000,5)
C...Selection of hard subprocesses.
      COMMON/PYSUBS/MSEL,MSELPD,MSUB(500),KFIN(2,-40:40),CKIN(200)
!       allow to put particles stable
      COMMON/PYDAT3/MDCY(500,3),MDME(8000,2),BRAT(8000),KFDP(8000,5)
!       store cross-section information
      COMMON/PYPARS/MSTP(200),PARP(200),MSTI(200),PARI(200)

!       set up HEPEVT
      PARAMETER (NMXHEP=4000)
      COMMON/HEPEVT/NEVHEP,NHEP,ISTHEP(NMXHEP),IDHEP(NMXHEP),
     &JMOHEP(2,NMXHEP),JDAHEP(2,NMXHEP),PHEP(5,NMXHEP),VHEP(4,NMXHEP)
      DOUBLE PRECISION PHEP, VHEP

C...Number of events.
      NEV=10000000

      MSEL=0            !light qcd quark decays
      MSUB(11)=1
      MSUB(12)=1
      MSUB(13)=1
      MSUB(28)=1
      MSUB(53)=1
      MSUB(68)=1
!      MSUB(92)=1        !single diffraction ( AB -> XB )
!      MSUB(93)=1        !single diffraction ( AB -> AX )
      MSUB(94)=1        !double diffraction
      MSUB(95)=1        !low pT production

      MSTP(2)=2         ! 2nd order in alpha_s

!      MDCY(PYCOMP(113),1) = 0   !put rho meson stable 
!      MDCY(PYCOMP(223),1) = 0   !put omega meson stable 
!      MDCY(PYCOMP(333),1) = 0   !put phi meson stable 

      MSTP(5)=113       ! set DW pytune


!       write outputfile
      open(1, file='mQ_minBiasDW.txt')

C...Initialize for the LHC.
      CALL PYINIT('CMS','p','p',13000D0)
 
C...Event generation loop.
      DO 200 IEV=1,NEV
        CALL PYEVNT
!        CALL PYEDIT(2)
        CALL PYHEPC(1)          ! convert PYJETS into HEPEVT
       
!       run over NHEP / entries of PYHEPC 
        do 210 i=1,NHEP
          if ( K(i,2) .eq. 113 .or. 
     &         K(i,2) .eq. 223 .or.
     &         K(i,2) .eq. 333 ) then

                write(1,*) IEV, IDHEP(i), PHEP(1,i),PHEP(2,i),
     &            PHEP(3,i), PHEP(4,i), PHEP(5,i)
          end if
 210  continue
C...End of event generation loop.
 200  CONTINUE

      write(1,*) -1*NEV
      close(1)

      CALL PYSTAT(1)      

      END
