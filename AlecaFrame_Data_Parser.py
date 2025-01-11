from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from os import mkdir, path, getcwd, getenv
import json
from requests import get

scriptdir = getcwd()
data_out_dir = path.join(scriptdir, "data")
data_file_name = "lastData.dat"
alecaframe_data_wd_path = path.join(scriptdir, data_file_name)
alecaframe_data_appdata_path = path.join(getenv("LOCALAPPDATA"), "AlecaFrame", data_file_name)
data_output_unmodified_path = path.join(data_out_dir, "lastData.json")
data_output_modified_path = path.join(data_out_dir, "lastData.out.json")
data_output_loadouts_path = path.join(data_out_dir, "lastData.ldts.json")

def main():
    print(">>> Script Initialized <<<")

    if not path.exists(alecaframe_data_wd_path):
        print(f"\"{alecaframe_data_wd_path}\" could not be found.")

        answer = input(f"Do you want to check in AlecaFrame's app directory? (Y/N): ").lower()
        if answer == "y":
            if not path.exists(path.join(alecaframe_data_appdata_path)):
                print(f"\"{data_file_name}\" found. Quitting")
                quit(2)
            else:
                decrypt_data(alecaframe_data_appdata_path)
        else:
            quit(1)
    else:
        decrypt_data(alecaframe_data_wd_path)

def decrypt_data(data_file: str = ""):
    print(f"Starting Decryption. File path is \"{data_file}\"")

    encryption_key = bytes(map(int, get("https://gist.githubusercontent.com/nrbdev/cd73cc5c02ee5e23aca3251423aa85b0/raw/").text.strip()[1:-1].split(',')))
    encryption_iv = bytes(map(int, get("https://gist.githubusercontent.com/nrbdev/8ebb6a1849ebbf80724b26faf30451a1/raw/").text.strip()[1:-1].split(',')))

    try:
        with open(data_file, "rb") as af_data_encrypted:
            encrypted_data = af_data_encrypted.read()
            af_data_encrypted.close()
    except Exception as e:
        print(f"Error reading {data_file}:", e)
        quit(3)

    cipher = Cipher(
        algorithms.AES(encryption_key),
        modes.CBC(encryption_iv)
    )
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return build_data(decrypted_data.decode("utf-8"))

def build_data(decrypted_data: str):

    if decrypted_data is None:
        print("No data. Quitting")
        quit(99)

    decrypted_data_json : dict[str] = json.loads(decrypted_data)

    if "InventoryJson" in decrypted_data_json:
        decrypted_data_json = json.loads(decrypted_data_json["InventoryJson"])

    decrypted_data_json_working_copy = decrypted_data_json.copy()

    excluded_keys = ["CrewShip"]

    final_data_unmodified = json.dumps(decrypted_data_json, indent=2)
    final_data_modified = {}
    final_data_loadouts = {}

    for key in decrypted_data_json_working_copy.keys():
        if any(excluded_key in key for excluded_key in excluded_keys):
            del decrypted_data_json[key]
            continue

        modified_items = []
        modified_loadouts = []
        if key == "LoadOutPresets":
            loadouts = decrypted_data_json[key]
            del decrypted_data_json[key]

            modified_loadouts = {}

            for loadout_type, loadout_data in loadouts.items():
                modified_loadouts_type = []
                for loadout in loadout_data:
                    if "ItemId" in loadout:
                        loadout["_id"] = loadout.pop("ItemId")
                    modified_loadouts_type.append(loadout)
                modified_loadouts[loadout_type] = modified_loadouts_type
            final_data_loadouts = modified_loadouts
        else:
            if isinstance(decrypted_data_json[key], (list, dict)):
                for item in decrypted_data_json[key]:
                    if isinstance(item, (dict)):
                        if "ItemId" in item:
                            item["_id"] = item.pop("ItemId", None)
                            modified_items.append(item)
                            final_data_modified[key] = modified_items
                        else:
                            final_data_modified[key] = decrypted_data_json[key]
                    else:
                        final_data_modified[key] = decrypted_data_json[key]
            else:
                final_data_modified[key] = decrypted_data_json[key]

    final_data_modified_json = json.dumps(final_data_modified, indent=2)
    final_data_loadouts_json = json.dumps(final_data_loadouts, indent=2)

    if not path.exists(data_out_dir):
        try:
            mkdir(data_out_dir)
        except Exception as e:
            print(f"Error. Failed to make \"{data_out_dir}\" folder", e)

    try:
        with open(data_output_unmodified_path, "w") as file:
            file.write(final_data_unmodified)
    except Exception as e:
        print(f"Failed to write to \"{data_output_unmodified_path}\"", e)
    finally:
        file.close()

    try:
        with open(data_output_modified_path, "w") as file:
            file.write(final_data_modified_json)
    except Exception as e:
        print(f"Failed to write to \"{data_output_modified_path}\"", e)
    finally:
        file.close()

    try:
        with open(data_output_loadouts_path, "w") as file:
            file.write(final_data_loadouts_json)
    except Exception as e:
        print(f"Failed to write to \"{data_output_loadouts_path}\"",e)
    finally:
        file.close()


if __name__ == "__main__":
    main()