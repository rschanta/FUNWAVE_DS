# if defined (FOAM)
Module MOD_FOAM
     USE GLOBAL, ONLY : SP,ZERO,Mloc,Mloc1,Nloc,Nloc1,DX,DY,DT,Nghost,pi,TIME, &
                        PLOT_INTV, U,V,AGE_breaking,Ibeg,Iend,Jbeg,Jend,nu_break, &
                        LARGE
                        
# if defined (PARALLEL)
     USE GLOBAL, ONLY : n_west,n_east,n_suth,n_nrth,MPI_PROC_NULL
# endif
     IMPLICIT NONE
     REAL(SP):: PLOT_INTV_FOAM,PLOT_COUNT_FOAM
     REAL(SP) :: BurstRate=0.01_SP
!     REAL(SP) :: Drag=0.1_SP
!     REAL(SP) :: SpeedLimit=2.0_SP
     REAL(SP) :: MinThick=0.01_SP
     REAL(SP) :: TransferRate=0.1_SP
     REAL(SP) :: CdFoam=0.5

     REAL(SP),DIMENSION(:,:),ALLOCATABLE :: EtaFoam,EtaFoamMax,UFoam,VFoam
     REAL(SP),DIMENSION(:,:),ALLOCATABLE :: Usurf1,Vsurf1,VFsurf1, &
                                            Usurf2,Vsurf2,VFsurf2, &
                                            Usurf,Vsurf,VFsurf,&
                                            DepthFoam

     INTEGER,DIMENSION(:,:),ALLOCATABLE :: MaskFoam
     REAL(SP),DIMENSION(:,:),ALLOCATABLE ::MxFoam,MyFoam,&
                         FxFoam,FyFoam,GxFoam,GyFoam
     REAL(SP),DIMENSION(:,:),ALLOCATABLE :: SinkM,SourceM
     REAL(SP) :: f_source = 0.05 ! default 
     REAL(SP) :: FoamTimeScale = 3.8  ! default 

     LOGICAL :: OUT_FOAM = .FALSE.


     REAL(SP),PARAMETER :: SMALL=0.000001_SP

     CONTAINS

SUBROUTINE ALLOCATE_FOAM
     IMPLICIT NONE
     
     ALLOCATE ( EtaFoam(Mloc,Nloc),UFoam(Mloc,Nloc),VFoam(Mloc,Nloc),&
                MaskFoam(Mloc,Nloc),EtaFoamMax(Mloc,Nloc))
     ALLOCATE ( MxFoam(Mloc1,Nloc),MyFoam(Mloc,Nloc1), &
                FxFoam(Mloc1,Nloc),FyFoam(Mloc,Nloc1), &
                GxFoam(Mloc1,Nloc),GyFoam(Mloc,Nloc1) )
     ALLOCATE ( SinkM(Mloc,Nloc),SourceM(Mloc,Nloc))

     ALLOCATE (Usurf1(Mloc,Nloc),Vsurf1(Mloc,Nloc),VFsurf1(Mloc,Nloc), &
               Usurf2(Mloc,Nloc),Vsurf2(Mloc,Nloc),VFsurf2(Mloc,Nloc),&
               Usurf(Mloc,Nloc),Vsurf(Mloc,Nloc),VFsurf(Mloc,Nloc),&
               DepthFoam(Mloc,Nloc) )

END SUBROUTINE ALLOCATE_FOAM

SUBROUTINE INITIALIZATION_FOAM

  USE GLOBAL,ONLY : itmp1,itmp2,itmp3,itmp4,itmp5,SMALL, INPUT_FILE_NAME
# if defined (PARALLEL)
  USE GLOBAL,ONLY : iista,jjsta   !ykchoi Jan/23/2018
# endif
                    
  USE INPUT_READ

     IMPLICIT NONE
     INTEGER :: I,J,K

  CHARACTER(LEN=80)::FILE_NAME=' '
  CHARACTER(LEN=80)::TMP_NAME=' '
  INTEGER :: Ifile,ierr

! read  from input.txt
      FILE_NAME=INPUT_FILE_NAME

     PLOT_COUNT_FOAM = 0
     CALL READ_FLOAT(PLOT_INTV_FOAM,FILE_NAME,'PLOT_INTV_FOAM',ierr)
     IF(ierr==1)THEN
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A80)')'PLOT_INTV_FOAM not specified, use SAME'
# else
      WRITE(3,'(A50)')'PLOT_INTV_FOAM not specified, use SAME'
