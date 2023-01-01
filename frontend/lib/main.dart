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
            body: Center(
                child: Row(children: [
              Text("$count"),
              FloatingActionButton(onPressed: () {
                setState(() {
                  count++;
                });
              })
            ]))));
  }
}

Future<Info> fetchLogin() async {
  final response = await http
      .get(Uri.parse('https://jsonplaceholder.typicode.com/albums/1'));

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
