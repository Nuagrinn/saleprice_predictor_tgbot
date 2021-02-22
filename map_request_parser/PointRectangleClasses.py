import matplotlib.pyplot as plt


class Point:
    def __init__(self, start_lat, start_long):
        self.lat = start_lat
        self.long = start_long

    def __repr__(self):
        return f'{self.__lat, self.__long}'

    @property
    def lat(self):
        return self.__lat

    @lat.setter
    def lat(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Coordinates must be int or float')
        self.__lat = value

    @property
    def long(self):
        return self.__long

    @long.setter
    def long(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Coordinates must be int or float')
        self.__long = value


# steplength 0.009-lat 0.019-long for onestep squares
# 0.36, 0.57 for general_rectangle for all Moscow
#  Point(55.5550383110236, 37.32541797666712) for general_rectangle

class Rectangle:
    # Lists to save coords in
    lat_list = []
    long_list = []
    single_rectangle_list = []

    def __init__(self, lat_steplenght, long_steplenght, point):

        # Length of rectangle side
        self.lat_steplenght = lat_steplenght
        self.long_steplenght = long_steplenght

        # Start rectangle
        self.BottomLeft = point
        self.BottomRight = Point(point.lat, point.long + long_steplenght)
        self.TopRight = Point(self.BottomRight.lat + lat_steplenght, self.BottomRight.long)
        self.TopLeft = Point(point.lat + lat_steplenght, point.long)

        self.lat_list.extend((self.BottomLeft.lat, self.BottomRight.lat, self.TopRight.lat, self.TopLeft.lat))
        self.long_list.extend((self.BottomLeft.long, self.BottomRight.long, self.TopRight.long, self.TopLeft.long))
        self.single_rectangle_list.append([self.BottomLeft, self.BottomRight, self.TopRight, self.TopLeft])
        self.point = self.TopLeft

    def __repr__(self):
        return f'BottomLeft{self.BottomLeft} ' \
               f'BottomRight{self.BottomRight} ' \
               f'TopRight{self.TopRight} ' \
               f'TopLeft{self.TopLeft} '

    def make_a_step(self):
        # Create new coordinates from previous rectangle
        self.BottomLeft = self.BottomRight
        self.BottomRight = Point(self.BottomLeft.lat, self.BottomLeft.long + self.long_steplenght)
        self.TopRight = Point(self.BottomRight.lat + self.lat_steplenght, self.BottomRight.long)
        self.TopLeft = Point(self.BottomLeft.lat + self.lat_steplenght, self.BottomLeft.long)

        # Add new coords to lists
        self.lat_list.extend((self.BottomLeft.lat, self.BottomRight.lat, self.TopRight.lat, self.TopLeft.lat))
        self.long_list.extend((self.BottomLeft.long, self.BottomRight.long, self.TopRight.long, self.TopLeft.long))
        self.single_rectangle_list.append([self.BottomLeft, self.BottomRight, self.TopRight, self.TopLeft])

    def plot_grid(self):
        plt.scatter(self.long_list, self.lat_list)
        plt.show()

    def get_line_coords(self, general_rectangle):

        while self.BottomRight.long <= general_rectangle.BottomRight.long:
            self.make_a_step()

    def get_all_coords(self, general_rectangle):
        while self.TopLeft.lat <= general_rectangle.TopLeft.lat:
            self.get_line_coords(general_rectangle)
            self.__init__(self.lat_steplenght, self.long_steplenght, self.point)
        print('Done!')
        return self.single_rectangle_list
