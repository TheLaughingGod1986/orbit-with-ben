#!/usr/bin/env python3
"""Render the worker launcher without interpreting paths as shell or XML code."""
import argparse
import pathlib
import plistlib


def render(home, engine, engine_url, owb, hos, model):
    template = pathlib.Path(__file__).with_name("com.owb.macbook-worker.plist")
    doc = plistlib.loads(template.read_bytes())
    replacements = {"__HOME__": home, "__ENGINE__": engine, "__ENGINE_URL__": engine_url,
                    "__OWB__": owb, "__HOS__": hos, "__MODEL__": model}

    def replace(value):
        if isinstance(value, str):
            for key, text in replacements.items():
                value = value.replace(key, str(text))
            return value
        if isinstance(value, list):
            return [replace(item) for item in value]
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        return value

    return plistlib.dumps(replace(doc), sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ("home", "engine", "engine-url", "owb", "hos", "model", "out"):
        parser.add_argument("--" + field, required=True)
    args = vars(parser.parse_args())
    out = pathlib.Path(args.pop("out"))
    out.write_bytes(render(**args))


if __name__ == "__main__":
    main()
