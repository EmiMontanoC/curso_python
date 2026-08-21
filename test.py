import argparse

def calculate_area(length, width):
    return length * width

def main():
    """"
    Main function to parse command line arguments and calculate the area.
    """
    parser = argparse.ArgumentParser(description="Calculate the area of a rectangle ")
    parser.add_argument("-l", "--length", type=float, required=True, help="Length of the rectangle")
    parser.add_argument("-w", "--width", type=float, required=True, help="Width of the rectangle")
    args = parser.parse_args()
    area = calculate_area(args.length, args.width)
    print(f"The area of the rectangle is: {area}") 
    
if __name__ == "__main__":
    main()
