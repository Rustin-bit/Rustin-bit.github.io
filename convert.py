import os
import json
from opencc import OpenCC

print("当前目录文件：", os.listdir())

cc = OpenCC('t2s')

for file in os.listdir():
    if file.endswith(".json"):

        print(f"正在转换: {file}")

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = json.dumps(data, ensure_ascii=False)
        simplified_text = cc.convert(text)
        new_data = json.loads(simplified_text)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

print("全部转换完成！")