# endif
       PLOT_INTV_FOAM = PLOT_INTV
     ELSE
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A20,F12.6)')'PLOT_INTV_FOAM =', PLOT_INTV_FOAM
# else
      WRITE(3,'(A20,F12.2)')'PLOT_INTV_FOAM =', PLOT_INTV_FOAM
# endif
     ENDIF


# if defined (USE_BURSTRATE)

!!!!     REAL(SP),PARAMETER :: BurstRate=0.01_SP

      CALL READ_FLOAT(BurstRate,FILE_NAME,'BurstRate',ierr)
      IF(ierr==1)THEN
        BurstRate = 0.01_SP
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A80)')'Foam BurstRate not specified, use Default:  0.01'
         WRITE(3,'(A80)')'Foam BurstRate not specified, use Default:  0.01'
      endif
# else
         WRITE(*,'(A80)')'Foam BurstRate not specified, use Default:  0.01'
         WRITE(3,'(A80)')'Foam BurstRate not specified, use Default:  0.01'
# endif
     ELSE
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A20,F12.6)')'Foam BurstRate =', BurstRate
# else
      WRITE(3,'(A20,F12.2)')'Foam BurstRate =', BurstRate
# endif
       ENDIF

# endif 
  ! end burst rate

      CALL READ_FLOAT(f_source,FILE_NAME,'f_source',ierr)
      IF(ierr==1)THEN
        f_source = 0.05_SP
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A80)')'Coefficient f_source not specified, use Default:  0.05'
         WRITE(3,'(A80)')'Coefficient f_source not specified, use Default:  0.05'
      endif
# else
         WRITE(*,'(A80)')'Coefficient f_source not specified, use Default:  0.05'
         WRITE(3,'(A80)')'Coefficient f_source not specified, use Default:  0.05'
# endif
     ELSE
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A20,F12.6)')'f_source =', f_source
# else
      WRITE(3,'(A20,F12.2)')'f_source =', f_source
# endif
       ENDIF

      CALL READ_FLOAT(FoamTimeScale,FILE_NAME,'FoamTimeScale',ierr)
      IF(ierr==1)THEN
        FoamTimeScale = 3.8_SP
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A80)')'FoamTimeScale not specified, use Default:  3.8'
         WRITE(3,'(A80)')'FoamTimeScale not specified, use Default:  3.8'
      endif
# else
         WRITE(*,'(A80)')'FoamTimeScale not specified, use Default:  3.8'
         WRITE(3,'(A80)')'FoamTimeScale not specified, use Default:  3.8'
# endif
     ELSE
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A20,F12.6)')'FoamTimeScale =', FoamTimeScale
# else
      WRITE(3,'(A20,F12.2)')'FoamTimeScale =', FoamTimeScale
# endif
       ENDIF

!!!!     REAL(SP),PARAMETER :: MinThick=0.01_SP

      CALL READ_FLOAT(MinThick,FILE_NAME,'MinThick',ierr)
      IF(ierr==1)THEN
        MinThick = 0.01_SP
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A80)')'Foam MinThick not specified, use Default:  0.01'
         WRITE(3,'(A80)')'Foam MinThick not specified, use Default:  0.01'
      endif
# else
         WRITE(*,'(A80)')'Foam MinThick not specified, use Default:  0.01'
         WRITE(3,'(A80)')'Foam MinThick not specified, use Default:  0.01'
# endif
     ELSE
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A20,F12.6)')'Foam MinThick =', MinThick
# else
      WRITE(3,'(A20,F12.2)')'Foam MinThick =', MinThick
# endif
       ENDIF

# if defined (USE_BURSTRATE)
      CALL READ_FLOAT(TransferRate,FILE_NAME,'TransferRate',ierr)
      IF(ierr==1)THEN
        TransferRate = 0.1_SP
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A80)')'Foam TransferRate not specified, use Default:  0.1'
         WRITE(3,'(A80)')'Foam TransferRate not specified, use Default:  0.1'
      endif
# else
         WRITE(*,'(A80)')'Foam TransferRate not specified, use Default:  0.1'
         WRITE(3,'(A80)')'Foam TransferRate not specified, use Default:  0.1'
# endif
     ELSE
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A20,F12.6)')'Foam TransferRate =', TransferRate
# else
      WRITE(3,'(A20,F12.2)')'Foam TransferRate =', TransferRate
# endif
       ENDIF

# endif
  ! end burst rate

      CALL READ_FLOAT(CdFoam,FILE_NAME,'CdFoam',ierr)
      IF(ierr==1)THEN
        CdFoam = 0.5_SP
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A80)')'Foam CdFoam not specified, use Default:  0.5'
         WRITE(3,'(A80)')'Foam CdFoam not specified, use Default:  0.5'
      endif
