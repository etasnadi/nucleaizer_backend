# nucleaizer_backend
[![Python package](https://github.com/etasnadi/nucleaizer_backend/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/etasnadi/nucleaizer_backend/actions/workflows/test_and_deploy.yml)
[![codecov](https://codecov.io/gh/etasnadi/nucleaizer_backend/branch/master/graph/badge.svg?token=ZOCTU6N7O2)](https://codecov.io/gh/etasnadi/nucleaizer_backend)
[![Documentation Status](https://readthedocs.org/projects/napari-nucleaizer-docs/badge/?version=latest)](https://napari-nucleaizer-docs.readthedocs.io/en/latest/?badge=latest)


## Overview

This package contains the code needed to execute the nucleAIzer nuclei segmentation algorithm. A Mask R-CNN and a pix2pix implementation is embedded.

Description of the method: "Hollandi et al.: nucleAIzer: A Parameter-free Deep Learning Framework for Nucleus Segmentation Using Image Style Transfer, Cell Systems, 2020. https://doi.org/10.1016/j.cels.2020.04.003"

This is a cleaned, simplified python interface for the algorithm (https://github.com/spreka/biomagdsb) (This prediction and training through command line)

If you want to use the web version, visit: http://nucleaizer.org (only prediction).

## Requirements

The nucleaizer backend runs on Windows and Linux only. MacOS is not supported yet.

### Prediction

Thre prediction runs on any machine where `tensorflow` is supported.

### Training

Some of the functionalities in our training code are implemented as MATLAB scripts. (See the full training code in https://github.com/spreka/biomagdsb repo.)

Therefore, a MATLAB (or MATLAB Runtime on Linux) is needed to execute the training.

* If you have MATLAB, the `biomagdsb` repository (containing the code) is pulled from git by the training script automatically to your home folder. Then, the scripts are executed with the `matlab` command (in headless mode). This method is supported on Windows an Linux.
    * If you do not have matlab on the system path, set the `MATLAB_COMMAND` environment variable pointing to the `matlab` binary.

* If you do not have a MATLAB license, you can install the MATLAB Runtime. The MATLAB code can execute the compiled version of the sciprt. Currently, we only have compiled versions for Linux. If you choose this option, the training script automatically downoads the compiled code and executes them. This method is only supported on Linux.
    * If you did not set the `LD_LIBRARY_PATH` for MATLAB Runtime properly,  set the `MATLAB_RUNTIME_PATHS` variable to point to your MATLAB Runtime.
    * If you wish to use the full MATLAB instead of the MATLAB Runtime, set the `USE_MATLAB_SCRIPT` environment variable.

## Install

Use `python3 -m pipi install -e <dir>` to install locally.

## Run

The training script can be called using the command line interface (CLI).

`python3 -m nucleaizer_backend.training_cli`

The only required argument is the input directory. This is where the `train`, `val` and `test` subdirectories are found.

There are two additional paths used by the training script:
1. The home directory for the algorithm (`NUCLEAIZER_HOME`). The auxiliary files to execute the training will be downloaded here. If not set it will be under the current urser's home folder with name `.nucleaizer`.
2. The work directoy (workflow), where the intermediate results put. The default is the `workflow` in the current directory.

By default, the whole pipeline is executed, that is exactly: `presegment,clustering,style,train`.
1. `presegment`: presegmentation setp. Using the presegmentation model, weak labels are generated for the elements of the `test` set.
2. `clustering`: clusters the test set based on image similarities using a pretrained distance predictor network. The clusters correspond to the styles.
3. `style`: uses image-to-image translation (pix2pix) to learn the translation from mask to microscopy image, while artificial labelled masks are generated. Then, the model is used to synthesize microscopy images for the generated masks. This is done for each cluster (style) so it can take a bit time.
4. `train`: trains a Mask R-CNN model on the concatenation of the samples in the `train` directory and the previously synthesized set of samples. The trained model will be in the `output_model` directory under the work dir.

## Further help

See the [documentation](https://napari-nucleaizer-docs.readthedocs.io/en/latest).