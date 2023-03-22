datas: dict[str, list[str]]


def get_by_name(name: str) -> list[str]:
    global datas
    return datas[name]
