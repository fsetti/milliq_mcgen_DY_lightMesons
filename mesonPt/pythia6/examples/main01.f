
C...Preamble: declarations.
      PROGRAM MAIN01
C...All real arithmetic in double precision.
      IMPLICIT NONE
C...Local arrays and data.
C....Global
C...Cross section information
      INTEGER NGENPD,NGEN
      REAL*8 XSEC
      COMMON/PYINT5/NGENPD,NGEN(0:500,3),XSEC(0:500,3)
      integer mint
      real*8 vint
      COMMON/PYINT1/MINT(400),VINT(400) 
      integer n,npad,k
      real*8 p,v
      COMMON/PYJETS/N,NPAD,K(4000,5),P(4000,5),V(4000,5)
      integer mstp,msti
      real*8 parp,pari
      COMMON/PYPARS/MSTP(200),PARP(200),MSTI(200),PARI(200)
      logical debug
      common/mrenna/debug
      INTEGER MSTU,MSTJ
      REAL*8 PARU,PARJ
      COMMON/PYDAT1/MSTU(200),PARU(200),MSTJ(200),PARJ(200)
      SAVE /PYDAT1/

C...User process event common block.
      INTEGER MAXNUP
      PARAMETER (MAXNUP=500)
      INTEGER NUP,IDPRUP,IDUP,ISTUP,MOTHUP,ICOLUP
      DOUBLE PRECISION XWGTUP,SCALUP,AQEDUP,AQCDUP,PUP,VTIMUP,SPINUP
      COMMON/HEPEUP/NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP,IDUP(MAXNUP),
     &ISTUP(MAXNUP),MOTHUP(2,MAXNUP),ICOLUP(2,MAXNUP),PUP(5,MAXNUP),
     &VTIMUP(MAXNUP),SPINUP(MAXNUP)
      SAVE /HEPEUP/

      INTEGER KCHG
      REAL*8 PMAS, PARF, VCKM
      COMMON/PYDAT2/KCHG(500,4),PMAS(500,4),PARF(2000),VCKM(4,4)
      SAVE /PYDAT2/

      CHARACTER*72 SIN
      COMMON/MYANLC/CHNAME, TOPDIR
      CHARACTER*6 CHNAME
      CHARACTER*8 TOPDIR
      CHARACTER*10 CHNEV
      CHARACTER*132 SLHANAME,LHENAME
      INTEGER I,NEV,ILIST,IMODE
      INTEGER MUPDA,LFN
      INTEGER IP,KF
      REAL*8  PE,THE,PHI
      INTEGER PYCOMP
      EXTERNAL PYDATA, PYCOMP

      READ(*,*,ERR=100,END=100) MUPDA,LFN
      IF( MUPDA.GT.1 .AND. LFN.NE.0) CALL PYUPDA(MUPDA,LFN)
      DO I=1,1000
       READ(*,'(A)',ERR=100,END=100) SIN
       CALL PYGIVE(SIN)
      ENDDO
100   NEV   = MINT(200)
      ILIST = MINT(199)      
C.....Use other MINTs (not too many!) to define mother, etc.
C-----------------------------------------------------------------
      CALL PYINIT('NONE','','',0D0)
C     Write out the decay table to edit
      IF( MUPDA.EQ.1 .AND. LFN.NE.0) CALL PYUPDA(MUPDA,LFN)

      IP = 0
      KF = 221
      PE = PMAS(PYCOMP(221),1) + 0.10
      THE = 0D0
      PHI = 0D0
      DO 200 I=1,NEV
         CALL PY1ENT(IP,KF,PE,THE,PHI)
         CALL PYLIST(1)
 200  CONTINUE
C/*
      IF(ILIST.NE.0) CALL PYLIST(12)
C-----------------------------------------------------------------
c      CALL USRDONE
C-----------------------------------------------------------------
      CALL PYSTAT(1)

      STOP
      END


