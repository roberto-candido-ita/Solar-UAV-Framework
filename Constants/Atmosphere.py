atmosphere = [1.2250,
              1.2133,
              1.2071,
              1.1901,
              1.1787,
              1.1673,
              1.1560,
              1.1448,
              1.1337,
              1.1226,
              1.1117,
              1.1008,
              1.0900,
              1.0793,
              1.0687,
              1.0581,
              1.0476,
              1.0373,
              1.0269,
              1.0167,
              1.0066,
              0.99649,
              0.98649,
              0.97657,
              0.96673,
              0.95696,
              0.94727,
              0.93765,
              0.92811,
              0.91865,
              0.90926]


def get_air_density(altitude):
    if altitude > 3000:
        altitude = 3000

    if altitude == 0:
        return atmosphere[altitude]
    else:
        return atmosphere[altitude // 100]
