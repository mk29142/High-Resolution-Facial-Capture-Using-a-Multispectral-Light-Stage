#!/bin/bash

os=${OSTYPE//[0-9.-]*/}

function createModel {
    path="`pwd`/createModel.py"
    pathToAgisoft="~/../../Applications/PhotoScanPro.app/Contents/MacOS/"

    eval "cd $pathToAgisoft"
    eval "./PhotoScanPro -r $path"
}

function diffuseSpecular {
    path="'pwd'/"
    # pathToMeshlab  = "~/../../Applications/meshlab.app/Contents/MacOS/"
    pathToMeshlab="~/Documents/newNewMeshlab/cnr-isti-vclab/meshlab/src/distrib/meshlab.app/Contents/MacOS/"

    # normal maps

    # diffuse project
    # nehab
    # specular project
    # nehab

    # done
}

case "$os" in
  darwin)

    if (($1 == "-r"))
    then
        createModel
    fi

    if (($1 == "-ds"))
    then
    fi

    ;;

  msys)
    echo "I'm Windows using git bash"
    pathToAgisoft = "C:\Program Files\Agisoft\PhotoScan\ Pro"
    ;;
  *)

esac