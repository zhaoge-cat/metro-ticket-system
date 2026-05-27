"""
地铁查询售票系统
功能：线路查询、站点查询、换乘查询、售票管理、数据统计
"""

import sqlite3
import math
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class MetroDatabase:
    """地铁数据库管理类"""
    
    def __init__(self, db_path: str = "metro_system.db"):
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._init_tables()
        self._seed_data()
    
    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)
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
            1: [("苹果园", 1, 0), ("古城路", 1, 2.5), ("八角游乐园", 1, 5), ("古城", 1, 7.5),
                ("八宝山", 1, 10), ("玉泉路", 1, 12.5), ("五棵松", 1, 15), ("万寿路", 1, 17.5),
                ("公主坟", 1, 20), ("军事博物馆", 1, 22.5)],
            2: [("西直门", 2, 0), ("积水潭", 2, 2.5), ("鼓楼大街", 2, 5), ("雍和宫", 2, 7.5),
                ("东直门", 2, 10), ("建国门", 2, 12.5), ("北京站", 2, 15), ("崇文门", 2, 17.5),
                ("前门", 2, 20), ("和平门", 2, 22.5)],
            3: [("东四十条", 3, 0), ("工人体育场", 3, 2), ("团结湖", 3, 4), ("农业展览馆", 3, 6),
                ("三元桥", 3, 8), ("亮马桥", 3, 10), ("燕莎桥", 3, 12), ("霄云桥", 3, 14),
                ("芳园里", 3, 16), ("将台", 3, 18)],
            4: [("公益西桥", 4, 0), ("角门西", 4, 2), ("马家堡", 4, 4), ("北京南站", 4, 6),
                ("陶然亭", 4, 8), ("菜市口", 4, 10), ("宣武门", 4, 12), ("西单", 4, 14),
                ("灵境胡同", 4, 16), ("平安里", 4, 18)]
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
    
    def get_all_lines(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM metro_lines ORDER BY line_id")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_line_stations(self, line_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM stations WHERE line_id = ? ORDER BY station_order",
            (line_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_station_by_name(self, station_name: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.*, m.line_name, m.color 
            FROM stations s 
            JOIN metro_lines m ON s.line_id = m.line_id 
            WHERE s.station_name LIKE ?
            ORDER BY s.station_name, m.line_id
        """, (f"%{station_name}%",))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_stations(self) -> List[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT station_name FROM stations ORDER BY station_name")
        return [row[0] for row in cursor.fetchall()]
    
    def calculate_fare(self, distance: float) -> float:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT price FROM pricing 
            WHERE ? >= min_distance AND ? < max_distance
        """, (distance, distance))
        result = cursor.fetchone()
        return result[0] if result else 7.0
    
    def add_ticket(self, start_station: str, end_station: str, line_name: str, 
                   price: float, passenger_count: int = 1) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (start_station, end_station, line_name, price, purchase_time, passenger_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (start_station, end_station, line_name, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), passenger_count))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_ticket_history(self, limit: int = 20) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM tickets ORDER BY purchase_time DESC LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
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
    
    def insert_line(self, line_name: str, color: str) -> bool:
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
    
    def insert_station(self, station_name: str, line_id: int, station_order: int, distance: float) -> bool:
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
    
    def delete_station(self, station_name: str, line_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM stations WHERE station_name = ? AND line_id = ?",
            (station_name, line_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_station(self, old_name: str, new_name: str, line_id: int) -> bool:
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
    """地铁查询核心类"""
    
    def __init__(self, db: MetroDatabase):
        self.db = db
    
    def find_path(self, start: str, end: str) -> Tuple[Optional[List], Optional[float]]:
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
                              start_name: str, end_name: str) -> Tuple[Optional[List], Optional[float]]:
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
                            start_name: str, end_name: str) -> Tuple[Optional[List], Optional[float]]:
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
    
    def _get_station_id(self, station_name: str, line_id: int) -> int:
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT station_id FROM stations WHERE station_name = ? AND line_id = ?",
            (station_name, line_id)
        )
        result = cursor.fetchone()
        return result[0] if result else -1
    
    def get_line_info(self, line_id: int) -> Dict:
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


