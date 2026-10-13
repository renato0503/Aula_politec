import json
from collections import Counter, defaultdict

data = """
C	B	B	C	C	C	B	C	C	A	A	A	A	A	A	C	A	A	B	A	B	B	A	B	A	A	B	A	A	B	C	A	B	C	C	C	D	C	C	C	A	A	A	A	A	B	C	C	C	C	AVANCADO
C	B	C	C	C	D	B	C	C	C	D	B	A	C	B	C	C	C	B	B	B	B	C	B	C	B	B	C	B	D	C	C	D	B	C	B	C	B	C	C	D	C	C	B	C	C	C	C	C	C	EXPERT
C	B	B	C	C	B	B	C	C	C	C	B	A	C	B	C	C	C	B	B	B	B	B	B	C	B	B	C	C	D	C	A	B	B	C	C	D	C	B	C	C	C	C	B	A	C	C	C	B	C	EXPERT
B	B	D	C	C	B	B	A	C	B	A	B	B	C	A	C	B	C	B	D	C	B	D	C	A	B	B	A	A	D	C	C	B	B	C	C	A	B	D	C	B	D	C	B	A	C	C	D	C	C	AVANCADO
B	B	D	B	C	C	B	C	C	B	D	B	C	C	B	C	C	C	B	B	B	C	B	C	C	B	B	C	A	D	C	D	A	D	C	C	C	C	D	D	B	B	B	B	B	B	C	C	D	C	AVANCADO
C	B	B	C	C	C	D	C	C	C	B	A	D	A	A	C	B	C	B	B	C	B	D	B	C	C	D	C	A	D	C	B	D	B	C	A	A	C	C	C	B	C	C	B	C	C	C	A	C	C	AVANCADO
B	B	B	C	C	B	B	A	C	C	A	B	D	B	A	C	C	B	A	B	B	B	B	C	C	B	D	C	A	A	B	A	B	C	C	C	C	C	B	C	D	B	C	B	B	C	C	D	C	C	AVANCADO
C	B	C	C	C	B	B	C	C	B	C	B	A	D	C	C	C	C	B	D	A	B	C	C	B	D	D	C	C	C	B	C	C	C	B	C	B	C	A	A	A	B	B	C	B	D	C	C	C	C	INTERMEDIARIO
C	B	B	D	C	D	B	A	C	B	B	C	D	C	B	C	D	D	A	C	C	C	C	C	B	D	D	C	D	B	B	C	C	B	B	C	C	D	D	B	C	C	C	C	B	B	C	C	B	D	BASICO
C	B	C	B	C	D	B	C	C	A	A	B	C	B	B	C	D	C	B	C	B	A	B	B	A	B	A	A	C	C	C	C	B	B	A	C	A	C	C	D	D	C	A	B	C	A	B	C	C	C	AVANCADO
B	B	B	C	C	C	B	C	C	C	A	B	A	A	A	C	A	C	B	A	B	B	B	B	C	B	A	C	B	D	C	D	C	B	C	C	D	C	A	C	C	C	C	B	C	C	C	C	C	C	AVANCADO
C	B	B	C	C	C	B	C	C	C	A	B	A	A	B	C	C	A	B	B	B	B	C	B	C	B	A	C	D	C	C	D	C	B	C	C	D	C	C	C	B	C	C	B	C	B	C	C	A	C	AVANCADO
C	B	B	C	C	C	B	C	C	C	D	B	B	C	B	C	D	C	B	B	A	B	B	A	A	B	B	C	B	D	C	C	D	B	C	C	D	B	C	C	D	D	C	B	C	A	C	A	A	C	AVANCADO
C	B	B	C	C	C	B	C	C	C	D	B	B	B	B	C	C	C	B	A	C	D	B	B	C	B	B	C	C	D	C	D	B	B	C	C	D	C	C	C	C	B	C	C	C	B	C	C	C	C	EXPERT
B	B	B	C	C	C	B	C	C	C	A	B	C	B	B	C	B	B	B	A	D	B	C	C	D	B	B	C	C	D	C	C	B	C	C	B	C	B	B	C	D	C	C	B	C	A	C	C	A	C	AVANCADO
C	B	C	C	C	C	B	C	C	C	A	B	A	C	A	C	D	A	A	A	B	B	D	B	C	B	B	A	C	C	C	D	D	B	C	C	D	C	B	C	D	A	A	B	C	C	C	C	B	B	AVANCADO
C	B	B	C	C	C	B	C	C	C	C	B	A	B	B	C	C	C	B	A	B	B	B	B	C	D	B	C	C	D	C	D	D	C	B	C	D	B	C	C	C	C	C	B	C	C	C	C	B	C	EXPERT
C	B	B	C	C	D	B	A	C	B	C	B	A	B	D	B	A	C	B	C	B	C	B	C	C	B	C	C	C	D	C	B	B	B	C	C	C	A	D	C	D	D	D	B	C	A	C	C	A	C	AVANCADO
B	B	C	C	C	C	B	A	C	B	A	B	A	C	B	C	C	C	B	B	B	B	D	D	C	B	B	C	C	D	C	C	B	D	C	B	C	A	A	C	A	A	C	B	D	A	C	C	C	C	AVANCADO
C	B	B	C	C	C	B	C	C	C	B	B	C	A	B	C	A	C	B	B	A	B	D	B	A	D	B	C	C	C	D	C	B	C	A	C	C	C	C	D	C	B	D	C	C	A	C	A	A	C	AVANCADO
C	B	D	C	C	B	B	A	C	B	A	D	C	A	D	C	C	B	B	A	A	A	A	C	C	D	D	D	D	B	D	A	B	C	D	D	D	A	C	D	A	A	C	B	C	A	C	C	B	B	BASICO
C	B	D	C	C	C	B	C	A	C	B	B	A	A	B	C	C	C	B	C	B	C	B	B	D	B	B	C	A	D	C	B	B	B	C	C	D	C	C	C	C	A	C	B	B	A	C	C	A	C	AVANCADO
C	B	C	B	C	C	B	A	C	C	C	B	B	C	B	C	C	C	B	C	C	C	C	B	C	C	B	C	C	B	C	C	B	C	B	C	C	C	C	C	B	B	B	B	C	B	C	B	C	C	AVANCADO
A	B	D	B	C	D	B	A	C	C	A	D	A	A	B	D	C	B	B	A	A	B	B	B	C	B	A	C	C	B	A	C	D	B	C	C	A	C	D	D	D	B	C	D	B	A	C	A	B	B	INTERMEDIARIO
C	B	B	B	C	C	B	C	C	C	C	A	A	B	D	C	A	B	B	A	A	D	A	B	C	B	B	C	D	B	C	C	B	D	C	C	C	C	A	B	D	D	C	D	C	A	C	C	C	C	AVANCADO
C	B	B	C	C	B	B	C	C	A	A	B	B	C	B	C	A	C	B	B	B	B	B	B	C	B	B	D	B	D	C	C	B	B	C	C	D	B	C	C	C	A	C	B	C	A	C	C	A	C	AVANCADO
C	B	B	B	C	B	B	C	C	C	A	B	A	C	B	C	B	C	B	A	B	C	A	C	C	B	B	C	C	C	C	D	A	B	A	C	D	A	A	C	C	C	A	B	B	A	C	D	D	C	AVANCADO
C	B	C	C	C	C	B	C	C	C	A	B	A	C	B	C	C	C	B	A	B	B	B	D	A	B	B	C	A	C	B	A	A	B	C	B	D	C	A	D	C	A	C	B	D	B	C	A	B	C	AVANCADO
A	B	D	B	C	B	B	C	C	C	A	D	C	C	B	C	A	A	B	B	B	B	A	C	D	D	D	C	B	D	C	C	B	C	C	B	C	C	C	D	B	B	B	B	C	C	A	A	B	B	INTERMEDIARIO
C	B	D	C	C	C	B	C	C	C	C	B	A	C	B	C	A	C	B	B	B	B	B	B	C	B	B	C	C	B	C	C	B	B	C	B	D	A	C	C	D	C	A	C	A	A	C	D	A	C	AVANCADO
C	B	B	C	C	C	B	C	C	C	C	B	B	A	B	A	C	C	B	B	B	B	B	B	C	B	B	C	C	D	C	C	C	B	C	C	D	C	C	C	D	C	C	A	C	C	C	C	C	C	EXPERT
""".strip()

