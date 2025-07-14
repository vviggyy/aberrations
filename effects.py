from aberration import Aberration
import argparse

def parse_args():
    parser = argparse.ArgumentParser("Apply lens aberration to input image.")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input image",
        default="hq720.jpg",
    ),
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to output file",
        default="out.jpg",
    ),
    parser.add_argument(
        "-m",
        "--m",
        type=int,
        help="m coefficient",
        default=0,
    )
    parser.add_argument(
        "-n",
        "--n",
        type=int,
        help="n coefficient",
        default=0,
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        help="size of kernel",
        default=5,
    )    
    
    return parser.parse_args()

    
if __name__ == "__main__":
    args = parse_args()
    
    ab = Aberration(args.m, args.n, size = args.size, plots= False)
    proces = ab._convolve(img_path=f"in/{args.input}")
    
    #save jpg
    ab._save(proces, f"{args.output}.jpg")