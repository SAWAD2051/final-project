import 'package:bugetify_app/models/task.dart';
import 'package:flutter/cupertino.dart';
import 'package:sqflite/sqflite.dart';

class DBHelper {
  static Database? _db;
  static final int _version = 1;
  static final String _tableName = 'tasks';

  static Future<void> initDb() async {
    if (_db != null) {
      debugPrint("not null db");
      return;
    }
    try {
      String _path = await getDatabasesPath() + 'tasks.db';
      debugPrint("in database path");
      _db = await openDatabase(
        _path,
        version: _version,
        onCreate: (db, version) {
          debugPrint("creating a new one");
          return db.execute(
            "CREATE TABLE $_tableName("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title STRING,  date STRING, "
            " repeat STRING,"
            "color INTEGER)",
          );
        },
      );
    } catch (e) {
      print(e);
    }
  }

  static Future<int> insert(Task task) async {
    print("insert function called");
    return await _db!.insert(_tableName, task.toJson());
  }

  static Future<int> delete(Task task) async =>
      await _db!.delete(_tableName, where: 'id = ?', whereArgs: [task.id]);

  static Future<List<Map<String, dynamic>>> query() async {
    print("query function called");
    return _db!.query(_tableName);
  }
}
