# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_transforms.ipynb (unless otherwise specified).

__all__ = ['AlbumentationTransformer']

# Cell
import albumentations as A
from .imports import *
from .core import *
from .data.all import *

# Cell
class AlbumentationTransformer:
    bbox_params=A.BboxParams(format='pascal_voc', label_fields=['oids'])
    def __init__(self, tfms):
        self.tfms = A.Compose(tfms, bbox_params=self.bbox_params)

    def __call__(self, record): return self.apply(record)

    def apply(self, record):
        d = self.tfms(
            image = open_img(record.iinfo.fp),
            bboxes = [o.xyxy for o in record.annot.bboxes],
            masks = [o.to_mask(record.iinfo.h, record.iinfo.w).data for o in record.annot.segs],
            oids = record.annot.oids,
            keypoints = record.annot.kpts,
        )
        # TODO: Don't use dicts
        h,w,_ = d['image'].shape
        iinfo = dict(h=h, w=w)
        annot = dict(
            oids=d['oids'],
            bboxes=[BBox.from_xyxy(*o) for o in d['bboxes']] if notnone(d['bboxes']) else None,
            segs=Mask(np.stack(d['masks'])) if notnone(d['masks']) else None,
        #     kpts=res['keypoints'] # TODO
        )
        return d['image'], record.new(iinfo=iinfo, annot=annot)