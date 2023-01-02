import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:dio/dio.dart';

void main() {
  runApp(const LoginPage());
}

class Info {
  final int userId;
  final int accountType;

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

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  int count = 0;
  String username = "";
  String password = "";
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
    return MaterialApp(
        home: Scaffold(
            appBar: AppBar(
              backgroundColor: Colors.blue,
              title: const Text("Classroom App"),
            ),
            body: Column(children: [
              const Text("Login page"),
              Form(
                  key: _formKey,
                  child: Row(
                    children: [
                      // The form follows
                      Row(children: [
                        const Text("Username:  "),
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
                                  username = text;
                                });
                              },
                            )),
                        const Text("Password:  "),
                        SizedBox(
                            width: 200.0,
                            child: TextFormField(
                              obscureText: true,
                              enableSuggestions: false,
                              autocorrect: false,
                              validator: (String? value) {
                                if (value == null || value.isEmpty) {
                                  return 'Please enter some text';
                                }
                                return null;
                              },
                              onChanged: (text) {
                                setState(() {
                                  password = text;
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
                              z.createUser(username, password);
                            }
                          },
                          child: const Text('Submit'),
                        )
                      ])
                    ],
                  )),
              Text("Username is: $username   "),
              Text("Password is: $password   "),
            ])));
  }
}

class DioClient {
  final Dio _dio = Dio();

  final _baseUrl = 'https://dev.dakshsrivastava.com/';

  Future<Info?> createUser(username, password) async {
    Info? retrievedUser;

    try {
      Response response = await _dio.post(
        _baseUrl + 'login/',
        data: {'name': username, 'password': password},
      );

      print('User logged in: ${response.data}');

      retrievedUser = Info.fromJson(response.data);
    } catch (e) {
      print('Error logging in: $e');
    }

    return retrievedUser;
  }
}
