from farm_energy.wake_model_mean_new.area import *
from numpy import deg2rad, tan, sqrt, cos, sin

from turbine_description import rotor_radius
from memoize import Memoize
jensen_k = 0.04


def determine_if_in_wake(x_upstream, y_upstream, x_downstream, y_downstream, wind_direction, radius=rotor_radius, k=jensen_k):  # According to Jensen Model only
    # Eq. of centreline is Y = tan (d) (X - Xt) + Yt
    # Distance from point to line
    wind_direction = deg2rad(wind_direction + 180.0)
    distance_to_centre = abs(- tan(wind_direction) * x_downstream + y_downstream + tan(wind_direction) * x_upstream - y_upstream) / sqrt(1.0 + tan(wind_direction) ** 2.0)
    # print distance_to_centre
    # Coordinates of the intersection between closest path from turbine in wake to centreline.
    X_int = (x_downstream + tan(wind_direction) * y_downstream + tan(wind_direction) * (tan(wind_direction) * x_upstream - y_upstream)) / (tan(wind_direction) ** 2.0 + 1.0)
    Y_int = (- tan(wind_direction) * (- x_downstream - tan(wind_direction) * y_downstream) - tan(wind_direction) * x_upstream + y_upstream) / (tan(wind_direction) ** 2.0 + 1.0)
    # Distance from intersection point to turbine
    distance_to_turbine = sqrt((X_int - x_upstream) ** 2.0 + (Y_int - y_upstream) ** 2.0)
    # # Radius of wake at that distance
    radius = wake_radius(distance_to_turbine, radius, k)
    if (x_downstream - x_upstream) * cos(wind_direction) + (y_downstream - y_upstream) * sin(wind_direction) <= 0.0:
        if abs(radius) >= abs(distance_to_centre):
            if abs(radius) >= abs(distance_to_centre) + radius:
                fraction = 1.0
                return fraction, distance_to_turbine
            elif abs(radius) < abs(distance_to_centre) + radius:
                fraction = AreaReal(radius, radius, distance_to_centre).area()
                return fraction, distance_to_turbine
        elif abs(radius) < abs(distance_to_centre):
            if abs(radius) <= abs(distance_to_centre) - radius:
                fraction = 0.0
                return fraction, distance_to_turbine
            elif abs(radius) > abs(distance_to_centre) - radius:
                fraction = AreaReal(radius, radius, distance_to_centre).area()
                return fraction, distance_to_turbine
    else:
        return 0.0, distance_to_turbine


determine_if_in_wake = Memoize(determine_if_in_wake)


def wake_deficit(Ct, x, k=jensen_k, r0=rotor_radius):
    return (1.0 - sqrt(1.0 - Ct)) / (1.0 + (k * x) / r0) ** 2.0


wake_deficit = Memoize(wake_deficit)


def wake_radius(x, r0=rotor_radius, k=jensen_k):
    return r0 + k * x


wake_radius = Memoize(wake_radius)

if __name__ == '__main__':
    # wake_deficit(0.79, 320.0, 0.04, 40.0)
    # print determine_if_in_wake(0, 0, 500, 0, 150.0, 64.0)

    def speed(deficit):
        return 8.5 * (1.0 - deficit)

    def ct_v80(U0):
        if U0 < 4.0:
            return 0.1
        elif U0 <= 25.0:
            return 7.3139922126945e-7 * U0 ** 6.0 - 6.68905596915255e-5 * U0 ** 5.0 + 2.3937885e-3 * U0 ** 4.0 + - 0.0420283143 * U0 ** 3.0 + 0.3716111285 * U0 ** 2.0 - 1.5686969749 * U0 + 3.2991094727
        else:
            return 0.1
    a_def = wake_deficit(ct_v80(8.5), 560.0, 0.04, 40.0)
    a = speed(a_def)
    b1 = wake_deficit(ct_v80(a), 560.0, 0.04, 40.0)
    b2 = wake_deficit(ct_v80(8.5), 1120.0, 0.04, 40.0)
    b_def = sqrt(b1 ** 2.0 + b2 ** 2.0)
    b = speed(b_def)
    print 8.5, a, b
