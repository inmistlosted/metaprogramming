import os

class FileGenerator(object):
    @staticmethod
    def get_python_class(className, attrs):
        attrs_args = ""
        attrs_inits = ""
        attrs_getsets = ""
        i = 0

        for attr in attrs:
            attr = attr.lower()
            koma = ", " if i > 0 else ""
            attrs_args += f"{koma}{attr}"

            attrs_inits += f"        self.__{attr} = {attr}\n"
            attrs_getsets += FileGenerator.create_getter(attr)
            attrs_getsets += FileGenerator.create_setter(attr)
            i += 1

        koma = ", " if len(attrs) > 0 else ""
        return f"""class {className}(object):
    def __init__(self{koma}{attrs_args}):
{attrs_inits}    
{attrs_getsets}"""

    @staticmethod
    def create_getter(attr):
        return f"""    @property
    def {attr}(self):
        return self.__{attr}\n\n"""

    @staticmethod
    def create_setter(attr):
        return f"""    @{attr}.setter
    def {attr}(self, {attr}):
        self.__{attr} = {attr}\n\n"""

    @staticmethod
    def create_class(class_name, content):
        if not os.path.exists(class_name):
            file_name = f"{class_name}.py"
            f = open(file_name, 'w')
            f.write(content)
            f.close()
            return True
        return False

    @staticmethod
    def import_module(file, module, class_name, created):
        if created:
            import_str = f"from {module} import {class_name}\n"

            with open(file, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(import_str + content)

    @staticmethod
    def import_package_module(file, package, class_name, created):
        if created:
            import_str = f"from {package}.{class_name.lower()} import {class_name}\n"

            with open(file, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(import_str + content)

    @staticmethod
    def create_package(package):
        if not os.path.exists(package):
            os.makedirs(package)
            init_path = os.path.join(package, '__init__.py')
            f = open(init_path, 'w')
            f.close()
            return True
        return False

    @staticmethod
    def create_package_module(package, module, content):
        if os.path.exists(package):
            file_name = os.path.join(package, f"{module}.py")

            if not os.path.exists(file_name):
                f = open(file_name, 'w')
                f.write(content)
                f.close()
                return True
        return False
