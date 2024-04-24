import os
import time
import subprocess
import pandas as pd
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor


def test_physionet_connection(username="", password=""):
    test_url = "https://physionet.org/files/mimic-cxr-jpg/2.0.0/"
    if username == "" and password == "":
        test_command = f"wget --spider '{test_url}'"
    else:
        test_command = f"wget --spider --user='{username}' --password='{password}' '{test_url}'"
    return subprocess.call(test_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def add_physionet_credentials_to_netrc(username, password):
    netrc_file_path = os.path.expanduser("~/.netrc")
    physionet_entry = f"machine physionet.org\nlogin {username}\npassword {password}\n"

    if physionet_entry not in open(netrc_file_path).read():
        with open(netrc_file_path, "a") as netrc_file:
            netrc_file.write(physionet_entry)
        os.chmod(netrc_file_path, 0o600)


def download_file(file_path, prefix="https://physionet.org/files/mimic-cxr-jpg/2.0.0/files"):
    wget_params = "-r -N -c -np --netrc"
    file_url = f"{prefix}/{file_path}"
    if subprocess.call(f"wget {wget_params} '{file_url}'", shell=True) != 0:
        print(f"Error: Failed to download {file_url}")
        exit(1)


def main():
    start_time = time.time()

    if test_physionet_connection():
        print("PhysioNet connection is already configured.")
    else:
        physionet_username = input("Enter your PhysioNet username: ")
        physionet_password = getpass("Enter your PhysioNet password: ")

        if not test_physionet_connection(physionet_username, physionet_password):
            print("Error: Unable to connect to PhysioNet. Please check your credentials.")
            exit(1)

        add_physionet_credentials_to_netrc(physionet_username, physionet_password)

    # download the meta file
    download_file("mimic-cxr-2.0.0-metadata.csv.gz", "https://physionet.org/files/mimic-cxr-jpg/2.0.0/")

    # read the meta file and download the frontal images
    meta_data = pd.read_csv("physionet.org/files/mimic-cxr-jpg/2.0.0/mimic-cxr-2.0.0-metadata.csv.gz")
    meta_data = meta_data[meta_data.ViewPosition.isin(["AP", "PA"])]  # NOTE: Only download frontal (AP/PA) images

    print(f"Total number of unique images: {len(meta_data)}")
    jpg_image_path_list = []
    for _, item in meta_data.iterrows():
        pid = str(item["subject_id"])
        sid = str(item["study_id"])
        iid = str(item["dicom_id"])
        jpg_image_path = f"p{pid[:2]}/p{pid}/s{sid}/{iid}.jpg"
        jpg_image_path_list.append(jpg_image_path)
    print(f"Total number of unique images: {len(jpg_image_path_list)}")

    # # single threaded download
    # for jpg_image_path in jpg_image_path_list:
    #     download_file(jpg_image_path)

    # Download the images in parallel
    print("Downloading images in parallel...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(download_file, jpg_image_path_list)

    print("All images have been successfully downloaded.")
    print(f"Script runtime: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
