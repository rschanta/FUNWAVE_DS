!------------------------------------------------------------------------------------
!
!      FILE mod_subgrid.F
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
!  TIDE_MODULE is a module to add tide/surge boundary conditions into wave simulation    
!
!  HISTORY :
!    07/28/2022 Fengyan Shi
!-------------------------------------------------------------------------------------
# if defined (SUBGRID)
MODULE SUBGRID_MODULE
  USE PARAM
  USE GLOBAL
  USE INPUT_READ
#if defined (PARALLEL)
  USE MPI
# endif
  IMPLICIT NONE
     REAL(SP) :: AvgEta,TmpEta,tmpv1,tmpv2,tmpv3,tmpv4,depmax
     INTEGER  :: Ktmp,tmpk1,tmpk2,pcount,pcount1,pcount2
     INTEGER :: SubMainGridRatio,NumPixel,II,JJ
     REAL(SP),DIMENSION(:,:),ALLOCATABLE :: Porosity, &
                              DepAvgSubgrid,DepMaxSubgrid
     INTEGER,DIMENSION(:,:),ALLOCATABLE ::MaskSubgrid
     REAL(SP),DIMENSION(:,:,:,:),ALLOCATABLE :: DepSubGrid
     CHARACTER(LEN=80) DEPTH_SUBGRID_FILE
     REAL(SP),DIMENSION(:,:),ALLOCATABLE :: rMASKS
     INTEGER :: VTYPE1,LINE
     LOGICAL :: OUT_POROSITY = .FALSE. 
     CHARACTER(LEN=80)::FDIR
  SAVE

CONTAINS

SUBROUTINE SUBGRID_INITIAL
                    
  USE INPUT_READ
  IMPLICIT NONE

  CHARACTER(LEN=80)::FILE_NAME=' '
  CHARACTER(LEN=80)::TMP_NAME=' '
  INTEGER :: Ifile,ierr


! read  from input.txt
      FILE_NAME=INPUT_FILE_NAME

        CALL READ_INTEGER(SubMainGridRatio,FILE_NAME,'SubMainGridRatio',ierr)
      IF(ierr==1)THEN
# if defined (PARALLEL)
      if (myid.eq.0) THEN
         WRITE(*,'(A80)')'SubMainGridRatio NOT FOUND, use 1 for default'
         WRITE(3,'(A80)')'SubMainGridRatio NOT FOUND, use 1 for default'
      endif
# else
         WRITE(*,'(A80)')'SubMainGridRatio NOT FOUND, use 1 for default'
         WRITE(3,'(A80)')'SubMainGridRatio NOT FOUND, use 1 for default'
# endif
      ENDIF

     CALL READ_LOGICAL(OUT_POROSITY,FILE_NAME,'Porosity',ierr)

     NumPixel=SubMainGridRatio*SubMainGridRatio

     ALLOCATE(Porosity(Mloc,Nloc),DepAvgSubgrid(Mloc,Nloc), &
               DepMaxSubgrid(Mloc,Nloc),MaskSubgrid(Mloc,Nloc), &
               rMASKS(Mloc,Nloc))
     ALLOCATE(DepSubGrid(Mloc,Nloc,SubMainGridRatio,SubMainGridRatio))

! read subgrid bathymetry

      CALL READ_STRING(DEPTH_FILE,FILE_NAME,'DEPTH_FILE',ierr)
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A12,A50)')'DEPTH_FILE:', DEPTH_FILE
# else
      WRITE(3,'(A12,A50)')'DEPTH_FILE:', DEPTH_FILE
# endif

      CALL READ_STRING(DEPTH_SUBGRID_FILE,FILE_NAME,'DEPTH_SUBGRID_FILE',ierr)
# if defined (PARALLEL)
      if (myid.eq.0) WRITE(3,'(A12,A50)')'SUBGRID DEPTH_FILE:', DEPTH_SUBGRID_FILE
# else
      WRITE(3,'(A12,A50)')'SUBGRID DEPTH_FILE:', DEPTH_SUBGRID_FILE
# endif


# if defined (PARALLEL)
     call GetFile (DEPTH_FILE,Depth)
# else
     OPEN(1,FILE=TRIM(DEPTH_FILE))

       DO J=Jbeg,Jend
        READ(1,*)(Depth(I,J),I=Ibeg,Iend)
       ENDDO

     CLOSE(1)
