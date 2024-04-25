import os
import time
import subprocess
from getpass import getpass
import json
import shutil


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


def download_and_extract(file_url, destination_dir):
    wget_params = "-r -N -c -np --netrc"
    file_name = os.path.basename(file_url)
    subprocess.run(f"wget {wget_params} '{file_url}'", shell=True)
    if file_name.endswith(".zip"):
        shutil.unpack_archive(os.path.join(destination_dir, file_name), destination_dir)
    elif file_name.endswith(".gz"):
        subprocess.run(f"gzip -d {os.path.join(destination_dir, file_name)}", shell=True)
    else:
        pass


def download_files(file_list):
    for file_url, destination_dir in file_list:
        download_and_extract(file_url, destination_dir)


def run_subprocess_command(command):
    subprocess.run(command, shell=True)


def run_dev_phase():
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

    # MIMIC_CXR = "https://physionet.org/files/mimic-cxr-jpg/2.0.0"
    # CHEST_IMAGENOME_BASE = "https://physionet.org/files/chest-imagenome/1.0.0"
    # CHEST_IMAGENOME_SILVER = f"{CHEST_IMAGENOME_BASE}/silver_dataset"
    # CHEST_IMAGENOME_GOLD = f"{CHEST_IMAGENOME_BASE}/gold_dataset"
    # CHEST_IMAGENOME_UTILS = f"{CHEST_IMAGENOME_BASE}/utils/scene_postprocessing"
    # CHEST_IMAGENOME_SEMANTICS = f"{CHEST_IMAGENOME_BASE}/semantics"
    # MIMIC_IV = "https://physionet.org/files/mimiciv/2.2"

    # file_list = [
    #     (f"{MIMIC_CXR}/mimic-cxr-2.0.0-metadata.csv.gz", "physionet.org/files/mimic-cxr-jpg/2.0.0"),
    #     (f"{CHEST_IMAGENOME_SILVER}/scene_graph.zip", "physionet.org/files/chest-imagenome/1.0.0/silver_dataset"),
    #     (f"{CHEST_IMAGENOME_GOLD}/gold_attributes_relations_500pts_500studies1st.txt", "physionet.org/files/chest-imagenome/1.0.0/gold_dataset"),
    #     (f"{CHEST_IMAGENOME_GOLD}/gold_bbox_coordinate_annotations_1000images.csv", "physionet.org/files/chest-imagenome/1.0.0/gold_dataset"),
    #     (f"{CHEST_IMAGENOME_UTILS}/scenegraph_postprocessing.py", "physionet.org/files/chest-imagenome/1.0.0/utils/scene_postprocessing"),
    #     (f"{CHEST_IMAGENOME_SEMANTICS}/attribute_relations_v1.txt", "physionet.org/files/chest-imagenome/1.0.0/semantics"),
    #     (f"{CHEST_IMAGENOME_SEMANTICS}/label_to_UMLS_mapping.json", "physionet.org/files/chest-imagenome/1.0.0/semantics"),
    #     (f"{CHEST_IMAGENOME_SEMANTICS}/objects_extracted_from_reports_v1.txt", "physionet.org/files/chest-imagenome/1.0.0/semantics"),
    #     (f"{MIMIC_IV}/hosp/admissions.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/diagnoses_icd.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/d_icd_diagnoses.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/d_icd_procedures.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/d_labitems.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/labevents.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/microbiologyevents.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/patients.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/prescriptions.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/procedures_icd.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/hosp/transfers.csv.gz", "physionet.org/files/mimiciv/2.2/hosp"),
    #     (f"{MIMIC_IV}/icu/chartevents.csv.gz", "physionet.org/files/mimiciv/2.2/icu"),
    #     (f"{MIMIC_IV}/icu/d_items.csv.gz", "physionet.org/files/mimiciv/2.2/icu"),
    #     (f"{MIMIC_IV}/icu/icustays.csv.gz", "physionet.org/files/mimiciv/2.2/icu"),
    #     (f"{MIMIC_IV}/icu/inputevents.csv.gz", "physionet.org/files/mimiciv/2.2/icu"),
    #     (f"{MIMIC_IV}/icu/outputevents.csv.gz", "physionet.org/files/mimiciv/2.2/icu"),
    # ]

    # orig_dir = os.getcwd()

    # download_files(file_list)

    # os.chdir("physionet.org/files/chest-imagenome/1.0.0/utils/scene_postprocessing")
    # with open("scenegraph_postprocessing_settings.json", "w") as f:
    #     json.dump(
    #         {
    #             "SCENE_DIR": "../../silver_dataset/scene_graph",
    #             "OUTPUT_DIR": "../../silver_dataset/scene_tabular",
    #             "OUTPUT_TYPE": ["attributes", "objects"],
    #             "RDF_LEVEL": "study_id",
    #             "RESOURCE": "../../semantics/label_to_UMLS_mapping.json",
    #             "AGGREGATION": "last",
    #             "INCLUDE_SECTIONS": "all",
    #         },
    #         f,
    #     )
    # run_subprocess_command("python scenegraph_postprocessing.py")
    # print("Done with scene postprocessing")
    # os.chdir(orig_dir)

    # SAVE_DIR = "dataset_builder/preprocessed_data/"
    # PREPROCESS_SCRIPTS = ["preprocess_cohort.py", "preprocess_label.py"]
    # SPLITS = ["train", "valid", "test"]
    # os.makedirs(SAVE_DIR, exist_ok=True)

    # for split in SPLITS:
    #     for script in PREPROCESS_SCRIPTS:
    #         run_subprocess_command(
    #             f"python dataset_builder/{script} "
    #             f"--mimic_cxr_jpg_dir physionet.org/files/mimic-cxr-jpg/2.0.0/ "
    #             f"--chest_imagenome_dir physionet.org/files/chest-imagenome/1.0.0/ "
    #             f"--save_dir {SAVE_DIR}"
    #         )

    splits = {"gold": 400, "silver": 800}
    for split, num_patient in splits.items():
        print(f"Processing {split} split with {num_patient} patients...")
        run_subprocess_command(
            f"python dataset_builder/preprocess_db.py "
            f"--split {split} "
            f"--mimic_iv_dir physionet.org/files/mimiciv/2.2/ "
            f"--mimic_cxr_jpg_dir physionet.org/files/mimic-cxr-jpg/2.0.0/ "
            f"--chest_imagenome_dir physionet.org/files/chest-imagenome/1.0.0/ "
            f"--db_name mimic_iv_cxr "
            f"--out_dir ./database "
            f"--deid "
            f"--timeshift "
            f"--current_time '2105-12-31 23:59:00' "
            f"--start_year 2100 "
            f"--time_span 5 "
            f"--cur_patient_ratio 0.1 "
            f"--num_patient {num_patient}"
        )
    print("Database preprocessing complete.")

    run_subprocess_command(
        f"python dataset_builder/generate_answer.py "
        f"--mimic_iv_dir physionet.org/files/mimiciv/2.2/ "
        f"--mimic_cxr_jpg_dir physionet.org/files/mimic-cxr-jpg/2.0.0/ "
        f"--chest_imagenome_dir physionet.org/files/chest-imagenome/1.0.0/ "
        f"--json_file_path dataset/mimic_iv_cxr/train/_train.json "
        f"--db_file_path database/mimic_iv_cxr/silver/mimic_iv_cxr.db "
        f"--output_path dataset/mimic_iv_cxr/train/train_data.json "
        f"--output_answer_path dataset/mimic_iv_cxr/train/train_answer.json"
    )

    end_time = time.time()
    runtime = end_time - start_time
    print(f"Script runtime: {runtime:.2f} seconds")


