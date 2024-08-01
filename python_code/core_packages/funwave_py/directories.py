import os

#%% LIST_FW_DIRS
def list_FW_dirs(super_path, run_name):
    """
    Returns a dictionary with all the paths associated with a FUNWAVE run within the super_path directory.

    Arguments:
    - super_path: Path to the super directory.
    - run_name: Name of the FUNWAVE run.

    Returns:
    - p: Dictionary containing all paths.
    """
    p = {
        'SP': super_path,
        'RN': os.path.join(super_path, run_name),
        'RN_str': run_name,
        # INPUTS: `input.txt` TEXT FILES 
            'i': os.path.join(super_path, run_name, 'inputs'),
                'i_': os.path.join(super_path, run_name, 'inputs', 'input_'),
        # INPUTS: PROCESSED INPUT FILES
            'I': os.path.join(super_path, run_name, 'inputs-proc'),
                'Is': os.path.join(super_path, run_name, 'inputs-proc', 'In_s.mat'),
                'It': os.path.join(super_path, run_name, 'inputs-proc', 'In_t.txt'),
                'Ip': os.path.join(super_path, run_name, 'inputs-proc', 'In_p.parquet'),
                'Id': os.path.join(super_path, run_name, 'inputs-proc', 'In_d.pkl'),
        # OUTPUTS: DIRECTORY FOR RAW TIME SERIES OUTPUT (backslash in RESULT_FOLDER)
            'o': f"{super_path}/{run_name}/outputs-raw",
                'o_': f"{super_path}/{run_name}/outputs-raw/out_",
        # OUTPUTS: DIRECTORY FOR PROCESSED/CONDENSED TIME SERIES OUTPUT
            'O': os.path.join(super_path, run_name, 'outputs-proc'),
                'O_': os.path.join(super_path, run_name, 'outputs-proc', 'Out_'),
        # BATHYMETRY FILES
            'b': os.path.join(super_path, run_name, 'bathy'),
                'b_': os.path.join(super_path, run_name, 'bathy', 'bathy_'),
        # BATHYMETRY FIGURES
            'bF': os.path.join(super_path, run_name, 'bathy_fig'),
                'bF_': os.path.join(super_path, run_name, 'bathy_fig', 'bathy_fig_'),
        # COUPLING FILES
            'c': os.path.join(super_path, run_name, 'coupling'),
                'c_': os.path.join(super_path, run_name, 'coupling', 'coupling_'),
        # SPECTRA FILES
            'sp': os.path.join(super_path, run_name, 'spectra'),
                'sp_': os.path.join(super_path, run_name, 'spectra', 'spectra_'),
        # SPECTRA FIGURES
            'spF': os.path.join(super_path, run_name, 'spectra_fig'),
                'spF_': os.path.join(super_path, run_name, 'spectra_fig', 'spectra_fig_'),
        # OTHER FUNWAVE OUTPUTS
            'F': os.path.join(super_path, run_name, 'other-FW-out'),
                'Fd': os.path.join(super_path, run_name, 'other-FW-out', 'dep.mat'),
                'Ft': os.path.join(super_path, run_name, 'other-FW-out', 'time_dt.txt'),
        # ANIMATIONS
            'ani': os.path.join(super_path, run_name, 'animations'),
                'aniE': os.path.join(super_path, run_name, 'animations', 'eta-animations'),
                    'aniE_': os.path.join(super_path, run_name, 'animations', 'eta-animations', 'eta_'),
                'aniU': os.path.join(super_path, run_name, 'animations', 'u-animations'),
                    'aniU_': os.path.join(super_path, run_name, 'animations', 'u-animations', 'u_'),
                'aniV': os.path.join(super_path, run_name, 'animations', 'v-animations'),
                    'aniV_': os.path.join(super_path, run_name, 'animations', 'v-animations', 'v_'),
                'aniUU': os.path.join(super_path, run_name, 'animations', 'U_undertow-animations'),
                    'aniUU_': os.path.join(super_path, run_name, 'animations', 'U_undertow-animations', 'U_undertow_'),
                'aniVU': os.path.join(super_path, run_name, 'animations', 'v_undertow-animations'),
                    'aniVU_': os.path.join(super_path, run_name, 'animations', 'v_undertow-animations', 'V_undertow_'),
        # OTHER STATISTICS OF INTEREST
            'S': os.path.join(super_path, run_name, 'stats')
    }

    return p

