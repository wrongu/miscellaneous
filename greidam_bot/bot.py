import praw
import time
import datetime
import smtplib
from email.mime.text import MIMEText

target = "Greidam"
message = "go to practice."
sub = u"ultimate"
mailfrom = "lange.richard.d+redditbot@gmail.com"
mailto = ["lange.richard.d+redditbot@gmail.com"]

last_post = 0
already_posted = []
delay = 10*60 # no more than one post every 10 minutes

def send_email(recipients, title, message):
	global mailfrom
	msg = MIMEText(message)

	msg['Subject'] = '[Redditbot] %s' % title
	msg['From'] = mailfrom
	msg['To'] = ";".join(recipients)

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')

	s.sendmail(mailfrom, recipients, msg.as_string())
	s.quit()

def load_history():
	global already_posted
	global last_post
	with open("history.txt", "r") as f:
		last_post = int(f.readline())
		already_posted = [l.strip() for l in f.readlines()]

def write_history():
	global already_posted
	global last_post
	with open("history.txt", "w") as f:
		f.write("%d\n" % last_post)
		for p in already_posted:
			f.write("%s\n" % p)

def run_bot():
	global already_posted
	global last_post
	global delay
	load_history()
	r = praw.Reddit(user_agent='McCune bot, written by wrongu_')
	r.login('coach_mccune', 'trollinggreidam')
	t = r.get_redditor(target)
	cs = t.get_comments(sub)
	for c in cs:
		if c.id not in already_posted:
			already_posted.append(c.id)
			now = int(time.time())
			time_since_last = now - last_post
			slp = delay - time_since_last
			if slp > 0:
				print "waiting %d seconds for this post" % slp
				time.sleep(slp)
			last_post = now
			c.reply(message)
			confirmation = "%s @ %d" % (c.body, c.created)
			print confirmation
			send_email(mailto, "posted comment.", confirmation)
		else:
			print "SKIP", c.body
		time.sleep(30) # don't spam the API

if __name__ == '__main__':
	try:
		run_bot()
	except KeyboardInterrupt as ki:
		print "-stopping-"
		write_history()
	except Exception as e:
		#send_email(mailto, "exception in run_bot()", "Exception content:\n%s" % e)
		print "ERROR", e
		write_history()
