import sys, getopt
import scrape_functions as sf

options = "i:"
long_options = ["input="]

def main():
    args = sys.argv[1:]
    file_path = ""

    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-i", "--input"):
                file_path = currentVal
    except getopt.error as err:
        print(str(err))
 
    sf.gather_comments(file_path)

if __name__ == "__main__":
    main()
