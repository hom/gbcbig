import json
from pathlib import Path

dirname = Path(__file__).parent
dist = Path.joinpath(dirname, "dist")
if not dist.exists():
    dist.mkdir()

error_path = dist / "gbcbig_parse_error.txt"
if error_path.exists():
    error_path.unlink()


def write_error(line, shape):
    with open(error_path, "a+", encoding="utf8") as f:
        f.write(line + shape + "\n\n")


characters = []
with open(dirname / "gbcbig.shp", "r", encoding="utf8") as f:
    lines = f.readlines()[4:]
    shape = ""
    gb2312 = ""
    unicode = ""
    length = ""
    character = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("\n"):
            print("empty line")
            i += 1
            continue
        if line.startswith("*"):
            j = 1
            shape = ""
            while not lines[i + j].startswith("\n"):
                shape += lines[i + j].replace("\n", "")
                j += 1
            # 添加形状
            chars = line[1:].replace(" ", "").replace("\n", "").split(",")
            gb2312 = chars[0]
            if gb2312 == "142" or gb2312 == "143":
                characters.append(
                    {
                        "shape": shape,
                        "gb2312": gb2312,
                        "unicode": "",
                        "length": chars[1],
                        "character": chars[2],
                    }
                )
                write_error(line, shape)
                i += j
                continue
            length = chars[1]
            try:
                character = bytes.fromhex(gb2312[1:]).decode("gb2312")
            except Exception as e:
                write_error(line, shape)
                i += j
                continue
            print(
                f"gb2312: {gb2312[1:]} unicode: {hex(ord(character))} length: {length} 汉字：{character}"
            )
            characters.append(
                {
                    "shape": shape,
                    "gb2312": gb2312[1:],
                    "unicode": hex(ord(character)),
                    "length": length,
                    "character": character,
                }
            )
            i += j

with open(dist / "gbcbig.json", "w", encoding="utf8") as f:
    json.dump(characters, f, ensure_ascii=False, indent=2)
