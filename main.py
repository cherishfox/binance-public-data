import os
from pathlib import Path
import hashlib
import zipfile
import pandas as pd


def list_files_and_dirs(path):
    """列出目录下的所有文件和文件夹"""
    return {d.name: [f.name for f in d.iterdir()] for d in Path(path).iterdir() if d.is_dir()}


def check_integrity(file_path, checksum_file_path):
    """校验文件完整性"""
    if not os.path.exists(checksum_file_path):
        return False
    with open(file_path, 'rb') as f:
        file_sha256 = hashlib.sha256(f.read()).hexdigest()
    with open(checksum_file_path, 'r') as f:
        expected_sha256 = f.read().strip().split(' ')[0]
    return file_sha256 == expected_sha256


def unzip_file(zip_path, extract_to):
    """解压zip文件"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def convert_csv_to_pickle(csv_path, pickle_path):
    """将CSV文件转换为pickle文件"""
    df = pd.read_csv(csv_path)
    df.to_pickle(pickle_path)


def process_directory(root_path, extract_to):
    """处理目录中的文件"""
    has_data_dict = list_files_and_dirs(root_path)
    for key, value in has_data_dict.items():
        if not value:
            continue
        file_name = value[0] if value[0].endswith('.zip') else value[1]
        file_path = root_path / key / file_name
        checksum_file_name = value[0] if value[0].endswith('.CHECKSUM') else value[1]
        checksum_file_path = root_path / key / checksum_file_name
        flag = check_integrity(file_path, checksum_file_path)
        if flag:
            unzip_file(file_path, extract_to)
            csv_files = [f for f in os.listdir(extract_to) if f.endswith('.csv')]
            for csv_file in csv_files:
                csv_path = os.path.join(extract_to, csv_file)
                pickle_path = os.path.join(extract_to, csv_file.replace('.csv', '.pickle'))
                convert_csv_to_pickle(csv_path, pickle_path)
                print(f"{csv_file} 已转换为 {pickle_path}")
        else:
            print(f"文件 {file_name} 校验失败")


def main(path):
    extract_to = 'extracted'
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    process_directory(Path(path), extract_to)


# 调用main函数将下载的zip文件解压后转换为.pickle文件进行存储
if __name__ == '__main__':
    main('binance-public-data/python/data/futures/um/daily/aggTrades')