# else
         WRITE(*,'(A80)')'Foam CdFoam not specified, use Default:  0.5'
         WRITE(3,'(A80)')'Foam CdFoam not specified, use Default:  0.5'
# endif
     ELSE
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A20,F12.6)')'Foam CdFoam =', CdFoam
# else
      WRITE(3,'(A20,F12.2)')'Foam CdFoam =', CdFoam
# endif
       ENDIF


! all other variables used for foam
     EtaFoam=ZERO
     EtaFoamMax=ZERO
     UFoam=ZERO
     VFoam=ZERO
     MaskFoam=1
     MxFoam=ZERO
     MyFoam=ZERO
     FxFoam=ZERO
     FyFoam=ZERO
     GxFoam=ZERO
     GyFoam=ZERO
     SinkM=ZERO
     SourceM=ZERO
     Usurf1=ZERO
     Vsurf1=ZERO
     VFsurf1=ZERO
     Usurf2=ZERO
     Vsurf2=ZERO
     VFsurf2=ZERO
     Usurf=ZERO
     Vsurf=ZERO
     VFsurf=ZERO   

END SUBROUTINE INITIALIZATION_FOAM

SUBROUTINE FOAM_UPDATE
     IMPLICIT NONE
     REAL(SP) :: Uabs,Uadd,Vadd
     INTEGER :: I,J,K

! sources
     Usurf=U
     Vsurf=V
     VFsurf=AGE_breaking


# if defined (USE_BURSTRATE)
      ! this is the old approach 
        DO J=1,Nloc
         DO I=1,Mloc
          IF(VFsurf(I,J)<0.1)VFsurf(I,J)=1000.0_SP
          VFsurf(I,J)=0.4_SP*EXP(-VFsurf(I,J))
          SinkM(I,J)=EtaFoam(I,J)*BurstRate
          SourceM(I,J)=VFsurf(I,J)*TransferRate*MaskFoam(I,J)
         ENDDO
        ENDDO
# else
     ! new approach using Reul and Chapron 2003
        DO J=1,Nloc
         DO I=1,Mloc
          ! set breaking init time
          IF(VFsurf(I,J)<2.0*DT) THEN
            VFsurf(I,J)=LARGE
            EtaFoamMax(I,J)=0.0
          ENDIF
          IF (EtaFoam(I,J) > EtaFoamMax(I,J)) EtaFoamMax(I,J)=EtaFoam(I,J)
!          SinkM(I,J)=EtaFoamMax(I,J)/FoamTimeScale*EXP(-VFsurf(I,J)/FoamTimeScale)
          SinkM(I,J)=EtaFoam(I,J)/FoamTimeScale*EXP(-VFsurf(I,J)/FoamTimeScale)
          SourceM(I,J)=f_source*nu_break(I,J)*MaskFoam(I,J)
         ENDDO
        ENDDO

# endif

! EtaFoam

!     DO J=1+Nghost,Nloc-2*Nghost
!    DO I=1+Nghost,Mloc-2*Nghost

      DO J=Jbeg,Jend
      DO I=Ibeg,Iend

       EtaFoam(I,J)=EtaFoam(I,J)-DT*MxFoam(I,J) &
                                -DT*MyFoam(I,J) &
                                -SinkM(I,J)*DT &
                                +SourceM(I,J)*DT 

       IF(EtaFoam(I,J)<ZERO)EtaFoam(I,J)=ZERO

     ENDDO
     ENDDO


!! UFoam,VFoam
!!     DO J=1+Nghost,Nloc-2*Nghost
!!     DO I=1+Nghost,Mloc-2*Nghost

!  this is the previous foam approach Shi et al ICCE 2012

!      DO J=Jbeg,Jend
!      DO I=Ibeg,Iend

!       IF(EtaFoam(I,J)>ZERO)THEN
!         Uabs=SQRT((Usurf(I,J)-UFoam(I,J))**2+(Vsurf(I,J)-VFoam(I,J))**2)
!         Uadd=Uabs*(Usurf(I,J)-UFoam(I,J))*CdFoam/MAX(EtaFoam(I,J),MinThick)*DT
!         Vadd=Uabs*(Vsurf(I,J)-VFoam(I,J))*CdFoam/MAX(EtaFoam(I,J),MinThick)*DT

