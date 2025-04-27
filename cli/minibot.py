import argparse
from agent.minikernel import MiniKernel

def main():
    parser = argparse.ArgumentParser(description="MiniKernel - Local AI DevOps Agent")
    parser.add_argument("--say", required=True, help="Natural language instruction")
    args = parser.parse_args()

    kernel = MiniKernel()
    kernel.run(args.say)

if __name__ == "__main__":
    main()
