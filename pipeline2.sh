#!/bin/bash

os=${OSTYPE//[0-9.-]*/}

function createModel {
    path="`pwd`/createModel.py"
    pathToAgisoft="~/../../Applications/PhotoScanPro.app/Contents/MacOS/"

    eval "cd $pathToAgisoft"
    eval "./PhotoScanPro -r $path"
}

function texture {
    path="`pwd`"
    # pathToMeshlab  = "~/../../Applications/meshlab.app/Contents/MacOS/"
    pathToMeshlab="~/Documents/newNewMeshlab/cnr-isti-vclab/meshlab/src/distrib/meshlab.app/Contents/MacOS/"

    # normal maps
    eval "python photometricNormals.py --maps"

    # diffuse project
    eval "python photometricNormals.py --diffuseProj"
    eval "cd $pathToMeshlab"
    eval "./meshlabserver -p $path/diffuseProject.mlp -o $path/diffuseAdded.ply -m vn -s $path/blenderScript.mlx"
    eval "cd $path"

    # nehab
    eval "wine mesh_opt.exe diffuseAdded.ply -lambda 0.01 -fixnorm 1:4  diffuseEmbossed.obj"

    eval "python photometricNormals.py --specularProj"
    eval "cd $pathToMeshlab"
    eval "./meshlabserver -p $path/specularProject.mlp -o $path/forBlender.obj -m vn -s $path/blenderScript.mlx"
    eval "cd $path"
    eval "python blur.py"
}

function blender {
    # make sure you have created displacement map using shadermap 4 and named it the same texture map from the texture stage.
    path="`pwd`"
    pathToBlender  = "~/../../Applications/blender.app/Contents/MacOS/"

    eval "cd $pathToBlender"
    eval "./blender -b -P $path/blender.py"

}

case "$os" in
  darwin)

    if [[ $1 == "-r" ]]
    then
        createModel
    fi

    if [[ $1 == "-d" ]]
    then
      texture
    fi

    if [[ $1 == "-b" ]]
    then
        blender
    fi

    ;;

  msys)
    echo "I'm Windows using git bash"
    ;;
  *)

esac