!         IF(ABS(Uadd)>ABS(Usurf(I,J)-UFoam(I,J)))Uadd=Usurf(I,J)
!         IF(ABS(Vadd)>ABS(Vsurf(I,J)-VFoam(I,J)))Vadd=Vsurf(I,J)

!         UFoam(I,J) = UFoam(I,J) + Uadd
!         VFoam(I,J) = VFoam(I,J) + Vadd

!        ELSE
!          UFoam(I,J)=ZERO
!          VFoam(I,J)=ZERO
!        ENDIF
!     ENDDO
!     ENDDO

END SUBROUTINE FOAM_UPDATE

SUBROUTINE FOAM_BC
     IMPLICIT NONE
     INTEGER :: I,J,K

! west
# if defined (PARALLEL)
     if(n_west.eq.MPI_PROC_NULL) then     
# endif

     DO J=1,Nloc
       Mxfoam(1,J)=ZERO
       EtaFoam(1,J)=ZERO
     ENDDO

# if defined (PARALLEL)
     endif
# endif

! east
# if defined (PARALLEL)
     if(n_east.eq.MPI_PROC_NULL) then     
# endif

     DO J=1,Nloc
       Mxfoam(Mloc1,J)=ZERO
       EtaFoam(Mloc,J)=ZERO
     ENDDO

# if defined (PARALLEL)
     endif
# endif


! south
# if defined (PARALLEL)
     if(n_suth.eq.MPI_PROC_NULL) then
# endif
     DO I=1,Mloc
       Myfoam(I,1)=ZERO
       EtaFoam(I,1)=ZERO
     ENDDO
# if defined (PARALLEL)
     endif
# endif

! north
# if defined (PARALLEL)
     if(n_nrth.eq.MPI_PROC_NULL) then
# endif
     DO I=1,Mloc
       Myfoam(I,Nloc1)=ZERO
       EtaFoam(I,Nloc)=ZERO
     ENDDO
# if defined (PARALLEL)
     endif
# endif

# if defined (PARALLEL)
     call phi_exch(EtaFoam)
! remove the approach of Shi et al. ICCE
!     call phi_exch(UFoam)
!     call phi_exch(VFoam)
# endif


END SUBROUTINE FOAM_BC

SUBROUTINE FOAM_FLUX_ICCE
     IMPLICIT NONE
     REAL(SP),DIMENSION(Mloc1,Nloc) :: VxL,VxR
     REAL(SP),DIMENSION(Mloc,Nloc1) :: VyL,VyR
     REAL(SP),DIMENSION(Mloc,Nloc) :: DelX,DelY
     INTEGER :: I,J,K

! MxFoam
     CALL DelxFun(DX,Mloc,Nloc,EtaFoam,DelX)
     CALL CONSTRUCT_X(Mloc,Mloc1,Nloc,DX,EtaFoam,DelX,VxL,VxR,1.0)
     DO J=1,Nloc   ! previous J=2,Nloc-1, not consistent with the y direction
      DO I=2,Mloc
       IF(0.5_SP*(UFoam(I-1,J)+UFoam(I,J))>ZERO)THEN
         MxFoam(I,J)=VxL(I,J)
       ELSE
         MxFoam(I,J)=VxR(I,J)
       ENDIF
      ENDDO
     ENDDO
     CALL DelxFun(DX,Mloc,Nloc,UFoam,DelX)
     CALL CONSTRUCT_X(Mloc,Mloc1,Nloc,DX,UFoam,DelX,VxL,VxR,1.0)
     DO J=1,Nloc
      DO I=2,Mloc
       IF(0.5_SP*(UFoam(I-1,J)+UFoam(I,J))>0)THEN
         MxFoam(I,J)=VxL(I,J)*MxFoam(I,J)
       ELSE
         MxFoam(I,J)=VxR(I,J)*MxFoam(I,J)
       ENDIF
      ENDDO
     ENDDO

! MyFoam
     CALL DelyFun(DY,Mloc,Nloc,EtaFoam,DelY)
     CALL CONSTRUCT_Y(Mloc,Nloc,Nloc1,DY,EtaFoam,DelY,VyL,VyR,1.0)
     DO J=2,Nloc
      DO I=1,Mloc
       IF(0.5_SP*(VFoam(I,J-1)+VFoam(I,J))>ZERO)THEN
         MyFoam(I,J)=VyL(I,J)
       ELSE
         MyFoam(I,J)=VyR(I,J)
       ENDIF
      ENDDO
     ENDDO
     CALL DelyFun(DY,Mloc,Nloc,VFoam,DelY)
     CALL CONSTRUCT_Y(Mloc,Nloc,Nloc1,DY,VFoam,DelY,VyL,VyR,1.0)
     DO J=2,Nloc
      DO I=1,Mloc
       IF(0.5_SP*(VFoam(I,J-1)+VFoam(I,J))>ZERO)THEN
         MyFoam(I,J)=VyL(I,J)*MyFoam(I,J)
       ELSE
         MyFoam(I,J)=VyR(I,J)*MyFoam(I,J)
       ENDIF
      ENDDO
     ENDDO



