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
  String title = "";
  String description = "";
  String teacherID = "";
  List<dynamic> people = [];
  List<dynamic> assignments = [];

  void setup() async {
    try {
      print(
          "Box values are: ${box.read('userID')}, ${box.read('accountType')}");
      userID = await box.read('userID');
      accountType = await box.read('accountType');
      classID = await box.read('class');
      print("userID: $userID, accountType: $accountType, classID: $classID");
      DioClient x = DioClient();
      var information = await x.info();
      print("information is ${information[0]}");
      var peoplec = await x.people();
      print("people are $people");
      var assignmentc = await x.assignments();
      setState(() {
        title = information[0][1];
        description = information[0][2];
        teacherID = information[0][3];
        people = peoplec;
        assignments = assignmentc;
      });
    } catch (e) {
      print("Fail");
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
            Text("Class ID: $classID"),
            Text("Class Name: $title"),
            Text("Class Description: $description"),
            Text("Teacher: $teacherID"),
            const Text("People:"),
            Column(
                children:
                    people.map<Widget>((c) => Text("  • ${c[0]}")).toList()),
            const Text("Assignments:"),
            Column(
                children: assignments
                    .map<Widget>((c) => TextButton(
                          onPressed: () {
                            box.write("assignment", c[0]);
                            Navigator.pushReplacementNamed(
                                context, "/assignment/");
                          },
                          child: Text("  • ${c[1]}"),
                        ))
                    .toList()),
            Conditional.single(
              context: context,
              conditionBuilder: (BuildContext context) =>
                  box.read('accountType') == "student",
              widgetBuilder: (BuildContext context) => Column(children: [
                Text('Student account'),
                TextButton(
                  onPressed: () {
                    DioClient z = DioClient();
                    z.deregister(userID);
                    Navigator.pushReplacementNamed(context, "/");
                  },
                  child: const Text('Deregister'),
                ),
              ]),
              fallbackBuilder: (BuildContext context) => Row(children: [
                TextButton(
                  onPressed: () {
                    Navigator.pushReplacementNamed(context, "/class_edit/");
                  },
                  child: const Text('Edit Classroom'),
                ),
                TextButton(
                  onPressed: () {
                    DioClient z = DioClient();
                    z.delete();
                    Navigator.pushReplacementNamed(context, "/");
                  },
                  child: const Text('Delete Classroom'),
                ),
                TextButton(
                  onPressed: () {
                    Navigator.pushReplacementNamed(
                        context, "/assignment_create/");
                  },
                  child: const Text('Create Assignment'),
                ),
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

  dynamic info() async {
    var id = await box.read("class");
    try {
      print('Sending to ${_baseUrl}classrooms/class/$id');
      Response response = await _dio.get('${_baseUrl}classrooms/class/$id');

      print('Class Info: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic people() async {
    var id = await box.read("class");
    try {
      print('Sending to ${_baseUrl}classrooms/people/$id');
      Response response = await _dio.get('${_baseUrl}classrooms/people/$id');

      print('People: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic delete() async {
    var id = await box.read("class");
    try {
      Response response = await _dio.delete('${_baseUrl}classrooms/$id');
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic deregister(userID) async {
    var id = await box.read("class");
    try {
      Response response = await _dio.put('${_baseUrl}classes/', data: {
        'student_id': userID,
        'class_id': id,
      });
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic assignments() async {
    var id = await box.read("class");
    try {
      print('Sending to ${_baseUrl}assignments/class/$id');
      Response response = await _dio.get('${_baseUrl}assignments/class/$id');

      print('Assignments: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }
}
