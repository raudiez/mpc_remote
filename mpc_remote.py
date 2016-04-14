import lirc
import time
import os

CMD_CHK_MPC_STATE="mpc | grep \"\[p\" | cut -d \" \" -f 1 | sed 's/\[//g' | sed 's/\]//g'"
CMD_MPC_PAUSE="mpc pause"
CMD_MPC_PLAY="mpc play"
CMD_MPC_PREV="mpc prev"
CMD_MPC_NEXT="mpc next"

sockid = lirc.init("mpd_remote", blocking=False)

status = os.popen(CMD_CHK_MPC_STATE).read()
playing = False
if status == "playing": playing = True

while True:
	try:
	  button = lirc.nextcode()
	  if len(button) == 0: continue
	  print(button[0])
	  if button[0] == "KEY_NEXT":
	  	os.system(CMD_MPC_NEXT)
	  if button[0] == "KEY_PREVIOUS":
	  	os.system(CMD_MPC_PREV)
	  if button[0] == "KEY_PLAYPAUSE":
	  	if playing:
	  		os.system(CMD_MPC_PAUSE)
	  		playing=False
	  	else:
	  		os.system(CMD_MPC_PLAY)
	  		playing=True

	  time.sleep(1)
	except KeyboardInterrupt:
	  lirc.deinit()
	  break
