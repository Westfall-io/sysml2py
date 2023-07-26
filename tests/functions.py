import re
import string


def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return ""  # so we will return empty to remove the comment
        else:  # otherwise, we will return the 1st group
            return match.group(1)  # captured quoted-string

    return regex.sub(_replacer, string)


def strip_ws(text):
    text = remove_comments(text)
    text = text.replace("specializes", ":>")
    text = text.replace("subsets", ":>")
    text = text.replace("redefines", ":>>")
    return text.translate(str.maketrans("", "", string.whitespace))
