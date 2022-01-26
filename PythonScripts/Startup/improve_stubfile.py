from pathlib import Path
from typing import List

import unreal

DEBUG = False


def improve_stubfile() -> None:
    """create an improved unreal module stubfile for better type annotation and autocompletion"""

    project_dir = Path(unreal.SystemLibrary.get_project_directory())
    original_stub = project_dir / 'Intermediate/PythonStub/unreal.py'

    if not original_stub.exists():
        return

    print('Creating python stubfile...')

    with original_stub.open(mode='r') as f:
        lines = f.readlines()

    lines.insert(2, 'from typing import List, Dict\n')
    unreal_classes = [line.split(' ')[1].split('(')[0]
                      for line in lines if line.startswith('class ')]

    unknown_classes: List[str] = []

    for index, line in enumerate(lines):
        if line.strip() == 'return None':
            if lines[index-3].strip() == 'Returns:':
                class_name = lines[index-2].strip().split(':')[0]
                if class_name in unreal_classes:
                    lines[index] = ('# --' + line[4:] if DEBUG else '') + \
                        line.replace('None', f'{class_name}()')
                elif class_name == 'type(Class)':
                    lines[index] = ('# --' + line[4:] if DEBUG else '') + \
                        line.replace('None', f'type(Class)')
                else:
                    unknown_classes.append(class_name)
        else:
            backup_line = line
            update_line = False

            while 'Array.cast(' in line:
                split_1 = line.split('Array.cast(', maxsplit=1)
                split_2 = split_1[1].split(', [])', maxsplit=1)
                line = f'{split_1[0]}List[{split_2[0]}](){split_2[1]}'
                update_line = True

            while 'Set.cast(' in line:
                split_1 = line.split('Set.cast(', maxsplit=1)
                split_2 = split_1[1].split(', [])', maxsplit=1)
                line = f'{split_1[0]}{{{split_2[0]}()}}{split_2[1]}'
                update_line = True

            while 'Map.cast(' in line:
                split_1 = line.split('Map.cast(', maxsplit=1)
                split_2 = split_1[1].split(', {})', maxsplit=1)
                line = f'{split_1[0]}Dict[{split_2[0]}](){split_2[1]}'
                update_line = True

            if update_line:
                lines[index] = f'# --{backup_line[4:]}' + \
                    line if DEBUG else line

    for class_name in unknown_classes:
        unreal.log_warning(f'unknown class found in stubfile: {class_name}')

    destination_stub = project_dir / 'Intermediate/PythonStubImproved/unreal.py'
    destination_stub.parent.mkdir(exist_ok=True, parents=True)
    with destination_stub.open(mode='w') as f:
        f.writelines(lines)

    print(f'Improved stubfile created: {destination_stub}')


def create_extended_unreal_module():
    project_dir = Path(unreal.SystemLibrary.get_project_directory())
    original_stub = project_dir / 'Intermediate/PythonStub/unreal.py'
    if not original_stub.exists():
        return
    with original_stub.open(mode='r') as f:
        stubfile_lines = f.readlines()
   
    
    out_lines: List[str] = ['import unreal\n\n\n']
    for index, line in enumerate(stubfile_lines):
        if line.startswith('class'):
            class_name = line.split(' ')[1].split('(')[0]
            out_lines.append(f'class {class_name}(unreal.{class_name}):\n')
            has_editor_properties = False
            sub_index = index
            while sub_index != -1:
                sub_index += 1
                if sub_index >= len(stubfile_lines):
                    sub_index = -1
                    break
                sub_line = stubfile_lines[sub_index]
                if sub_line.startswith('class'):
                    sub_index = -1
                elif sub_line.strip().startswith('**Editor Properties:**'):
                    has_editor_properties = True
                    subsub_index = sub_index + 1
                    while subsub_index != -1:
                        subsub_index += 1
                        subsub_line = stubfile_lines[subsub_index]
                        if subsub_line.strip().startswith('- ``'):
                            property_name = subsub_line.split('``')[1]
                            property_type = subsub_line.split('`` (', maxsplit=1)[1].split('): ', maxsplit=1)[0]
                            property_doc = '        r"""\n        {subsub_line}\n        """\n'
                            property_readonly = '[Read-Write]' not in subsub_line
                            out_lines.append(
                                f'    @property\n'
                                f'    def e_{property_name}(self) -> unreal.{property_type}:\n'
                                f'        return self.get_editor_property("{property_name}")\n'
                            )
                            if not property_readonly:
                                out_lines.append(
                                    f'    @e_{property_name}.setter\n'
                                    f'    def e_{property_name}(self, value):\n'
                                    f'        self.set_editor_property("{property_name}, value")\n'
                                )
                        elif subsub_line.endswith('"""\n'):
                            subsub_index = -1
                        
                            

            if not has_editor_properties:
                out_lines.append('    pass\n\n')
        
    path = project_dir / 'Intermediate/PythonStubImproved/unreal_extended.py'
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open(mode='w') as f:
        f.writelines(out_lines)


if __name__ == '__main__':
    # improve_stubfile()
    create_extended_unreal_module()