# endif

! distribute depth to ghost cells, this part will be repeated in init.F
    VTYPE1=1
# if defined (CARTESIAN)
    CALL PHI_COLL(Mloc,Nloc,Ibeg,Iend,Jbeg,Jend,Nghost,Depth,VTYPE1,PERIODIC)
# else
    CALL PHI_COLL(Mloc,Nloc,Ibeg,Iend,Jbeg,Jend,Nghost,Depth,VTYPE1)
# endif

   CALL GetFile_Subgrid (DEPTH_SUBGRID_FILE,DepSubGrid,MaskSubgrid)

     DO J=1,Nloc
     DO I=1,Mloc
      ! initially check all grid points, in update, only check subgrid region
       tmpv2=ZERO
       depmax=-LARGE
       pcount=0
       Porosity(I,J)=ZERO
       DO JJ=1,SubMainGridRatio
       DO II=1,SubMainGridRatio
          tmpv1=DepSubGrid(I,J,II,JJ)
          IF(tmpv1.GT.ZERO)THEN
            tmpv2=tmpv2+tmpv1
            pcount=pcount+1
          ENDIF
          IF(tmpv1.GT.depmax) depmax=tmpv1
       ENDDO
       ENDDO
       DepMaxSubgrid(I,J)=depmax
       IF(pcount==0)THEN
         DepAvgSubgrid(I,J)=-LARGE
       ELSE
         DepAvgSubgrid(I,J)=tmpv2/REAL(NumPixel)
         Porosity(I,J)=REAL(pcount)/REAL(NumPixel)
       ENDIF
     ENDDO
     ENDDO

! if porosity = zero,meaning dry point, just set 1 in etauv_solver
     DO J=1,Nloc
     DO I=1,Mloc
       IF(Porosity(I,J) < SMALL) Porosity(I,J)=1.0_SP
     ENDDO
     ENDDO

     IF (OUT_POROSITY)THEN
        FDIR=TRIM(RESULT_FOLDER)
        TMP_NAME = TRIM(FDIR)//'porosity.ini'
        call PutFile(TMP_NAME,POROSITY)
     ENDIF


END SUBROUTINE SUBGRID_INITIAL

SUBROUTINE UPDATE_SUBGRID

     DO J=1,Nloc
     DO I=1,Mloc
     IF(MaskSubgrid(I,J) .eq. 1)THEN
       tmpv2=ZERO
       pcount=0
       Porosity(I,J)=ZERO
       DO JJ=1,SubMainGridRatio
       DO II=1,SubMainGridRatio
          tmpv1=Eta(I,J)+DepSubGrid(I,J,II,JJ)
          IF(tmpv1.GT.ZERO)THEN
            tmpv2=tmpv2+tmpv1
            pcount=pcount+1
          ENDIF
       ENDDO
       ENDDO
       IF(pcount==0)THEN
         DepAvgSubgrid(I,J)=-LARGE
       ELSE
         DepAvgSubgrid(I,J)=tmpv2/REAL(NumPixel)
         Porosity(I,J)=REAL(pcount)/REAL(NumPixel)
       ENDIF
     ENDIF ! end subgrid mask
     ENDDO
     ENDDO

! if porosity = zero,meaning dry point, just set 1 in etauv_solver
     DO J=1,Nloc
     DO I=1,Mloc
       IF(Porosity(I,J) < SMALL) Porosity(I,J)=1.0_SP
     ENDDO
     ENDDO


END SUBROUTINE UPDATE_SUBGRID

