from collections import Counter, defaultdict
import re

STOP_WORDS = set([
    'the','a','an','and','or','but','in','on','at','to','for','of','with',
    'is','it','its','this','that','are','was','were','be','been','being',
    'have','has','had','do','does','did','will','would','could','should',
    'may','might','shall','can','need','dare','ought','used','from','by',
    'as','into','through','during','before','after','above','below','up',
    'down','out','off','over','under','again','then','once','here','there',
    'when','where','why','how','all','both','each','few','more','most',
    'other','some','such','no','not','only','same','so','than','too','very',
    'just','about','new','your','our','their','his','her','my','we','you',
    'they','he','she','i','us','them','him','me','what','which','who',
])

WORD_PATTERN = re.compile(r'\b[a-z]{3,}\b')

word_freq = Counter()
cooccur = defaultdict(int)
is_ready = False

def precompute():
    global word_freq, cooccur, is_ready
    from kobe_wave.models import Article

    print("⚙️  Précalcul des co-occurrences en cours...")
    for title in Article.objects.values_list("title", flat=True).iterator(chunk_size=2000):
        if not title:
            continue
        words = list(set(w for w in WORD_PATTERN.findall(title.lower()) if w not in STOP_WORDS))
        for w in words:
            word_freq[w] += 1
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                cooccur[tuple(sorted([words[i], words[j]]))] += 1

    is_ready = True
    print(f"✅ Précalcul terminé — {len(word_freq)} mots, {len(cooccur)} paires")
