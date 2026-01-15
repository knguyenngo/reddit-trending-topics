import sys, getopt
import scrape_functions as sf

options = "s:nhtcl:f:u:"
long_options = ["subreddit=", "new", "hot", "controversial", "top", "limit=", "from-hours=", "until-hours="]

def main():
    # Read in arguments
    args = sys.argv[1:]
    sub_name = ""
    listing = ""
    listing_args = None
    time_range = None
    from_hours = None
    until_hours = None

    # Parse options and values
    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-s", "--subreddit"):
                sub_name = currentVal
            elif currentArg in ("-n", "--new"):
                listing = "new"
            elif currentArg in ("-h", "--hot"):
                listing = "hot"
            elif currentArg in ("-t", "--top"):
                listing = "top"
            elif currentArg in ("-c", "--controversial"):
                listing = "controversial"
            elif currentArg in ("-l", "--limit"):
                listing_args = {"limit": int(currentVal)}
            elif currentArg in ("-f", "--from-hours"):
                from_hours = int(currentVal)
            elif currentArg in ("-u", "--until-hours"):
                until_hours = int(currentVal)
    except getopt.error as err:
        print(str(err))

    # Scrape all posts under listing within time range
    sf.get_raw_data(sub_name, from_hours, until_hours, listing, listing_args)

if __name__ == "__main__":
    main()
