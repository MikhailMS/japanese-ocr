if [ $1 == 'file' ]
then
  if [ $2 == 'proxy' ]
  then
    docker run -it -p 6006:6006 -p 8888:8888 -v `pwd`:/japanese-ocr/src -w /japanese-ocr/src -f Dockerfile_proxy bash
  elif [ $2 == 'noproxy' ]
  then
    docker run -it -p 6006:6006 -p 8888:8888 -v `pwd`:/japanese-ocr/src -w /japanese-ocr/src -f Dockerfile_noproxy bash
  fi
elif [ $1 == 'nofile' ]
then
  if [ $2 == 'proxy' ]
  then
    docker run -it -p 6006:6006 -p 8888:8888 -v `pwd`:/japanese-ocr/src -w /japanese-ocr/src --env HTTP_PROXY="" --env HTTPS_PROXY="" kerasnp:tag bash
  elif [ $2 == 'noproxy' ]
  then
    docker run -it -p 6006:6006 -p 8888:8888 -v `pwd`:/japanese-ocr/src -w /japanese-ocr/src kerasnp:tag bash
  fi
fi

