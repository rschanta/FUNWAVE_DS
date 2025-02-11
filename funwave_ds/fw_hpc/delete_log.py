
import os
# Access the environment variables needed 
func_name = os.getenv('FUNC_NAME')
log_name = os.getenv('LOG_DIR')
tri_num = os.getenv('TRI_NUM')

out_name = f'{log_name}/{func_name}/out/out{tri_num}.out'
err_name =f'{log_name}/{func_name}/err/err{tri_num}.out'

# Logs to Make
normal_log = f'{log_name}/{func_name}/normal_terminations.txt'
cdf_log = f'{log_name}/{func_name}/cdfs_made.txt'
ani_log = f'{log_name}/{func_name}/animations_made.txt'
success_log = f'{log_name}/{func_name}/success_log.txt'
fail_log = f'{log_name}/{func_name}/fail_log.txt'

found_normal,found_netCDF,found_ani = False,False,False

with open(out_name, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if "Normal Termination!" in line:
            found_normal = True
            with open(normal_log, 'a', encoding='utf-8') as log:
                log.write(f"{tri_num}\n")
                
        if "NET-CDF Successfully saved!" in line:
            found_netCDF = True
            with open(cdf_log, 'a', encoding='utf-8') as log:
                log.write(f"{tri_num}\n")

        if "Finished Animation!" in line:
            found_ani = True
            with open(ani_log, 'a', encoding='utf-8') as log:
                log.write(f"{tri_num}\n")

# Delete the file
if all([found_normal, found_netCDF, found_ani]):
    os.remove(out_name)
    os.remove(err_name)
    with open(success_log, 'a', encoding='utf-8') as log:
                log.write(f"{tri_num}\n")
else:
    with open(fail_log, 'a', encoding='utf-8') as log:
                log.write(f"{tri_num}\n")
