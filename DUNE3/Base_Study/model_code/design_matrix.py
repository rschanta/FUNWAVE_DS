def design_matrix_D3_base():
      inputs = {
      "Title": {
            "TITLE": "DYNAMIC"
      },

      "Parallel Info": {
            "PX": "32",
            "PY": "1"
      },

      "Depth": {
            "DEPTH_TYPE": "DATA",
      },

      "Dimension": {
            "Mglob": "DYNAMIC",
            "Nglob": "3"
      },

      "Time": {
            "TOTAL_TIME": "600.0",
            "PLOT_INTV": "0.01",
            "PLOT_INTV_STATION": "0.1",
            "SCREEN_INTV": "25.0"
      },

      "Grid": {
            "DX": "DYNAMIC",
            "DY": "DYNAMIC"
      },

      "Wavemaker": {
            "WAVEMAKER": "WK_TIME_SERIES",
            "Xc_WK": "DYNAMIC",
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

      "Custom Nondimensional Inputs": {
            "D3_Trial": (5,24,20),
            "PI_2": "3.0",
            "PI_3": "1.5",
            "PI_4": "0.1",
            "PI_5": "4",
            "T_higher": "40.0",
            "T_lower": "2.0"
      },

      }

      return inputs