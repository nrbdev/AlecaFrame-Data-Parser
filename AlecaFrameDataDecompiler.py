from genericpath import exists
import json
import argparse
from textwrap import indent
from matplotlib.font_manager import json_dump
from requests import get
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from os import mkdir, path, getcwd, getenv

debug = False

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, help='(optional) Custom path for lastData.dat')
args = parser.parse_args()

scriptdir = getcwd()
data_out_dir = path.join(scriptdir, "output")
default_data_file_name = "lastData.dat"
alecaframe_data_local_path = path.join(scriptdir, default_data_file_name)
alecaframe_data_appdata_path = path.join(getenv("LOCALAPPDATA"), "AlecaFrame", default_data_file_name)


def main():
    args = parser.parse_args()

    if args.path:
        if path.exists(args.path):
            print(f"Using command-line path: {args.path}")
            return decrypt_data(args.path)
        else:
            print("Path from command-line doesnt exist.")
            quit(1)

    if not exists(alecaframe_data_local_path):
        answer = input(f"{default_data_file_name} not found. Search in AlecaFrame's app directory? (Y/N): ").lower()
        if (answer == "y"):
            if not path.exists(path.join(alecaframe_data_appdata_path)):
                print(f"{alecaframe_data_appdata_path} not found. Quitting.")
                quit(1)
            else:
                decrypt_data(alecaframe_data_appdata_path)
        else:
            quit(2)
    else:
        decrypt_data(alecaframe_data_local_path)

    print("Completed successfully.")


def decrypt_data(data_file_path: str):
    encryption_key = bytes(map(int, get("https://gist.githubusercontent.com/nrbdev/cd73cc5c02ee5e23aca3251423aa85b0/raw/").text.strip()[1:-1].split(',')))
    encryption_iv = bytes(map(int, get("https://gist.githubusercontent.com/nrbdev/8ebb6a1849ebbf80724b26faf30451a1/raw/").text.strip()[1:-1].split(',')))

    try:
        with open(data_file_path, "rb") as f:
            encrypted_data = f.read()
    except Exception as e:
        print(f"Error reading {data_file_path}:", e)
        quit(3)

    cipher = Cipher(
        algorithms.AES(encryption_key),
        modes.CBC(encryption_iv)
    )
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return save_data(decrypted_data)


def save_data(decrypted_data: str):
    raw_data_output_path = path.join(data_out_dir, "lastData.json")
    itemid_fixed_data_output_path = path.join(data_out_dir, "lastData_patched.json")

    if decrypted_data is None:
        print("Received no data. Quitting.")
        quit(5)

    decrypted_data_json : dict[str] = json.loads(decrypted_data)

    # Old inventories sometimes have this
    if "InventoryJson" in decrypted_data_json:
        decrypted_data_json = json.loads(decrypted_data_json["InventoryJson"])

    if not path.exists(data_out_dir):
        try:
            mkdir(data_out_dir)
        except Exception as e:
            print(f"Error creating {data_out_dir} folder:", e)
            quit(6)

    with open(raw_data_output_path, "w") as f:
        f.write(json.dumps(decrypted_data_json, indent=2))
        print(f"Data saved to {raw_data_output_path}")

    with open(itemid_fixed_data_output_path, "w") as f:
        f.write(json.dumps(fix_data(decrypted_data_json), indent=2))
        print(f"Data saved to {itemid_fixed_data_output_path}")


def fix_data(decrypted_data_json: dict[str]):
    # Convert to $oid for MongoDB

    patched_data_json = {}

    for key in decrypted_data_json:
        if isinstance(decrypted_data_json[key], (list, dict)):
            patched_data_json[key] = []
            for item in decrypted_data_json[key]:
                if isinstance(item, dict):
                    if "ItemId" in item:
                        item["_id"] = item.pop("ItemId", None)
                        patched_data_json[key].append(item)
                    else:
                        patched_data_json[key].append(item)
                else:
                    patched_data_json[key].append(item)
        else:
            patched_data_json[key] = decrypted_data_json[key]

        if (debug):
            print(f"[debug] (fix_data) Processed key: {key}")

    return patched_data_json


if __name__ == "__main__":
    main()