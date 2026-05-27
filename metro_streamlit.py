"""
地铁查询售票系统 - 网页版
使用Streamlit创建交互式网页界面
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
from typing import Dict

st.set_page_config(
    page_title="🚇 地铁查询售票系统",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Noto Sans SC', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-shadow: none;
    }
    
    .st-emotion-cache-18ni7ap {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .st-emotion-cache-16txtl3 {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8eaed 100%);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6c757d;
        margin-top: 0.25rem;
    }
    
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .info-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    }
    
    .danger-box {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    .line-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .station-badge {
        display: inline-block;
        background: linear-gradient(135deg, #e0e5ec 0%, #d0d5dc 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.875rem;
        color: #374151;
        font-weight: 500;
    }
    
    .nav-item {
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .price-tag {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ef4444;
    }
    
    .path-step {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .path-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 1rem;
    }
    
    .path-start {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .path-end {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .path-middle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .table-container {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        overflow: hidden;
    }
    
    .tab-header {
        font-weight: 600;
        color: #374151;
        padding: 0.75rem 1rem;
        border-bottom: 2px solid #667eea;
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


class MetroDatabase:
    def __init__(self, db_path: str = "metro_system.db"):
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._init_tables()
        self._seed_data()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def _init_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metro_lines (
                line_id INTEGER PRIMARY KEY,
                line_name TEXT NOT NULL UNIQUE,
                color TEXT,
                total_stations INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                station_id INTEGER PRIMARY KEY AUTOINCREMENT,
                station_name TEXT NOT NULL,
                line_id INTEGER NOT NULL,
                station_order INTEGER NOT NULL,
                distance_from_start REAL DEFAULT 0,
                FOREIGN KEY (line_id) REFERENCES metro_lines(line_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS station_connections (
                connection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                station1_id INTEGER NOT NULL,
                station2_id INTEGER NOT NULL,
                line_id INTEGER NOT NULL,
                travel_time INTEGER DEFAULT 2,
                FOREIGN KEY (station1_id) REFERENCES stations(station_id),
                FOREIGN KEY (station2_id) REFERENCES stations(station_id),
                FOREIGN KEY (line_id) REFERENCES metro_lines(line_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pricing (
                pricing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                min_distance REAL DEFAULT 0,
                max_distance REAL,
                price REAL DEFAULT 2
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_station TEXT NOT NULL,
                end_station TEXT NOT NULL,
                line_name TEXT NOT NULL,
                price REAL NOT NULL,
                purchase_time TEXT NOT NULL,
                passenger_count INTEGER DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS station_traffic (
                traffic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                station_name TEXT NOT NULL,
                date TEXT NOT NULL,
                passenger_count INTEGER DEFAULT 0,
                ticket_count INTEGER DEFAULT 0
            )
        """)

        self.conn.commit()

    def _seed_data(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM metro_lines")
        if cursor.fetchone()[0] > 0:
            return

        lines = [
            (1, "1号线", "#E30613", 10),
            (2, "2号线", "#003AB4", 10),
            (3, "3号线", "#C19A00", 10),
            (4, "4号线", "#009A44", 10),
        ]
        cursor.executemany(
            "INSERT INTO metro_lines (line_id, line_name, color, total_stations) VALUES (?, ?, ?, ?)",
            lines
        )

        stations_data = {
            1: [("苹果园", 1, 0), ("古城路", 2, 2.5), ("八角游乐园", 3, 5), ("古城", 4, 7.5),
                ("八宝山", 5, 10), ("玉泉路", 6, 12.5), ("五棵松", 7, 15), ("万寿路", 8, 17.5),
                ("公主坟", 9, 20), ("军事博物馆", 10, 22.5)],
            2: [("西直门", 1, 0), ("积水潭", 2, 2.5), ("鼓楼大街", 3, 5), ("雍和宫", 4, 7.5),
                ("东直门", 5, 10), ("建国门", 6, 12.5), ("北京站", 7, 15), ("崇文门", 8, 17.5),
                ("前门", 9, 20), ("和平门", 10, 22.5)],
            3: [("东四十条", 1, 0), ("工人体育场", 2, 2), ("团结湖", 3, 4), ("农业展览馆", 4, 6),
                ("三元桥", 5, 8), ("亮马桥", 6, 10), ("燕莎桥", 7, 12), ("霄云桥", 8, 14),
                ("芳园里", 9, 16), ("将台", 10, 18)],
            4: [("公益西桥", 1, 0), ("角门西", 2, 2), ("马家堡", 3, 4), ("北京南站", 4, 6),
                ("陶然亭", 5, 8), ("菜市口", 6, 10), ("宣武门", 7, 12), ("西单", 8, 14),
                ("灵境胡同", 9, 16), ("平安里", 10, 18)]
        }

        for line_id, stations in stations_data.items():
            for station_name, order, distance in stations:
                cursor.execute(
                    "INSERT INTO stations (station_name, line_id, station_order, distance_from_start) VALUES (?, ?, ?, ?)",
                    (station_name, line_id, order, distance)
                )

        for line_id in range(1, 5):
            cursor.execute(
                "SELECT station_id FROM stations WHERE line_id = ? ORDER BY station_order",
                (line_id,)
            )
            station_ids = [row[0] for row in cursor.fetchall()]
            for i in range(len(station_ids) - 1):
                cursor.execute(
                    "INSERT INTO station_connections (station1_id, station2_id, line_id, travel_time) VALUES (?, ?, ?, ?)",
                    (station_ids[i], station_ids[i+1], line_id, 3)
                )
                cursor.execute(
                    "INSERT INTO station_connections (station1_id, station2_id, line_id, travel_time) VALUES (?, ?, ?, ?)",
                    (station_ids[i+1], station_ids[i], line_id, 3)
                )

        pricing_tiers = [
            (0, 6, 3),
            (6, 12, 4),
            (12, 20, 5),
            (20, 32, 6),
            (32, 100, 7)
        ]
        cursor.executemany(
            "INSERT INTO pricing (min_distance, max_distance, price) VALUES (?, ?, ?)",
            pricing_tiers
        )

        self.conn.commit()

    def get_all_lines(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM metro_lines ORDER BY line_id")
        return [dict(row) for row in cursor.fetchall()]

    def get_line_stations(self, line_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM stations WHERE line_id = ? ORDER BY station_order",
            (line_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_station_by_name(self, station_name: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.*, m.line_name, m.color
            FROM stations s
            JOIN metro_lines m ON s.line_id = m.line_id
            WHERE s.station_name LIKE ?
            ORDER BY s.station_name, m.line_id
        """, (f"%{station_name}%",))
        return [dict(row) for row in cursor.fetchall()]

    def get_all_stations(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT station_name FROM stations ORDER BY station_name")
        return [row[0] for row in cursor.fetchall()]

    def calculate_fare(self, distance: float):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT price FROM pricing
            WHERE ? >= min_distance AND ? < max_distance
        """, (distance, distance))
        result = cursor.fetchone()
        return result[0] if result else 7.0

    def add_ticket(self, start_station: str, end_station: str, line_name: str,
                   price: float, passenger_count: int = 1):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (start_station, end_station, line_name, price, purchase_time, passenger_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (start_station, end_station, line_name, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), passenger_count))
        self.conn.commit()
        return cursor.lastrowid

    def get_ticket_history(self, limit: int = 50):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM tickets ORDER BY purchase_time DESC LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT SUM(price * passenger_count) FROM tickets")
        total_revenue = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(passenger_count) FROM tickets")
        total_tickets = cursor.fetchone()[0] or 0

        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT SUM(price * passenger_count) FROM tickets
            WHERE date(purchase_time) = ?
        """, (today,))
        today_revenue = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT SUM(passenger_count) FROM tickets
            WHERE date(purchase_time) = ?
        """, (today,))
        today_tickets = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT line_name, COUNT(*), SUM(passenger_count), SUM(price * passenger_count)
            FROM tickets GROUP BY line_name
        """)
        line_stats = [dict(row) for row in cursor.fetchall()]

        return {
            "total_revenue": total_revenue,
            "total_tickets": total_tickets,
            "today_revenue": today_revenue,
            "today_tickets": today_tickets,
            "line_stats": line_stats
        }

    def insert_line(self, line_name: str, color: str):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT MAX(line_id) FROM metro_lines")
            max_id = cursor.fetchone()[0] or 0
            cursor.execute(
                "INSERT INTO metro_lines (line_id, line_name, color) VALUES (?, ?, ?)",
                (max_id + 1, line_name, color)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def insert_station(self, station_name: str, line_id: int, station_order: int, distance: float):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO stations (station_name, line_id, station_order, distance_from_start) VALUES (?, ?, ?, ?)",
                (station_name, line_id, station_order, distance)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_station(self, station_name: str, line_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM stations WHERE station_name = ? AND line_id = ?",
            (station_name, line_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def update_station(self, old_name: str, new_name: str, line_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE stations SET station_name = ? WHERE station_name = ? AND line_id = ?",
            (new_name, old_name, line_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def close(self):
        if self.conn:
            self.conn.close()


class MetroQuery:
    def __init__(self, db: MetroDatabase):
        self.db = db

    def find_path(self, start: str, end: str):
        if start == end:
            return [start], 0

        stations = self.db.get_all_stations()

        if start not in stations or end not in stations:
            return None, None

        start_stations = self.db.get_station_by_name(start)
        end_stations = self.db.get_station_by_name(end)

        best_path = None
        min_price = float('inf')

        for start_info in start_stations:
            for end_info in end_stations:
                if start_info['line_id'] == end_info['line_id']:
                    path, price = self._find_same_line_path(
                        start_info['station_id'],
                        end_info['station_id'],
                        start_info['line_id'],
                        start,
                        end
                    )
                    if path and price < min_price:
                        min_price = price
                        best_path = path
                else:
                    path, price = self._find_transfer_path(
                        start_info, end_info, start, end
                    )
                    if path and price < min_price:
                        min_price = price
                        best_path = path

        return best_path, min_price if best_path else None

    def _find_same_line_path(self, start_id: int, end_id: int, line_id: int,
                              start_name: str, end_name: str):
        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT * FROM stations WHERE line_id = ? ORDER BY station_order
        """, (line_id,))

        stations = [dict(row) for row in cursor.fetchall()]

        start_idx = next((i for i, s in enumerate(stations) if s['station_id'] == start_id), None)
        end_idx = next((i for i, s in enumerate(stations) if s['station_id'] == end_id), None)

        if start_idx is None or end_idx is None:
            return None, None

        path_stations = [s['station_name'] for s in stations[min(start_idx, end_idx):max(start_idx, end_idx) + 1]]

        station_count = abs(end_idx - start_idx)
        distance = station_count * 2.5
        price = self.db.calculate_fare(distance)

        return path_stations, price

    def _find_transfer_path(self, start_info: Dict, end_info: Dict,
                            start_name: str, end_name: str):
        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT DISTINCT station_name FROM stations WHERE line_id = ?
        """, (start_info['line_id'],))
        start_line_stations = {row[0] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT DISTINCT station_name FROM stations WHERE line_id = ?
        """, (end_info['line_id'],))
        end_line_stations = {row[0] for row in cursor.fetchall()}

        transfer_stations = start_line_stations & end_line_stations

        if not transfer_stations:
            return None, None

        best_path = None
        min_price = float('inf')

        for transfer in transfer_stations:
            path1, price1 = self._find_same_line_path(
                start_info['station_id'],
                self._get_station_id(transfer, start_info['line_id']),
                start_info['line_id'],
                start_name,
                transfer
            )
            path2, price2 = self._find_same_line_path(
                self._get_station_id(transfer, end_info['line_id']),
                end_info['station_id'],
                end_info['line_id'],
                transfer,
                end_name
            )

            if path1 and path2:
                total_path = path1 + path2[1:]
                total_price = price1 + price2
                if total_price < min_price:
                    min_price = total_price
                    best_path = total_path

        return best_path, min_price

    def _get_station_id(self, station_name: str, line_id: int):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT station_id FROM stations WHERE station_name = ? AND line_id = ?",
            (station_name, line_id)
        )
        result = cursor.fetchone()
        return result[0] if result else -1

    def get_line_info(self, line_id: int):
        lines = self.db.get_all_lines()
        line = next((l for l in lines if l['line_id'] == line_id), None)

        if not line:
            return None

        stations = self.db.get_line_stations(line_id)
        return {
            "line": line,
            "stations": stations,
            "station_count": len(stations)
        }


