from logs.setup_logs import init_logs
from readers.file_reader import FileReader

def main():
    encoded_image = FileReader.read_input_as_string()

    width = 25
    height = 6

    layers = []

    ## Find Layer
    for layer_num, i in enumerate(range(0, len(encoded_image), width*height)):
        print(f"Starting processing at {i}")
        print(f"Creating layer {layer_num}")
        layers.append([])
        ## Build layer
        for j in range(i, i + width*height):
            print(f"putting {encoded_image[j]} in layer {layer_num}")
            layers[-1].append(int(encoded_image[j]))

    print(f"Layers: {layers}")
    sorted_layers = sorted(map(lambda layer: list(filter(lambda num: num != 0, layer)), layers), key=lambda layer: len(layer))
    validation_layer = sorted_layers[-1]
    print(f"layer with least zeros is: {validation_layer}")
    print(f"The validation layer checksums to: {validation_layer.count(1) * validation_layer.count(2)}")


if __name__ == '__main__':
    main()
