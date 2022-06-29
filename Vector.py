from __future__ import annotations

from math import sqrt, acos, pi

CANNOT_NORMALIZE_ZERO_VECTOR = 'Cannot normalize the zero vector'
CANNOT_COMPUTE_ANGLE_WITH_ZERO_VEC = 'Cannot compute angle with the zero vector'
NO_UNIQUE_PARALLEL_COMPONENT_MSG = "There is not unique parallel component"
NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "There is not unique orthogonal component"

class Vector(object):

    def __init__(self, coordinates: list):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __add__(self, other: 'Vector') -> 'Vector':
        try:
            if not len(self) == len(other):
                raise ValueError

            new_coor = [x + y for x, y in zip(self.coordinates, other.coordinates)]
            return Vector(new_coor)

        except ValueError:
            raise ValueError('The vectors are with different lengths')

    def __sub__(self, other):
        try:
            if not len(self) == len(other):
                raise ValueError

            new_coor = [x - y for x, y in zip(self.coordinates, other.coordinates)]
            return Vector(new_coor)

        except ValueError:
            raise ValueError('The vectors are with different lengths')

    def __rmul__(self, scalar: float) -> 'Vector':
        new_coor = [scalar * coor for coor in self.coordinates]
        return Vector(new_coor)

    def is_orthogonal(self, other: 'Vector', tolerance=1e-10) -> bool:
        return abs(self.dot(other)) < tolerance

    def is_parallel(self, other: 'Vector') -> bool:
        return self.is_zero() or other.is_zero() or self.angle_with(other) % pi == 0

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def magnitude(self) -> float:
        return sqrt(sum([coor **2 for  coor in self.coordinates]))

    def normalize(self) -> 'Vector':
        try:
            magnitude = self.magnitude()
            return 1. / magnitude * self

        except ZeroDivisionError:
            raise Exception(CANNOT_NORMALIZE_ZERO_VECTOR)

    def dot(self, other: 'Vector') -> float:
        try:
            if len(self) != len(other):
                raise ValueError
            return sum([x * y for x, y in zip(self.coordinates, other.coordinates)])

        except ValueError:
            raise ValueError('The vectors are with different lengths')

    def angle_with(self, other: 'Vector', in_degrees=False) -> float:
        try:

            cos_theta = self.dot(other) / (self.magnitude() * other.magnitude())
            theta_rad = acos(cos_theta)

            if in_degrees:
                return theta_rad * 180. / pi

            return theta_rad

        except Exception as e:
            if str(e) == CANNOT_NORMALIZE_ZERO_VECTOR:
                raise Exception(CANNOT_COMPUTE_ANGLE_WITH_ZERO_VEC)

    def component_orthogonal_to(self, other: 'Vector') -> 'Vector':
        try:
            projection = self.component_parallel_to(other)
            return self - projection

        except Exception as e:
            if str(e) == NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, other: 'Vector') -> 'Vector':
        try:
            other_unit_vec = other.normalize()
            weight = self.dot(other_unit_vec)
            return weight * other_unit_vec

        except Exception as e:
            if str(e) == CANNOT_NORMALIZE_ZERO_VECTOR:
                raise Exception(NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e





    def __len__(self) -> int:
        return len(self.coordinates)

    def __str__(self) -> str:
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, other: 'Vector') -> bool:
        return self.coordinates == other.coordinates
