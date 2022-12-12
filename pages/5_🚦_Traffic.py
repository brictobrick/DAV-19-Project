import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objs as go
import glob
import os
from datetime import datetime


st.title('# 차량별 혼잡도')
st.subheader("버스노선별 이용현황")


def scale(l1, l2):
    def cal(x):
        return (np.max(l1)-np.min(l1)) * (x - np.min(l2)) / (0.001+np.max(l2)-np.min(l2)) + np.min(l1)
    return cal

df = pd.read_csv("dataset/mod_st_by_line.csv", encoding="EUC_KR")

line_set = set(df['노선ID'])
node_set = df['stn_name_mod']

G = nx.Graph()

bus_nums = ["5516", "관악02", "5511", "5513"]

bus_dict={
    11110236 : "5511",
    11110238 : "5513",
    11110241 : "5516",
    11110537 : "관악02"
}

for station in node_set:
    G.add_node(station)

st_by_line=dict()

for line in line_set:
    st_by_line[line] = list(df[df['노선ID']==line]['stn_name_mod'])
    for i in range(len(st_by_line[line])):
        G.add_edges_from([(st_by_line[line][i], st_by_line[line][(i+1)%len(st_by_line[line])])])

for nodes in st_by_line.values():
    for node in nodes:
        x=df[df['stn_name_mod']==node]['x'].iloc[0]
        y=df[df['stn_name_mod']==node]['y'].iloc[0]

        G.nodes[node]['pos'] = [x, y]

edge_traces=[]
colors = ['purple', 'green', 'red', 'blue']
i=0;

for line in line_set:
    edge_trace = go.Scatter(
        x=[],
        y=[],
        legendgroup = bus_nums[i],
        name=bus_nums[i],
        text=[],
        hoverinfo='text',
        line=dict(width=1),
        mode='lines + markers',
        marker=dict(
            line=dict(width=1),
            color = colors[i],
            size=[],
        )
    )

    for edge in G.edges():
        if (edge[0] in st_by_line[line]) and (edge[1] in st_by_line[line]):
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
            edge_trace['marker']['size'] += tuple([5, 5, 0])
            edge_trace['text'] += tuple([node if ("_" not in node) else node.split("_")[0] + " 앞" for node in [edge[0], edge[1]]+["None"]])
    i+=1

    edge_traces.append(edge_trace)

edge_traces[3].line = dict(width=1, dash="dash")




fig = go.Figure(data=edge_traces,
            layout=go.Layout(
                title="관악02, 5511, 5513, 5516 노선별 현황",
                title_x=0.45,
                titlefont=dict(size=15),
                showlegend=True,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))


def stn_anot(fig, stns, legend_group, x_offset=0, y_offset=0, color="#000000"):
    fig.add_trace(go.Scatter(
            legendgroup=legend_group,
            x=[G.nodes[s]['pos'][0] + x_offset for s in stns],
            y=[G.nodes[s]['pos'][1] + y_offset for s in stns],
            mode="text",
            showlegend=False,
            text=["<b>" + s +"</b>" for s in stns],
            textfont=dict(
                family="dotum",
                size=11,
                color=color,
                ),
            textposition="middle center",
            # bordercolor="#c7c7c7",
            # borderwidth=2,
            # borderpad=4,
            opacity=0.8,
            )
        )

st_name = ['낙성대역', '기숙사삼거리', '건설환경종합연구소', 'BK국제관']
stn_anot(fig, st_name, "관악02", 0, 0.2, 'green')

st_name =['신림2동차고지', '신림역2번출구']
stn_anot(fig, st_name, "5516", 0, 0.2, 'purple')

st_name = ['사육신공원', '노량진역']
stn_anot(fig, st_name, "5516", 0, -0.2, 'purple')

st_name = ['중앙대학교', '중앙대후문']
stn_anot(fig, st_name, "5511", 0, -0.2, 'red')

stn_anot(fig, ["성현동동아아파트"], "5511", 0.3, color='orange')
stn_anot(fig, ["성현동동아아파트"], "5513", 0.3, color='orange')

stn_anot(fig, ["관악푸르지오아파트"], "5511", -0.3, color='orange')
stn_anot(fig, ["관악푸르지오아파트"], "5513", -0.3, color='orange')

stn_anot(fig, ["제2공학관"], "관악02", 0.15, 0.2, color='orange')
stn_anot(fig, ["제2공학관"], "5511", 0.15, 0.2, color='orange')
stn_anot(fig, ["제2공학관"], "5513", 0.15, 0.2, color='orange')

times = pd.read_csv("dataset/time_range.csv")
times = times.iloc[:,0].astype("str").tolist()

bus_df  = pd.read_csv("dataset/total_bus_pos.csv")
bus_set = set(bus_df['vehID'])

pop_scale = scale([7,30],bus_df['recentPop'])

for time in times:

    bus_by_time = bus_df[bus_df["measured_time"] == int(time)].drop_duplicates("vehID", keep="last")

    c=0;

    for line in set(bus_by_time['routeID']):
        bus_by_time_line = bus_by_time[bus_by_time["routeID"] == line]

        info = []
        for i, rows in bus_by_time_line.iterrows():
            info.append(f"노선 : {bus_dict[line]} <br>차량 번호 : {rows.vehID} <br>재차 인원 : {int(rows.recentPop)}")

        fig.add_trace(
            go.Scatter(
                visible=False,
                legendgroup = bus_dict[line],
                mode='markers',
                text=info,
                hoverinfo="text",
                name=bus_dict[line] + " (차량)",
                showlegend=True,
                x=bus_by_time_line['recent_x'],
                y=bus_by_time_line['recent_y'],
                marker=dict(
                    size=pop_scale(bus_by_time_line['recentPop']),
                )
               )
             )
        c+=1
        

for i in range(15,19):
    fig.data[i].visible=True

steps=[]
for i in range(len(times)):
    step = dict(
        method="update",
        args=[{"visible": [True]*15 + 4*[False] * len(times)}],
        label = datetime.strptime(times[i], "%Y%m%d%H%M%S").strftime("%H시 %M분"),
    )
    step["args"][0]["visible"][15+4*(i):4*(i+1)] = [True]*4
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "시간 : "},
    pad={"t": 50, "l" : 50, "r" : 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)



st.plotly_chart(fig, use_container_width=True) 