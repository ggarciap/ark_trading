from crontab import CronTab
cron = CronTab(user=True)
job = cron.new(command='echo hello_world >> test.txt')
job.minute.every(1)
cron.write()
