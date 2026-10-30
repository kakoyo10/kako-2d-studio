"""tools/common.py — shared helpers (ffmpeg decode, json io, time formatting, Chinese-aware tokens)."""
import json, os, re, subprocess, sys
import numpy as np


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r.stdout


def probe_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path])
    return float(out.strip())


def load_audio(path, sr=16000, mono=True):
    """Decode any audio/video file with ffmpeg into float32 numpy (mono: shape [n], stereo: [n, 2])."""
    ch = 1 if mono else 2
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-acodec", "pcm_f32le", "-ac", str(ch), "-ar", str(sr), "-"],
                       capture_output=True)
    if p.returncode != 0:
        sys.exit(f"ffmpeg could not decode {path}: {p.stderr.decode()[-800:]}")
    a = np.frombuffer(p.stdout, dtype=np.float32).copy()
    return a if mono else a.reshape(-1, 2)


def save_json(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def ts(sec):
    m, s = divmod(max(0.0, sec), 60)
    return f"{int(m):02d}:{s:05.2f}"


def norm_word(w):
    return re.sub(r"[^\w']+", "", w.lower())


CJK = "\u3400-\u9fff\uf900-\ufaff"
CJK_RE = re.compile(f"[{CJK}]")
# one token per Chinese character (trailing punctuation stays attached), one token per run of other non-space text
TOKEN_RE = re.compile(f"[{CJK}][^\\w\\s]*|[^\\s{CJK}]+")


ABBREV = {"mr", "mrs", "ms", "dr", "prof", "st", "jr", "sr", "vs", "mt", "no", "etc", "e.g", "i.e"}


def is_strong_end(word, extra=""):
    """Sentence-ending punctuation, but not "Dr." / "Mr." / single initials like "J."."""
    w = word.strip()
    if re.fullmatch(r"(?i)(?:[a-z]|" + "|".join(re.escape(a) for a in ABBREV) + r")\.", w):
        return False
    return bool(re.search(r"[.?!…。！？" + extra + r"]['\"”’)）」』]*$", w))


def is_cjk(s):
    return bool(CJK_RE.search(s or ""))


def tokenize(text):
    """Split a script into timing tokens: Chinese per character, everything else per whitespace-separated word."""
    return TOKEN_RE.findall(text)


def join_tokens(tokens):
    """Join tokens back into text: a space only between two non-Chinese tokens."""
    out = ""
    for t in tokens:
        t = t.strip()
        if not t:
            continue
        if out and not is_cjk(out[-1]) and not is_cjk(t[0]) and not re.match(r"[，。！？；：、]", out[-1]):
            out += " "
        out += t
    return out


def sentences_from_words(words, max_gap=0.8):
    """Group word dicts into sentences on . ? ! and long pauses."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_punct = is_strong_end(w["word"])
        gap = (nxt["start"] - w["end"]) if nxt else 9
        if end_punct or gap > max_gap or not nxt:
            out.append({"i": len(out), "start": round(cur[0]["start"], 3), "end": round(cur[-1]["end"], 3),
                        "text": join_tokens(x["word"] for x in cur)})
            cur = []
    return out


def write_timeline(outdir, words, sentences, source):
    save_json(os.path.join(outdir, "words.json"), {"source": source, "words": words})
    save_json(os.path.join(outdir, "sentences.json"), sentences)
    with open(os.path.join(outdir, "transcript.txt"), "w", encoding="utf-8") as f:
        for s in sentences:
            f.write(f"[{ts(s['start'])} -> {ts(s['end'])}] {s['text']}\n")
    print(f"timeline: {len(words)} words, {len(sentences)} sentences -> {outdir}")
