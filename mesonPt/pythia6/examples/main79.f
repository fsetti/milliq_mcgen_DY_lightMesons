      PROGRAM MAIN79

C...Test program for new gcc4 compiler.
C...Top pair events are generated at the LHC, 14 TeV.
C...Final charged multiplicity is histogrammed.
C...The final total cross section should be 4.9E-07 mb,
C...the average multiplicity 243, and the rms 70.2, 
C...all within statistical fluctuations. 

C******************************************************************

C...All real arithmetic in double precision.
      IMPLICIT DOUBLE PRECISION(A-H, O-Z)
C...Three Pythia functions return integers, so need declaring.
      INTEGER PYK,PYCHGE,PYCOMP

      integer mint
      real*8 vint
      COMMON/PYINT1/MINT(400),VINT(400)       

      CHARACTER*72 SIN
      
C...EXTERNAL statement links PYDATA on most machines.
      EXTERNAL PYDATA

C...Commonblocks.
C...The event record.
      COMMON/PYJETS/N,NPAD,K(4000,5),P(4000,5),V(4000,5)
C...Selection of hard scattering subprocesses.
      COMMON/PYSUBS/MSEL,MSELPD,MSUB(500),KFIN(2,-40:40),CKIN(200)

C...Number of events.
      NEV=100
      DO I=1,1000
       READ(*,'(A)',ERR=100,END=100) SIN
       CALL PYGIVE(SIN)
      ENDDO
100   CONTINUE

C...Initialize for the LHC.
      CALL PYINIT('CMS','p','p',14000D0)

C...Histogram.
      CALL PYBOOK(1,'Final charged multiplicity',100,-1D0,599D0)
 
C...Event generation loop.
      DO 200 IEV=1,NEV
        CALL PYEVNT

C...Remove all but charged particles and histogram multiplicity.
        CALL PYEDIT(3)
        CALL PYFILL(1,DBLE(N),1D0)

C...End of event generation loop.
 200  CONTINUE

C...Cross section. Histogram.
      CALL PYSTAT(1)      
      CALL PYHIST

      END
