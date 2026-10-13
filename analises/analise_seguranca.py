# -*- coding: utf-8 -*-
"""
Análise de Segurança Pública — POLITEC/MT
Gera figures JSON e HTML com injeção correta dos charts
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json, pathlib, re, warnings
warnings.filterwarnings('ignore')

BASE = pathlib.Path(r'D:\Dev\Aula Politec')
ANALISE = pathlib.Path(r'D:\Dev\Aula Politec\analises')

REGION_MAP = {1:'Centro-Oeste', 2:'Nordeste', 3:'Sudeste', 4:'Sul', 5:'Norte'}
RC = {
    'Centro-Oeste': '#6c63ff',
    'Nordeste':    '#f85149',
    'Sudeste':     '#3fb950',
    'Sul':         '#d29922',
    'Norte':       '#f783ac',
    'Brasil':      '#58a6ff',
}

def read_csv(pat, val_name):
    path = list(BASE.glob(pat))[0]
    df = pd.read_csv(str(path), encoding='utf-8')
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={'Período':'Periodo','Região ID':'RegiaoID','Valor':val_name})
    df['Periodo'] = pd.to_datetime(df['Periodo']).dt.year
    df['Regiao'] = df['RegiaoID'].map(REGION_MAP)
    return df

mvi  = read_csv('Mortes*', 'MVI')
haf  = read_csv('Homicídios por Armas*', 'HAF')
hj   = read_csv('Homicídios de Jovens*', 'HJ')
taxa = read_csv('Taxa de Homicídios*', 'TaxaHAF')

df = mvi[['Periodo','Regiao','MVI']].merge(
      haf[['Periodo','Regiao','HAF']], on=['Periodo','Regiao'], how='left').merge(
      hj[['Periodo','Regiao','HJ']], on=['Periodo','Regiao'], how='left').merge(
      taxa[['Periodo','Regiao','TaxaHAF']], on=['Periodo','Regiao'], how='left')
df = df[(df['Periodo']>=1989)&(df['Periodo']<=2022)].copy()
df['PctAF']  = df['HAF'] / df['MVI'] * 100
df['PctJov'] = df['HJ']  / df['MVI'] * 100

br = df.groupby('Periodo').agg(MVI=('MVI','sum'),HAF=('HAF','sum'),HJ=('HJ','sum')).reset_index()
br['Regiao'] = 'Brasil'
br['PctAF']  = br['HAF'] / br['MVI'] * 100
br['PctJov'] = br['HJ']  / br['MVI'] * 100
df_all = pd.concat([df, br], ignore_index=True)

br89 = br[br['Periodo']==1989].iloc[0]
br22 = br[br['Periodo']==2022].iloc[0]

# ── Gerar figures (só o dict JSON, sem HTML) ──────────────────────────────
def line_fig(df_all, y_col, title, ytitle, ann=None):
    fig = go.Figure()
    for reg in ['Brasil','Centro-Oeste','Nordeste','Sudeste','Sul','Norte']:
        sub = df_all[df_all['Regiao']==reg].dropna(subset=[y_col]).sort_values('Periodo')
        fig.add_trace(go.Scatter(
            x=sub['Periodo'].tolist(), y=sub[y_col].tolist(),
            mode='lines+markers', name=reg,
            line=dict(color=RC.get(reg,'#aaa'), width=2 if reg!='Brasil' else 3.5),
            marker=dict(size=4),
        ))
    kwargs = dict(
        title=text(title), xaxis=dict(title='Ano', gridcolor='#30363d', color='#8b949e'),
        yaxis=dict(title=ytitle, gridcolor='#30363d', color='#8b949e'),
        template='plotly_dark',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(color='#e6edf3')),
        margin=dict(l=60, r=20, t=60, b=60),
        paper_bgcolor='#161b22', plot_bgcolor='#161b22',
        font=dict(color='#e6edf3'),
    )
    if ann:
        kwargs['annotations'] = [dict(x=ann[0], y=ann[1], text=ann[2], showarrow=True,
                                      arrowhead=2, font=dict(color='#888', size=12))]
    fig.update_layout(**kwargs)
    return fig

def text(s):
    return {'text': s}

figures = {}

# 1. MVI series
figures['chart1_mvi'] = line_fig(df_all, 'MVI',
    'Mortes Violentas Intencionais (MVI) — por Regiao (1989-2022)',
    'Numero de Vítimas', ann=(2019, 50000, 'Quebra 2018-19'))

# 2. HAF series
figures['chart2_haf'] = line_fig(df_all, 'HAF',
    'Homicidios por Armas de Fogo (HAF) — por Regiao (1989-2022)',
    'Numero de Vítimas')

# 3. Taxa HAF
figures['chart3_taxa'] = line_fig(df_all, 'TaxaHAF',
    'Taxa de Homicidios por AF (por 100 mil hab.) — por Regiao (1980-2022)',
    'Taxa / 100 mil hab.')

# 4. % Jovens
figures['chart4_pctjov'] = line_fig(df_all, 'PctJov',
    '% de Vitimas Jovens (15-29 anos) nas MVI — por Regiao (1989-2022)',
    '% do total de MVI')

# 5. Heatmap MVI
ordem = ['Norte','Nordeste','Centro-Oeste','Sudeste','Sul']
hdata = df[df['Regiao'].isin(ordem)].pivot(index='Regiao', columns='Periodo', values='MVI')
hdata = hdata.reindex([r for r in ordem if r in hdata.index])
fig = go.Figure(data=go.Heatmap(
    z=hdata.values.tolist(), x=hdata.columns.tolist(), y=hdata.index.tolist(),
    colorscale='Reds', colorbar=dict(title='MVI'),
    hovertemplate='%{y} %{x}: %{z:,}<extra></extra>',
))
fig.update_layout(
    title=text('Heatmap — Mortes Violentas por Regiao e Ano (1989-2022)'),
    xaxis=dict(title='Ano', gridcolor='#30363d', color='#8b949e'),
    yaxis=dict(title='Regiao', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=340,
    margin=dict(l=100, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart5_hm_mvi'] = fig

# 6. Heatmap % AF
haf_p = df[df['Regiao'].isin(ordem)].pivot(index='Regiao', columns='Periodo', values='PctAF')
haf_p = haf_p.reindex([r for r in ordem if r in haf_p.index])
fig = go.Figure(data=go.Heatmap(
    z=haf_p.values.tolist(), x=haf_p.columns.tolist(), y=haf_p.index.tolist(),
    colorscale='OrRd', colorbar=dict(title='% AF'),
    hovertemplate='%{y} %{x}: %{z:.1f}%<extra></extra>',
    zmin=10, zmax=80,
))
fig.update_layout(
    title=text('Heatmap — % de MVI por Arma de Fogo por Regiao e Ano (1989-2022)'),
    xaxis=dict(title='Ano', gridcolor='#30363d', color='#8b949e'),
    yaxis=dict(title='Regiao', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=340,
    margin=dict(l=100, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart6_hm_af'] = fig

# 7. Scatter MVI vs HAF
fig = go.Figure()
for reg in ['Brasil','Centro-Oeste','Nordeste','Sudeste','Sul','Norte']:
    sub = df_all[df_all['Regiao']==reg].dropna(subset=['MVI','HAF']).sort_values('Periodo')
    fig.add_trace(go.Scatter(
        x=sub['MVI'].tolist(), y=sub['HAF'].tolist(),
        mode='lines+markers', name=reg,
        line=dict(color=RC.get(reg,'#aaa'), width=2 if reg!='Brasil' else 3.5),
        marker=dict(size=5),
        text=sub['Periodo'].tolist(),
        hovertemplate='%{text}<br>MVI: %{x:,}<br>HAF: %{y:,}<extra>%{fullData.name}</extra>',
    ))
brs = df_all[df_all['Regiao']=='Brasil'].dropna(subset=['MVI','HAF'])
z = np.polyfit(brs['MVI'], brs['HAF'], 1)
p = np.poly1d(z)
xl = np.linspace(float(brs['MVI'].min()), float(brs['MVI'].max()), 100)
fig.add_trace(go.Scatter(x=xl.tolist(), y=p(xl).tolist(), mode='lines', name='Tendencia',
    line=dict(color='white', width=1.5, dash='dash'),
    hovertemplate='Tendencia linear<extra></extra>'))
fig.update_layout(
    title=text('Correlacao: MVI vs Homicidios por Armas de Fogo (por regiao)'),
    xaxis=dict(title='MVI (total)', gridcolor='#30363d', color='#8b949e'),
    yaxis=dict(title='HAF (total)', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=420,
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(color='#e6edf3')),
    margin=dict(l=60, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart7_scatter'] = fig

# 8. Scatter MVI vs HJ
fig = go.Figure()
for reg in ['Brasil','Centro-Oeste','Nordeste','Sudeste','Sul','Norte']:
    sub = df_all[df_all['Regiao']==reg].dropna(subset=['MVI','HJ']).sort_values('Periodo')
    fig.add_trace(go.Scatter(
        x=sub['MVI'].tolist(), y=sub['HJ'].tolist(),
        mode='lines+markers', name=reg,
        line=dict(color=RC.get(reg,'#aaa'), width=2 if reg!='Brasil' else 3.5),
        marker=dict(size=5),
        text=sub['Periodo'].tolist(),
        hovertemplate='%{text}<br>MVI: %{x:,}<br>HJ: %{y:,}<extra>%{fullData.name}</extra>',
    ))
brs2 = df_all[df_all['Regiao']=='Brasil'].dropna(subset=['MVI','HJ'])
z2 = np.polyfit(brs2['MVI'], brs2['HJ'], 1)
p2 = np.poly1d(z2)
x2 = np.linspace(float(brs2['MVI'].min()), float(brs2['MVI'].max()), 100)
fig.add_trace(go.Scatter(x=x2.tolist(), y=p2(x2).tolist(), mode='lines', name='Tendencia',
    line=dict(color='white', width=1.5, dash='dash'),
    hovertemplate='Tendencia linear<extra></extra>'))
fig.update_layout(
    title=text('Correlacao: MVI vs Homicidios de Jovens (por regiao)'),
    xaxis=dict(title='MVI (total)', gridcolor='#30363d', color='#8b949e'),
    yaxis=dict(title='HJ — Homicidios de Jovens', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=420,
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(color='#e6edf3')),
    margin=dict(l=60, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart8_scatter_hj'] = fig

# 9. Barra MVI 2022
df89 = df[df['Periodo']==1989].set_index('Regiao')['MVI']
df22 = df[df['Periodo']==2022].set_index('Regiao')['MVI']
br_reg = [r for r in ['Centro-Oeste','Nordeste','Sudeste','Sul','Norte'] if r in df22.index]
v22 = [int(df22[r]) for r in br_reg]
vars_b = [(df22[r]-df89[r])/df89[r]*100 for r in br_reg]
fig = go.Figure()
fig.add_trace(go.Bar(
    x=br_reg, y=v22,
    marker_color=['#f85149' if v>0 else '#3fb950' for v in vars_b],
    text=[f'{v:,.0f}' for v in v22], textposition='outside',
    textfont=dict(color='#e6edf3'),
))
for i,(r,v) in enumerate(zip(br_reg, vars_b)):
    fig.add_annotation(x=r, y=v22[i]*0.5, text=f'{v:+.0f}% vs 1989',
        showarrow=False, font=dict(color='white', size=11))
fig.update_layout(
    title=text('MVI por Regiao — 2022 (variacao vs 1989)'),
    xaxis=dict(title='Regiao', gridcolor='#30363d', color='#8b949e'),
    yaxis=dict(title='Mortes Violentas (2022)', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=380,
    margin=dict(l=60, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart9_bar_mvi'] = fig

# 10. Barra Taxa HAF 2022
taxa22 = df[df['Periodo']==2022].set_index('Regiao')['TaxaHAF']
br2 = [r for r in ['Centro-Oeste','Nordeste','Sudeste','Sul','Norte'] if r in taxa22.index]
vt = [float(taxa22[r]) for r in br2]
fig = go.Figure()
fig.add_trace(go.Bar(
    x=br2, y=vt,
    marker_color=[RC.get(r,'#888') for r in br2],
    text=[f'{v:.1f}' for v in vt], textposition='outside',
    textfont=dict(color='#e6edf3'),
))
fig.update_layout(
    title=text('Taxa de Homicidios por AF — por Regiao em 2022 (por 100 mil hab.)'),
    xaxis=dict(title='Regiao', gridcolor='#30363d', color='#8b949e'),
    yaxis=dict(title='Taxa / 100.000 hab.', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=380,
    margin=dict(l=60, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart10_bar_taxa'] = fig

# 11. % AF Brasil
br_pctaf = br.dropna(subset=['PctAF']).sort_values('Periodo')
pctaf_2017 = float(br_pctaf[br_pctaf['Periodo']==2017]['PctAF'].values[0])
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=br_pctaf['Periodo'].tolist(), y=br_pctaf['PctAF'].tolist(),
    mode='lines+markers', fill='tozeroy',
    line=dict(color='#f85149', width=3), marker=dict(size=5), name='% AF',
))
fig.update_layout(
    title=text('Evolucao da Participacao de Armas de Fogo nas MVI — Brasil (1989-2022)'),
    xaxis=dict(title='Ano', gridcolor='#30363d', color='#8b949e'),
    yaxis=dict(title='% das MVI com arma de fogo', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=380,
    margin=dict(l=60, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
    annotations=[dict(x=2017, y=pctaf_2017,
        text=f'Pico 2017 ({pctaf_2017:.0f}%)',
        showarrow=True, arrowhead=2, font=dict(color='#f85149'))]
)
figures['chart11_pctaf'] = fig

# 12. Matriz correlação
corr_cols = ['MVI','HAF','HJ','PctAF','PctJov']
br_corr = br[corr_cols].corr().round(2)
labels_c = ['MVI (abs)','HAF (abs)','HJ (jovens)','%AF','%Jovens']
fig = go.Figure(data=go.Heatmap(
    z=br_corr.values.tolist(), x=labels_c, y=labels_c,
    colorscale='RdBu', zmin=-1, zmax=1,
    colorbar=dict(title='Pearson r'),
    text=br_corr.values.tolist(),
    texttemplate='%{text:.2f}',
    textfont=dict(color='white', size=13),
    hovertemplate='%{x} x %{y}: r = %{z:.3f}<extra></extra>',
))
fig.update_layout(
    title=text('Matriz de Correlacao de Pearson — Brasil Agregado (1989-2022)'),
    template='plotly_dark', height=400,
    margin=dict(l=120, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart12_corr'] = fig

# 13. HJ series
figures['chart13_hj'] = line_fig(df_all, 'HJ',
    'Homicidios de Jovens (15-29 anos) — por Regiao (1989-2022)',
    'Numero de Vitimas Jovens')

# 14. Boxplot MVI
fig = go.Figure()
for reg in ['Centro-Oeste','Nordeste','Sudeste','Sul','Norte']:
    sub = df[df['Regiao']==reg]['MVI'].dropna()
    fig.add_trace(go.Box(y=sub.tolist(), name=reg,
                          marker_color=RC.get(reg,'#888'), boxmean=True))
fig.update_layout(
    title=text('Distribuicao de MVI por Regiao (1989-2022) — Boxplot'),
    yaxis=dict(title='MVI', gridcolor='#30363d', color='#8b949e'),
    template='plotly_dark', height=380, showlegend=False,
    margin=dict(l=60, r=20, t=60, b=60),
    paper_bgcolor='#161b22', plot_bgcolor='#161b22',
    font=dict(color='#e6edf3'),
)
figures['chart14_box'] = fig

# ── Serializar figures para JSON ──────────────────────────────────────────
# Converter para dicts serializáveis
def fig_to_dict(fig):
    return fig.to_dict()

figures_json = {k: fig_to_dict(v) for k, v in figures.items()}

with open(ANALISE / 'charts_data.json', 'w', encoding='utf-8') as f:
    json.dump(figures_json, f, ensure_ascii=False, indent=2)

print(f'{len(figures_json)} figures gerados.')
print('Keys:', list(figures_json.keys()))
