import cv2
import numpy as np
from tkinter import filedialog
from tkinter import Tk, Label
import time

DEFAULT_COLOR: np.ndarray = np.array((0.5,0.5,0.5),dtype = np.float)

class ImageTransformer:

    def __init__(self):
        # Make an "open file" dialog, to ask for a filename.
        root = Tk()
        Label(root,text="Showing file dialog").pack();
        root.update()
        filename: str = filedialog.askopenfilename(message="Find the source image.")
        root.withdraw()

        self.source_image: np.ndarray = cv2.imread(filename)/256.0

        cv2.waitKey(10)
        cv2.imshow("source",self.source_image)

        self.result_image: np.ndarray = np.ones((2*self.source_image.shape[0], 2*self.source_image.shape[1], 3), dtype=np.float)

        for i in range(0, 3):
            self.result_image[:, :, i] = DEFAULT_COLOR[i]

        self.row_offset: int = self.source_image.shape[0]  # these will determine where (0,0) goes in the image.
        self.col_offset: int = self.source_image.shape[1]

        self.transform: np.ndarray = np.array([[1, 0, 0],
                                   [0, 1, 0],
                                   [0, 0, 1]], dtype = np.float)
        self.inverse_transform: np.ndarray = np.linalg.inv(self.transform)

    def get_source_color_at(self,r: float, c:float) -> np.ndarray:
        """
        Gets the color in the source image corresponding to the given point... which need not be an integer. If these
        (r,c) coordinates are out of bounds, return DEFAULT_COLOR.
        See "Interpolation" section of the Transforms video for the "H" algorithm....
        :param r:
        :param c:
        :return: an ndarray with 3 numbers 0-1.
        """
        num_rows,num_cols,depth = self.source_image.shape
        result_color: np.ndarray = DEFAULT_COLOR
        if r>=0 and r<num_rows and c>=0 and c< num_cols:

            # ---------------------------------------------------
            # TODO: You write this! Find what result_color should be.
            # note that if you are looking for the color at row 3, column 5, you can say "self.source_image[3,5]" and
            #   this will be a 3-element (b,g,r) list.

            pass # replace this line.

            # ---------------------------------------------------
        return result_color

    def display_result(self) -> None:
        """
        Applies the self.transform transformation to the self.source_image to build the self.result_image; displays both
        images.
        :return: None
        """
        result_rows,result_cols, depth = self.result_image.shape

        for y in range(0,result_rows):
            for x in range(0,result_cols):
                source_point: np.ndarray = np.array([x-self.col_offset,\
                                         y-self.row_offset,\
                                         1])
                # ---------------------------------------------------
                # TODO: You write this! Calculate the (double,double) location of the point in the original graphic that
                #       would transform to (x,y) in this graphic. Set the variables x_prime and y_prime to this location.
                #       Hint: Make use of the stuff on lines 32-35....
                #       Note: You are not doing any drawing, just calculating the location on the source image that will
                #             correspond to this location.


                (x_prime,y_prime) = (0,0) # replace this line.


                # ----------------------------------------------------
                # The code below this line copies the color from the location you just calculated and sets it at the
                #   given (x,y).

                color = self.get_source_color_at(y_prime,x_prime) #note: reversed because we need (r,c) not (x,y)

                if np.array_equal(color,DEFAULT_COLOR) and (x == self.col_offset or y == self.row_offset):
                    color = (255,255,255)  #draws the axes, if the graphic isn't covering them

                self.result_image[y,x] = color

        cv2.imshow("source",self.source_image)
        cv2.imshow("result",self.result_image)
        cv2.moveWindow("result",300,0)

        cv2.waitKey(0) # wait for the user to press any key, then...
        cv2.destroyAllWindows() #... close all the windows.

    def print_transform(self) -> None:
        """
        prints self.transform to the screen.
        :return: None
        """
        print(self.transform)

    def save_result(self) -> None:
        """
        saves a file with the timestamp in the filename. Look at the "output" folder to get these results.
        :return:  None
        """
        timestamp: str = time.strftime("%b_%d@%H-%M-%S")
        cv2.imwrite(f"output/image_{timestamp}.png",self.result_image*256)
            #Note: the times 256 is to move this from 0.0-1.0 format for opencv to 0-255 for png files.