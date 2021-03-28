from typing import List

from cloudstoragetui.cloud.gcloud_adapter import GCloudAdapter
from cloudstoragetui.cloud import gcloud
from cloudstoragetui.cloud.adapter import CloudAdapter
from cloudstoragetui.cloud.provider import CloudProviders

class CloudClient:

    @classmethod
    def list_filenames_by_fullpath(cls, path, provider) -> List[str]:
        if provider == CloudProviders.GCLOUD:
            return gcloud.list_filenames_by_fullpath(path)

    @classmethod
    def initiate(cls, provider: str) -> CloudAdapter:
        if provider == CloudProviders.GCLOUD:
            return GCloudAdapter()
