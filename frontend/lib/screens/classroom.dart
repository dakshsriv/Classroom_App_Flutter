import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter_conditional_rendering/flutter_conditional_rendering.dart';
import 'package:dio/dio.dart';

void main() async {
  await GetStorage.init();
  runApp(const Classroom());
}

final box = GetStorage();

class Classroom extends StatefulWidget {
  const Classroom({super.key});

  @override
  State<Classroom> createState() => _ClassroomState();
}

class _ClassroomState extends State<Classroom> {
  String userID = "";
  String accountType = "";
  String classID = "";
  List<dynamic> info = [];
  List<dynamic> people = [];

  void setup() async {
    try {
      print(
          "Box values are: ${box.read('userID')}, ${box.read('accountType')}");
      userID = await box.read('userID');
      accountType = await box.read('accountType');
      classID = await box.read('class');
      print("userID: $userID, accountType: $accountType, classID: $classID");
    } catch (e) {
      SchedulerBinding.instance.addPostFrameCallback((_) {
        Navigator.pushNamedAndRemoveUntil(context, "/", (_) => false);
      });
    }
  }

  @override
  void initState() {
    super.initState();

    setup();

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
          Column(children: [
            TextButton(
              onPressed: () {
                box.write("class", "");
                Navigator.pushNamedAndRemoveUntil(context, "/", (_) => false);
              },
              child: const Text('All classes'),
            ),
            const Text("People:"),
            Column(
                children:
                    people.map<Widget>((c) => Text("  • ${c[0]}")).toList()),
            Conditional.single(
              context: context,
              conditionBuilder: (BuildContext context) =>
                  box.read('accountType') == "student",
              widgetBuilder: (BuildContext context) => Column(children: [
                Text('Student account'),
              ]),
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

  dynamic info(id) async {
    try {
      print('Sending to ${_baseUrl}classes/$id');
      Response response = await _dio.post('${_baseUrl}classroom/class/$id');

      print('Classes: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }
}
