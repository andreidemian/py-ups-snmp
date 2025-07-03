def toFloat(strValue: str) -> float:
    if(strValue == '0'):
        return 0.0
    return float(f"{strValue[:-1]}.{strValue[-1]}")

def convert_centiseconds(cs : int) -> dict:
    seconds = (cs // 100) % 60
    minutes = (cs // (100 * 60)) % 60
    hours = (cs // (100 * 60 * 60)) % 24
    return { 'hours': hours, 'minutes': minutes, 'seconds': seconds, 'centiseconds': cs }
