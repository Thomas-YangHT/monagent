#!(which bash)
def checkout(){  
    git checkout && \
    git pull && \
    checkout=1 || failure=1
}

def testcode(){    
    pytest || failure=1
}

def build(){
    REGIP="192.168.10.92:5000"
    PN=monagent 
    echo  $REGIP"/"$PN
    cd $PN && \
    version=`date +%Y%m%d-%H%M%S` && \
    docker build --no-cache -t $REGIP/$PN:v$version -f ./dockerfile.alpine.python . && \
    docker tag  $REGIP/$PN:v$version   $REGIP/$PN && \
    docker push $REGIP/$PN:v$version && \
    docker push $REGIP/$PN && \
    #sh ./docker-run.sh
    kubectl --kubeconfig /root/.kube/config set image deployment/$PN $PN=$REGIP/$PN:v$version -n default && \
    cd ../moncenter && \
    docker build --no-cache -t moncenter -f ./dockerfile.alpine.monagent.center .  && \
    sh docker-run.sh  && \
    cd ../monclient  && \
    cp instmon.sh fileUpdate.py /export/download/monagent.client/  && \
    success=1 || failure=1
}

checkout()  && \
testcode()  && \
build()

if [ failure=1 ]; then
        python sendmesstowx.py "build failed: https://github.com/Thomas-YangHT/monagent/"
fi
    
if [ success=1 ]; then
        python sendmesstowx.py "build successed"
fi