import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:get_storage/get_storage.dart';
import 'package:dio/dio.dart';

void main() async {
  await GetStorage.init();
  runApp(const RegisterPage());
}

enum AccountType { student, teacher }

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

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  String username = "";
  String password = "";
  String accountType = "Student";
  final _formKey = GlobalKey<FormState>();

  AccountType? _type = AccountType.student;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.blue,
          title: const Text("Classroom App"),
        ),
        body: Column(children: [
          const Text("Register page"),
          Form(
              key: _formKey,
              child: Column(
                children: [
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
                  ListTile(
                    title: const Text('Student'),
                    leading: Radio<AccountType>(
                      value: AccountType.student,
                      groupValue: _type,
                      onChanged: (AccountType? value) {
                        setState(() {
                          _type = value;
                        });
                      },
                    ),
                  ),
                  ListTile(
                    title: const Text('Teacher'),
                    leading: Radio<AccountType>(
                      value: AccountType.teacher,
                      groupValue: _type,
                      onChanged: (AccountType? value) {
                        setState(() {
                          _type = value;
                        });
                      },
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () {
                      // Validate will return true if the form is valid, or false if
                      // the form is invalid.
                      if (_formKey.currentState!.validate()) {
                        print("Submission");
                        DioClient z = DioClient();
                        z.register(username, password, _type);
                        Navigator.pushReplacementNamed(context, '/login/');
                      }
                    },
                    child: const Text('Submit'),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pushReplacementNamed(context, "/login/");
                    },
                    child: const Text('Cancel'),
                  ),
                ],
              )),
          Text("Username is: $username   "),
          Text("Password is: $password   "),
          Text("Account type is: $_type"),
        ]));
  }
}

class DioClient {
  final Dio _dio = Dio();
  final box = GetStorage();
  final _baseUrl = 'https://dev.dakshsrivastava.com/';

  void register(username, password, type) async {

    try {
      String accountType = "Student";
      if (type == AccountType.teacher) {
        accountType = "Teacher";
      }
      Response response = await _dio.post(
        '${_baseUrl}register/',
        data: {'name': username, 'password': password, "account_type": accountType},
      );

      print('User logged in: ${response.data}');
    } catch (e) {
      print('Error logging in: $e');
    }

  }
}
