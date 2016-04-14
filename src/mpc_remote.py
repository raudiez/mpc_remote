import lirc
import time
import os

CMD_CHK_MPC_STATE="mpc | grep \"\[p\" | cut -d \" \" -f 1 | sed 's/\[//g' | sed 's/\]//g'"
CMD_MPC_PAUSE="mpc pause"
CMD_MPC_PLAY="mpc play"
CMD_MPC_PREV="mpc prev"
CMD_MPC_NEXT="mpc next"
playing = False
mpc_mode = False

sockid = lirc.init("mpd_remote", blocking=False)

def chk_playing_status():
	global playing
	status = os.popen(CMD_CHK_MPC_STATE).read()
	if status == "playing":
		playing = True
	else :
		playing = False

chk_playing_status()
while True:
	try:
	  button = lirc.nextcode()
	  if len(button) == 0: continue
	  if button[0] == "KEY_NEXT" and mpc_mode:
	  	chk_playing_status()
	  	if not playing:
	  		playing=True
	  	os.system(CMD_MPC_NEXT)
	  if button[0] == "KEY_PREVIOUS" and mpc_mode:
	  	chk_playing_status()
	  	if not playing:
	  		playing=True
	  	os.system(CMD_MPC_PREV)
	  if button[0] == "KEY_PLAYPAUSE" and mpc_mode:
	  	chk_playing_status()
	  	if playing:
	  		os.system(CMD_MPC_PAUSE)
	  		playing=False
	  	else:
	  		os.system(CMD_MPC_PLAY)
	  		playing=True
	  if button[0] == "KEY_MODE":
	  	if mpc_mode:
	  		mpc_mode = False
	  		os.system("systemctl start mediacenter")
	  		os.system(CMD_MPC_PAUSE)
	  	else:
	  		mpc_mode = True
	  		os.system("systemctl stop mediacenter")
	  		if playing:
	  			os.system(CMD_MPC_PLAY)

	  time.sleep(1)
	except KeyboardInterrupt:
	  lirc.deinit()
	  break
