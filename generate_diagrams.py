"""
Metro Query System - Diagram Generator
Generates system architecture, flowcharts, and ER diagrams
Using English labels to avoid font issues
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import networkx as nx


def create_system_architecture_diagram():
    """Generate system architecture diagram"""
    fig, ax = plt.subplots(figsize=(14, 11))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')

    ax.text(7, 11.5, 'Metro Query System - Architecture', fontsize=18, fontweight='bold', ha='center')

    color_ui = '#87CEEB'
    color_logic = '#98FB98'
    color_data = '#FFB6C1'

    # UI Layer
    ui_boxes = [
        (3, 9, 2.5, 1.2, 'CLI Interface', color_ui),
        (7, 9, 2.5, 1.2, 'Streamlit UI', color_ui),
        (11, 9, 2.5, 1.2, 'Database Layer', color_ui),
    ]
    for x, y, w, h, text, color in ui_boxes:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(patch)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=12, fontweight='bold')

    # Logic Layer
    logic_boxes = [
        (3.5, 6, 2.2, 1.2, 'MetroDatabase\n(Data Management)', color_logic),
        (7, 6, 2.2, 1.2, 'MetroQuery\n(Route Planning)', color_logic),
        (10.5, 6, 2.2, 1.2, 'MetroVisualizer\n(Output)', color_logic),
    ]
    for x, y, w, h, text, color in logic_boxes:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(patch)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=11)

    # Data Layer
    data_boxes = [
        (1.5, 2.8, 1.8, 1.0, 'metro_lines', color_data),
        (3.5, 2.8, 1.8, 1.0, 'stations', color_data),
        (5.5, 2.8, 1.8, 1.0, 'connections', color_data),
        (7.5, 2.8, 1.8, 1.0, 'tickets', color_data),
        (9.5, 2.8, 1.8, 1.0, 'pricing', color_data),
        (11.5, 2.8, 1.8, 1.0, 'traffic', color_data),
    ]
    for x, y, w, h, text, color in data_boxes:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                               facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(patch)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=10)

    # Arrows
    for x in [4.25, 8.25, 12.25]:
        ax.add_patch(FancyArrowPatch((x, 8.6), (x, 7.4), arrowstyle='->', mutation_scale=25, linewidth=2, color='gray'))
    for x in [4.6, 8.1, 11.6]:
        ax.add_patch(FancyArrowPatch((x, 5.6), (x, 3.9), arrowstyle='->', mutation_scale=25, linewidth=2, color='gray'))

    # Layer Labels
    ax.text(0.8, 10.2, 'UI Layer', fontsize=14, fontweight='bold', color='#0000CD')
    ax.text(0.8, 7.2, 'Logic Layer', fontsize=14, fontweight='bold', color='#006400')
    ax.text(0.8, 3.8, 'Data Layer', fontsize=14, fontweight='bold', color='#8B0000')

    plt.tight_layout()
    plt.savefig('system_architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
    print('Generated: system_architecture.png')
    plt.close()


def create_path_planning_flowchart():
    """Generate path planning flowchart"""
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 15)
    ax.axis('off')

    ax.text(6, 14.5, 'Path Planning Flowchart', fontsize=18, fontweight='bold', ha='center')

    nodes = [
        (6, 13, 1.8, 0.8, 'Start', 'start'),
        (6, 11.5, 2.2, 0.8, 'Input Start/End', 'process'),
        (6, 10, 2.4, 0.9, 'Same Station?', 'decision'),
        (9.5, 8.3, 2.2, 0.9, 'Return\nPrice=0', 'process'),
        (6, 8.3, 2.4, 0.9, 'Find Stations', 'process'),
        (6, 6.6, 2.4, 0.9, 'Same Line?', 'decision'),
        (2.5, 4.8, 2.4, 0.9, 'Same Line\nAlgorithm', 'process'),
        (9.5, 4.8, 2.4, 0.9, 'Transfer\nAlgorithm', 'process'),
        (6, 3.2, 2.4, 0.9, 'Compare &\nSelect Best', 'process'),
        (6, 1.5, 2.2, 0.8, 'Output Result', 'process'),
        (6, 0.3, 1.5, 0.7, 'End', 'end'),
    ]

    for x, y, w, h, text, node_type in nodes:
        if node_type == 'decision':
            pts = [(x, y + h/2 + 0.1), (x + w/2 + 0.1, y), (x, y - h/2 - 0.1), (x - w/2 - 0.1, y)]
            ax.add_patch(plt.Polygon(pts, facecolor='#FFD700', edgecolor='black', linewidth=2))
        elif node_type in ['start', 'end']:
            ax.add_patch(mpatches.Ellipse((x, y), w, h, facecolor='#90EE90', edgecolor='black', linewidth=2))
        else:
            ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.05",
                                       facecolor='#ADD8E6', edgecolor='black', linewidth=2))
        ax.text(x, y, text, ha='center', va='center', fontsize=12)

    arrows = [
        ((6, 12.5), (6, 12.0), ''), ((6, 11.0), (6, 10.5), ''),
        ((7.0, 9.6), (8.5, 8.8), 'Yes'), ((4.0, 9.6), (6, 8.8), 'No'),
        ((6, 9.2), (6, 8.8), ''), ((6, 7.5), (6, 7.1), ''),
        ((4.0, 6.2), (3.0, 5.2), 'Yes'), ((8.0, 6.2), (9.0, 5.2), 'No'),
        ((3.5, 4.0), (5.5, 3.6), ''), ((8.5, 4.0), (6.5, 3.6), ''),
        ((6, 2.4), (6, 2.0), ''), ((6, 1.0), (6, 0.7), ''),
    ]

    for (x1, y1), (x2, y2), label in arrows:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->', mutation_scale=20, linewidth=1.5, color='black'))
        if label:
            ax.text((x1+x2)/2 + 0.3, (y1+y2)/2 + 0.15, label, fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('path_planning_flowchart.png', dpi=300, bbox_inches='tight', facecolor='white')
    print('Generated: path_planning_flowchart.png')
    plt.close()


def create_database_erd():
    """Generate database ER diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, 'Database ER Diagram', fontsize=18, fontweight='bold', ha='center')

    tables = [
        {
            'name': 'metro_lines',
            'x': 1.5, 'y': 7,
            'columns': ['line_id (PK)', 'line_name', 'color', 'total_stations']
        },
        {
            'name': 'stations',
            'x': 5, 'y': 7,
            'columns': ['station_id (PK)', 'station_name', 'line_id (FK)', 'station_order', 'distance']
        },
        {
            'name': 'connections',
            'x': 9, 'y': 7,
            'columns': ['conn_id (PK)', 'station1_id (FK)', 'station2_id (FK)', 'line_id (FK)', 'travel_time']
        },
        {
            'name': 'pricing',
            'x': 1.5, 'y': 3,
            'columns': ['price_id (PK)', 'min_distance', 'max_distance', 'price']
        },
        {
            'name': 'tickets',
            'x': 5.5, 'y': 3,
            'columns': ['ticket_id (PK)', 'start_station', 'end_station', 'line_name', 'price', 'purchase_time']
        },
        {
            'name': 'traffic',
            'x': 10, 'y': 3,
            'columns': ['traffic_id (PK)', 'station_name', 'date', 'passenger_count', 'ticket_count']
        },
    ]

    for table in tables:
        header_h = 0.6
        ax.add_patch(Rectangle((table['x'], table['y']), 3, header_h, facecolor='#4169E1', edgecolor='black', linewidth=2))
        ax.text(table['x'] + 1.5, table['y'] + header_h/2, table['name'], ha='center', va='center',
                color='white', fontsize=11, fontweight='bold')

        row_h = 0.38
        for i, col in enumerate(table['columns']):
            y_pos = table['y'] - (i + 1) * row_h
            bg = '#E6E6FA' if i % 2 == 0 else '#F0F0F0'
            ax.add_patch(Rectangle((table['x'], y_pos), 3, row_h, facecolor=bg, edgecolor='black', linewidth=1))
            text_color = 'red' if '(PK)' in col or '(FK)' in col else 'black'
            ax.text(table['x'] + 0.15, y_pos + row_h/2, col, ha='left', va='center', color=text_color, fontsize=9)

    ax.annotate('', xy=(4.2, 7.3), xytext=(3.5, 7.3), arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(3.85, 7.5, '1:n', fontsize=11, fontweight='bold')
    ax.annotate('', xy=(8.2, 7.3), xytext=(7.2, 7.3), arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(7.7, 7.5, '1:n', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('database_erd.png', dpi=300, bbox_inches='tight', facecolor='white')
    print('Generated: database_erd.png')
    plt.close()


def create_price_calculation_chart():
    """Generate price calculation chart"""
    fig, ax = plt.subplots(figsize=(12, 7))

    prices = [3, 4, 5, 6, 7]
    labels = ['0-6km', '6-12km', '12-20km', '20-32km', '>32km']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

    bars = ax.bar(range(len(prices)), prices, color=colors, edgecolor='black', linewidth=2, width=0.6)

    ax.set_xticks(range(len(prices)))
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylabel('Price (Yuan)', fontsize=14)
    ax.set_xlabel('Distance Range', fontsize=14)
    ax.set_title('Metro Fare Calculation', fontsize=18, fontweight='bold')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.15, f'¥{height}',
                ha='center', va='bottom', fontsize=14, fontweight='bold')

    ax.set_ylim(0, 8.5)
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig('price_calculation.png', dpi=300, facecolor='white')
    print('Generated: price_calculation.png')
    plt.close()


def create_metro_network_graph():
    """Generate metro network graph"""
    fig, ax = plt.subplots(figsize=(12, 12))

    G = nx.Graph()

    line1 = ['Pinguoyuan', 'Guchenglu', 'Bajiaoyouleyuan', 'Gucheng', 'Babaoshan',
             'Yuquanlu', 'Wukesong', 'Wanshoulu', 'Gongzhufen', 'Junshibowuguan']
    line2 = ['Xizhimen', 'Jishuitan', 'Guloudajie', 'Yonghegong', 'Dongzhimen',
             'Jianguomen', 'Beijingzhan', 'Chongwenmen', 'Qianmen', 'Hepingmen']
    line3 = ['Dongshisitiaojie', 'Gongrentiyuchang', 'Tuanjiehu', 'Nongyezhanlanguan', 'Sanyuanqiao',
             'Liangmaqiao', 'Yanshaqiao', 'Xiaoyunqiao', 'Fangyuanli', 'Jiangtai']
    line4 = ['Gongyixiqiao', 'Jiaomenxi', 'Majiapu', 'Beijingnanzhan', 'Taoranting',
             'Caishikou', 'Xuanwumen', 'Xidan', 'Lingjingtong', 'Pinganli']

    pos = {}
    for i, station in enumerate(line1):
        pos[station] = (2 + i * 0.85, 2)
        G.add_node(station, color='#E30613')
    for i, station in enumerate(line2):
        pos[station] = (2 + i * 0.85, 10)
        G.add_node(station, color='#003AB4')
    for i, station in enumerate(line3):
        pos[station] = (1, 2.5 + i * 0.8)
        G.add_node(station, color='#C19A00')
    for i, station in enumerate(line4):
        pos[station] = (10, 2.5 + i * 0.8)
        G.add_node(station, color='#009A44')

    def add_edges(stations):
        for i in range(len(stations) - 1):
            G.add_edge(stations[i], stations[i + 1])
    add_edges(line1); add_edges(line2); add_edges(line3); add_edges(line4)

    node_colors = [G.nodes[n]['color'] for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, edgecolors='black', linewidths=1.5, ax=ax)
    nx.draw_networkx_edges(G, pos, width=2.5, alpha=0.8, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold', ax=ax)

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#E30613', markersize=14, label='Line 1'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#003AB4', markersize=14, label='Line 2'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#C19A00', markersize=14, label='Line 3'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#009A44', markersize=14, label='Line 4'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=12)
    ax.set_title('Metro Network Topology', fontsize=20, fontweight='bold')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig('metro_network_graph.png', dpi=300, facecolor='white')
    print('Generated: metro_network_graph.png')
    plt.close()


def create_module_structure_chart():
    """Generate module structure chart"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, 'Module Structure', fontsize=20, fontweight='bold', ha='center')

    modules = [
        {'name': 'MetroSystem\n(Main Class)', 'x': 7, 'y': 7.5, 'color': '#FF6B6B'},
        {'name': 'MetroDatabase\n(Data Mgmt)', 'x': 3, 'y': 5, 'color': '#4ECDC4'},
        {'name': 'MetroQuery\n(Route Query)', 'x': 7, 'y': 5, 'color': '#45B7D1'},
        {'name': 'MetroVisualizer\n(Output)', 'x': 11, 'y': 5, 'color': '#96CEB4'},
    ]

    for mod in modules:
        ax.add_patch(FancyBboxPatch((mod['x'] - 1.5, mod['y'] - 0.7), 3, 1.4,
                                   boxstyle="round,pad=0.1", facecolor=mod['color'],
                                   edgecolor='black', linewidth=2))
        ax.text(mod['x'], mod['y'], mod['name'], ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')

    for x in [3, 7, 11]:
        ax.add_patch(FancyArrowPatch((7, 6.5), (x, 5.9), arrowstyle='->', mutation_scale=25, linewidth=2, color='black'))

    sub_funcs = [
        {'x': 3, 'y': 2.5, 'color': '#4ECDC4', 'funcs': ['get_all_lines()', 'get_station_by_name()', 'calculate_fare()', 'add_ticket()']},
        {'x': 7, 'y': 2.5, 'color': '#45B7D1', 'funcs': ['find_path()', '_find_same_line()', '_find_transfer()']},
        {'x': 11, 'y': 2.5, 'color': '#96CEB4', 'funcs': ['print_line_map()', 'print_path()', 'print_statistics()']},
    ]

    for sf in sub_funcs:
        box_h = 0.4 * len(sf['funcs']) + 0.5
        ax.add_patch(FancyBboxPatch((sf['x'] - 1.8, sf['y'] - box_h/2), 3.6, box_h,
                                   boxstyle="round,pad=0.05", facecolor=sf['color'],
                                   edgecolor='black', linewidth=1.5, alpha=0.5))
        ax.text(sf['x'], sf['y'] + box_h/2 - 0.25, 'Methods:', ha='center', va='center', fontsize=10, fontweight='bold')
        for i, func in enumerate(sf['funcs']):
            ax.text(sf['x'], sf['y'] + box_h/2 - 0.6 - i * 0.4, func, ha='center', va='center', fontsize=9)
        ax.plot([sf['x'], sf['x']], [4.3, 3.8], 'k--', linewidth=1.5)

    plt.tight_layout()
    plt.savefig('module_structure.png', dpi=300, bbox_inches='tight', facecolor='white')
    print('Generated: module_structure.png')
    plt.close()


def main():
    print('=' * 60)
    print('    Metro Query System - Diagram Generator')
    print('=' * 60)

    diagram_dir = 'diagrams'
    if not os.path.exists(diagram_dir):
        os.makedirs(diagram_dir)
    os.chdir(diagram_dir)

    print('\nGenerating diagrams...\n')
    create_system_architecture_diagram()
    create_path_planning_flowchart()
    create_database_erd()
    create_price_calculation_chart()
    create_metro_network_graph()
    create_module_structure_chart()

    print('\n' + '=' * 60)
    print('All diagrams generated successfully!')
    print('=' * 60)


if __name__ == '__main__':
    main()
