import base64
import json
import zlib


def bp_string_to_json(bps: str) -> dict:
    json_bytes = zlib.decompress(base64.b64decode(bps[1:]))
    return json.loads(json_bytes)


if __name__ == '__main__':
    s = '0eNrdWN9v2jAQ/lciv' \
        '+wlIBwSAtE0aeoep01qH7cJmcQUa44dOXYZQvnfd04KZElok9J1Gg/88MV3vu+7O9' \
        '/BHq24oZliQqNojxKax4plmkmBIvRVOEQkjlyvnViKhFlx7nAmftLE0dIhTkpTqXZO' \
        'TDkffxdfpGYxdfTGvphKQCtdMUG0VO9yh4nMaIfVDTANcrkVjjQaHo6RixiclKPo2x' \
        '7l7F4Qbr3Su4yCOw9MaQMSFwmSWkG1Y3SLCtATCf2FIly4AzTvappepybTND2pJTRm' \
        'CVWjE66agWkPAySOTWp4Q9MvfriICg0E0wp7udgthUlXVAGqk+NmlWtSxsdFmcxZFa' \
        'o9AjMjz0U7+AAOELAoaFwGzD7F9u1eUSrq5lmCohD2MhUbpsslLn4UhQXS8MA7eZAS' \
        'zkecpFmHB+E4qHyYjIPKC60kX67ohjwwwAzbDqcdM8oK10zletk7bh9RZRyosHnr+X' \
        'aVZkSVxEboAyqGcOCfAT3tB3r+CPoqMPududoR6RIyPgO4qudB4IY479Uct+tpYx00' \
        '1rPGGuOmoGkRN01ivykI+lVO0C+JZldVObN+oINrqpzwqTZx7rKukCdMVUeXF20XD4' \
        '8mTzzkr0BE0CDiPWgMrdyKotJutgP3jNDLtZLpsmz3KFoTntNB/OIeheYiz+ormrS0' \
        'eza0+RFIJrcQq3zLdLxpx8l/8p57jfSsMXiIzOSyDG1y0Lrc5iWFN2bS0nTRFnKx/D' \
        '6xU8mNwa09kz83gaWKvKWdTOgh5G3KFyfkkhM1yoigvM34oZ1iKI0OK/b4RzMpTZhJ' \
        'R5QDK4rFo0xy2ra3qN+sXQbxsDaPr+GywgMHOu8qQE+H9eLrAO0P68XXkd7BS5qx9y' \
        '+b8azFxPBmbPvha7bi5swb/o1OjHsOi5M3SVAidnrDxP2zDdlFJqdwFJcKWNTK0DPM' \
        'XkLNsJkS1/h5oyw+Di85tXZekKoXpvxF82dHaJ4bnYJnns/s1NRzKjtWT6/9zbl4fi' \
        '5p5r3qyftPy6mTq4oLYL78uy2q/anpIk5WMGZG6PbO+UxgTHU+0VSC/IGqvKqPOfbD' \
        'hRdOFyEO4Yd/8RvoUjYa'
    j = bp_string_to_json(s)
    print(j['blueprint'])
