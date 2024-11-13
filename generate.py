import json
import os
import shutil
import subprocess
from typing import Optional
import zipfile

version: Optional[str] = None

def create_resource_pack(version):
    file_list = [
        'itemscroller.json',
        'litematica.json',
        'malilib.json',
        'minihud.json',
        'tweakeroo.json',
    ]
    def write_file(language, version):
        in_file = os.path.join('Masa-Family-Bucket-Translation-Pack', language, file)
        out_file = os.path.join('assets', file.split('.')[0], 'lang', language + '.json')

        with open(in_file, 'r', encoding='utf-8') as f:
            in_file = json.load(f)
            if version == 'neo':
                for key in in_file:
                    if " | " in in_file[key]:
                        in_file[key] = in_file[key].split(" | ")[1]
        output_dir = os.path.dirname(out_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = open(out_file, 'w', encoding='utf-8')
        output_file.write(json.dumps(in_file, ensure_ascii=False, indent=4))
        output_file.close()

    for file in file_list:
        write_file('zh_cn', version)
        write_file('zh_tw', version)
        
        

def rename_mcmeta():
    with open('pack.mcmeta', 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    data['pack']['pack_format'] = 32
    data['pack']['supported_formats'] = [ 9, 32 ]
    data['pack']['description'] = '§e[1.20.4]MASA全家桶汉化包'

    with open('pack.mcmeta', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def zip_files(version: str):
    def zip_files_and_folders(zip_filename, items_to_zip):
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in items_to_zip:
                if os.path.isdir(item):
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(item))
                            zipf.write(file_path, arcname)
                else:
                    zipf.write(item, os.path.basename(item))
    items_to_zip = [
        'assets',
        'pack.mcmeta',
        'pack.png',
    ]
    if version == 'neo':
        zip_filename = './masa-mods-chinese-neo.zip'
    else:
        zip_filename = './masa-mods-chinese.zip'
    zip_files_and_folders(zip_filename, items_to_zip)

def delete_files():
    shutil.rmtree('./assets')

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Generate the MASA mods Chinese translation pack.')
    parser.add_argument('-v', '--version',
                        choices=['classic', 'neo'],
                        type=str,
                        required=False,
                        default='classic',
                        help='The version of the translation pack.')
    return parser.parse_args()

version = parse_args().version
create_resource_pack(version)
rename_mcmeta()
zip_files(version)
delete_files()
print('Done!')


