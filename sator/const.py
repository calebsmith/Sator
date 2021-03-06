MAX_OCTAVE = 10
FORTE_NAMES = {
    0: "{}",
    1: "1-1",
    3: "2-1",
    5: "2-2",
    7: "3-1",
    9: "2-3",
    11: "3-2",
    15: "4-1",
    17: "2-4",
    19: "3-3",
    21: "3-6",
    23: "4-2",
    27: "4-3",
    31: "5-1",
    33: "2-5",
    35: "3-4",
    37: "3-7",
    39: "4-4",
    43: "4-11",
    45: "4-10",
    47: "5-2",
    51: "4-7",
    55: "5-3",
    63: "6-1",
    65: "2-6",
    67: "3-5",
    69: "3-8",
    71: "4-5",
    73: "3-10",
    75: "4-13",
    77: "4-12",
    79: "5-4",
    83: "4-Z15",
    85: "4-21",
    87: "5-9",
    91: "5-10",
    93: "5-8",
    95: "6-2",
    99: "4-8",
    103: "5-6",
    107: "5-Z12",
    111: "6-Z3",
    119: "6-Z4",
    127: "7-1",
    133: "3-9",
    135: "4-6",
    137: "3-11",
    139: "4-Z29",
    141: "4-14",
    143: "5-5",
    147: "4-18",
    149: "4-22",
    151: "5-Z36",
    153: "4-17",
    155: "5-16",
    157: "5-11",
    159: "6-Z36",
    163: "4-16",
    165: "4-23",
    167: "5-14",
    171: "5-24",
    173: "5-23",
    175: "6-9",
    179: "5-Z18",
    183: "6-Z11",
    187: "6-Z10",
    189: "6-8",
    191: "7-2",
    195: "4-9",
    199: "5-7",
    203: "5-19",
    207: "6-5",
    215: "6-Z12",
    219: "6-Z13",
    223: "7-4",
    231: "6-Z6",
    239: "7-5",
    255: "8-1",
    273: "3-12",
    275: "4-19",
    277: "4-24",
    279: "5-13",
    283: "5-Z17",
    287: "6-Z37",
    291: "4-20",
    293: "4-27",
    295: "5-Z38",
    297: "4-26",
    299: "5-27",
    301: "5-25",
    303: "6-Z40",
    307: "5-21",
    309: "5-26",
    311: "6-15",
    313: "5-Z37",
    315: "6-14",
    317: "6-Z39",
    319: "7-3",
    325: "4-25",
    327: "5-15",
    331: "5-29",
    333: "5-28",
    335: "6-Z41",
    339: "5-30",
    341: "5-33",
    343: "6-22",
    347: "6-Z24",
    349: "6-21",
    351: "7-9",
    355: "5-20",
    359: "6-Z43",
    363: "6-Z25",
    365: "6-Z23",
    367: "7-Z36",
    371: "6-16",
    375: "7-13",
    379: "7-11",
    381: "7-8",
    383: "8-2",
    399: "6-Z38",
    403: "5-22",
    407: "6-Z17",
    411: "6-Z19",
    415: "7-6",
    423: "6-18",
    427: "6-Z26",
    431: "7-14",
    439: "7-Z38",
    443: "7-Z37",
    447: "8-4",
    455: "6-7",
    463: "7-7",
    471: "7-15",
    479: "8-5",
    495: "8-6",
    511: "9-1",
    585: "4-28",
    587: "5-31",
    591: "6-Z42",
    595: "5-32",
    597: "5-34",
    599: "6-Z46",
    603: "6-27",
    605: "6-Z45",
    607: "7-10",
    615: "6-Z44",
    619: "6-Z28",
    623: "7-16",
    631: "7-Z17",
    639: "8-3",
    661: "5-35",
    663: "6-Z47",
    667: "6-Z49",
    671: "7-Z12",
    679: "6-Z48",
    683: "6-34",
    685: "6-33",
    687: "7-24",
    691: "6-31",
    693: "6-32",
    695: "7-27",
    699: "7-26",
    701: "7-23",
    703: "8-11",
    715: "6-30",
    717: "6-Z29",
    719: "7-19",
    723: "6-Z50",
    727: "7-29",
    731: "7-31",
    733: "7-25",
    735: "8-13",
    743: "7-20",
    747: "7-28",
    751: "8-Z29",
    755: "7-Z18",
    759: "8-14",
    763: "8-12",
    765: "8-10",
    767: "9-2",
    819: "6-20",
    823: "7-21",
    831: "8-7",
    855: "7-30",
    859: "7-32",
    863: "8-Z15",
    871: "7-22",
    879: "8-18",
    887: "8-19",
    891: "8-17",
    895: "9-3",
    927: "8-8",
    943: "8-16",
    951: "8-20",
    959: "9-4",
    975: "8-9",
    991: "9-5",
    1023: "10-1",
    1365: "6-35",
    1367: "7-33",
    1371: "7-34",
    1375: "8-21",
    1387: "7-35",
    1391: "8-22",
    1399: "8-24",
    1407: "9-6",
    1455: "8-23",
    1463: "8-27",
    1467: "8-26",
    1471: "9-7",
    1495: "8-25",
    1503: "9-8",
    1519: "9-9",
    1535: "10-2",
    1755: "8-28",
    1759: "9-10",
    1775: "9-11",
    1791: "10-3",
    1911: "9-12",
    1919: "10-4",
    1983: "10-5",
    2015: "10-6",
    2047: "11-1",
    4095: "12-1",
}

