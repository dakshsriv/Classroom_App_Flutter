import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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
                    children: [ // The form follows
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
                                            // Process data.
                                          }
                                        },
                                        child: const Text('Submit'),
                                      )])
                    ],
                  )
                
              ),
              Text("Username is: $username   "),
              Text("Password is: $password   "),
            ])));
  }
}

Future<Info> fetchLogin(username, password) async {
  final response =
      await http.post(Uri.parse('https://dev.dakshsrivastava.com/login/'),
          body: jsonEncode(<String, String>{
            'name': username,
            'password': password,
          }));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Info.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load info');
  }
}