def run_test_phase():

    if os.path.exists("dataset/mimic_iv_cxr/_valid.json"):
        with open("dataset/mimic_iv_cxr/_valid.json", "r") as f:
            valid_data = json.load(f)
        if "_gold_program" not in valid_data[0]:
            raise ValueError("Currently, the script only supports the dev phase.")
    else:
        raise ValueError("Currently, the script only supports the dev phase.")

    start_time = time.time()
    run_subprocess_command(
        f"python dataset_builder/generate_answer.py "
        f"--mimic_iv_dir physionet.org/files/mimiciv/2.2/ "
        f"--mimic_cxr_jpg_dir physionet.org/files/mimic-cxr-jpg/2.0.0/ "
        f"--chest_imagenome_dir physionet.org/files/chest-imagenome/1.0.0/ "
        f"--json_file_path dataset/mimic_iv_cxr/_valid.json "
        f"--db_file_path database/mimic_iv_cxr/silver/mimic_iv_cxr.db "
        f"--output_path dataset/mimic_iv_cxr/valid_data.json"
        f"--output_answer_path dataset/mimic_iv_cxr/valid_answer.json"
    )

    end_time = time.time()
    runtime = end_time - start_time
    print(f"Script runtime: {runtime:.2f} seconds")


if __name__ == "__main__":

    import argparse

    args = argparse.ArgumentParser()
    args.add_argument("--phase", type=str, default="dev", choices=["dev", "test"])
    args = args.parse_args()

    if args.phase == "dev":
        run_dev_phase()
    elif args.phase == "test":
        run_test_phase()
    else:
        raise ValueError("Invalid phase.")
