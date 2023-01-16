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
  List<dynamic> classes = [];
  String newClass = "";
  String waste = "";
  final _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();

    try {
      print(
          "Box values are: ${box.read('userID')}, ${box.read('accountType')}");
      userID = box.read('userID');
      accountType = box.read('accountType');
      print("userID: $userID, accountType: $accountType");
    } catch (e) {
      SchedulerBinding.instance.addPostFrameCallback((_) {
        Navigator.pushNamedAndRemoveUntil(context, "/login/", (_) => false);
      });
      print('Not logged in');
    }
    y();

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
  void joinClass() async {
    DioClient z = DioClient();
    int w = await z.join(userID, newClass, context) as int;
    if (w == 1) {
      print("Reached");
      setState(() {
        waste = "1";
      });
    }
    print(w);
  }

  @override
  void y() async {
    DioClient z = DioClient();
    if (accountType == "student") {
      var x = await z.classes_student(userID) as List<dynamic>; // Add await
      setState(() {
        classes = x;
      });
    } else {
      print("Passing $userID as userID");
      var x = await z.classes_teacher(userID) as List<dynamic>; // Add await
      setState(() {
        classes = x;
      });
    }
  }

  void send(context, c) async {
    box.write("class", c);
    Navigator.pushNamedAndRemoveUntil(context, "/classroom/", (_) => false);
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
                    .map<Widget>((c) => TextButton(
                          onPressed: () {
                            send(context, c[0]);
                          },
                          child: Text("  • ${c[0]}"),
                        ))
                    .toList()),
            Conditional.single(
              context: context,
              conditionBuilder: (BuildContext context) =>
                  box.read('accountType') == "student",
              widgetBuilder: (BuildContext context) => Column(children: [
                Text('Student account'),
                Form(
                    key: _formKey,
                    child: Row(
                      children: [
                        // The form follows
                        Row(children: [
                          const Text("Join class:  "),
                          SizedBox(
                              width: 200.0,
                              child: TextFormField(
                                validator: (String? value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Please enter some text';
                                  }
                                  return null;
                                },
                                onChanged: (text) {
                                  setState(() {
                                    newClass = text;
                                  });
                                },
                              )),
                          ElevatedButton(
                            onPressed: () {
                              // Validate will return true if the form is valid, or false if
                              // the form is invalid.
                              if (_formKey.currentState!.validate()) {
                                print("Submission");

                                joinClass();
                              }
                            },
                            child: const Text('Join'),
                          ),
                        ])
                      ],
                    ))
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

  dynamic classes_student(id) async {
    try {
      print('Sending to ${_baseUrl}classes/$id');
      Response response = await _dio.get('${_baseUrl}classes/$id');

      print('Classes: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  dynamic classes_teacher(id) async {
    try {
      Response response = await _dio.get('${_baseUrl}classrooms/teacher/$id');

      print('Classes: ${response.data}');
      print('Classes type: ${response.data.runtimeType}');

      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes in: $e');
    }
  }

  dynamic join(userID, classID, context) async {
    try {
      Response response = await _dio.post('${_baseUrl}classes/', data: {
        'student_id': userID,
        'class_id': classID,
      });
      if (response.data != "NULL") {
        return 1;
      }
    } catch (e) {
      print('Error getting classes in: $e');
      return 0;
    }
  }
}
