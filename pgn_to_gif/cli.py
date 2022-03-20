from typing import Literal, Optional, Sequence
import argparse
from pathlib import Path
from .utils import *
import chess
import pyperclip


def parse_orientation(orientation: Literal["white", "black"]) -> chess.Color:
    if orientation == "white":
        return chess.WHITE
    elif orientation == "black":
        return chess.BLACK
    else:
        raise ValueError(f"unknown {orientation=}")


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    pgn_sources = parser.add_mutually_exclusive_group()

    pgn_sources.add_argument(
        "--input-file",
        dest="input_file",
        type=Path,
        help="path to pgn file to read",
    )
    parser.add_argument(
        "--output-file",
        dest="output_file",
        default="./game.gif",
        type=Path,
        help="path to gif file to save",
    )
    pgn_sources.add_argument(
        "--from-clipboard",
        dest="from_clipboard",
        action="store_const",
        default=False,
        const=True,
        help="Read PGN from clipboard",
    )
    parser.add_argument(
        "--add-initial-position",
        dest="add_initial_position",
        default=True,
        action="store_const",
        const=True,
        help="add initial position to gif",
    )
    parser.add_argument(
        "--highlight-last-move",
        dest="highlight_last_move",
        default=False,
        action="store_const",
        const=True,
        help="highlight last move on board",
    )
    parser.add_argument(
        "--orientation",
        dest="orientation",
        default="white",
        choices=["white", "black"],
        help="orientation of board",
    )
    parser.add_argument(
        "--size", dest="size", default=400, type=int, help="size of board"
    )
    parser.add_argument(
        "--coordinates",
        dest="coordinates",
        default="true",
        action="store_const",
        const=True,
        help="add board coordinates",
    )
    parser.add_argument(
        "--css-path",
        dest="css_path",
        default=None,
        type=Path,
        help="path to css file to style board",
    )
    parser.add_argument(
        "--loop",
        dest="loop",
        default=0,
        type=int,
        help="number of loops for gif, 0 means infinite",
    )
    parser.add_argument(
        "--duration",
        dest="duration",
        default=1.0,
        type=float,
        help="duration of each frame (in seconds) in gif",
    )
    parser.add_argument(
        "--fps", dest="fps", default=1.0, type=float, help="frame per second of gif"
    )
    parser.add_argument(
        "--palettesize",
        dest="palettesize",
        default=64,
        type=int,
        help="number of colors to quantize images to",
    )
    parser.add_argument(
        "--subrectangles",
        dest="subrectangles",
        action="store_const",
        const=True,
        help="optimize gif by storing change",
    )
    parser.add_argument(
        "--processes",
        dest="processes",
        default=1,
        type=int,
        help="number of processes when converting svgs to pngs",
    )

    args = parser.parse_args(argv)

    if (not args.from_clipboard) and (not args.input_file):
        parser.error('Must specify either "--from-clipboard" or "--input_file"')

    if args.from_clipboard:
        pgn = pyperclip.paste()
    else:
        pgn = read_pgn(args.input_file)

    style = None if args.css_path is None else read_css(args.css_path)
    orientation = parse_orientation(args.orientation)
    add_initial_position = args.add_initial_position
    highlight_last_move = args.highlight_last_move
    coordinates = args.coordinates
    subrectangles = args.subrectangles
    pgn_to_gif(
        pgn,
        args.output_file,
        add_initial_position,
        highlight_last_move,
        orientation,
        args.size,
        coordinates,
        style,
        args.loop,
        args.duration,
        args.fps,
        args.palettesize,
        subrectangles,
        args.processes,
    )


if __name__ == "__main__":
    main()
