import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import cv2
import math
import numpy as np

from PIL import Image

import torch
import torchvision.transforms as transforms

from simpleAICV.classification.autorandaugment import ImageNet1KPolicy, SubAugmentPolicy


class Opencv2PIL:

    def __init__(self):
        pass

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = Image.fromarray(np.uint8(image))

        return {
            'image': image,
            'label': label,
        }


class PIL2Opencv:

    def __init__(self):
        pass

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = np.asarray(image).astype(np.float32)

        return {
            'image': image,
            'label': label,
        }


class TorchRandomResizedCrop:

    def __init__(self, resize=224):
        self.RandomResizedCrop = transforms.RandomResizedCrop(int(resize))

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = self.RandomResizedCrop(image)

        return {
            'image': image,
            'label': label,
        }


class TorchPad:

    def __init__(self, padding=4, fill=0, padding_mode='reflect'):
        self.Pad = transforms.Pad(padding=padding,
                                  fill=fill,
                                  padding_mode=padding_mode)

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = self.Pad(image)

        return {
            'image': image,
            'label': label,
        }


class TorchRandomHorizontalFlip:

    def __init__(self, prob=0.5):
        self.RandomHorizontalFlip = transforms.RandomHorizontalFlip(prob)

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = self.RandomHorizontalFlip(image)

        return {
            'image': image,
            'label': label,
        }


class TorchRandomCrop:

    def __init__(self, resize=224):
        self.RandomCrop = transforms.RandomCrop(int(resize))

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = self.RandomCrop(image)

        return {
            'image': image,
            'label': label,
        }


class TorchColorJitter:

    def __init__(self, brightness=0.4, contrast=0.4, saturation=0.4, hue=0):
        self.ColorJitter = transforms.ColorJitter(brightness=brightness,
                                                  contrast=contrast,
                                                  saturation=saturation,
                                                  hue=hue)

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = self.ColorJitter(image)

        return {
            'image': image,
            'label': label,
        }


class TorchResize:

    def __init__(self, resize=224):
        self.Resize = transforms.Resize(int(resize))

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = self.Resize(image)

        return {
            'image': image,
            'label': label,
        }


class TorchCenterCrop:

    def __init__(self, resize=224):
        self.CenterCrop = transforms.CenterCrop(int(resize))

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = self.CenterCrop(image)

        return {
            'image': image,
            'label': label,
        }


class Normalize:

    def __init__(self):
        pass

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = image / 255.
        image = image.astype(np.float32)

        return {
            'image': image,
            'label': label,
        }


class NormalizeTo255:

    def __init__(self):
        pass

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = image * 255.
        image = image.astype(np.float32)

        return {
            'image': image,
            'label': label,
        }


class AutoAugment:

    def __init__(self, policy_list=ImageNet1KPolicy):
        self.policy_list = policy_list

    def __call__(self, sample):
        image, label = sample['image'], sample['label']

        idx = np.random.choice(len(self.policy_list))
        policy = self.policy_list[idx]
        for per_policy in policy:
            func = SubAugmentPolicy(per_policy[0], per_policy[1],
                                    per_policy[2])
            image = func(image)

        return {
            'image': image,
            'label': label,
        }


class RandAugment:

    def __init__(self, N=2, M=10):
        self.transform_list = [
            'autocontrast', 'equalize', 'invert', 'rotate', 'posterize',
            'solarize', 'color', 'contrast', 'brightness', 'sharpness',
            'shearx', 'sheary', 'translatex', 'translatey', 'cutout',
            'solarizeadd'
        ]
        self.N = N
        self.M = M

    def __call__(self, sample):
        image, label = sample['image'], sample['label']

        for _ in range(self.N):
            policy_idx = np.random.choice(len(self.transform_list))
            policy_name = self.transform_list[policy_idx]
            magnitude_level = float(self.M)
            prob = np.random.uniform(0.2, 0.8)
            func = SubAugmentPolicy(policy_name, magnitude_level, prob)
            image = func(image)

        return {
            'image': image,
            'label': label,
        }


