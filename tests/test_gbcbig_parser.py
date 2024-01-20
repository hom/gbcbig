import json
from pathlib import Path

dirname = Path.joinpath(Path(__file__).parent, "gbcbig")
print(dirname)

shp_path = Path("shps")

error_path = shp_path / "gbcbig_parse_error.txt"
if error_path.exists():
    error_path.unlink()


def write_error(line, shape):
    with open(error_path, "a+") as f:
        f.write(line + shape + "\n\n")


def test_parse_gbcbig():
    """Test parsing of shp file"""
    characters = []
    with open(shp_path / "gbcbig.shp", "r") as f:
        lines = f.readlines()[7:]
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

    with open(shp_path / "gbcbig.json", "w") as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)
