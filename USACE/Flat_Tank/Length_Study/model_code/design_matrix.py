def design_matrix_long_study():
      inputs = {
      "Title": {
            "TITLE": "DYNAMIC"
      },

      "Parallel Info": {
            "PX": "32",
            "PY": "1"
      },

      "Depth": {
            "DEPTH_TYPE": "FLAT",
            "DEPTH_FLAT": (1.0,20.0,20)
      },

      "Dimension": {
            "Mglob": "DYNAMIC",
            "Nglob": "3"
      },

      "Time": {
            "TOTAL_TIME": "DYNAMIC",
            "PLOT_INTV": "1.0",
            "PLOT_INTV_STATION": "0.1",
            "SCREEN_INTV": "25.0"
      },

      "Grid": {
            "DX": "DYNAMIC",
            "DY": "DYNAMIC"
      },

      "Wavemaker": {
            "WAVEMAKER": "WK_REG",
            "Tperiod": (2.0,16.0,15),
            "Xc_WK": "DYNAMIC",
            "AMP_WK": "DYNAMIC",
            "DEP_WK": "DYNAMIC",
            "Yc_WK": "0.0",
            "Theta_WK": "0.0",
            "Delta_WK": "3.0"
      },

      "Periodic Boundary Condition": {
            "PERIODIC": "F"
      },

      "Sponge Layer": {
            "DIFFUSION_SPONGE": "F",
            "FRICTION_SPONGE": "T",
            "DIRECT_SPONGE": "T",
            "Csp": "0.0",
            "Sponge_south_width": "0.0",
            "Sponge_north_width": "0.0",
            "Sponge_west_width": "DYNAMIC",
            "Sponge_east_width": "DYNAMIC"
      },

      "Friction": {
            "Cd": "0.0",
      },

      "Numerics": {
            "CFL": "0.5",
            "FroudeCap": "3.0"
      },

      "Wet-Dry": {
            "MinDepth": "0.05",
            "VISCOSITY_BREAKING": "T"
      },

      "Breaking": {
            "Cbrk1": "0.65",
            "Cbrk2": "0.35"
      },


      "Output": {
            "FIELD_IO_TYPE": "BINARY",
            "DEPTH_OUT": "T",
            "ETA": "T",
            "MASK": "T",
            "U": "F",
            "V": "F",
      },

      "Stations": {
                  "STATIONS_FILE": "DYNAMIC",
                  "NumberStations": "50",        
      },

      "Custom Nondimensional Inputs": {
            "PI_1": "4",
            "PI_2": "1.0",
            "PI_3": "50.0",
            "PI_4": "100.0",  # ONLY EDIT! HERE
            "PI_5": "4",
            "EPSILON": "0.05",
            "TAU_1": "150",
      },

      }

      return inputs