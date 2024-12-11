# MalWare

This private repository is designed to keep track of my malware project!

## RAT Features:

### File Management:
- `!current_dir` - Displays your current directory.
- `!delete_file <file_name>` - Deletes a specified file from the current directory.
- `!list_files` - Lists files in the current directory.
- `!change_dir <path>` - Changes the current working directory.
- `!search_file <keyword>` - Recursively searches for files containing a keyword in the current directory.
- `!disk_usage` - Reports disk space usage.

### Remote Access:
- `!stop_access` - Stops remote access entirely.
- `!panic` - Activates panic mode; stops remote access and deletes startup files.

### System Commands:
- `!cmd <command>` - Executes a system command.
- `!screenshot` - Takes a screenshot and sends it.
- `!download <file_name>` - Downloads a file from the current directory.
- `!upload` - Uploads a sent file.
- `!execute <file_path>` - Executes a specified file.
- `!rename <old_name> <new_name>` - Renames a file in the current directory.
- `!process_list` - Lists all running processes.
- `!schedule_task <task> <time>` - Schedules a task to run at a specified time.
- `!service <action> <service_name>` - Manages Windows services (start/stop/restart).
- `!system_info` - Displays system information (OS, CPU, memory usage).

### Documentation:
- `!help` - Lists all commands and their descriptions.

> **Disclaimer:** This repository is definitly NOT for educational purposes only.