FORTE_INTS = {
    "{}": 0,
    "1-1": 1,
    "2-1": 3,
    "2-2": 5,
    "3-1": 7,
    "2-3": 9,
    "3-2": 11,
    "4-1": 15,
    "2-4": 17,
    "3-3": 19,
    "3-6": 21,
    "4-2": 23,
    "4-3": 27,
    "5-1": 31,
    "2-5": 33,
    "3-4": 35,
    "3-7": 37,
    "4-4": 39,
    "4-11": 43,
    "4-10": 45,
    "5-2": 47,
    "4-7": 51,
    "5-3": 55,
    "6-1": 63,
    "2-6": 65,
    "3-5": 67,
    "3-8": 69,
    "4-5": 71,
    "3-10": 73,
    "4-13": 75,
    "4-12": 77,
    "5-4": 79,
    "4-Z15": 83,
    "4-21": 85,
    "5-9": 87,
    "5-10": 91,
    "5-8": 93,
    "6-2": 95,
    "4-8": 99,
    "5-6": 103,
    "5-Z12": 107,
    "6-Z3": 111,
    "6-Z4": 119,
    "7-1": 127,
    "3-9": 133,
    "4-6": 135,
    "3-11": 137,
    "4-Z29": 139,
    "4-14": 141,
    "5-5": 143,
    "4-18": 147,
    "4-22": 149,
    "5-Z36": 151,
    "4-17": 153,
    "5-16": 155,
    "5-11": 157,
    "6-Z36": 159,
    "4-16": 163,
    "4-23": 165,
    "5-14": 167,
    "5-24": 171,
    "5-23": 173,
    "6-9": 175,
    "5-Z18": 179,
    "6-Z11": 183,
    "6-Z10": 187,
    "6-8": 189,
    "7-2": 191,
    "4-9": 195,
    "5-7": 199,
    "5-19": 203,
    "6-5": 207,
    "6-Z12": 215,
    "6-Z13": 219,
    "7-4": 223,
    "6-Z6": 231,
    "7-5": 239,
    "8-1": 255,
    "3-12": 273,
    "4-19": 275,
    "4-24": 277,
    "5-13": 279,
    "5-Z17": 283,
    "6-Z37": 287,
    "4-20": 291,
    "4-27": 293,
    "5-Z38": 295,
    "4-26": 297,
    "5-27": 299,
    "5-25": 301,
    "6-Z40": 303,
    "5-21": 307,
    "5-26": 309,
    "6-15": 311,
    "5-Z37": 313,
    "6-14": 315,
    "6-Z39": 317,
    "7-3": 319,
    "4-25": 325,
    "5-15": 327,
    "5-29": 331,
    "5-28": 333,
    "6-Z41": 335,
    "5-30": 339,
    "5-33": 341,
    "6-22": 343,
    "6-Z24": 347,
    "6-21": 349,
    "7-9": 351,
    "5-20": 355,
    "6-Z43": 359,
    "6-Z25": 363,
    "6-Z23": 365,
    "7-Z36": 367,
    "6-16": 371,
    "7-13": 375,
    "7-11": 379,
    "7-8": 381,
    "8-2": 383,
    "6-Z38": 399,
    "5-22": 403,
    "6-Z17": 407,
    "6-Z19": 411,
    "7-6": 415,
    "6-18": 423,
    "6-Z26": 427,
    "7-14": 431,
    "7-Z38": 439,
    "7-Z37": 443,
    "8-4": 447,
    "6-7": 455,
    "7-7": 463,
    "7-15": 471,
    "8-5": 479,
    "8-6": 495,
    "9-1": 511,
    "4-28": 585,
    "5-31": 587,
    "6-Z42": 591,
    "5-32": 595,
    "5-34": 597,
    "6-Z46": 599,
    "6-27": 603,
    "6-Z45": 605,
    "7-10": 607,
    "6-Z44": 615,
    "6-Z28": 619,
    "7-16": 623,
    "7-Z17": 631,
    "8-3": 639,
    "5-35": 661,
    "6-Z47": 663,
    "6-Z49": 667,
    "7-Z12": 671,
    "6-Z48": 679,
    "6-34": 683,
    "6-33": 685,
    "7-24": 687,
    "6-31": 691,
    "6-32": 693,
    "7-27": 695,
    "7-26": 699,
    "7-23": 701,
    "8-11": 703,
    "6-30": 715,
    "6-Z29": 717,
    "7-19": 719,
    "6-Z50": 723,
    "7-29": 727,
    "7-31": 731,
    "7-25": 733,
    "8-13": 735,
    "7-20": 743,
    "7-28": 747,
    "8-Z29": 751,
    "7-Z18": 755,
    "8-14": 759,
    "8-12": 763,
    "8-10": 765,
    "9-2": 767,
    "6-20": 819,
    "7-21": 823,
    "8-7": 831,
    "7-30": 855,
    "7-32": 859,
    "8-Z15": 863,
    "7-22": 871,
    "8-18": 879,
    "8-19": 887,
    "8-17": 891,
    "9-3": 895,
    "8-8": 927,
    "8-16": 943,
    "8-20": 951,
    "9-4": 959,
    "8-9": 975,
    "9-5": 991,
    "10-1": 1023,
    "6-35": 1365,
    "7-33": 1367,
    "7-34": 1371,
    "8-21": 1375,
    "7-35": 1387,
    "8-22": 1391,
    "8-24": 1399,
    "9-6": 1407,
    "8-23": 1455,
    "8-27": 1463,
    "8-26": 1467,
    "9-7": 1471,
    "8-25": 1495,
    "9-8": 1503,
    "9-9": 1519,
    "10-2": 1535,
    "8-28": 1755,
    "9-10": 1759,
    "9-11": 1775,
    "10-3": 1791,
    "9-12": 1911,
    "10-4": 1919,
    "10-5": 1983,
    "10-6": 2015,
    "11-1": 2047,
    "12-1": 4095,
}
Z_PARTNERS = {
    83: 139,
    107: 151,
    111: 159,
    119: 287,
    139: 83,
    151: 107,
    159: 111,
    179: 295,
    183: 303,
    187: 317,
    215: 335,
    219: 591,
    231: 399,
    283: 313,
    287: 119,
    295: 179,
    303: 183,
    313: 283,
    317: 187,
    335: 215,
    347: 599,
    359: 407,
    363: 663,
    365: 605,
    367: 671,
    399: 231,
    407: 359,
    411: 615,
    427: 679,
    439: 755,
    443: 631,
    591: 219,
    599: 347,
    605: 365,
    615: 411,
    619: 667,
    631: 443,
    663: 363,
    667: 619,
    671: 367,
    679: 427,
    717: 723,
    723: 717,
    751: 863,
    755: 439,
    863: 751,
}
