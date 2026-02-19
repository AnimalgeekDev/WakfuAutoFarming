import os
import shutil
import cv2
import albumentations as A
from albumentations import BboxParams
import argparse


def read_yolo_labels(label_path):
    """Read YOLO label file and return list of bboxes and class labels.

    Each line: <class> <x_center> <y_center> <width> <height>
    Returns bboxes as list of tuples (x_center, y_center, w, h) (floats normalized)
    and labels as list of strings (or ints as strings) to keep compatibility with albumentations.
    """
    bboxes = []
    labels = []
    if not os.path.exists(label_path):
        return bboxes, labels
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            cls = parts[0]
            coords = list(map(float, parts[1:5]))
            bboxes.append(tuple(coords))
            labels.append(cls)
    return bboxes, labels


def write_yolo_labels(label_path, bboxes, labels):
    """Write YOLO label file from bboxes and labels.

    bboxes expected as list of (x_center, y_center, w, h) normalized floats.
    labels expected matching length.
    """
    with open(label_path, "w") as f:
        for cls, bbox in zip(labels, bboxes):
            f.write(f"{cls} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")


def ensure_dirs(base_out):
    images_orig = os.path.join(base_out, "images_original")
    labels_orig = os.path.join(base_out, "labels_original")
    images_aug = os.path.join(base_out, "images")
    labels_aug = os.path.join(base_out, "labels")
    os.makedirs(images_orig, exist_ok=True)
    os.makedirs(labels_orig, exist_ok=True)
    os.makedirs(images_aug, exist_ok=True)
    os.makedirs(labels_aug, exist_ok=True)
    return images_orig, labels_orig, images_aug, labels_aug


def augment_yolo_dataset(input_dir, output_dir, num_augmented=5):
    """Read images and YOLO labels from input_dir and write originals + augmented outputs to output_dir.

    - Copies originals into output_dir/images_original and output_dir/labels_original
    - Saves augmented images into output_dir/images and labels into output_dir/labels
    """
    # Define augmentation pipeline with bbox support (YOLO format: x_center y_center w h normalized)
    aug = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.Rotate(limit=10, p=0.4, border_mode=cv2.BORDER_CONSTANT),
        A.GaussianBlur(p=0.2),
        A.RandomScale(scale_limit=0.15, p=0.4),
        A.ShiftScaleRotate(shift_limit=0.02, scale_limit=0, rotate_limit=0, p=0.3),
    ], bbox_params=BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.0))

    images_orig_dir, labels_orig_dir, images_out_dir, labels_out_dir = ensure_dirs(output_dir)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        image_path = os.path.join(input_dir, filename)
        base_name, ext = os.path.splitext(filename)
        label_filename = base_name + '.txt'
        label_path = os.path.join(input_dir, label_filename)

        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image {image_path}, skipping.")
            continue

        # Read labels
        bboxes, labels = read_yolo_labels(label_path)

        # Copy originals safely to output (do not overwrite existing files)
        out_image_orig = os.path.join(images_orig_dir, filename)
        out_label_orig = os.path.join(labels_orig_dir, label_filename)
        if not os.path.exists(out_image_orig):
            shutil.copy2(image_path, out_image_orig)
        if os.path.exists(label_path) and not os.path.exists(out_label_orig):
            shutil.copy2(label_path, out_label_orig)

        # Generate augmented images
        for i in range(num_augmented):
            try:
                augmented = aug(image=image, bboxes=bboxes, class_labels=labels)
            except Exception as e:
                print(f"Augmentation failed for {filename} iter {i}: {e}")
                continue

            aug_image = augmented['image']
            aug_bboxes = augmented.get('bboxes', [])
            aug_labels = augmented.get('class_labels', [])

            # If no bboxes remain after augmentation, skip saving to avoid bad labels
            if len(aug_bboxes) == 0:
                # If original had no bbox, still save augmented image with empty label file
                if len(bboxes) == 0:
                    out_aug_image = os.path.join(images_out_dir, f"{base_name}_aug_{i}{ext}")
                    out_aug_label = os.path.join(labels_out_dir, f"{base_name}_aug_{i}.txt")
                    cv2.imwrite(out_aug_image, aug_image)
                    open(out_aug_label, 'w').close()
                else:
                    # Skip this augmentation because all boxes disappeared
                    continue
            else:
                out_aug_image = os.path.join(images_out_dir, f"{base_name}_aug_{i}{ext}")
                out_aug_label = os.path.join(labels_out_dir, f"{base_name}_aug_{i}.txt")
                cv2.imwrite(out_aug_image, aug_image)
                write_yolo_labels(out_aug_label, aug_bboxes, aug_labels)


def parse_args():
    p = argparse.ArgumentParser(description='Data augmentation for YOLO (keeps originals safe).')
    p.add_argument('input_dir', help='Directory with original images and YOLO .txt labels')
    p.add_argument('output_dir', help='Directory where originals will be copied and augmented data saved')
    p.add_argument('--num', type=int, default=5, help='Number of augmented images to generate per original')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    augment_yolo_dataset(args.input_dir, args.output_dir, num_augmented=args.num)