END SUBROUTINE FOAM_FLUX_ICCE

SUBROUTINE FOAM_FLUX
     IMPLICIT NONE
     REAL(SP),DIMENSION(Mloc1,Nloc) :: VxL,VxR
     REAL(SP),DIMENSION(Mloc,Nloc1) :: VyL,VyR
     REAL(SP),DIMENSION(Mloc,Nloc) :: DelX,DelY
     INTEGER :: I,J,K

! upwinding

    DO J=Jbeg,Jend
    DO I=Ibeg,Iend
     IF(u(I,J)>ZERO)THEN
# if defined (CARTESIAN)
       MxFoam(I,J)=(u(I,J)*EtaFoam(I,J)-u(I-1,J)*EtaFoam(I-1,J))/DX
# else
       MxFoam(I,J)=(u(I,J)*EtaFoam(I,J)-u(I-1,J)*EtaFoam(I-1,J))/DX(I,J)
# endif
     ELSE
# if defined (CARTESIAN)
       MxFoam(I,J)=(u(I+1,J)*EtaFoam(I+1,J)-u(I,J)*EtaFoam(I,J))/DX
# else
       MxFoam(I,J)=(u(I+1,J)*EtaFoam(I+1,J)-u(I,J)*EtaFoam(I,J))/DX(I,J)
# endif
     ENDIF
    ENDDO
    ENDDO

    DO J=Jbeg,Jend
    DO I=Ibeg,Iend
     IF(v(I,J)>ZERO)THEN
# if defined (CARTESIAN)
       MyFoam(I,J)=(v(I,J)*EtaFoam(I,J)-v(I,J-1)*EtaFoam(I,J-1))/DY
# else
       MyFoam(I,J)=(v(I,J)*EtaFoam(I,J)-v(I,J-1)*EtaFoam(I,J-1))/DY(I,J)
# endif
     ELSE
# if defined (CARTESIAN)
       MyFoam(I,J)=(v(I,J+1)*EtaFoam(I,J+1)-v(I,J)*EtaFoam(I,J))/DY
# else
       MyFoam(I,J)=(v(I,J+1)*EtaFoam(I,J+1)-v(I,J)*EtaFoam(I,J))/DY(I,J)
# endif
     ENDIF
    ENDDO
    ENDDO

END SUBROUTINE FOAM_FLUX

SUBROUTINE UPDATE_FOAM_MASK ! useless so far
     IMPLICIT NONE
     REAL(SP)::left,right,top,bottom
     INTEGER :: I,J,K

     DO J=1,Nloc
     DO I=1,Mloc
! flood
       IF(MASKFoam(I,J)<1)THEN
         ! left
        IF(I/=1)THEN
         IF(MASKFoam(I-1,J)==1.AND.(EtaFoam(I-1,J)-EtaFoam(I,j))>MinThick)THEN
           MaskFoam(I,J)=1
         ENDIF
        ENDIF
         ! right
        IF(I/=Mloc)THEN
         IF(MaskFoam(I+1,J)==1.AND.(EtaFoam(I+1,J)-EtaFoam(I,j))>MinThick)THEN
           MaskFoam(I,J)=1
         ENDIF
        ENDIF
         ! bottom
        IF(J/=1)THEN
         IF(MaskFoam(I,J-1)==1.AND.(EtaFoam(I,J-1)-EtaFoam(I,j))>MinThick)THEN
           MaskFoam(I,J)=1
         ENDIF
        ENDIF
         ! top
        IF(J/=Nloc)THEN
         IF(MaskFoam(I,J+1)==1.AND.(EtaFoam(I,J+1)-EtaFoam(I,j))>MinThick)THEN
           MaskFoam(I,J)=1
         ENDIF
        ENDIF
! drying
       ELSE
         IF(EtaFoam(I,J)<MinThick)THEN
          MaskFoam(I,J)=0
          EtaFoam(I,J)=ZERO
         ENDIF    
       ENDIF

     ENDDO
     ENDDO

END SUBROUTINE UPDATE_FOAM_MASK


END MODULE MOD_FOAM
# endif
