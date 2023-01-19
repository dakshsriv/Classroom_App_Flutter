import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:get_storage/get_storage.dart';
import 'package:dio/dio.dart';

void main() async {
  await GetStorage.init();
  runApp(const EditClassroomPage());
}

class Info {
  final String userId;
  final String accountType;

  const Info({
    required this.userId,
    required this.accountType,
  });

  factory Info.fromJson(Map<String, dynamic> json) {
    return Info(
      userId: json['id'],
      accountType: json['type'],
    );
  }
}

var box = GetStorage();

class EditClassroomPage extends StatefulWidget {
  const EditClassroomPage({super.key});

  @override
  State<EditClassroomPage> createState() => _EditClassroomPageState();
}

class _EditClassroomPageState extends State<EditClassroomPage> {
  String title = "";
  String description = "";
  String classID = box.read("class");
  String userID = box.read('userID');
  final _formKey = GlobalKey<FormState>();
  String titleInit = "";
  String descriptionInit = "";

  void setup() async {
    try {
      print(
          "Box values are: ${box.read('userID')}, ${box.read('accountType')}");
      DioClient x = DioClient();
      var information = await x.info();
      print("information is ${information[0]}");
      setState(() {
        titleInit = information[0][1];
        descriptionInit = information[0][2];
        print("titleInit: $titleInit, descriptionInit: $descriptionInit");
      });
    } catch (e) {
      print("Fail");
    }
  }

  @override
  void initState() {
    super.initState();
    setup();
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.blue,
          title: const Text("Classroom App"),
        ),
        body: Column(children: [
          const Text("Edit a classroom"),
          Form(
              key: _formKey,
              child: Row(
                children: [
                  // The form follows
                  Row(children: [
                    const Text("Title:  "),
                    SizedBox(
                        width: 200.0,
                        child: TextFormField(
                          initialValue: titleInit,
                          validator: (String? value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter some text';
                            }
                            return null;
                          },
                          onChanged: (text) {
                            setState(() {
                              title = text;
                            });
                          },
                        )),
                    const Text("Description:  "),
                    SizedBox(
                        width: 200.0,
                        child: TextFormField(
                          initialValue: descriptionInit,
                          validator: (String? value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter some text';
                            }
                            return null;
                          },
                          onChanged: (text) {
                            setState(() {
                              description = text;
                            });
                          },
                        )),
                    ElevatedButton(
                      onPressed: () {
                        // Validate will return true if the form is valid, or false if
                        // the form is invalid.
                        if (_formKey.currentState!.validate()) {
                          print("Submission");
                          DioClient z = DioClient();
                          z.edit(title, description, classID, context);
                          Navigator.pushReplacementNamed(
                              context, '/classroom/');
                        }
                      },
                      child: const Text('Edit'),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.pushReplacementNamed(context, "/classroom/");
                      },
                      child: const Text('Cancel'),
                    ),
                  ])
                ],
              )),
          Text("title is: $title   "),
          Text("description is: $description   "),
        ]));
  }
}

class DioClient {
  final Dio _dio = Dio();
  final _baseUrl = 'https://dev.dakshsrivastava.com/';
  String userID = box.read("userID");

  dynamic info() async {
    var id = await box.read("class");
    try {
      print('Sending to ${_baseUrl}classrooms/class/$id');
      Response response = await _dio.get('${_baseUrl}classrooms/class/$id');

      print('Edit class Info: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }

  Future<Info?> edit(title, description, classID, context) async {
    Info? retrievedUser;

    try {
      Response response = await _dio.put(
        '${_baseUrl}classrooms/$classID',
        data: {
          'title': title,
          'description': description,
          'teacher_id': userID
        },
      );

      Navigator.pushNamedAndRemoveUntil(context, "/classroom/", (_) => false);
    } catch (e) {
      print('Error logging in: $e');
    }

    return retrievedUser;
  }
}