class MetroVisualizer:
    """地铁可视化类"""
    
    @staticmethod
    def print_line_map(db: MetroDatabase):
        lines = db.get_all_lines()
        
        print("\n" + "=" * 60)
        print("                      地 铁 线 路 图")
        print("=" * 60)
        
        for line in lines:
            stations = db.get_line_stations(line['line_id'])
            station_names = [s['station_name'] for s in stations]
            
            print(f"\n【{line['line_name']}】({line['color']})")
            print("-" * 40)
            print("→ " + " → ".join(station_names))
            print(f"  共 {len(stations)} 站")
        
        print("\n" + "=" * 60)
    
    @staticmethod
    def print_path(path: List[str], price: float):
        if not path:
            print("未找到可达路径！")
            return
        
        print("\n" + "-" * 40)
        print("              路 径 查 询 结 果")
        print("-" * 40)
        print(f"起点：{path[0]}")
        print(f"终点：{path[-1]}")
        print(f"站数：{len(path)} 站")
        print(f"票价：¥{price:.1f} 元")
        print("\n途经站点：")
        
        for i, station in enumerate(path):
            if i == 0:
                print(f"  └─ {station}")
            elif i == len(path) - 1:
                print(f"  └─ {station}")
            else:
                print(f"    → {station}")
        
        print("-" * 40)
    
    @staticmethod
    def print_statistics(stats: Dict):
        print("\n" + "=" * 40)
        print("              运 营 统 计 信 息")
        print("=" * 40)
        print(f"\n【累计数据】")
        print(f"  总票房：¥{stats['total_revenue']:.2f} 元")
        print(f"  总售票：{stats['total_tickets']} 张")
        
        print(f"\n【今日数据】")
        print(f"  今日票房：¥{stats['today_revenue']:.2f} 元")
        print(f"  今日售票：{stats['today_tickets']} 张")
        
        if stats['line_stats']:
            print(f"\n【各线路售票统计】")
            print("-" * 30)
            for stat in stats['line_stats']:
                print(f"  {stat['line_name']}: {stat['COUNT(*)']} 笔, "
                      f"{stat['SUM(passenger_count)']} 人次, "
                      f"¥{stat['SUM(price * passenger_count)']:.2f}")
        
        print("\n" + "=" * 40)


