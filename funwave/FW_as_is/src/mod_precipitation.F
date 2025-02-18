!------------------------------------------------------------------------------------
!
!      FILE mod_precipitation.F
!
!      This file is part of the FUNWAVE-TVD program under the Simplified BSD license
!
!-------------------------------------------------------------------------------------
! 
!    Copyright (c) 2016, FUNWAVE Development Team
!
!    (See http://www.udel.edu/kirby/programs/funwave/funwave.html
!     for Development Team membership)
!
!    All rights reserved.
!
!    FUNWAVE_TVD is free software: you can redistribute it and/or modify
!    it under the terms of the Simplified BSD License as released by
!    the Berkeley Software Distribution (BSD).
!
!    Redistribution and use in source and binary forms, with or without
!    modification, are permitted provided that the following conditions are met:
!
!    1. Redistributions of source code must retain the above copyright notice, this
!       list of conditions and the following disclaimer.
!    2. Redistributions in binary form must reproduce the above copyright notice,
!    this list of conditions and the following disclaimer in the documentation
!    and/or other materials provided with the distribution.
!
!    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
!    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
!    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
!    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
!    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
!    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
!    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
!    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
!    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
!    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
!  
!    The views and conclusions contained in the software and documentation are those
!    of the authors and should not be interpreted as representing official policies,
!    either expressed or implied, of the FreeBSD Project.
!  
!-------------------------------------------------------------------------------------
!
!  PRECIPITATION is a module to model rainfall effects   
!
!  HISTORY :
!    09/07/2023  Fengyan Shi
!
!-------------------------------------------------------------------------------------

# if defined (PRECIPITATION)

MODULE PRECIPITATION_MODULE
  USE PARAM
  USE GLOBAL,ONLY : Mloc,Nloc,Nghost,Ibeg,Iend,Jbeg,Jend,Mglob,Nglob
  USE INPUT_READ
#if defined (PARALLEL)
  USE GLOBAL,ONLY : myid,ier, npx,npy,PX,PY,iista,jjsta
  USE MPI
# endif
  IMPLICIT NONE
  SAVE

       LOGICAL :: RainWaveInteraction = .FALSE.
       REAL(SP), DIMENSION(:,:),ALLOCATABLE :: PrecRateData1,PrecRateData2, PrecRateData, &
                                               PrecRateModel

    REAL(SP) :: TimePrec1,TimePrec2
    CHARACTER (LEN=80) :: NamePrec1,NamePrec2
    INTEGER,DIMENSION(:),ALLOCATABLE ::  IXco,IYco
    LOGICAL :: OUT_Precipitation = .TRUE.
    REAL(SP):: PLOT_INTV_PREC,PLOT_COUNT_PREC 
    INTEGER :: M_PrecDim,N_PrecDim
    CHARACTER(LEN=80)::FILE_NAME=' '
    CHARACTER(LEN=80)::RAINFALL_FILE =' '      
       


#if defined (PARALLEL)
    REAL(SP) :: myvar
# endif    

CONTAINS
  
! READ Precipitation

SUBROUTINE PRECIPITATION_INITIAL
  USE GLOBAL,ONLY : itmp1,itmp2,itmp3,itmp4,SMALL,LARGE,INPUT_FILE_NAME
                    
  USE INPUT_READ
  IMPLICIT NONE

  INTEGER :: Ifile,ierr
  CHARACTER(LEN=80):: PrecName
  CHARACTER(LEN=80) :: WHAT


! read precipitation from input.txt
      FILE_NAME=INPUT_FILE_NAME

# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,*)'                                         '
      if (myid.eq.0) WRITE(3,*)'-------------- Precipitation INFO ----------'
# else
      WRITE(3,*)'                                         '
      WRITE(3,*)'-------------- Precipitation INFO ----------'   
# endif


! -------------------rainfall and wave interaction ---------------

    CALL READ_LOGICAL(RainWaveInteraction,  &
     FILE_NAME,'RainWaveInteraction',ierr)
      IF(ierr==1)THEN
        RainWaveInteraction = .FALSE.
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A40)')'no RainWaveInteraction'
         WRITE(3,'(A40)')'no RainWaveInteraction'
      endif
