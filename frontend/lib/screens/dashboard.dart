import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter_conditional_rendering/flutter_conditional_rendering.dart';
import 'package:dio/dio.dart';

void main() async {
  await GetStorage.init();
  runApp(const Dashboard());
}

final box = GetStorage();

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  String userID = "";
  String accountType = "";
  var classes = [];
  

  @override
  void initState() {
    super.initState();

    try {
      userID = box.read('userID');
      accountType = box.read('accountType');
      print("userID: $userID, accountType: $accountType");
    } catch (e) {
      SchedulerBinding.instance.addPostFrameCallback((_) {
        Navigator.pushNamedAndRemoveUntil(context, "/login/", (_) => false);
      });
    }
    DioClient z = DioClient();
    if (accountType == "student") {
      z.classes_student(userID);
    } else {
      print("Passing $userID as userID");
      z.classes_teacher(userID);
    }
    /*SchedulerBinding.instance.addPostFrameCallback((_) {
      userID = box.read("userID");
      accountType = box.read("accountType");
      if (userID == null)
      {
        Navigator.of(context).pushNamed("/login/");
      }
      
    });*/
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
            backgroundColor: Colors.blue, title: const Text("Classroom App")),
        body: Column(children: [
          Text("The user id is: $userID"),
          Text("The account type is: $accountType"),
          Column(children: [
            TextButton(
              onPressed: () {
                box.write("userID", "");
                box.write("accountType", "");
                Navigator.pushNamedAndRemoveUntil(
                    context, "/login/", (_) => false);
              },
              child: const Text('Log out'),
            ),
            const Text("Classes:"),
            Column(
                children: classes
                    .map((c) => Text("  • ${c[0]}"))
                    .toList()),
            Conditional.single(
              context: context,
              conditionBuilder: (BuildContext context) =>
                  box.read('accountType') == "student",
              widgetBuilder: (BuildContext context) => const Text('Student account'),
              fallbackBuilder: (BuildContext context) => Row(children: [
                const Text('Teacher account!'),
                TextButton(
                  onPressed: () {
                    Navigator.pushNamedAndRemoveUntil(
                        context, "/class_create/", (_) => false);
                  },
                  child: const Text('Create a class'),
                )
              ]),
            ),
          ])
        ]));
  }
}

class DioClient {
  final Dio _dio = Dio();
  final box = GetStorage();
  final _baseUrl = 'https://dev.dakshsrivastava.com/';

  void classes_student(id) async {
    try {
      Response response = await _dio.get('${_baseUrl}classes/$id');

      print('Classes: ${response.data}');
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  void classes_teacher(id) async {
    try {
      Response response = await _dio.get('${_baseUrl}classrooms/teacher/$id');

      print('Classes: ${response.data}');
    } catch (e) {
      print('Error getting classes in: $e');
    }
  }
}
