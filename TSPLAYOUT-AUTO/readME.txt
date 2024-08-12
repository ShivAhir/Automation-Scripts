TSPLAYOUT is a feature that allows us to play compressed streams on sVIP using the frame itself and without any external help.

Just have the tsplayout-auto.service at /etc/systemd/system location, have the script tsplayout_auto.py and have the streams to be played at /udata/home/mvx location.
Also, remember to reload-daemon and then enabling the service and starting the service.
Use:
1. sudo systemctl daemon-reload
2. sudo systemctl enable tsplayout-auto.service
3. sudo systemctl start tsplayout-auto.service
4. sudo systemctl status tsplayout-auto.service (to check if the service is running properly)
