# Timecode Fixer

## Overview

Timecode Fixer is a command-line tool that reads two XML files, matches clip items by name, extracts their numeric identifiers, and updates the timecodes in the edit XML using the correct timecodes from the source XML. The updated XML is exported as `output.xml` in the same directory as the script.

## Features

* Extracts clip metadata and timecodes from XML files
* Matches clips based on numeric parts of their names
* Replaces incorrect timecodes in the edit XML
* Outputs a clean, updated XML file
* Simple command-line usage

## Requirements

* Python 3.7+
* `pandas`
* `numpy`

Install dependencies:

```bash
pip install pandas numpy
```

## Usage

Run the script from the command line:

```bash
python3 timecodeFixer.py edit.xml source.xml
```

* **edit.xml** → XML file whose timecodes need to be corrected
* **source.xml** → XML file containing correct timecodes

The script will generate:

```
output.xml
```

in the same directory as `timecodeFixer.py`.

## How It Works

1. Both XML files are parsed.
2. Clip names are scanned for numeric strings used as matching keys.
3. Timecodes from the source XML are matched to the corresponding clips in the edit XML.
4. The edit XML is rewritten with corrected timecodes.

## Output

A fully updated XML file named `output.xml` containing corrected clip timecodes.

## Example

```bash
python3 timecodeFixer.py edit.xml source.xml
```

After running the command, you will see:

```
Timecodes updated successfully. Output saved to: /path/to/output.xml
```
