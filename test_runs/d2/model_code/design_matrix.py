
def design_matrix():
      inputs = {
      "Title": {
            "TITLE": "DYNAMIC"
      },

      "Parallel Info": {
            "PX": "8",
            "PY": "4"
      },

      "Depth": {
            "DEPTH_TYPE": "DATA"
      },

      "Dimension": {
            "Mglob": "DYNAMIC",
            "Nglob": "DYNAMIC"
      },

      "Time": {
            "TOTAL_TIME": "150.0",
            "PLOT_INTV": "0.1",
            "PLOT_INTV_STATION": "0.1",
            "SCREEN_INTV": "10.0"
      },

      "Grid": {
            "DX": "DYNAMIC",
            "DY": "DYNAMIC"
      },

      "Wavemaker": {
            "WAVEMAKER": "WK_REG",
            "Tperiod": ["2.0","9.0"],
            "Xc_WK": "DYNAMIC",
            "AMP_WK": "DYNAMIC",
            "DEP_WK": "DYNAMIC",
            "Yc_WK": "0.0",
            "Theta_WK": ["0.0" ,"5.0","10.0","15.0","20.0"],
            "Delta_WK": "3.0"
      },

      "Periodic Boundary Condition": {
            "PERIODIC": "T"
      },

      "Sponge Layer": {
            "DIFFUSION_SPONGE": "F",
            "FRICTION_SPONGE": "T",
            "DIRECT_SPONGE": "T",
            "Csp": "0.0",
            "Cdsponge": "1.0",
            "Sponge_south_width": "0.0",
            "Sponge_north_width": "0.0",
            "Sponge_west_width": "DYNAMIC",
            "Sponge_east_width": "0.0"
      },

      "Friction": {
            "Cd": "0.0"
      },

      "Numerics": {
            "CFL": "0.5",
            "FroudeCap": "3.0"
      },

      "Wet-Dry": {
            "MinDepth": "0.01",
            "VISCOSITY_BREAKING": "T"
      },

      "Breaking": {
            "Cbrk1": "0.65",
            "Cbrk2": "0.35"
      },

      "Wave Averaging": {
            "T_INTV_mean": "160.0",
            "STEADY_TIME": "160.0"
      },

      "Output": {
            "FIELD_IO_TYPE": "BINARY",
            "DEPTH_OUT": "T",
            "ETA": "T",
            "MASK": "T",
            "U": "T",
            "V": "T",
      },

      "Custom Inputs": {
                  "h_offshore": "10.0",        
                  "h_onshore": "1.0",         
                  "s": "0.0333",              
                  "bar_depth": "1.0",         
                  "bar_height": "2.0",        
                  "bar_width": "60.0",       
                  "channel_depth": "2.0",     
                  "channel_width": "10.0",   
                  "beach_LS_width": "DYNAMIC",   
                  "T_bar": "True",
                  "T_slp": "True",
                  "T_cha": "True",
      },

      "Custom Nondimensional Inputs": {
            "PI_W": "1.5",
            "PI_D": "1.0",
            "PI_F": "1.0",
            "PI_S": "0.0",
            "PI_N": "0.0",
      },
      "Pipeline": {
          "PIPELINE": 'Standard'}
      
      }

      return inputs