from FileReader import FileReader
import pdb
from collections import deque

# FileReader for file operations on training set
reader = FileReader()

weights = [[0]*30 for i in range(20)]
LEARNING_RATE = 0.1

# when using fixed max iterations
MAX_ITERATIONS = 100

# when using a convergence approach to measure fluctuation across iterations
# and stop when the fluctuation is below a certain threshold
history = deque([0],maxlen=10)
threshold = 1
radius = 100

epoch = 0


"""Sums weights given image"""
def sum_of_weights(image_array):
    total = 0
    # Since not all images are the same size,
    # need way to have the pixel list grow for smaller images
    while len(weights) < len(image_array):
        weights.append([])

    for i in range(len(image_array)):
        # Continuation of allowance for pixel list to grow
        #  to accomodate larger files, new pixels initially set to " "
        while len(weights[i]) < len(image_array[i]):
            weights[i].append(0)
        for j in range(len(image_array[i])):

        # sum the product of weight and pixel value for each pixel
            total += weights[i][j] * ord(image_array[i][j])

    # outcome
    if total > 0:
        return 1
    else:
        return -1


"""Updates weights based on error function from image outcome"""
def update_weights(image_array, error):
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            weights[i][j] += LEARNING_RATE * ord(image_array[i][j]) * error


### TRAINING ###
# when using MAX_ITERATIONS, use the following
# continue iterating until number of iterations reaches the MAX_ITERATIONS
# while epoch < MAX_ITERATIONS:

# when using convergence approach, use the following
# continue iterating until the fluctuation decreases beyond a certain radius
while radius > threshold or min(history) > 0 or epoch < MAX_ITERATIONS:
    epoch += 1

    # reset FileReader files pointers
    reader.reset()

    # counters for correct and incorrect classifications
    num_correct = 0
    num_incorrect = 0

    # loop through training set
    for i in range(reader.TRAINING_SIZE):
        try:
            image_array = reader.next_file()
            label = reader.get_label()

            output = sum_of_weights(image_array)
            actual_output = 0

            if label == "8":
                actual_output = 1
            else:
                actual_output = -1

            ERROR = actual_output - output

            if ERROR:
                num_incorrect += 1
            else:
                num_correct += 1

            update_weights(image_array, ERROR)

        except Exception as e:
            # start debugger at stack exception point
            pdb.post_mortem()

    # print number of correct and incorrect classifications
    print "Correct:" + str(num_correct) + ", Incorrect:" + str(num_incorrect)

    # update radius based on new iteration
    history.append(num_incorrect)
    radius = (max(history) - min(history))

print "Number of iterations to convergence: " + str(epoch)

#for filename in ['data1/1.txt', 'data1/2.txt', 'data1/3.txt', 'data1/4.txt', 'data1/5.txt']:
### EVALUATION ###
while True:
    filename = raw_input("Enter a file path or type q to quit:")
    # user is quitting the program
    if filename == "q":
        break
    # else, try to read the file and classify it
    # wrap in try-except in case file path is invalid
    try:
        test_img = reader.read_image_file(filename)
        output = sum_of_weights(test_img)
        if output == 1:
            print "It's an 8!"
        else:
            print "It's not an 8! What the hell is wrong with you?"

    except Exception as e:
        print "Not a valid file path, please try again"
