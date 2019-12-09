#!/usr/bin/env python
import os
import sys

from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# config
os.chdir(os.path.join(os.path.dirname(sys.argv[0]), '.'))
if os.path.exists('settings.py'):
    exec(open('settings.py').read())

DEFAULT_TAG = "python_sample_basic"
DEFAULT_TAG0 = "dog"
DEFAULT_TAG1 = "snow"
DEFAULT_TAG2 = "olive"
DEFAULT_TAG3 = "pet"
DEFAULT_TAG4 = "joy"

def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))


def upload_files():
# a. Automatically limit image size to 500x500 pixels on upload.
    print("--- Upload a local file")
    response = upload("asuna.jpg", tags=DEFAULT_TAG0)
    dump_response(response)
    url, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        width=500,
        height=500,
        crop="fit"
    )
    print("Automatically limit image size to 500x500 pixels on upload url: " + url)
    print("")

    print("--- Upload a local file")
    response = upload("asuna.jpg", tags=DEFAULT_TAG0)
    dump_response(response)
    url, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        width=200,
        height=150,
        overlay="cloudinary-icon_bgbrty",
        crop="fill"
    )
    print("Fill 200x150 WaterMark url: " + url)
    print("")
    
    print("--- Upload a local file with custom public ID")
    response = upload(
        "olive.jpg",
        tags=DEFAULT_TAG2,
        public_id="olive_you",
    )
    dump_response(response)
    url, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        width=1920,
        height=1080,
        crop="fit"
    )
    print("Add Public Tag url: " + url)
    print("")
# a. One with the Cloudinary logo as an overlay (watermark).
    print("--- Upload a local file with eager transformation of scaling to 500x500 with WaterMark Overlay")
    response = upload(
        "snow.jpg",
        tags=DEFAULT_TAG1,
        public_id="eager_water_lake",
        eager=dict(
            width=500,
            height=500,
            overlay="cloudinary-icon_bgbrty",
            crop="scale"
        ),
    )
# b.Second with the image saturation increased to 50%
    print("--- Fetch an uploaded remote image, fitting it into 500x500 and reducing saturation")
    response = upload(
        "pumpkin.jpg",
        tags=DEFAULT_TAG4,
        width=500,
        height=500,
        crop="fit",
        effect="saturation:50",
    )
    dump_response(response)
    url, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
        width=200,
        height=150,
        crop="fill",
        gravity="faces",
        radius=10,
        effect="sepia",
    )
    print("Fill 200x150, round corners, apply the sepia effect, url: " + url)
    print("")


def cleanup():
    response = resources_by_tag(DEFAULT_TAG)
    resources = response.get('resources', [])
    if not resources:
        print("No images found")
        return
    print("Deleting {0:d} images...".format(len(resources)))
    delete_resources_by_tag(DEFAULT_TAG)
    print("Done!")


if len(sys.argv) > 1:
    if sys.argv[1] == 'upload':
        upload_files()
    if sys.argv[1] == 'cleanup':
        cleanup()
else:
    print("--- Uploading files and then cleaning up")
    print("    you can only choose one instead by passing 'upload' or 'cleanup' as an argument")
    print("")
    upload_files()
