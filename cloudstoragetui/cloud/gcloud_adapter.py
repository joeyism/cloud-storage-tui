from typing import List

from cloudstoragetui.cloud import gcloud
from cloudstoragetui.cloud.adapter import CloudAdapter
from cloudstoragetui.filesystem import Folder, File
from cloudstoragetui.cloud.provider import CloudProviders

class GCloudAdapter(CloudAdapter):

    def initiate_buckets(self) -> List[List[Folder]]:
        results: List[Folder] = []
        bucket_paths = gcloud.list_buckets()
        for bucket_path in bucket_paths:
            results.append(Folder(bucket_path, None, CloudProviders.GCLOUD))
        return [results, [], []]