lines = [l.strip() for l in data.split('\n') if l.strip()]

gabarito = {
    1:'C',2:'B',3:'B',4:'C',5:'C',6:'C',7:'B',8:'C',9:'C',10:'C',
    11:'C',12:'B',13:'B',14:'C',15:'B',16:'C',17:'C',18:'C',
    19:'B',20:'B',21:'B',22:'B',23:'B',24:'B',
    25:'C',26:'B',27:'B',28:'C',29:'C',30:'D',
    31:'C',32:'C',33:'C',34:'B',35:'C',36:'C',37:'D',38:'C',
    39:'C',40:'C',41:'D',42:'C',43:'C',44:'B',
    45:'C',46:'C',47:'C',48:'C',49:'C',50:'C'
}

block_defs = {
    'Bloco 1 - Informatica Basica (P1-P10)': list(range(1,11)),
    'Bloco 2 - Noes de Informatica (P11-P18)': list(range(11,19)),
    'Bloco 3 - Excel e Planilhas (P19-P24)': list(range(19,25)),
    'Bloco 4 - Estatistica e Dados (P25-P30)': list(range(25,31)),
    'Bloco 5 - Power BI e DAX (P31-P38)': list(range(31,39)),
    'Bloco 6 - Git e GitHub (P39-P44)': list(range(39,45)),
    'Bloco 7 - Inteligencia Artificial (P45-P50)': list(range(45,51)),
}

