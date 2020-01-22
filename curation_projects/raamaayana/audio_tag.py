import logging
import os
from pathlib import Path

import regex

from doc_curation.md_helper import MdFile

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")


def get_adhyaaya_to_mp3_map():
    mp3_root = "/home/vvasuki/rAmAyaNa-audio/"
    mp3_paths = Path(mp3_root).glob(pattern="**/*.mp3")
    adhyaaya_to_mp3_map = {}
    for mp3_path in mp3_paths:
        kaanda = regex.findall("Kanda_\\d_", str(mp3_path))[0].replace("Kanda", "").replace("_", "")
        adhyaaya = regex.findall("\\d\\d\\d", str(mp3_path))[0]
        adhyaaya_id = "%s-%s" % (kaanda, adhyaaya)
        web_mp3_path = str(mp3_path).replace(mp3_root, "https://archive.org/download/Ramayana-recitation-Sriram-harisItArAmamUrti-Ghanapaati-v2/").replace("mp3/", "")
        adhyaaya_to_mp3_map[adhyaaya_id] = web_mp3_path
    return adhyaaya_to_mp3_map

if __name__ == '__main__':
    adhyaaya_to_mp3_map = get_adhyaaya_to_mp3_map()
    # logging.debug(adhyaaya_to_mp3_map)
    md_file_path = "/home/vvasuki/vvasuki-git/kAvya/content/TIkA/padya/purANa/rAmAyaNa/Andhra/"
    md_files = MdFile.get_md_files_from_path(dir_path=md_file_path, file_pattern="**/*.md", file_name_filter=lambda x: len(regex.findall("\\d\\d\\d", os.path.basename(x))) > 0)
    for md_file in md_files:
        # md_file.replace_in_content("<div class=\"audioEmbed\".+?></div>\n", "")
        logging.debug(md_file.file_path)
        kaanda = regex.findall("/\\d_", str(md_file.file_path))[0].replace("/", "").replace("_", "")
        adhyaaya = regex.findall("\\d\\d\\d", str(md_file.file_path))[0]
        adhyaaya_id = "%s-%s" % (kaanda, adhyaaya)
        logging.debug(adhyaaya_id)
        (yml, _) = md_file.read_md_file()
        # logging.debug(adhyaaya_to_mp3_map[adhyaaya_id])
        md_file.prepend_to_content('<div class="audioEmbed"  caption="श्रीराम-हरिसीताराममूर्ति-घनपाठिभ्यां वचनम्" src="%s"></div>\n' % adhyaaya_to_mp3_map[adhyaaya_id], dry_run=False)