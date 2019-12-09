from readers.file_reader import FileReader

BLACK = '0'
WHITE = '1'
CLEAR = '2'

B_FILL = '\33[40m0'
W_FILL = '\33[47m1'
C_FILL = '\33[0m2'

COLOR = {
    BLACK: B_FILL,
    WHITE: W_FILL,
    CLEAR: C_FILL
}


def main():
    encoded_image = FileReader.read_input_as_string()

    width = 25
    height = 6

    final_image = [COLOR[CLEAR] for _ in range(width*height)]

    ## Find Layer
    for layer_num, i in enumerate(range(0, len(encoded_image), width*height)):
        ## Build layer
        for j in range(i, i + width*height):
            curr = encoded_image[j]
            idx = j % len(final_image)
            if final_image[idx] == COLOR[CLEAR]:
                final_image[idx] = str(COLOR[encoded_image[j]])

    readable_final_image = '\n'.join(map(lambda row: ''.join(row),
                                         [final_image[x:x+width] for x in range(0, len(final_image)-1, width)]))
    print(f"Final image: \n{readable_final_image}")


if __name__ == '__main__':
    main()
