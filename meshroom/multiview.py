import os

from .core.graph import Graph


def photogrammetryPipeline():
    # type: () -> Graph
    graph = Graph('pipeline')

    cameraInit = graph.addNewNode('CameraInit',
                                  sensorDatabase=os.environ.get('ALICEVISION_SENSOR_DB', 'sensor_width_camera_database.txt'))

    featureExtraction = graph.addNewNode('FeatureExtraction',
                                         input=cameraInit.outputSfm)
    # TODO: imageMatching
    featureMatching = graph.addNewNode('FeatureMatching',
                                       input=cameraInit.outputSfm,
                                       featuresDirectory=featureExtraction.output)
    structureFromMotion = graph.addNewNode('StructureFromMotion',
                                           input=cameraInit.outputSfm,
                                           featuresDirectory=featureExtraction.output,
                                           matchesDirectory=featureMatching.output)
    prepareDenseScene = graph.addNewNode('PrepareDenseScene',
                                         input=structureFromMotion.output)
    camPairs = graph.addNewNode('CamPairs',
                                mvsConfig=prepareDenseScene.mvsConfig)
    depthMap = graph.addNewNode('DepthMap',
                                mvsConfig=camPairs.mvsConfig)
    depthMapFilter = graph.addNewNode('DepthMapFilter',
                                      mvsConfig=depthMap.mvsConfig)
    meshing = graph.addNewNode('Meshing',
                               mvsConfig=depthMapFilter.mvsConfig)
    texturing = graph.addNewNode('Texturing',
                                 mvsConfig=meshing.mvsConfig)
    return graph
