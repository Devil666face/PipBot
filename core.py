import shutil
import os
from pathlib import Path

class PipLoader:
    def __init__(self, pip_name:str):
        self.pack_name = pip_name.replace(' ','_')
        self.pack_name_list = pip_name.split()
        self.pack_name_orig = pip_name
        self.pack_name_list.append('wheel')
        # self.pack_name_list.append('pip')
        self.create_folder_for_pack()
        self.download()
    
    def get_files(self):
        shutil.make_archive(self.pack_dir,'zip',self.pack_dir)
        return os.listdir(self.pack_dir), f'{self.pack_dir}.zip'

    def create_folder_for_pack(self):
        if (os.path.exists(self.pack_name)):
            shutil.rmtree(Path(os.getcwd(),self.pack_name))
        self.pack_dir = Path(os.getcwd(),self.pack_name)
        os.mkdir(self.pack_dir)
        print(f'Make directory for {self.pack_name}')

    def download(self):
        self.make_req_file()
        os.system(f'pip download -d {self.pack_dir} --isolated {self.pack_name_orig} wheel pip setuptools')  

    def make_req_file(self):
        for index, pack in enumerate(self.pack_name_list):
            self.req_path = Path(self.pack_name,f'requiremets_{self.pack_name}_{index}.txt')
            os.system(f'johnnydep {pack} --output-format pinned > {self.req_path}')

        self.unite_req_files()

    def unite_req_files(self):
        self.req_text = []
        for file in os.listdir(self.pack_dir):
            if file.endswith('.txt'):
                with (open(Path(self.pack_dir,file) ,'r', encoding='utf-8')) as txt_file:
                    for line in txt_file:
                        self.req_text.append(line)
                os.remove(Path(self.pack_dir,file))

        with (open(Path(self.pack_dir,'requirements.txt') ,'w', encoding='utf-8')) as req_file:
            for line in self.req_text:
                req_file.write(str(line))

    def __del__(self):
        shutil.rmtree(self.pack_dir)
        os.remove(f'{self.pack_name}.zip')
        del self

    def get_command(self):
        return f'pip install --no-index --find-links {self.pack_name} -r .\{self.pack_name}\\requirements.txt'