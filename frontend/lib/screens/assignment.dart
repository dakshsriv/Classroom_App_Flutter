import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter_conditional_rendering/flutter_conditional_rendering.dart';
import 'package:dio/dio.dart';

void main() async {
  await GetStorage.init();
  runApp(const Assignment());
}

final box = GetStorage();

class Assignment extends StatefulWidget {
  const Assignment({super.key});

  @override
  State<Assignment> createState() => _AssignmentState();
}

class _AssignmentState extends State<Assignment> {
  List<dynamic> info = [];
  String title = "";
  String description = "";
  String assignmentID = "";
  String status = "Unfinished";

  void setup() async {
    try {
    print("Box values are: ${box.read('userID')}, ${box.read('accountType')}");
    assignmentID = await box.read('assignment');
    DioClient x = DioClient();
    var information = await x.info();
    print("information is ${information[0]}");
    info = await x.info();
    if (await box.read('accountType') == "student") {
      dynamic statusc = await x.getStatus();
      statusc = statusc[0][2];
      if (statusc == 0) {
        status = "Unfinished";
      } else if (statusc == 1) {
        status = "Finished";
      }
      print('status is $status');
    }
    setState(() {
      title = info[0][1];
      description = info[0][2];
    });
    } catch (e) {
      print("Fail");
      SchedulerBinding.instance.addPostFrameCallback((_) {
        Navigator.pushNamedAndRemoveUntil(context, "/classroom/", (_) => false);
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
            Text("Assignment Name: $title"),
            Text("Assignment Description: $description"),
            Conditional.single(
              context: context,
              conditionBuilder: (BuildContext context) =>
                  box.read('accountType') == "student",
              widgetBuilder: (BuildContext context) => Column(children: [
                Text('Student account'),
                Text('Status: $status'),
                TextButton(
                  onPressed: () {
                    DioClient z = DioClient();
                    z.submit();
                    Navigator.pushReplacementNamed(context, "/assignment/");
                  },
                  child: const Text('Submit/Unsubmit'),
                ),
              ]),
              fallbackBuilder: (BuildContext context) => Row(children: [
                TextButton(
                  onPressed: () {
                    Navigator.pushReplacementNamed(
                        context, "/assignment_edit/");
                  },
                  child: const Text('Edit Assignment'),
                ),
                TextButton(
                  onPressed: () {
                    DioClient z = DioClient();
                    z.delete();
                    Navigator.pushReplacementNamed(context, "/classroom/");
                  },
                  child: const Text('Delete Assignment'),
                ),
                /*
                TextButton(
                  onPressed: () {
                    Navigator.pushReplacementNamed(
                        context, "/assignment_create/");
                  },
                  child: const Text('Create Assignment'),
                ) , */
              ]),
            )
          ]),
          TextButton(
            onPressed: () {
              Navigator.pushReplacementNamed(context, "/classroom/");
            },
            child: const Text('Back to classroom'),
          ),
        ]));
  }
}

class DioClient {
  final Dio _dio = Dio();
  final box = GetStorage();
  final _baseUrl = 'https://dev.dakshsrivastava.com/';

  dynamic info() async {
    var id = await box.read("assignment");
    try {
      print('Sending to ${_baseUrl}assignments/$id');
      Response response = await _dio.get('${_baseUrl}assignments/$id');

      print('Assignment Info: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic delete() async {
    var id = await box.read("assignment");
    try {
      Response response = await _dio.delete('${_baseUrl}assignments/$id');
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic submit() async {
    var assignmentID = await box.read("assignment");
    var userID = await box.read("userID");
    try {
      Response response = await _dio.post('${_baseUrl}submit/', data:{"student_id":userID, "assignment_id":assignmentID});
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic getStatus() async {
    var assignmentID = await box.read("assignment");
    var userID = await box.read("userID");
    try {
      Response response = await _dio.post('${_baseUrl}status/',
          data: {"student_id": userID, "assignment_id": assignmentID});
      print(response.data);
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }
}