#%% MK_FW_DIR
def mk_FW_dir(super_path,run_name):
    
    
    # Get list of directories from list_FW_dirs
        p = list_FW_dirs(super_path,run_name);
        
        # RUN_NAME
        os.makedirs(p['RN'], exist_ok=True)
        # INPUTS: `input.txt` TEXT FILES 
        os.makedirs(p['i'], exist_ok=True)
        # INPUTS: PROCESSED INPUT FILES
        os.makedirs(p['I'], exist_ok=True)
        # OUTPUTS: DIRECTORY FOR RAW TIME SERIES OUTPUT
        os.makedirs(p['o'], exist_ok=True)
        # OUTPUTS: DIRECTORY FOR PROCESSED/CONDENSED TIME SERIES OUTPUT
        os.makedirs(p['O'], exist_ok=True)
        # BATHYMETRY FILES
        os.makedirs(p['b'], exist_ok=True)
        # BATHYMETRY FIGURES
        os.makedirs(p['bF'], exist_ok=True)
        # COUPLING FILES
        os.makedirs(p['c'], exist_ok=True)
        # SPECTRA
        os.makedirs(p['sp'], exist_ok=True)
        # SPECTRA FIGURES
        os.makedirs(p['spF'], exist_ok=True)
        # OTHER FUNWAVE OUTPUTS
        os.makedirs(p['F'], exist_ok=True)
        # OTHER STATISTICS OF INTEREST
        os.makedirs(p['S'], exist_ok=True)
        # ANIMATIONS
        os.makedirs(p['ani'], exist_ok=True)
        os.makedirs(p['aniE'], exist_ok=True)
        os.makedirs(p['aniU'], exist_ok=True)
        os.makedirs(p['aniV'], exist_ok=True)
        os.makedirs(p['aniUU'], exist_ok=True)
        os.makedirs(p['aniVU'], exist_ok=True)
        
        print('Directories successfully created!')
 
#%% LIST_FW_TRI_DIRS
def list_FW_tri_dirs(tri_num, p):
    """
    Arguments:
    - tri_num: (int) trial number
    - p: (dict) `p` dictionary output from `list_FW_dirs`
    """
    ptr = {
        # Trial number
            'num_str': f"{tri_num:05d}",
        # Run Name
            'RN': p['RN_str'],
        # Input Name/Title
            'input_name': f"input_{tri_num:05d}",
        # Input Name/Title
            'tri_name': f"tri_{tri_num:05d}",
        # Path to the input_XXXXX.txt file
            'i_file': f"{p['i_']}{tri_num:05d}.txt",
        # Path to out_XXXXX folder (RESULT_FOLDER) to put into FUNWAVE 
            'RESULT_FOLDER': f"{p['o_']}{tri_num:05d}/",
        # Path to bathy_XXXXX.txt file
            'b_file': f"{p['b_']}{tri_num:05d}.txt",
        # Path to coupling_XXXXX.txt file
            'c_file': f"{p['c_']}{tri_num:05d}.txt",
        # Path to spectra_XXXXX.txt file
            'sp_file': f"{p['sp_']}{tri_num:05d}.txt",
        # Path to condensed output structure
            'out_file': f"{p['O_']}{tri_num:05d}.mat",
            'out_record': f"{p['O_']}{tri_num:05d}.tfrecord",
        # Path to dep.out
            'dep_file': f"{p['o_']}{tri_num:05d}/dep.out",
        # Path to cd_breakwater.out
            'cd_breakwater_file': f"{p['o_']}{tri_num:05d}/cd_breakwater.out",
        # Path to time_dt.out
            'time_dt_file': f"{p['o_']}{tri_num:05d}/time_dt.txt",
        # Path to bathymetry figure
            'b_fig': f"{p['bF_']}{tri_num:05d}.png",
        # Path to spectra figure
            'sp_fig': f"{p['spF_']}{tri_num:05d}.png",
        # Path to animations
            'aniE': f"{p['aniE_']}{tri_num:05d}.avi",
            'aniU': f"{p['aniU_']}{tri_num:05d}.avi",
            'aniUU': f"{p['aniUU_']}{tri_num:05d}.avi",
            'aniVU': f"{p['aniVU_']}{tri_num:05d}.avi"
    }

    return ptr
        
    