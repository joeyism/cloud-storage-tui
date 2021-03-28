import curses
from cloudstoragetui.display import screen_init
from cloudstoragetui.cloud.cloudclient import CloudClient
from cloudstoragetui.cloud.provider import CloudProviders

def main():
    cloud_adapter = CloudClient.initiate(CloudProviders.GCLOUD)
    curses.wrapper(screen_init, cloud_adapter=cloud_adapter)

if __name__ == "__main__":
    main()
