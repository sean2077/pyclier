import argparse

from . import prog_name, __version__


def subcommand1_func(args):
    print(f"subcommand1 received argument a: {args.a}")


def main():
    # create main parser
    parser = argparse.ArgumentParser(
        prog=prog_name, description="example python cli tool."
    )
    # add option of main command
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # create subcommands' main parser
    subparser = parser.add_subparsers(title="Commands", metavar="<command>")

    # add subcommands
    ## add subcommand1
    subcommand1 = subparser.add_parser("subcommand1", help="subcommand1.")
    # add option of subcommand
    subcommand1.add_argument("-a", help="option of subcommand1")
    subcommand1.set_defaults(func=subcommand1_func)

    # parse args
    args = parser.parse_args()

    # run command
    if hasattr(args, "func"):  # run subcommand
        args.func(args)
    else:  # run main command
        parser.print_help()


if __name__ == "__main__":
    main()
