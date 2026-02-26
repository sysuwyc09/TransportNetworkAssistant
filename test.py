import pkg_resources
import numpy as np

# 检查已安装模块的NumPy依赖
for pkg in pkg_resources.working_set:
    try:
        reqs = [str(req) for req in pkg.requires() if "numpy" in str(req).lower()]
        if reqs:
            print(f"模块 {pkg.key} 依赖NumPy：{reqs}")
    except:
        pass