class MetroSystem:
    """地铁查询售票系统主类"""
    
    def __init__(self):
        self.db = MetroDatabase()
        self.query = MetroQuery(self.db)
        self.visualizer = MetroVisualizer()
    
    def run(self):
        while True:
            self._print_main_menu()
            choice = input("\n请选择功能 (1-9): ").strip()
            
            if choice == '1':
                self._query_all_lines()
            elif choice == '2':
                self._query_line_detail()
            elif choice == '3':
                self._query_station()
            elif choice == '4':
                self._path_finding()
            elif choice == '5':
                self._buy_ticket()
            elif choice == '6':
                self._show_ticket_history()
            elif choice == '7':
                self._show_statistics()
            elif choice == '8':
                self._data_management()
            elif choice == '9':
                self._show_map()
            elif choice == '0':
                print("\n感谢使用地铁查询售票系统，再见！")
                break
            else:
                print("\n无效选择，请重新输入！")
    
    def _print_main_menu(self):
        print("\n" + "=" * 50)
        print("       地 铁 查 询 售 票 系 统")
        print("=" * 50)
        print("  1. 查看所有线路")
        print("  2. 线路详情查询")
        print("  3. 站点信息查询")
        print("  4. 路径换乘查询")
        print("  5. 购买车票")
        print("  6. 售票历史记录")
        print("  7. 运营统计信息")
        print("  8. 数据管理")
        print("  9. 地铁线路图")
        print("  0. 退出系统")
        print("-" * 50)
    
    def _query_all_lines(self):
        lines = self.db.get_all_lines()
        print("\n" + "-" * 40)
        print("            地 铁 线 路 列 表")
        print("-" * 40)
        for line in lines:
            stations = self.db.get_line_stations(line['line_id'])
            print(f"  {line['line_id']}. {line['line_name']} ({line['color']}) - {len(stations)}站")
        print("-" * 40)
    
    def _query_line_detail(self):
        lines = self.db.get_all_lines()
        print("\n可选线路：")
        for line in lines:
            print(f"  {line['line_id']}. {line['line_name']}")
        
        try:
            line_id = int(input("\n请选择线路编号: ").strip())
            info = self.query.get_line_info(line_id)
            
            if info:
                print(f"\n【{info['line']['line_name']}】详细信息：")
                print(f"  颜色标识：{info['line']['color']}")
                print(f"  站点数量：{info['station_count']} 站")
                print(f"\n站点列表：")
                for i, station in enumerate(info['stations'], 1):
                    print(f"  {i}. {station['station_name']} (第{station['station_order']}站, 距起点{station['distance_from_start']:.1f}km)")
            else:
                print("未找到该线路！")
        except ValueError:
            print("请输入有效的数字！")
    
    def _query_station(self):
        station_name = input("请输入站点名称: ").strip()
        if not station_name:
            print("站点名称不能为空！")
            return
        
        results = self.db.get_station_by_name(station_name)
        
        if results:
            print(f"\n找到 {len(results)} 个相关站点：")
            print("-" * 40)
            for r in results:
                print(f"  {r['station_name']} - 线路: {r['line_name']} (第{r['station_order']}站)")
            print("-" * 40)
        else:
            print("未找到该站点！")
    
    def _path_finding(self):
        print("\n--- 路径换乘查询 ---")
        start = input("请输入起点站: ").strip()
        end = input("请输入终点站: ").strip()
        
        if not start or not end:
            print("起点和终点不能为空！")
            return
        
        path, price = self.query.find_path(start, end)
        
        if path:
            self.visualizer.print_path(path, price)
        else:
            print("\n未找到从起点到终点的可达路径！")
            print("提示：请检查站点名称是否正确，或两点可能不在同一网络中。")
    
    def _buy_ticket(self):
        print("\n--- 购 买 车 票 ---")
        
        stations = self.db.get_all_stations()
        print("\n可用站点：")
        for i, s in enumerate(stations[:20], 1):
            print(f"  {s}", end="  ")
            if i % 5 == 0:
                print()
        if len(stations) > 20:
            print(f"\n  ... 等共 {len(stations)} 个站点")
        
        start = input("\n请输入起点站: ").strip()
        end = input("请输入终点站: ").strip()
        
        if not start or not end:
            print("起点和终点不能为空！")
            return
        
        path, price = self.query.find_path(start, end)
        
        if not path:
            print("未找到有效路径，请检查站点名称！")
            return
        
        try:
            count = int(input(f"票价 ¥{price:.1f} 元，请输入购票数量: ").strip())
            if count <= 0:
                print("购票数量必须大于0！")
                return
        except ValueError:
            print("请输入有效的数字！")
            return
        
        start_info = self.db.get_station_by_name(start)
        line_name = start_info[0]['line_name'] if start_info else "未知"
        
        ticket_id = self.db.add_ticket(start, end, line_name, price, count)
        
        total_price = price * count
        print(f"\n{'=' * 40}")
        print(f"         购 票 成 功 ！")
        print(f"{'=' * 40}")
        print(f"  票号：{ticket_id}")
        print(f"  起点：{start}")
        print(f"  终点：{end}")
        print(f"  数量：{count} 张")
        print(f"  总价：¥{total_price:.1f} 元")
        print(f"  时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 40}")
    
    def _show_ticket_history(self):
        history = self.db.get_ticket_history(20)
        
        if not history:
            print("\n暂无售票记录！")
            return
        
        print("\n" + "=" * 70)
        print("                    售 票 历 史 记 录")
        print("=" * 70)
        print(f"{'票号':<6} {'起点':<10} {'终点':<10} {'线路':<8} {'数量':<4} {'金额':<8} {'时间':<20}")
        print("-" * 70)
        
        for t in history:
            print(f"{t['ticket_id']:<6} {t['start_station']:<10} {t['end_station']:<10} "
                  f"{t['line_name']:<8} {t['passenger_count']:<4} ¥{t['price'] * t['passenger_count']:<7.1f} {t['purchase_time']:<20}")
        
        print("=" * 70)
    
    def _show_statistics(self):
        stats = self.db.get_statistics()
        self.visualizer.print_statistics(stats)
    
    def _show_map(self):
        self.visualizer.print_line_map(self.db)
    
    def _data_management(self):
        while True:
            print("\n--- 数 据 管 理 ---")
            print("  1. 添加新线路")
            print("  2. 添加新站点")
            print("  3. 删除站点")
            print("  4. 修改站点")
            print("  0. 返回主菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self._add_line()
            elif choice == '2':
                self._add_station()
            elif choice == '3':
                self._delete_station()
            elif choice == '4':
                self._update_station()
            elif choice == '0':
                break
            else:
                print("无效选择！")
    
    def _add_line(self):
        line_name = input("请输入新线路名称: ").strip()
        color = input("请输入线路颜色标识: ").strip()
        
        if not line_name:
            print("线路名称不能为空！")
            return
        
        if self.db.insert_line(line_name, color):
            print(f"线路 '{line_name}' 添加成功！")
        else:
            print("添加失败，线路名称可能已存在！")
    
    def _add_station(self):
        lines = self.db.get_all_lines()
        print("\n可用线路：")
        for line in lines:
            print(f"  {line['line_id']}. {line['line_name']}")
        
        try:
            line_id = int(input("\n请选择线路编号: ").strip())
            station_name = input("请输入站点名称: ").strip()
            order = int(input("请输入站点序号: ").strip())
            distance = float(input("请输入距离起点距离(km): ").strip())
            
            if self.db.insert_station(station_name, line_id, order, distance):
                print(f"站点 '{station_name}' 添加成功！")
            else:
                print("添加失败！")
        except ValueError:
            print("请输入有效的数字！")
    
    def _delete_station(self):
        station_name = input("请输入要删除的站点名称: ").strip()
        lines = self.db.get_all_lines()
        
        print("\n站点所在线路：")
        for line in lines:
            stations = self.db.get_line_stations(line['line_id'])
            if any(s['station_name'] == station_name for s in stations):
                print(f"  {line['line_id']}. {line['line_name']}")
        
        try:
            line_id = int(input("\n请选择线路编号: ").strip())
            if self.db.delete_station(station_name, line_id):
                print(f"站点 '{station_name}' 删除成功！")
            else:
                print("删除失败，站点不存在！")
        except ValueError:
            print("请输入有效的数字！")
    
    def _update_station(self):
        station_name = input("请输入要修改的站点名称: ").strip()
        new_name = input("请输入新名称: ").strip()
        
        if not station_name or not new_name:
            print("站点名称不能为空！")
            return
        
        lines = self.db.get_all_lines()
        print("\n站点所在线路：")
        for line in lines:
            stations = self.db.get_line_stations(line['line_id'])
            if any(s['station_name'] == station_name for s in stations):
                print(f"  {line['line_id']}. {line['line_name']}")
        
        try:
            line_id = int(input("\n请选择线路编号: ").strip())
            if self.db.update_station(station_name, new_name, line_id):
                print(f"站点已修改为 '{new_name}'！")
            else:
                print("修改失败！")
        except ValueError:
            print("请输入有效的数字！")
    
    def close(self):
        self.db.close()


def main():
    try:
        system = MetroSystem()
        system.run()
        system.close()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断，再见！")
    except Exception as e:
        print(f"\n程序发生错误: {e}")


if __name__ == "__main__":
    main()