import os
import sys
import cv2
import warnings
import argparse
import numpy as np
import nibabel as nib
import SimpleITK as sitk
from typing import Optional, Tuple

from medimodule.utils import Checker

warnings.filterwarnings('ignore', '.*output shape of zoom.*')
warnings.filterwarnings("ignore", category=DeprecationWarning)


def BrainBET(
    task: str,
    weight: str,
    image_path: str,
    save_path: Optional[str] = None,
    gpus: str = "-1"
) -> Tuple[np.array, np.array]:
    """
    """

    from medimodule.Brain import MRI_BET
    Checker.check_input_type(image_path, "nii")
    Checker.set_gpu(gpu_idx=gpus, framework="pytorch")

    model = MRI_BET(weight)
    image, mask = model.predict(
        os.path.abspath(image_path),
        img_type="T1" if "mri" in task else "MRA",
        save_path=save_path)

    return image, mask


def BrainBlackBloodSegmentation(
    task: str,
    weight: str,
    image_path: str,
    save_path: Optional[str] = None,
    gpus: str = "-1"
) -> Tuple[np.array, np.array]:
    """
    """

    from medimodule.Brain import BlackbloodSegmentation
    Checker.check_input_type(image_path, "nii")
    Checker.set_gpu(gpu_idx=gpus, framework="tf2")

    model = BlackbloodSegmentation(weight)
    image, mask = model.predict(
        os.path.abspath(image_path),
        save_path=save_path)

    return image, mask


def ChestLRmarkDetection(
    task: str,
    weight: str,
    image_path: str,
    save_path: Optional[str] = None,
    gpus: str = "-1"
) -> np.array:
    """
    """
    from medimodule.Chest import ChestLRmarkDetection
    Checker.check_input_type(image_path, ["png","jpg","bmp"])
    Checker.set_gpu(gpu_idx=gpus, framework="tf2")

    model = ChestLRmarkDetection(weight)
    image = model.predict(
        os.path.abspath(image_path),
    )

    return image

def main(args):
    Checker.check_args(args.part, args.task)
    
    if args.part == "Brain":
        if args.task in ["mribet", "mrabet"]:
            BrainBET(
                task=args.task,
                weight=args.weight,
                image_path=args.image_path,
                save_path=args.save_path,
                gpus=args.gpus)
                
        elif args.task == "blackblood_segmentation":
            BrainBlackBloodSegmentation(
                task=args.task,
                weight=args.weight,
                image_path=args.image_path,
                save_path=args.save_path,
                gpus=args.gpus)

    elif args.part == "Chest":
        if args.task == "lrmark_detection":
            ChestLRmarkDetection(
                task=args.task,
                weight=args.weight,
                image_path=args.image_path,
                save_path=args.save_path,
                gpus=args.gpus)
        elif args.task == "viewpoint_classification":
            ViewpointClassifier(
                task=args.task,
                weight=args.weight,
                image_path=args.image_path,
                save_path=args.save_path,
                gpus=args.gpus)
        elif args.task == "enhance_classification":
            EnhanceCTClassification(
                task=args.task,
                weight=args.weight,
                image_path=args.image_path,
                save_path=args.save_path,
                gpus=args.gpus)

    elif args.part == "Abdomen":
        pass
    elif args.part == "Colon":
        pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part",       type=str,   default=None, required=True,
                        help="[Brain / Chest / Abdomen / Colon]")
    parser.add_argument("--task",       type=str,   default=None, required=True,
                        help="Choose a specific part to be executed.")
    parser.add_argument("--weight",     type=str,   default=None)
    parser.add_argument("--image_path", type=str,   default=None, required=True)
    parser.add_argument("--save_path",  type=str,   default=None)
    parser.add_argument("--gpus",       type=str,   default="-1")

    args = parser.parse_args()

    main(args)