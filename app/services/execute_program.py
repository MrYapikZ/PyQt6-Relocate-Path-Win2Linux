import subprocess
from string import Template
from typing import Optional, Any
from app.services.file_manager import FileManager
from app.raw.blender_script import blender_script


class ExecuteProgram:
    @staticmethod
    def blender_execute(blender_path: str, file_path: str, source_script: Any = blender_script):
        try:
            tpl = Template(source_script)
            script = tpl.substitute(FILEPATH=file_path)
            tmp_path = FileManager().convert_string2tempfile(script)
            subprocess.run([blender_path, "--background", "--python", tmp_path])
            return True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing Blender: {e}")
            return False
