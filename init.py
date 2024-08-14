sbatch_tags = {
    "nodes": "1",
    "tasks-per-node": "32",
    "job-name": "generate_files",
    "partition": "standard",
    "time": "7-00:00:00",
    "output": "/work/thsu/rschanta/RTS-PY/logs/gen/gen_out%a.out",
    "error": "/work/thsu/rschanta/RTS-PY/logs/gen/err_out%a.out",
    "mail-user": "rschanta@udel.edu",
    "mail-type": "BEGIN,END,FAIL",
    "export": "ALL"
}