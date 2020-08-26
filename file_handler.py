from pathlib import Path

def getFile(path, mode = "r"):
	cdir = Path(__file__).resolve().parent

	return open(cdir / path, mode)