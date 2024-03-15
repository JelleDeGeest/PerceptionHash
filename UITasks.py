import time
from PerceptionHash import PerceptionHash


def long_running_task(data):
    print(data)
    print(data['graphs'])
    source = "load" if data['imageSource'] == "distorted" else "new"
    distorted_folders = data['selectedFolders']
    distortion_techniques = data['encodingTechniques']
    hashing_techniques = data['hashingTechniques']
    graphs = data['graphs']
    print(data)
    PerceptionHash(source, distorted_folders, distortion_techniques, hashing_techniques, graphs)

    return 