block_labels = {
    'Bloco 1 - Informatica Basica (P1-P10)': 'Bloco 1 - Informatica Basica (P1-P10)',
    'Bloco 2 - Noes de Informatica (P11-P18)': 'Bloco 2 - Noes de Informatica (P11-P18)',
    'Bloco 3 - Excel e Planilhas (P19-P24)': 'Bloco 3 - Excel e Planilhas (P19-P24)',
    'Bloco 4 - Estatistica e Dados (P25-P30)': 'Bloco 4 - Estatistica e Dados (P25-P30)',
    'Bloco 5 - Power BI e DAX (P31-P38)': 'Bloco 5 - Power BI e DAX (P31-P38)',
    'Bloco 6 - Git e GitHub (P39-P44)': 'Bloco 6 - Git e GitHub (P39-P44)',
    'Bloco 7 - Inteligencia Artificial (P45-P50)': 'Bloco 7 - Inteligencia Artificial (P45-P50)',
}

def score(respostas, qs):
    return sum(1 for q in qs if gabarito[q] == respostas[q-1])

results = []
for line in lines:
    parts = line.split()
    respostas = parts[:50]
    nivel = parts[50]
    total = sum(1 for q in range(1,51) if gabarito[q] == respostas[q-1])
    block_scores = {}
    for bname, bqs in block_defs.items():
        block_scores[bname] = score(respostas, bqs)
    results.append({'respostas': respostas, 'nivel': nivel, 'total': total, 'blocks': block_scores})

# Block stats
block_stats = {}
for bname, bqs in block_defs.items():
    vals = [r['blocks'][bname] for r in results]
    total_qs = len(bqs)
    pct = sum(vals)/len(vals)/total_qs*100
    block_stats[bname] = {
        'avg_pct': round(pct, 1),
        'avg_score': round(sum(vals)/len(vals), 1),
        'max': max(vals),
        'total_qs': total_qs
    }

# Level stats
level_dist = Counter(r['nivel'] for r in results)
level_avg = {}
for nivel in ['BASICO','INTERMEDIARIO','AVANCADO','EXPERT']:
    scores = [r['total'] for r in results if r['nivel'] == nivel]
    if scores:
        level_avg[nivel] = {'avg': round(sum(scores)/len(scores), 1), 'count': len(scores)}

# Question-level
q_correct = [0]*50
for r in results:
    for q in range(50):
        if r['respostas'][q] == gabarito[q+1]:
            q_correct[q] += 1

# Per level per block
level_block_scores = {}
for nivel in ['BASICO','INTERMEDIARIO','AVANCADO','EXPERT']:
    nivel_results = [r for r in results if r['nivel'] == nivel]
    if not nivel_results:
        continue
    level_block_scores[nivel] = {}
    for bname, bqs in block_defs.items():
        vals = [r['blocks'][bname] for r in nivel_results]
        total_qs = len(bqs)
        pct = sum(vals)/len(vals)/total_qs*100
        level_block_scores[nivel][bname] = {'avg_pct': round(pct,1), 'count': len(nivel_results)}

# Output JSON
output = {
    'total_respondents': len(results),
    'block_stats': block_stats,
    'level_dist': dict(level_dist),
    'level_avg': level_avg,
    'q_correct': q_correct,
    'level_block_scores': level_block_scores,
    'overall_avg': round(sum(r['total'] for r in results)/len(results), 1),
}
print(json.dumps(output, ensure_ascii=False, indent=2))
