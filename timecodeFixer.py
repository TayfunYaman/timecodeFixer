import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import sys
import os


def extract_timecodes(xml_path: str) -> pd.DataFrame:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    data = []

    for clip in root.iter('clipitem'):
        def get(tag):
            elem = clip.find(tag)
            return elem.text if elem is not None else 'N/A'

        data.append({
            "name": get('name'),
            "start": get('start'),
            "end": get('end'),
            "in": get('in'),
            "out": get('out'),
            "timecode": (
                clip.find('.//timecode/string').text
                if clip.find('.//timecode/string') is not None
                else 'N/A'
            )
        })

    return pd.DataFrame(data)


def update_xml_timecodes(xml_path: str, df: pd.DataFrame, output_xml: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for clip in root.iter('clipitem'):
        clip_name_elem = clip.find('name')
        if clip_name_elem is None:
            continue

        clip_name = clip_name_elem.text
        matched_timecode = df.loc[df['name'] == clip_name, 'timecode']

        if not matched_timecode.empty:
            timecode_elem = clip.find('.//timecode/string')
            if timecode_elem is not None:
                timecode_elem.text = matched_timecode.iloc[0]

    tree.write(output_xml)


def prepare_corrected_dataframe(df_edit: pd.DataFrame, df_source: pd.DataFrame) -> pd.DataFrame:
    df_edit = df_edit.copy()
    df_source = df_source.copy()

    df_edit['name_key'] = df_edit['name'].str.extract(r'(\d+)')
    df_source['name_key'] = df_source['name'].str.extract(r'(\d+)')

    merged = pd.merge(df_edit, df_source[['name_key', 'timecode']], on='name_key', how='left')

    merged['timecode'] = merged['timecode_y']
    merged.drop(['timecode_x', 'timecode_y', 'name_key'], axis=1, inplace=True)

    merged['timecode'] = merged['timecode'].replace("N/A", np.nan)
    merged = merged.dropna(subset=['timecode'])

    return merged


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 timecodeFixer.py edit_xml_path source_xml_path")
        sys.exit(1)

    edit_xml_path = sys.argv[1]
    source_xml_path = sys.argv[2]

    output_xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.xml")

    df_edit = extract_timecodes(edit_xml_path)
    df_source = extract_timecodes(source_xml_path)

    df_corrected = prepare_corrected_dataframe(df_edit, df_source)

    update_xml_timecodes(edit_xml_path, df_corrected, output_xml_path)

    print(f"Timecodes updated successfully. Output saved to: {output_xml_path}")


if __name__ == "__main__":
    main()