# else
         WRITE(*,'(A40)')'no RainWaveInteraction'
         WRITE(3,'(A40)')'no RainWaveInteraction'
# endif
       ENDIF

! ------------------- output -----------------
  CALL READ_LOGICAL(OUT_PRECIPITATION,FILE_NAME,'OUT_PRECIPITATION',ierr)
      IF(ierr==1)THEN
        OUT_PRECIPITATION = .TRUE.
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A40)')'default, make PRECIPITATION OUTPUT'
         WRITE(3,'(A40)')'default, make PRECIPITATION OUTPUT'
      endif
# else
         WRITE(*,'(A40)')'default, make PRECIPITATION OUTPUT'
         WRITE(3,'(A40)')'default, make PRECIPITATION OUTPUT'
# endif
       ENDIF

! -------------------------

! rainfall file
      CALL READ_STRING(RAINFALL_FILE,FILE_NAME,'RAINFALL_FILE',ierr)

      IF(ierr==1)THEN
# if defined (PARALLEL)
        IF(MYID==0)  &
       WRITE(*,*) 'RAINFALL_FILE CANNOT BE FOUND. STOP'
       CALL MPI_FINALIZE (ier)
       STOP
# else
        WRITE(*,*) 'RAINFALL_FILE CANNOT BE FOUND. STOP'
        STOP
# endif

      ELSE

# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A15,A50)')'RAINFALL_FILE:', RAINFALL_FILE
# else
      WRITE(3,'(A15,A50)')'RAINFALL_FILE:', RAINFALL_FILE
# endif

      ENDIF

! open file
  Ifile=400
  OPEN(Ifile,FILE=TRIM(RAINFALL_FILE))

! read file
         READ(Ifile,*)  WHAT ! title
         READ(Ifile,*)  M_PrecDim, N_PrecDim
         READ(Ifile,*)  WHAT ! t, file name
         READ(Ifile,*)  TimePrec2
         READ(Ifile,'(A80)')  NamePrec2

         TimePrec1 = TimePrec2
         NamePrec1 = NamePrec2

# if defined (PARALLEL)
   IF(MYID==0)THEN
   WRITE(3,*) 'Initial Time, FileName: ', TimePrec2,TRIM(NamePrec2)
   ENDIF
# else
   WRITE(3,*) 'Initial Time, FileName: ', TimePrec2,TRIM(NamePrec2)
# endif

! ----------------------------
   ALLOCATE (PrecRateData1(M_PrecDim,N_PrecDim), &
             PrecRateData2(M_PrecDim,N_PrecDim), &
             PrecRateData(M_PrecDim,N_PrecDim))
   ALLOCATE (PrecRateModel(Mloc,Nloc)) 
   ALLOCATE (iXco(Mloc),iYco(Nloc))

      
! iXco, and iYco, they are global grid point numbers in x and y

# if defined (PARALLEL)
	iXco(Ibeg) = iista
!--- iista is the start point defined by choi

# else
     iXco(Ibeg) = 1
# endif
     DO I = Ibeg+1,Mloc
       iXco(I) = iXco(I-1)+1
     ENDDO
     DO I = Ibeg-1,Ibeg-Nghost,-1
       iXco(I) = iXco(I+1)-1
     ENDDO

# if defined (PARALLEL)
      iYco(Jbeg) = jjsta
!---ykchoi Jan/23/2018]
# else
     iYco(Jbeg) = 1
# endif
     DO J = Jbeg+1,Nloc
       iYco(J) = iYco(J-1)+1
     ENDDO
     DO J = Jbeg-1,Jbeg-Nghost,-1
       iYco(J) = iYco(J+1)-1
     ENDDO

! read data
  Ifile=401
  OPEN(Ifile,FILE=TRIM(NamePrec2))
  DO J=1,N_PrecDim
    READ(Ifile,*)(PrecRateData2(I,J),I=1,M_PrecDim)
  ENDDO
  CLOSE(Ifile)


End SUBROUTINE PRECIPITATION_INITIAL