class TorchMeanStdNormalize:

    def __init__(self, mean, std):
        self.to_tensor = transforms.ToTensor()
        self.Normalize = transforms.Normalize(mean=mean, std=std)

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']
        image = self.to_tensor(image)
        image = self.Normalize(image)
        # 3 H W ->H W 3
        image = image.permute(1, 2, 0)
        image = image.numpy()

        return {
            'image': image,
            'label': label,
        }


class ReflectPad:

    def __init__(self, pad=4):
        self.pad = pad

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']
        image = cv2.copyMakeBorder(image, self.pad, self.pad, self.pad,
                                   self.pad, cv2.BORDER_REFLECT)

        return {
            'image': image,
            'label': label,
        }


class PCAJitter:

    def __init__(self,
                 pca_std=0.1,
                 vals=[[0.2175, 0.0188, 0.0045]],
                 vecs=[[-0.5675, 0.7192, 0.4009], [-0.5808, -0.0045, -0.8140],
                       [-0.5836, -0.6948, 0.4203]]):
        self.pca_std = pca_std
        self.vals = vals
        self.vecs = vecs

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'annots'、'scale' keys.
        '''
        image, label = sample['image'], sample['label']

        alpha = np.random.normal(0, self.pca_std, size=(1, 3))
        alpha = np.repeat(alpha, 3, axis=0)
        vals = np.repeat(np.array(self.vals), 3, axis=0)
        rgb = np.sum(np.array(self.vecs) * alpha * vals, axis=1)

        for i in range(3):
            image[:, :, i] = image[:, :, i] + rgb[i]

        return {
            'image': image,
            'label': label,
        }


class RandomCrop:

    def __init__(self, resize=32):
        self.resize = int(resize)

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']
        origin_h, origin_w, _ = image.shape

        if origin_w < self.resize or origin_h < self.resize:
            image = cv2.copyMakeBorder(image,
                                       0,
                                       max(0, self.resize - origin_h),
                                       max(0, self.resize - origin_w),
                                       0,
                                       cv2.BORDER_CONSTANT,
                                       value=[0, 0, 0])

        top, left, h, w = self.get_top_left_w_h(origin_h, origin_w)
        image = image[top:top + h, left:left + w, :]

        return {
            'image': image,
            'label': label,
        }

    def get_top_left_w_h(self, origin_h, origin_w):
        if origin_w == self.resize and origin_h == self.resize:
            return 0, 0, origin_h, origin_w

        i = np.random.randint(0, origin_h - self.resize + 1)
        j = np.random.randint(0, origin_w - self.resize + 1)

        return i, j, self.resize, self.resize


class RandomResizedCrop:

    def __init__(self,
                 resize=224,
                 scale_range=[0.08, 1.0],
                 ratio_range=[3. / 4., 4. / 3.]):
        self.resize = int(resize)
        self.scale_range = scale_range
        self.ratio_range = ratio_range

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        origin_h, origin_w, _ = image.shape

        top, left, h, w = self.get_top_left_w_h(origin_h, origin_w)

        image = image[top:top + h, left:left + w, :]
        image = cv2.resize(image, (self.resize, self.resize))

        return {
            'image': image,
            'label': label,
        }

    def get_top_left_w_h(self, origin_h, origin_w):
        area = origin_h * origin_w

        log_ratio = [
            math.log(self.ratio_range[0]),
            math.log(self.ratio_range[1])
        ]

        for _ in range(10):
            target_area = area * np.random.uniform(self.scale_range[0],
                                                   self.scale_range[1])
            aspect_ratio = math.exp(
                np.random.uniform(log_ratio[0], log_ratio[1]))

            w = int(round(math.sqrt(target_area * aspect_ratio)))
            h = int(round(math.sqrt(target_area / aspect_ratio)))

            if 0 < w <= origin_w and 0 < h <= origin_h:
                top = np.random.randint(0, origin_h - h + 1)
                left = np.random.randint(0, origin_w - w + 1)

                return top, left, h, w

        # Fallback to central crop
        in_ratio = float(origin_w) / float(origin_h)
        if in_ratio < min(self.ratio_range):
            w = origin_w
            h = int(round(w / min(self.ratio_range)))
        elif in_ratio > max(self.ratio_range):
            w = int(round(h * max(self.ratio_range)))
            h = origin_h
        else:  # whole image
            w = origin_w
            h = origin_h

        top = (origin_h - h) // 2
        left = (origin_w - w) // 2

        return top, left, h, w


class CenterCrop:

    def __init__(self, resize=224):
        self.resize = int(resize)

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        origin_h, origin_w, _ = image.shape
        crop_height, crop_width = self.resize, self.resize

        if crop_width > origin_w or crop_height > origin_h:
            padding_ltrb = [
                (crop_width - origin_w) // 2 if crop_width > origin_w else 0,
                (crop_height - origin_h) // 2 if crop_height > origin_h else 0,
                (crop_width - origin_w + 1) //
                2 if crop_width > origin_w else 0,
                (crop_height - origin_h + 1) //
                2 if crop_height > origin_h else 0,
            ]
            image = cv2.copyMakeBorder(image,
                                       padding_ltrb[1],
                                       padding_ltrb[3],
                                       padding_ltrb[0],
                                       padding_ltrb[2],
                                       cv2.BORDER_CONSTANT,
                                       value=[0, 0, 0])
            origin_h, origin_w, _ = image.shape

            if crop_width == origin_w and crop_height == origin_h:
                return {
                    'image': image,
                    'label': label,
                }

        crop_top = int(round((origin_h - crop_height) / 2.))
        crop_left = int(round((origin_w - crop_width) / 2.))

        new_h, new_w = max(crop_top + crop_height,
                           origin_h), max(crop_left + crop_width, origin_w)
        padded_image = np.zeros((new_h, new_w, 3), dtype=np.float32)
        padded_image[:origin_h, :origin_w, :] = image
        image = padded_image
        image = image[crop_top:crop_top + crop_height,
                      crop_left:crop_left + crop_width, :]

        return {
            'image': image,
            'label': label,
        }


class RandomHorizontalFlip:

    def __init__(self, prob=0.5):
        self.prob = prob

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        if np.random.uniform(0, 1) < self.prob:
            image = image[:, ::-1, :]

        return {
            'image': image,
            'label': label,
        }


class ColorJitter:

    def __init__(self, brightness=0.4, contrast=0.4, saturation=0.4, hue=0):
        assert brightness >= 0 and contrast >= 0 and saturation >= 0 and hue >= 0, 'brightness/contrast/saturation/hue value must be non negative!'
        assert 0.0 <= hue <= 0.5, 'hue value should >=0.0 and <=0.5!'
        self.brightness_range = [
            max(0.0, 1 - float(brightness)), 1 + float(brightness)
        ]
        self.contrast_range = [
            max(0.0, 1 - float(contrast)), 1 + float(contrast)
        ]
        self.saturation_range = [
            max(0.0, 1 - float(saturation)), 1 + float(saturation)
        ]
        self.hue_range = [-hue, hue]

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']
        image = image.astype(np.float32)

        color_jitter_type_idx = np.random.choice([0, 1, 2, 3])
        if color_jitter_type_idx == 0:
            brightness_factor = np.random.uniform(self.brightness_range[0],
                                                  self.brightness_range[1])
            image = image * brightness_factor
            image = np.clip(image, 0, 255)

        elif color_jitter_type_idx == 1:
            contrast_factor = np.random.uniform(self.contrast_range[0],
                                                self.contrast_range[1])
            mean_value = round(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).mean())
            image = (1 -
                     contrast_factor) * mean_value + contrast_factor * image
            image = np.clip(image, 0, 255)

        elif color_jitter_type_idx == 2:
            saturation_factor = np.random.uniform(self.saturation_range[0],
                                                  self.saturation_range[1])
            degenerate = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY),
                                      cv2.COLOR_GRAY2RGB)
            image = (
                1 - saturation_factor) * degenerate + saturation_factor * image
            image = np.clip(image, 0, 255)

        elif color_jitter_type_idx == 3:
            hue_factor = np.random.uniform(self.hue_range[0],
                                           self.hue_range[1])
            image = image.astype(np.uint8)
            hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV_FULL)
            hsv_image[..., 0] += np.uint8(hue_factor * 255)
            image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB_FULL)

        image = image.astype(np.float32)

        return {
            'image': image,
            'label': label,
        }


class Resize:

    def __init__(self, resize=224):
        self.resize = int(resize)

    def __call__(self, sample):
        '''
        sample must be a dict,contains 'image'、'label' keys.
        '''
        image, label = sample['image'], sample['label']

        image = cv2.resize(image, (self.resize, self.resize))

        return {
            'image': image,
            'label': label,
        }


class ClassificationCollater:

    def __init__(self):
        pass

    def __call__(self, data):
        images = [s['image'] for s in data]
        labels = [s['label'] for s in data]

        images = np.array(images).astype(np.float32)
        labels = np.array(labels).astype(np.float32)

        images = torch.from_numpy(images).float()
        # B H W 3 ->B 3 H W
        images = images.permute(0, 3, 1, 2)
        labels = torch.from_numpy(labels).long()

        return {
            'image': images,
            'label': labels,
        }


class ClassificationDataPrefetcher:

    def __init__(self, loader):
        self.loader = iter(loader)
        self.stream = torch.cuda.Stream()
        self.preload()

    def preload(self):
        try:
            sample = next(self.loader)
            self.next_inputs, self.next_labels = sample['image'], sample[
                'label']
        except StopIteration:
            self.next_inputs = None
            self.next_labels = None

            return
        with torch.cuda.stream(self.stream):
            self.next_inputs = self.next_inputs.cuda(non_blocking=True)
            self.next_labels = self.next_labels.cuda(non_blocking=True)
            self.next_inputs = self.next_inputs.float()

    def next(self):
        torch.cuda.current_stream().wait_stream(self.stream)
        inputs = self.next_inputs
        labels = self.next_labels
        self.preload()

        return inputs, labels


class AverageMeter:
    '''Computes and stores the average and current value'''

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class AccMeter:
    '''Computes and stores the average and current value'''

    def __init__(self):
        self.reset()

    def reset(self):
        self.acc1_correct_num = 0
        self.acc5_correct_num = 0
        self.sample_num = 0
        self.acc1 = 0
        self.acc5 = 0

    def update(self, acc1_correct_num, acc5_correct_num, sample_num):
        self.acc1_correct_num += acc1_correct_num
        self.acc5_correct_num += acc5_correct_num
        self.sample_num += sample_num

    def compute(self):
        self.acc1 = float(self.acc1_correct_num
                          ) / self.sample_num if self.sample_num != 0 else 0
        self.acc5 = float(self.acc5_correct_num
                          ) / self.sample_num if self.sample_num != 0 else 0


class TotalAccMeter:
    '''Computes and stores the average and current value'''

    def __init__(self):
        self.reset()

    def reset(self):
        self.acc1 = 0
        self.acc5 = 0
        self.count = 0
        self.acc1_avg = 0
        self.acc5_avg = 0

    def update(self, acc1, acc5, n=1):
        self.acc1 += acc1 * n
        self.acc5 += acc5 * n
        self.count += n

    def compute(self):
        self.acc1_avg = float(self.acc1) / self.count if self.count != 0 else 0
        self.acc5_avg = float(self.acc5) / self.count if self.count != 0 else 0


def compute_batch_accuracy(output, target, topk=(1, 5)):
    '''Computes the accuracy over the k top predictions for the specified values of k'''
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(1.0 / batch_size))

        return res


def load_state_dict(saved_model_path, model, excluded_layer_name=()):
    '''
    saved_model_path: a saved model.state_dict() .pth file path
    model: a new defined model
    excluded_layer_name: layer names that doesn't want to load parameters
    only load layer parameters which has same layer name and same layer weight shape
    '''
    if not saved_model_path:
        print('No pretrained model file!')
        return

    saved_state_dict = torch.load(saved_model_path,
                                  map_location=torch.device('cpu'))

    filtered_state_dict = {
        name: weight
        for name, weight in saved_state_dict.items()
        if name in model.state_dict() and not any(
            excluded_name in name for excluded_name in excluded_layer_name)
        and weight.shape == model.state_dict()[name].shape
    }

    if len(filtered_state_dict) == 0:
        print('No pretrained parameters to load!')
    else:
        model.load_state_dict(filtered_state_dict, strict=False)

    return