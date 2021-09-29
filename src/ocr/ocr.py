import pytesseract
import cv2
from src.ocr.placements import PLACEMENTS as placements
from src.vars.vars import Env

pytesseract.pytesseract.tesseract_cmd = Env.OCR_ENGINE_PATH

def ocr(
    path: str
) -> dict:
    """Reads image of the incoming author"""
    image = cv2.imread(
        path, 
        Env.IMREAD_FLAG
    )

    threshold = cv2.threshold(
        image, 
        Env.THRESHOLD_VALUE, 
        Env.MAX_VALUE, 
        cv2.THRESH_BINARY_INV
    )[1]

    stats = stat_parser(
        pytesseract.image_to_string(
            threshold, 
            lang=Env.OCR_LANGUAGE, 
            config=Env.OCR_CONFIG, 
            nice=Env.OCR_PROC_PRIORITY
        ).split()
    )
    return stats

def stat_parser(ocr_data: list) -> list:
    """Returns screenshot stats"""
    for index, data in enumerate(ocr_data):
        if placement := placements.get(data):
            return [placement, *ocr_data[index + 1:index + 4]]

'''
['FIRST','1', '2', 3]
'''

# Old method

# def finding_stats(num):
#     """Find the players placement"""
#     numbers = 'First,Second,Third,Fourth,Fifth,Sixth,Seventh,Eighth,Ninth,Tenth,' \
#                  'Eleventh,Twelfth,Thirteenth,Fourteenth,Fifteenth,Sixteenth,Seventeenth,' \
#                  'Eighteenth,Nineteenth,Twentieth,Twenty-first,Twenty-second,Twenty-third,Twenty-fourth,' \
#                  'Twenty-fifth,Twenty-sixth,Twenty-seventh,Twenty-eighth,Twenty-ninth,Thirtieth,Thirty-first,' \
#                  'Thirty-second,Thirty-third,Thirty-fourth,Thirty-fifth,Thirty-sixth,Thirty-seventh,Thirty-eighth,' \
#                  'Thirty-ninth,Fortieth,Forty-first,Forty-second,Forty-third,Forty-fourth,Forty-fifth,Forty-sixth,' \
#                  'Forty-seventh,Forty-eighth,Forty-ninth,Fiftieth'
#     splitnums = numbers.strip().upper().split(',')
#     counting = 0
#     for n in num:
#         for s in splitnums:
#             if n == s:
#                 return num[counting:counting + 4]
#         counting += 1
#     return 0

