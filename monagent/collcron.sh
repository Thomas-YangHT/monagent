cd $HOME/monagent.client
/usr/bin/python ./fileUpdate.py uploadmon.py > ./fileupdate.log 2>upload.err && \
/usr/bin/python ./fileUpdate.py collexec.sh  >>./fileupdate.log 2>>upload.err && \
/usr/bin/python ./fileUpdate.py collfunc     >>./fileupdate.log 2>>upload.err && \
/usr/bin/python ./fileUpdate.py collconf     >>./fileupdate.log 2>>upload.err && \
/usr/bin/python ./fileUpdate.py collcron.sh  >>./fileupdate.log 2>>upload.err && \
/usr/bin/python ./uploadmon.py upmoninfo  >./upmoninfo.log  2>>upload.err 
/usr/bin/python ./uploadmon.py upbaseinfo >./upbaseinfo.log 2>>upload.err
/usr/bin/python ./uploadmon.py upportinfo >./upportinfo.log 2>>upload.err
/usr/bin/python ./uploadmon.py upwebinfo  >./upwebinfo.log  2>>upload.err
#/usr/bin/python ./uploadmon.py upbakinfo  >./upbakinfo.log  2>>upload.err
/usr/bin/python ./uploadmon.py uperrinfo  >./uperrinfo.log  2>>upload.err
