from_name="XHY服务器告警"
from="alarm@xunheyun.cn"  
to_mail_address="168447636@qq.com yanghaitao@xunheyun.com wucj@xunheyun.com"
cc_mail_addres=""  
email_content="/root/alarm"  
email_subject="XHY告警"
attachfile="alarm"
attachfile2="alarm" 
attachment="/root/$attachfile"
attachment2="/root/$attachfile2"

/usr/sbin/sendmail -t -F "$from_name" <<EOF
SUBJECT: $email_subject `date +%Y-%m-%d`
TO: $(echo $to_mail_address)
CC: $cc_mail_addres
MIME-VERSION: 1.0
Content-Type: multipart/mixed; boundary="GvXjxJ+pjyke8COw"

--GvXjxJ+pjyke8COw
Content-type: text/html; charset=ISO-8859-15
Content-Transfer-Encoding: 7bit

$(cat $email_content)

--GvXjxJ+pjyke8COw
Content-type: text/html;name="$attachfile"
Content-Transfer-Encoding: base64
Content-ID: <cid1>
Content-Disposition: inline; filename="$attachfile"

$(base64 $attachment)

--GvXjxJ+pjyke8COw
Content-type: application/zip
Content-Transfer-Encoding: base64
Content-Disposition: attachement; filename=$attachfile2

$(base64 $attachment2)

EOF