SUBROUTINE PRECIPITATION_DISTRIBUTION
  USE GLOBAL,ONLY : Mloc,Nloc,tmp1,tmp2,SMALL,TIME,ZERO
  USE INPUT_READ
  IMPLICIT NONE
  INTEGER :: Ifile,ierr,I,J,II,JJ
  REAL(SP) :: rII,rJJ
  INTEGER :: IOstatus

    IF(TIME>TimePrec1.AND.TIME>TimePrec2) THEN

         TimePrec1=TimePrec2
         NamePrec1=NamePrec2
         PrecRateData1=PrecRateData2

    Ifile = 400

    READ(Ifile,*,IOSTAT=IOstatus)  TimePrec2
    IF(IOstatus< 0)GOTO 120
    READ(Ifile,*)  NamePrec2

# if defined (PARALLEL)
   IF(MYID==0)THEN
   WRITE(3,*) 'READ RainFall, Time, FileName: ', TimePrec2,TRIM(NamePrec2)
   ENDIF
# else
   WRITE(3,*) 'READ RainFall, Time, FileName: ', TimePrec2,TRIM(NamePrec2)
# endif

! read data
  Ifile=401

  OPEN(Ifile,FILE=TRIM(NamePrec2))
  DO J=1,N_PrecDim
    READ(Ifile,*)(PrecRateData2(I,J),I=1,M_PrecDim)
  ENDDO
  CLOSE(Ifile)

    ENDIF ! end time > timeprec2

! calculate rainfall on grid
    tmp2=ZERO
    tmp1=ZERO

    IF(TIME>TimePrec1)THEN
      IF(TimePrec1.EQ.TimePrec2)THEN
        ! no more data
        tmp2=ZERO
        tmp1=ZERO
      ELSE
      tmp2=(TimePrec2-TIME) &
            /MAX(SMALL, ABS(TimePrec2-TimePrec1))
      tmp1=1.0_SP - tmp2;
      ENDIF  ! no more data?
    ENDIF ! time>time_1

    PrecRateData = PrecRateData2*tmp1 +PrecRateData1*tmp2

! convert from mm/hr to m/s
    PrecRateData = PrecRateData*0.000000277778

120 CONTINUE  ! no more data for vessel Kves

! interpolation

    DO J=Jbeg,Jend-1
    DO I=Ibeg,Iend-1
      rII=(REAL(iXco(I))-1.0_SP)/(REAL(Mglob)-1.0_SP)*(REAL(M_PrecDim)-1.0_SP)+1.0
      rJJ=(REAL(iYco(J))-1.0_SP)/(REAL(Nglob)-1.0_SP)*(REAL(N_PrecDim)-1.0_SP)+1.0
      II=FLOOR(rII)
      JJ=FLOOR(rJJ)
      tmp1=(1.0_SP-rII+II)*PrecRateData(II,JJ)+(rII-II)*PrecRateData(II+1,JJ)
      tmp2=(1.0_SP-rII+II)*PrecRateData(II,JJ+1)+(rII-II)*PrecRateData(II+1,JJ+1)
      PrecRateModel(I,J)=(1.0-rJJ+JJ)*tmp1+(rJJ-JJ)*tmp2
    ENDDO
    ENDDO

    DO J=Jbeg,Jend-1
      PrecRateModel(Iend,J) = PrecRateModel(Iend-1,J)
    ENDDO
    DO I=Ibeg,Iend-1
      PrecRateModel(I,Jend) = PrecRateModel(I,Jend-1)
    ENDDO
    PrecRateModel(Iend,Jend)=PrecRateModel(Iend-1,Jend-1)

! debug -------

!    if(myid==0)then
!    open(500,file='tmp1.txt')
!    elseif(myid==1)then
!    open(500,file='tmp2.txt')
!    elseif(myid==2)then
!    open(500,file='tmp3.txt')
!    elseif(myid==3)then
!    open(500,file='tmp4.txt')
!    endif
!     do j=1,nloc
!       write(500,*)(PrecRateModel(i,j),i=1,mloc)
!     enddo
!    close(500)
!    stop
!    CALL MPI_FINALIZE (ier)
! debug over --------

END SUBROUTINE PRECIPITATION_DISTRIBUTION


END MODULE PRECIPITATION_MODULE

# endif 
! end prec
