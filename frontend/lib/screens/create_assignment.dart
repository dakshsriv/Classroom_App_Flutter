import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:get_storage/get_storage.dart';
import 'package:dio/dio.dart';

void main() async {
  await GetStorage.init();
  runApp(const CreateAssignmentPage());
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

class CreateAssignmentPage extends StatefulWidget {
  const CreateAssignmentPage({super.key});

  @override
  State<CreateAssignmentPage> createState() => _CreateAssignmentPageState();
}

class _CreateAssignmentPageState extends State<CreateAssignmentPage> {
  String title = "";
  String description = "";
  String classID = box.read("class");
  String userID = box.read('userID');
  final _formKey = GlobalKey<FormState>();

  

  @override
  void initState() {
    super.initState();
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
          const Text("Create an assignment"),
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
                      child: const Text('Create'),
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

  Future<Info?> edit(title, description, classID, context) async {
    Info? retrievedUser;

    try {
      Response response = await _dio.post(
        '${_baseUrl}assignments/$classID',
        data: {
          'class_id': classID,
          'name': title,
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
