# Schdule task to fetch threat feeds and upload to Cloadflare every 10am

# Define the task name
$taskName = "DailyThreatFeeds"

# Define the Python script path
$scriptPath = "$HOME\threats\fetch_upload_feeds.py"

# Define the time for the task (10 AM)
$triggerTime = "10:00"

# Define the action (run Python with the script)
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument $scriptPath

# Define the trigger (daily at 10 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At $triggerTime

# Define task settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Run fetch_upload_feeds.py daily at 10 AM"

Write-Host "Task Scheduler for fetch_upload_feeds.py has been created to run daily at 10 AM."

# Run PowerShell as an administrator
# ./setup_task.ps1
