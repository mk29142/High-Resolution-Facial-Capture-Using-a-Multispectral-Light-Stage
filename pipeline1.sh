#!/bin/bash

os=${OSTYPE//[0-9.-]*/}

function createModel {
    path="`pwd`/createModel.py"
    pathToAgisoft="~/../../Applications/PhotoScanPro.app/Contents/MacOS/"

    eval "cd $pathToAgisoft"
    eval "./PhotoScanPro -r $path"
}

function diffuse {
    path="`pwd`"
    # pathToMeshlab  = "~/../../Applications/meshlab.app/Contents/MacOS/"
    pathToMeshlab="~/Documents/newNewMeshlab/cnr-isti-vclab/meshlab/src/distrib/meshlab.app/Contents/MacOS/"

    # normal maps
    eval "python photometricNormals.py --maps"

    # diffuse project
    eval "python photometricNormals.py --diffuseProj"
    eval "cd $pathToMeshlab"
    eval "./meshlabserver -p $path/diffuseProject.mlp -o $path/diffuseAdded.ply -m vn -s $path/diffuseScript.mlx"
    eval "cd $path"

    # nehab
    eval "wine mesh_opt.exe diffuseAdded.ply -lambda 0.01 -fixnorm 1:4  diffuseEmbossed.obj"
}

function specular {
    path="`pwd`"
    # pathToMeshlab  = "~/../../Applications/meshlab.app/Contents/MacOS/"
    pathToMeshlab="~/Documents/newNewMeshlab/cnr-isti-vclab/meshlab/src/distrib/meshlab.app/Contents/MacOS/"

    # specular project
    eval "python photometricNormals.py --specularProj"
    eval "cd $pathToMeshlab"
    eval "./meshlabserver -p $path/specularProject.mlp -o $path/specularAdded.ply -m vn -s $path/specularScript.mlx"
    eval "cd $path"

    # nehab
    eval "wine mesh_opt.exe specularAdded.ply -lambda 0.01 -fixnorm 1:4 -smooth 1:1  specularEmbossed.ply"
    # done
}

case "$os" in
  darwin)

    if [[ $1 == "-r" ]]
    then
        createModel
    fi

    if [[ $1 == "-ds" ]]
    then
      diffuse
      specular
    fi

    ;;

  msys)
    echo "I'm Windows using git bash"
    ;;
  *)

esac