# if defined (PARALLEL)
SUBROUTINE GetFile_SubGrid (FILE,PHI,MaskS)
     USE GLOBAL
     IMPLICIT NONE

     INTEGER :: l,Ix,Iy
     REAL(SP),DIMENSION(:,:,:,:),ALLOCATABLE :: PHIGLOB
     CHARACTER(LEN=80) FILE
     REAL(SP),DIMENSION(Mloc,Nloc,SubMainGridRatio,SubMainGridRatio),INTENT(OUT) :: PHI
     REAL(SP),DIMENSION(MGlob,NGlob):: PHI_tmp_glob
     REAL(SP),DIMENSION(Mloc,Nloc):: PHI_tmp_loc
     INTEGER,DIMENSION(Mloc,Nloc),INTENT(OUT) :: MaskS
     REAL(SP),DIMENSION(Mloc,Nloc) :: MaskS_R
     REAL(SP),DIMENSION(:,:),ALLOCATABLE :: MaskS_glob_R
     REAL(SP),DIMENSION(SubMainGridRatio*SubMainGridRatio) :: tmp_read

     ALLOCATE(PHIGLOB(MGlob, &
                      NGlob, &
                      SubMainGridRatio,SubMainGridRatio), &                  
                      MaskS_glob_R(MGlob,NGlob))

        OPEN(1,FILE=TRIM(FILE))     
     
        MaskS_glob_R = 0
        PHIGLOB = 0.0
        DO J=1,Nglob*Mglob
          READ(1,*,END=100)Ix,Iy,(tmp_read(I),I=1,SubMainGridRatio*SubMainGridRatio)
          MaskS_glob_R(Ix,Iy)=1
          DO JJ=1,SubMainGridRatio
          DO II=1,SubMainGridRatio
            PHIGLOB(Ix,Iy,II,JJ) &
                 = tmp_read((JJ-1)*SubMainGridRatio+II)
          ENDDO
          ENDDO
        ENDDO
100     CONTINUE
        CLOSE(1)

     DO JJ=1,SubMainGridRatio
     DO II=1,SubMainGridRatio
       PHI_tmp_glob(:,:)=PHIGLOB(:,:,II,JJ)
       CALL GLOB_to_LOC(PHI_tmp_glob,PHI_tmp_loc)
       PHI(:,:,II,JJ)=PHI_tmp_loc(:,:)
     ENDDO
     ENDDO

     CALL GLOB_to_LOC(MaskS_glob_R,MaskS_R)
     MaskS = INT(MaskS_R)

     DO J=1,Nloc
     DO I=1,Mloc
      IF(MaskS(I,J)<1)THEN
       DO JJ=1,SubMainGridRatio
       DO II=1,SubMainGridRatio
         PHI(I,J,II,JJ)=Depth(I,J)
       ENDDO
       ENDDO
      ENDIF
     ENDDO
     ENDDO

! check
!open(2,file='tmp0.txt')
!     do jj=1,SubMainGridRatio
!      write(2,192) (PHI(200+Nghost,1+Nghost,II,JJ),II=1,SubMainGridRatio)
!     enddo
!close(2)
!192   format(3000f12.6)


     DEALLOCATE(PHIGLOB,MaskS_glob_R)

END SUBROUTINE Getfile_Subgrid
# else
! not paralle
SUBROUTINE GetFile_SubGrid (FILE,PHI,MaskS)
     USE GLOBAL
     IMPLICIT NONE
     INTEGER :: l,Ix,Iy

     CHARACTER(LEN=80) FILE
     REAL(SP),DIMENSION(Mloc,Nloc,SubMainGridRatio,SubMainGridRatio),INTENT(OUT) :: PHI
     INTEGER,DIMENSION(Mloc,Nloc),INTENT(OUT) :: MaskS
     REAL(SP),DIMENSION(SubMainGridRatio*SubMainGridRatio) :: tmp_read

        OPEN(1,FILE=TRIM(FILE))

        DO J=1,Nloc
        DO I=1,Mloc
          DO JJ=1,SubMainGridRatio
          DO II=1,SubMainGridRatio
            PHI(I,J,II,JJ) = Depth(I,J) 
          ENDDO
          ENDDO
        ENDDO
        ENDDO        
     
        MaskS = 0
        DO J=1,Nglob*Mglob
          READ(1,*,END=100)Ix,Iy,(tmp_read(I),I=1,SubMainGridRatio*SubMainGridRatio)
          MaskS(Ix+Nghost,Iy+Nghost)=1
          DO JJ=1,SubMainGridRatio
          DO II=1,SubMainGridRatio
            PHI(Ix+Nghost,Iy+Nghost,II,JJ) &
                 = tmp_read((JJ-1)*SubMainGridRatio+II)
          ENDDO
          ENDDO
        ENDDO
100     CONTINUE
        CLOSE(1)

END SUBROUTINE GetFile_SubGrid
# endif
! end parallel

