"""
地铁查询售票系统 - 测试用例
覆盖所有功能模块的单元测试
"""

import unittest
import sqlite3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from metro_cli import MetroDatabase, MetroQuery


class TestMetroSystem(unittest.TestCase):
    """地铁系统测试类"""

    def setUp(self):
        """在每个测试方法前执行"""
        # 使用临时数据库
        self.db = MetroDatabase(":memory:")
        self.query = MetroQuery(self.db)

    def tearDown(self):
        """在每个测试方法后执行"""
        self.db.close()

    def test_1_get_all_lines(self):
        """测试：查看所有线路"""
        lines = self.db.get_all_lines()
        self.assertEqual(len(lines), 4)
        line_names = [line['line_name'] for line in lines]
        self.assertIn("1号线", line_names)
        self.assertIn("2号线", line_names)
        self.assertIn("3号线", line_names)
        self.assertIn("4号线", line_names)
        print("✓ 测试通过：查看所有线路")

    def test_2_get_line_stations(self):
        """测试：线路详情查询"""
        stations = self.db.get_line_stations(1)
        self.assertEqual(len(stations), 10)
        station_names = [s['station_name'] for s in stations]
        self.assertIn("苹果园", station_names)
        self.assertIn("五棵松", station_names)
        self.assertIn("军事博物馆", station_names)
        print("✓ 测试通过：线路详情查询")

    def test_3_get_station_by_name(self):
        """测试：站点信息查询"""
        results = self.db.get_station_by_name("五棵松")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['station_name'], "五棵松")
        self.assertEqual(results[0]['line_name'], "1号线")
        
        results = self.db.get_station_by_name("门")
        self.assertTrue(len(results) > 0)
        print("✓ 测试通过：站点信息查询")

    def test_4_get_all_stations(self):
        """测试：获取所有站点列表"""
        stations = self.db.get_all_stations()
        self.assertEqual(len(stations), 40)
        self.assertIn("苹果园", stations)
        self.assertIn("西直门", stations)
        print("✓ 测试通过：获取所有站点列表")

    def test_5_calculate_fare(self):
        """测试：票价计算"""
        fare1 = self.db.calculate_fare(5)   # 0-6公里
        self.assertEqual(fare1, 3.0)
        
        fare2 = self.db.calculate_fare(10)  # 6-12公里
        self.assertEqual(fare2, 4.0)
        
        fare3 = self.db.calculate_fare(15)  # 12-20公里
        self.assertEqual(fare3, 5.0)
        
        fare4 = self.db.calculate_fare(25)  # 20-32公里
        self.assertEqual(fare4, 6.0)
        
        fare5 = self.db.calculate_fare(40)  # 32+公里
        self.assertEqual(fare5, 7.0)
        print("✓ 测试通过：票价计算")

    def test_6_find_path_same_line(self):
        """测试：同线路路径查询"""
        path, price = self.query.find_path("苹果园", "五棵松")
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "苹果园")
        self.assertEqual(path[-1], "五棵松")
        self.assertTrue(price > 0)
        print("✓ 测试通过：同线路路径查询")

    def test_7_find_path_same_station(self):
        """测试：起点终点相同"""
        path, price = self.query.find_path("五棵松", "五棵松")
        self.assertEqual(path, ["五棵松"])
        self.assertEqual(price, 0)
        print("✓ 测试通过：起点终点相同")

    def test_8_find_path_invalid_station(self):
        """测试：无效站点查询"""
        path, price = self.query.find_path("不存在的站点", "五棵松")
        self.assertIsNone(path)
        self.assertIsNone(price)
        
        path, price = self.query.find_path("五棵松", "不存在的站点")
        self.assertIsNone(path)
        self.assertIsNone(price)
        print("✓ 测试通过：无效站点查询")

    def test_9_add_ticket(self):
        """测试：购买车票"""
        ticket_id = self.db.add_ticket("苹果园", "五棵松", "1号线", 5.0, 2)
        self.assertTrue(ticket_id > 0)
        
        history = self.db.get_ticket_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['start_station'], "苹果园")
        self.assertEqual(history[0]['end_station'], "五棵松")
        self.assertEqual(history[0]['passenger_count'], 2)
        print("✓ 测试通过：购买车票")

    def test_10_ticket_history(self):
        """测试：售票历史记录"""
        self.db.add_ticket("苹果园", "五棵松", "1号线", 5.0, 1)
        self.db.add_ticket("西直门", "东直门", "2号线", 4.0, 2)
        
        history = self.db.get_ticket_history()
        self.assertEqual(len(history), 2)
        print("✓ 测试通过：售票历史记录")

    def test_11_statistics(self):
        """测试：运营统计信息"""
        self.db.add_ticket("苹果园", "五棵松", "1号线", 5.0, 2)
        self.db.add_ticket("西直门", "东直门", "2号线", 4.0, 3)
        
        stats = self.db.get_statistics()
        self.assertEqual(stats['total_tickets'], 5)
        self.assertEqual(stats['total_revenue'], 5*2 + 4*3)
        print("✓ 测试通过：运营统计信息")

    def test_12_insert_line(self):
        """测试：添加新线路"""
        result = self.db.insert_line("5号线", "#FF5722")
        self.assertTrue(result)
        
        lines = self.db.get_all_lines()
        self.assertEqual(len(lines), 5)
        line_names = [line['line_name'] for line in lines]
        self.assertIn("5号线", line_names)
        
        result = self.db.insert_line("5号线", "#FF5722")
        self.assertFalse(result)
        print("✓ 测试通过：添加新线路")

    def test_13_insert_station(self):
        """测试：添加新站点"""
        result = self.db.insert_station("新站点", 1, 11, 25.0)
        self.assertTrue(result)
        
        stations = self.db.get_line_stations(1)
        self.assertEqual(len(stations), 11)
        station_names = [s['station_name'] for s in stations]
        self.assertIn("新站点", station_names)
        print("✓ 测试通过：添加新站点")

    def test_14_delete_station(self):
        """测试：删除站点"""
        result = self.db.delete_station("苹果园", 1)
        self.assertTrue(result)
        
        stations = self.db.get_line_stations(1)
        self.assertEqual(len(stations), 9)
        station_names = [s['station_name'] for s in stations]
        self.assertNotIn("苹果园", station_names)
        
        result = self.db.delete_station("不存在的站点", 1)
        self.assertFalse(result)
        print("✓ 测试通过：删除站点")

    def test_15_update_station(self):
        """测试：修改站点"""
        result = self.db.update_station("苹果园", "苹果园新区", 1)
        self.assertTrue(result)
        
        stations = self.db.get_line_stations(1)
        station_names = [s['station_name'] for s in stations]
        self.assertIn("苹果园新区", station_names)
        self.assertNotIn("苹果园", station_names)
        
        result = self.db.update_station("不存在的站点", "新名称", 1)
        self.assertFalse(result)
        print("✓ 测试通过：修改站点")

    def test_16_get_line_info(self):
        """测试：获取线路信息"""
        info = self.query.get_line_info(1)
        self.assertIsNotNone(info)
        self.assertEqual(info['line']['line_name'], "1号线")
        self.assertEqual(info['station_count'], 10)
        self.assertEqual(len(info['stations']), 10)
        
        info = self.query.get_line_info(999)
        self.assertIsNone(info)
        print("✓ 测试通过：获取线路信息")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("          地铁查询售票系统 - 测试用例")
    print("=" * 60)
    print()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMetroSystem)
    runner = unittest.TextTestRunner(verbosity=0)
    
    print("正在执行测试...\n")
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print(f"测试结果：运行 {result.testsRun} 个测试")
    print(f"  ✓ 通过：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  ✗ 失败：{len(result.failures)}")
    print(f"  ✗ 错误：{len(result.errors)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
