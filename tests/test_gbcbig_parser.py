import json
from pathlib import Path

gbcbig = Path.joinpath(Path(__file__).parent, "gbcbig")
parse_error_file = Path(gbcbig, "gbcbig_parse_error.txt")
if parse_error_file.exists():
    parse_error_file.unlink()


def write_error(line, shape):
    with open(parse_error_file, "a+") as f:
        f.write(line + shape + "\n\n")


def test_parse_gbcbig():
    """Test parsing of shp file"""
    characters = []
    with open(gbcbig / "gbcbig.shp", "r") as f:
        lines = f.readlines()[7:]
        shape = ""
        gb2312 = ""
        unicode = ""  # noqa: F841
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
                except Exception as e:  # noqa: F841
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

    with open(gbcbig / "gbcbig.json", "w") as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)