@st.cache_resource
def get_metro_system():
    db = MetroDatabase()
    return MetroQuery(db), db


def main():
    st.markdown('<h1 class="main-header">🚇 地铁查询售票系统</h1>', unsafe_allow_html=True)

    query, db = get_metro_system()
    all_stations = db.get_all_stations()
    all_lines = db.get_all_lines()

    page = st.sidebar.radio(
        "📋 功能菜单",
        ["🏠 首页概览", "🗺️ 线路查询", "🔍 站点查询", "🛤️ 路径规划", "🎫 购票", "📊 数据管理", "📈 统计信息"],
        index=0,
        key="main_nav"
    )

    if page == "🏠 首页概览":
        st.markdown("---")
        st.markdown("### 📊 运营概览")

        stats = db.get_statistics()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">¥{stats['total_revenue']:.2f}</div>
                <div class="metric-label">💰 累计票房</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_tickets']}</div>
                <div class="metric-label">🎫 累计售票</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">¥{stats['today_revenue']:.2f}</div>
                <div class="metric-label">💵 今日票房</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['today_tickets']}</div>
                <div class="metric-label">👥 今日售票</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🗺️ 地铁线路总览")

        for line in all_lines:
            stations = db.get_line_stations(line['line_id'])
            station_names = [s['station_name'] for s in stations]

            with st.expander(f"🚇 {line['line_name']} ({len(stations)}站)", expanded=False):
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {line['color']}11 0%, {line['color']}22 100%);
                            padding: 1.5rem; border-radius: 12px; border-left: 4px solid {line['color']};'>
                    <div style='display: flex; flex-wrap: wrap; gap: 0.5rem;'>
                        {"".join([f"<span class='station-badge'>{s}</span>" for s in station_names])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    elif page == "🗺️ 线路查询":
        st.markdown("---")
        st.markdown("### 🗺️ 线路详情查询")

        line_options = {f"{line['line_name']}": line['line_id'] for line in all_lines}
        selected_line = st.selectbox("选择线路", list(line_options.keys()), index=0)

        if selected_line:
            line_id = line_options[selected_line]
            info = query.get_line_info(line_id)

            if info:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {info['line']['color']}11 0%, {info['line']['color']}22 100%);
                            padding: 2rem; border-radius: 16px; margin: 1rem 0; border-left: 4px solid {info['line']['color']};'>
                    <h2 style='color: {info['line']['color']}; margin: 0;'>🚇 {info['line']['line_name']}</h2>
                    <p style='color: #666; margin-top: 0.5rem; font-size: 0.9rem;'>
                        <span style='display: inline-block; width: 16px; height: 16px; border-radius: 4px; background: {info['line']['color']}; margin-right: 0.5rem;'></span>
                        线路颜色标识
                    </p>
                    <p style='color: #666; font-size: 0.9rem;'>📍 站点数量: <strong>{info['station_count']}</strong> 站</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 📍 站点列表")

                stations_df = pd.DataFrame(info['stations'])
                stations_df.columns = ['站点ID', '站点名称', '线路ID', '站点序号', '距起点距离(km)']
                stations_df = stations_df[['站点名称', '站点序号', '距起点距离(km)']]
                stations_df['距起点距离(km)'] = stations_df['距起点距离(km)'].apply(lambda x: f"{x:.1f}")

                st.markdown("""
                <div class="table-container">
                    <div class="tab-header">站点信息</div>
                """, unsafe_allow_html=True)
                st.dataframe(stations_df, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

                station_names = " → ".join([s['station_name'] for s in info['stations']])
                st.markdown(f"""
                <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;'>
                    <strong style='color: #374151;'>线路走向：</strong>
                    <p style='font-size: 1.1rem; color: {info['line']['color']}; font-weight: 500; margin-top: 0.5rem;'>
                        {station_names}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    elif page == "🔍 站点查询":
        st.markdown("---")
        st.markdown("### 🔍 站点信息查询")

        search_term = st.text_input("输入站点名称搜索", placeholder="例如：东直门", key="station_search")

        if search_term:
            results = db.get_station_by_name(search_term)

            if results:
                st.markdown(f"""
                <div class="success-box">
                    ✅ 找到 {len(results)} 个相关站点
                </div>
                """, unsafe_allow_html=True)

                for r in results:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, {r['color']}11 0%, {r['color']}22 100%);
                                padding: 1.5rem; border-radius: 12px; margin: 0.5rem 0;
                                border-left: 4px solid {r['color']};'>
                        <h3 style='color: {r['color']}; margin: 0;'>📍 {r['station_name']}</h3>
                        <p style='color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                            线路: <strong>{r['line_name']}</strong> |
                            站点序号: 第{r['station_order']}站 |
                            距起点: {r['distance_from_start']:.1f}km
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-box">
                    ⚠️ 未找到该站点，请检查名称是否正确
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📋 所有站点列表")
        all_stations_df = pd.DataFrame(all_stations, columns=['站点名称'])
        st.markdown("""
        <div class="table-container">
            <div class="tab-header">站点列表</div>
        """, unsafe_allow_html=True)
        st.dataframe(all_stations_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "🛤️ 路径规划":
        st.markdown("---")
        st.markdown("### 🛤️ 路径换乘查询")

        col1, col2 = st.columns(2)

        with col1:
            start_station = st.selectbox("起点站", all_stations, index=0, key="path_start")

        with col2:
            end_station = st.selectbox("终点站", all_stations, index=len(all_stations)-1 if len(all_stations) > 1 else 0, key="path_end")

        if st.button("🔍 查询路径", type="primary", use_container_width=True):
            if start_station == end_station:
                st.markdown("""
                <div class="info-box">
                    🚶 起点和终点相同，无需乘坐地铁
                </div>
                """, unsafe_allow_html=True)
            else:
                path, price = query.find_path(start_station, end_station)

                if path:
                    st.markdown("""
                    <div class="success-box">
                        ✅ 找到最优路径！
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">📍 {path[0]}</div>
                            <div class="metric-label">起点</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">🏁 {path[-1]}</div>
                            <div class="metric-label">终点</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value price-tag">¥{price:.1f}</div>
                            <div class="metric-label">票价</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("#### 🗺️ 途经站点")

                    for i, station in enumerate(path):
                        if i == 0:
                            st.markdown(f"""
                            <div class="path-step">
                                <div class="path-icon path-start">🚉</div>
                                <div>
                                    <strong>{station}</strong>
                                    <span style='color: #666; font-size: 0.875rem; margin-left: 0.5rem;'>起点</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif i == len(path) - 1:
                            st.markdown(f"""
                            <div class="path-step">
                                <div class="path-icon path-end">🏁</div>
                                <div>
                                    <strong>{station}</strong>
                                    <span style='color: #666; font-size: 0.875rem; margin-left: 0.5rem;'>终点</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="path-step">
                                <div class="path-icon path-middle">●</div>
                                <div>{station}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
                        <strong>📊 行程信息：</strong>
                        共 <strong>{len(path)}</strong> 站，预计票价 <strong class='price-tag'>¥{price:.1f}</strong> 元
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="danger-box">
                        ❌ 未找到从起点到终点的可达路径
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("提示：请检查站点名称是否正确")

    elif page == "🎫 购票":
        st.markdown("---")
        st.markdown("### 🎫 购买车票")

        col1, col2 = st.columns(2)

        with col1:
            ticket_start = st.selectbox("起点站", all_stations, key="ticket_start")

        with col2:
            ticket_end = st.selectbox("终点站", all_stations, key="ticket_end")

        if "price" not in st.session_state:
            st.session_state.price = 0
        if "fare_calculated" not in st.session_state:
            st.session_state.fare_calculated = False

        if st.button("💰 计算票价", type="primary", use_container_width=True, key="calc_fare"):
            if ticket_start == ticket_end:
                st.markdown("""
                <div class="info-box">
                    🚶 起点和终点相同，无需购票
                </div>
                """, unsafe_allow_html=True)
                st.session_state.fare_calculated = False
            else:
                path, price = query.find_path(ticket_start, ticket_end)

                if path:
                    st.session_state.price = price
                    st.session_state.fare_calculated = True
                    st.markdown(f"""
                    <div class="success-box">
                        票价计算完成！票价：<strong>¥{price:.1f}</strong> 元
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="danger-box">
                        ❌ 无法找到有效路径，请重新选择站点
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.fare_calculated = False

        if st.session_state.fare_calculated:
            passenger_count = st.number_input("购票数量", min_value=1, max_value=10, value=1, key="passenger_count")

            if st.button("🛒 确认购票", type="secondary", use_container_width=True, key="confirm_ticket"):
                start_info = db.get_station_by_name(ticket_start)
                line_name = start_info[0]['line_name'] if start_info else "未知"

                ticket_id = db.add_ticket(ticket_start, ticket_end, line_name, st.session_state.price, passenger_count)
                total_price = st.session_state.price * passenger_count

                st.markdown(f"""
                <div class="success-box">
                    🎉 购票成功！<br>
                    <div style='margin-top: 1rem;'>
                        <p>票号: <strong>{ticket_id}</strong></p>
                        <p>起点: {ticket_start}</p>
                        <p>终点: {ticket_end}</p>
                        <p>数量: {passenger_count} 张</p>
                        <p>总价: <strong>¥{total_price:.1f}</strong> 元</p>
                        <p style='font-size: 0.875rem; color: rgba(255,255,255,0.8);'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.session_state.fare_calculated = False

        st.markdown("---")
        st.markdown("### 📜 购票历史")

        history = db.get_ticket_history(20)

        if history:
            history_df = pd.DataFrame(history)
            history_df = history_df[['ticket_id', 'start_station', 'end_station', 'line_name', 'passenger_count', 'price', 'purchase_time']]
            history_df.columns = ['票号', '起点', '终点', '线路', '数量', '单价', '购买时间']
            history_df['总价'] = history_df['单价'] * history_df['数量']
            history_df['总价'] = history_df['总价'].apply(lambda x: f"¥{x:.1f}")
            history_df['单价'] = history_df['单价'].apply(lambda x: f"¥{x:.1f}")

            st.markdown("""
            <div class="table-container">
                <div class="tab-header">购票历史记录</div>
            """, unsafe_allow_html=True)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                📭 暂无购票记录
            </div>
            """, unsafe_allow_html=True)

    elif page == "📊 数据管理":
        st.markdown("---")
        st.markdown("### 📊 数据管理")

        tab1, tab2, tab3, tab4 = st.tabs(["➕ 添加线路", "➕ 添加站点", "🗑️ 删除站点", "✏️ 修改站点"])

        with tab1:
            st.markdown("#### 添加新线路")
            new_line_name = st.text_input("线路名称", key="new_line_name")
            new_line_color = st.text_input("线路颜色代码", placeholder="#RRGGBB", value="#667eea", key="new_line_color")

            if st.button("添加线路", type="primary", key="add_line"):
                if new_line_name and new_line_color:
                    if db.insert_line(new_line_name, new_line_color):
                        st.markdown(f"""
                        <div class="success-box">
                            ✅ 线路 '{new_line_name}' 添加成功！
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("""
                        <div class="danger-box">
                            ❌ 添加失败，线路名称可能已存在
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-box">
                        ⚠️ 请填写完整信息
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            st.markdown("#### 添加新站点")
            line_options_simple = {line['line_name']: line['line_id'] for line in all_lines}
            select_line = st.selectbox("选择线路", list(line_options_simple.keys()), key="add_station_line")
            new_station_name = st.text_input("站点名称", key="new_station_name")
            new_station_order = st.number_input("站点序号", min_value=1, max_value=100, value=1, key="new_station_order")
            new_station_distance = st.number_input("距起点距离(km)", min_value=0.0, max_value=1000.0, value=0.0, step=0.5, key="new_station_distance")

            if st.button("添加站点", type="primary", key="add_station"):
                if new_station_name and select_line:
                    line_id = line_options_simple[select_line]
                    if db.insert_station(new_station_name, line_id, new_station_order, new_station_distance):
                        st.markdown(f"""
                        <div class="success-box">
                            ✅ 站点 '{new_station_name}' 添加成功！
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown("""
                        <div class="danger-box">
                            ❌ 添加失败
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-box">
                        ⚠️ 请填写完整信息
                    </div>
                    """, unsafe_allow_html=True)

        with tab3:
            st.markdown("#### 删除站点")
            delete_station_name = st.selectbox("选择要删除的站点", all_stations, key="delete_station_name")

            if delete_station_name:
                station_info = db.get_station_by_name(delete_station_name)
                if station_info:
                    st.write(f"该站点位于：{station_info[0]['line_name']}")

                    if st.button("🗑️ 确认删除", type="secondary", key="delete_station"):
                        line_id = station_info[0]['line_id']
                        if db.delete_station(delete_station_name, line_id):
                            st.markdown(f"""
                            <div class="success-box">
                                ✅ 站点 '{delete_station_name}' 删除成功！
                            </div>
                            """, unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown("""
                            <div class="danger-box">
                                ❌ 删除失败
                            </div>
                            """, unsafe_allow_html=True)

        with tab4:
            st.markdown("#### 修改站点")
            update_station_old = st.selectbox("选择要修改的站点", all_stations, key="update_station_old")
            update_station_new = st.text_input("新站点名称", key="update_station_new")

            if update_station_old:
                station_info = db.get_station_by_name(update_station_old)
                if station_info:
                    line_id = station_info[0]['line_id']

                    if st.button("✏️ 确认修改", type="secondary", key="update_station"):
                        if update_station_new:
                            if db.update_station(update_station_old, update_station_new, line_id):
                                st.markdown(f"""
                                <div class="success-box">
                                    ✅ 站点已修改为 '{update_station_new}'！
                                </div>
                                """, unsafe_allow_html=True)
                                st.rerun()
                            else:
                                st.markdown("""
                                <div class="danger-box">
                                    ❌ 修改失败
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="warning-box">
                                ⚠️ 请输入新站点名称
                            </div>
                            """, unsafe_allow_html=True)

    elif page == "📈 统计信息":
        st.markdown("---")
        st.markdown("### 📈 运营统计信息")

        stats = db.get_statistics()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">¥{stats['total_revenue']:.2f}</div>
                <div class="metric-label">💰 累计票房</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_tickets']}</div>
                <div class="metric-label">🎫 累计售票</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">¥{stats['today_revenue']:.2f}</div>
                <div class="metric-label">💵 今日票房</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['today_tickets']}</div>
                <div class="metric-label">👥 今日售票</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        if stats['line_stats']:
            st.markdown("#### 📊 各线路售票统计")

            line_stats_df = pd.DataFrame(stats['line_stats'])

            if 'COUNT(*)' in line_stats_df.columns:
                line_stats_df.columns = ['线路', '售票笔数', '售出人次', '票房收入']
            elif 'count(*)' in line_stats_df.columns:
                line_stats_df.columns = ['线路', '售票笔数', '售出人次', '票房收入']
            else:
                line_stats_df.columns = ['线路', '售票笔数', '售出人次', '票房收入']

            line_stats_df['票房收入'] = line_stats_df['票房收入'].apply(lambda x: f"¥{x:.2f}")

            st.markdown("""
            <div class="table-container">
                <div class="tab-header">线路统计</div>
            """, unsafe_allow_html=True)
            st.dataframe(line_stats_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("#### 📈 票房占比")

            if len(stats['line_stats']) > 0:
                chart_data = pd.DataFrame({
                    '线路': [s['line_name'] for s in stats['line_stats']],
                    '票房': [s['SUM(price * passenger_count)'] for s in stats['line_stats']]
                })

                st.bar_chart(chart_data.set_index('线路'))
        else:
            st.markdown("""
            <div class="info-box">
                📭 暂无售票统计数据
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()