# if defined (PARALLEL)
SUBROUTINE GLOB_to_LOC(VarGlob,PHI)
     USE GLOBAL
     IMPLICIT NONE

     REAL(SP),DIMENSION(MGlob,NGlob),INTENT(IN) :: VarGlob
     REAL(SP),DIMENSION(MGlob+2*Nghost,NGlob+2*Nghost) :: PHIGLOB
     REAL(SP),DIMENSION(Mloc,Nloc),INTENT(OUT) :: PHI

![-------ykchoi (08/May/2017)
     INTEGER :: irank, lenx, leny, lenxy, ireq
     INTEGER :: Nista, Niend, Njsta, Njend
     INTEGER :: istanum, iendnum, jstanum, jendnum
     INTEGER, ALLOCATABLE :: Nistas(:), Niends(:), Njstas(:), Njends(:)
     INTEGER :: istatus(mpi_status_size)
     REAL(SP), ALLOCATABLE :: xx(:,:)
! -------ykchoi (08/May/2017) ]

! TEMP

     if (myid.eq.0) then
        DO J=Nghost+1,NGlob+NGhost
         DO I=Nghost+1,MGlob+Nghost
           PHIGLOB(I,J) = VarGlob(I-Nghost,J-Nghost)
         ENDDO
        ENDDO
! ghost cells
        DO I=Nghost+1,MGlob+Nghost
           DO J=1,Nghost
              PHIGLOB(I,J)=PHIGLOB(I,Nghost+1)
           ENDDO
           DO J=NGlob+Nghost+1,NGlob+2*Nghost
              PHIGLOB(I,J)=PHIGLOB(I,NGlob+Nghost)
           ENDDO
        ENDDO
        DO J=1,NGlob+2*Nghost
           DO I=1,Nghost
              PHIGLOB(I,J)=PHIGLOB(Nghost+1,J)
           ENDDO
           DO I=MGlob+Nghost+1,MGlob+2*Nghost
              PHIGLOB(I,J)=PHIGLOB(MGlob+Nghost,J)
           ENDDO
        ENDDO
     endif

![-------
     Nista = iista + Nghost;
     Niend = iiend + Nghost;
     Njsta = jjsta + Nghost;
     Njend = jjend + Nghost;

     allocate( Nistas(nprocs), Niends(nprocs), Njstas(nprocs), Njends(nprocs) )

     call MPI_Gather( Nista, 1, MPI_INTEGER, Nistas, 1, MPI_INTEGER, &
                      0, MPI_COMM_WORLD, ier )
     call MPI_Gather( Niend, 1, MPI_INTEGER, Niends, 1, MPI_INTEGER, &
                      0, MPI_COMM_WORLD, ier )
     call MPI_Gather( Njsta, 1, MPI_INTEGER, Njstas, 1, MPI_INTEGER, &
                      0, MPI_COMM_WORLD, ier )
     call MPI_Gather( Njend, 1, MPI_INTEGER, Njends, 1, MPI_INTEGER, &
                      0, MPI_COMM_WORLD, ier )

     if( myid == 0 )then
	 PHI = PHIGLOB( 1:Mloc, 1:Nloc )
     endif

     do irank=1, px*py-1
	  if( myid == 0 ) then
	    istanum = Nistas(irank+1) - Nghost
	    iendnum = Niends(irank+1) + Nghost
	    jstanum = Njstas(irank+1) - Nghost
          jendnum = Njends(irank+1) + Nghost

	    lenx = iendnum - istanum + 1
	    leny = jendnum - jstanum + 1
	    lenxy = lenx*leny
	    allocate( xx(lenx, leny) )

	    xx = PHIGLOB( istanum:iendnum, jstanum:jendnum )
	    call mpi_isend( xx, lenxy, mpi_sp, irank, 1, mpi_comm_world, ireq, ier )
	    call mpi_wait( ireq, istatus, ier )
          deallocate( xx )

	  elseif( myid == irank ) then
	    
	    lenx = Niend-Nista+1+2*Nghost
	    leny = Njend-Njsta+1+2*Nghost
	    lenxy = lenx*leny

	    call mpi_irecv( PHI, lenxy, mpi_sp, 0, 1, mpi_comm_world, ireq, ier )
	    call mpi_wait( ireq, istatus, ier )

	  endif
     enddo

     deallocate( Nistas, Niends, Njstas, Njends )

! -------

END SUBROUTINE GLOB_to_LOC
# endif

END MODULE SUBGRID_MODULE
# endif 
! end subgrid
