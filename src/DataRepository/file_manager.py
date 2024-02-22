import os

class FileManager:

    @staticmethod
    def is_file_exist(filename):
        return os.path.exists(filename)

    @staticmethod
    def filename(ts_code, period_type):
        __data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

        # 确保data子目录存在
        if not os.path.exists(__data_dir):
            os.makedirs(__data_dir)

        filename = os.path.join(__data_dir, f"{ts_code}_{period_type}.csv")
        return filename