# -*- coding=UTF-8 -*-
# pyright: strict


import os
from typing import Dict, List, Optional, Text, Tuple

import cv2
import numpy as np
from PIL.Image import Image, fromarray

from auto_derby import imagetools

from . import window, action
import json

import logging
LOGGER = logging.getLogger(__name__)


DATA_PATH = os.getenv("AUTO_DERBY_OCR_LABELS_PATH", "ocr_labels.json")
IMAGE_PATH = os.getenv("AUTO_DERBY_OCR_IMAGES_PATH", "ocr_images.local")


def _load() -> Dict[Text, Text]:
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        return {}


def _save() -> None:
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(_LABELS, f, indent=2, ensure_ascii=False)


_LABELS = _load()


_PREVIEW_PADDING = 4


def _pad_img(img: np.ndarray, padding: int = _PREVIEW_PADDING) -> np.ndarray:
    p = padding
    return cv2.copyMakeBorder(img, p, p, p, p, cv2.BORDER_CONSTANT)


def _auto_level(img: np.ndarray) -> np.ndarray:
    black = np.percentile(img, 5)
    white = np.percentile(img, 95)
    if black == white:
        return img

    return np.clip((img - black) / (white - black) * 255, 0, 255).astype(np.uint8)


def _query(h: Text) -> Tuple[Text, float]:
    # TODO: use a more efficient data structure, maybe vp-tree
    if not _LABELS:
        return "", 0
    return sorted(((v, imagetools.compare_hash(h, k)) for k, v in _LABELS.items()), key=lambda x: x[1],  reverse=True)[0]


def _text_from_image(img: np.ndarray) -> Text:
    hash_img = cv2.GaussianBlur(img, (7, 7), 1, borderType=cv2.BORDER_CONSTANT)
    h = imagetools.image_hash(fromarray(hash_img), save_path=IMAGE_PATH)
    match, similarity = _query(h)
    LOGGER.debug("match label: hash=%s, value=%s, similarity=%0.3f",
                 h, match, similarity)
    if similarity > 0.8:
        return match
    ans = ""
    close_img = imagetools.show(fromarray(_pad_img(img)), h)
    close_msg = window.info("遇到新文本\n请在终端中标注")
    try:
        with action.recover_cursor(), window.recover_foreground(): # may during a drag
            while len(ans) != 1:
                ans = input("请输入当前显示图片对应的文本：")
        _LABELS[h] = ans
        LOGGER.info("labeled: hash=%s, value=%s", h, ans)
    finally:
        close_msg()
        close_img()
    _save()
    ret = _LABELS[h]
    LOGGER.debug("use label: hash=%s, value=%s", h, ret)
    return ret


def _union_bbox(*bbox: Optional[Tuple[int, int, int, int]]) -> Tuple[int, int, int, int]:
    b = [i for i in bbox if i]
    ret = b[0]
    for i in b[1:]:
        ret = (
            min(ret[0],  i[0]),
            min(ret[1],  i[1]),
            max(ret[2],  i[2]),
            max(ret[3],  i[3]),
        )
    return ret


def _rect2bbox(rect: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    x, y, w, h = rect
    l, t, r, b = x, y, x+w, y+h
    return l, t, r, b


def _bbox_contains(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> bool:
    return (
        a[0] <= b[0] and
        a[1] <= b[1] and
        a[2] >= b[2] and
        a[3] >= b[3]
    )

_LINE_HEIGHT = 32

def text(img: Image) -> Text:
    ret = ""

    w, h = img.width, img.height
    
    if img.height < _LINE_HEIGHT:
        w = round(_LINE_HEIGHT / h * w)
        h = _LINE_HEIGHT
        img = img.resize((w, h))
    cv_img = np.asarray(img.convert("L"))
    cv_img = _auto_level(cv_img)
    if cv_img[0, 0] == 255:
        cv_img = 255 - cv_img
    _, binary_img = cv2.threshold(
        cv_img,
        0,
        255,
        cv2.THRESH_OTSU,
    )

    contours, _ = cv2.findContours(
        binary_img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE,
    )

    if len(contours) == 0:
        LOGGER.debug("ocr result is empty")
        return ''

    contours_with_bbox = sorted(((i, _rect2bbox(cv2.boundingRect(i)))
                                 for i in contours), key=lambda x: x[1][0])

    max_char_width = max(bbox[2] - bbox[0] for _, bbox in contours_with_bbox)

    char_img_list: List[Tuple[Tuple[int, int, int, int], np.ndarray]] = []
    char_parts: List[np.ndarray] = []
    char_parts_bbox = None

    def _push_char():
        if not char_parts:
            return
        mask = np.zeros_like(binary_img)
        cv2.drawContours(
            mask,
            char_parts,
            -1,
            (255,),
            thickness=cv2.FILLED,
        )
        char_img = cv2.copyTo(binary_img, mask)
        assert char_parts_bbox is not None
        l, t, r, b = char_parts_bbox
        char_img = char_img[
            t:b,
            l:r,
        ]
        char_img_list.append((char_parts_bbox, char_img))

    for i, bbox in contours_with_bbox:
        is_new_char = (
            char_parts_bbox and
            bbox[0] > char_parts_bbox[0] + max_char_width * 0.6 and
            not _bbox_contains(char_parts_bbox, bbox)
        )
        if is_new_char:
            _push_char()
            char_parts = []
            char_parts_bbox = None
        char_parts.append(i)
        char_parts_bbox = _union_bbox(char_parts_bbox, bbox)
    _push_char()

    if os.getenv("DEBUG") == __name__:
        segmentation_img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        for i in contours:
            x, y, w, h = cv2.boundingRect(i)
            cv2.rectangle(segmentation_img, (x, y), (x+w, y+h),
                          (0, 0, 255), thickness=1)
        chars_img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        for bbox, _ in char_img_list:
            l, t, r, b = bbox
            cv2.rectangle(chars_img, (l, t), (r, b),
                          (0, 0, 255), thickness=1)
        cv2.imshow("ocr input", cv_img)
        cv2.imshow("ocr binary", binary_img)
        cv2.imshow("ocr segmentation", segmentation_img)
        cv2.imshow("ocr chars", chars_img)
        cv2.waitKey(200)
        cv2.destroyAllWindows()

    for _, i in char_img_list:
        ret += _text_from_image(i)

    LOGGER.debug("ocr result: %s", ret)

    return ret
